# -*- coding: utf-8 -*-
"""32-验证实验.py
Reproducibility experiment for the NIDS evaluation-practice review.
How much does the train/test partitioning protocol change the performance a
paper would report, on the two datasets most used by the 93 coded studies?
Protocols: official fixed split (where one exists), random 80/20, stratified
5-fold CV, duplicate+group aware strict split, and deduplicate-training-only.
Models: RandomForest(100) and a small PyTorch MLP. Console output is ASCII.
"""
import os, json, time
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, recall_score
import torch, torch.nn as nn

BASE = os.path.dirname(os.path.abspath(__file__))
DATAD = os.path.join(BASE, 'data')
OUT = os.path.join(BASE, 'output', 'exp')
os.makedirs(OUT, exist_ok=True)
SEEDS = [1, 2, 3, 4, 5]
N_EPOCHS = 20

DOS = set('back land neptune pod smurf teardrop mailbomb apache2 processtable udpstorm worm'.split())
PROBE = set('satan ipsweep nmap portsweep mscan saint'.split())
R2L = set('guess_passwd ftp_write imap phf multihop warezmaster warezclient spy xlock xsnoop snmpget snmpgetattack snmpguess named sendmail httptunnel'.split())
U2R = set('buffer_overflow loadmodule rootkit perl sqlattack xterm ps'.split())

def nsl_class(lab):
    l = str(lab).strip().lower().rstrip('.')
    if l == 'normal': return 'normal'
    if l in DOS: return 'dos'
    if l in PROBE: return 'probe'
    if l in R2L: return 'r2l'
    if l in U2R: return 'u2r'
    return 'other'

def load_nsl():
    tr = pd.read_csv(os.path.join(DATAD, 'nsl_train_j.csv'), header=None, low_memory=False)
    te = pd.read_csv(os.path.join(DATAD, 'nslkdd_test.csv'), header=None, low_memory=False)
    assert tr.shape[1] == 43 and te.shape[1] == 43, 'NSL-KDD column count changed'
    ntr = len(tr)
    both = pd.concat([tr, te], ignore_index=True)
    ybin = (both[41].astype(str).str.strip().str.lower() != 'normal').astype(int).values
    ymc = both[41].map(nsl_class).astype('category').cat.codes.values.astype(int)
    mc_names = list(both[41].map(nsl_class).astype('category').cat.categories)
    X = both.drop(columns=[41, 42]).copy()
    for c in [1, 2, 3]:
        X[c] = X[c].astype('category').cat.codes
    X = X.astype('float32').reset_index(drop=True)
    return X, ybin, ymc, mc_names, ntr

def load_unsw():
    df = pd.read_csv(os.path.join(DATAD, 'unsw_nb15_full.csv'), low_memory=False)
    assert df.shape[1] == 45, 'UNSW-NB15 column count changed'
    df['attack_cat'] = df['attack_cat'].fillna('Unknown').replace('', 'Unknown')
    ymc = df['attack_cat'].astype('category')
    mc_names = list(ymc.cat.categories)
    ymc = ymc.cat.codes.values.astype(int)
    ybin = df['label'].astype(int).values
    X = df.drop(columns=['id', 'label', 'attack_cat']).copy()
    for c in X.columns:
        if X[c].dtype == object:
            X[c] = X[c].astype('category').cat.codes
    X = X.astype('float32').reset_index(drop=True)
    return X, ybin, ymc, mc_names, None

class MLP(nn.Module):
    def __init__(self, d, k):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, 128), nn.ReLU(), nn.Dropout(0.1),
                                 nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, k))
    def forward(self, x): return self.net(x)

def fit_predict(Xtr, ytr, Xte, seed, k):
    out = {}
    t0 = time.time()
    rf = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=seed)
    rf.fit(Xtr, ytr)
    out['rf'] = rf.predict(Xte)
    t1 = time.time()
    torch.manual_seed(seed); np.random.seed(seed)
    mu = Xtr.mean(0); sd = Xtr.std(0) + 1e-9
    A = torch.tensor((Xtr - mu) / sd, dtype=torch.float32)
    B = torch.tensor(ytr, dtype=torch.long)
    net = MLP(Xtr.shape[1], k)
    opt = torch.optim.Adam(net.parameters(), 1e-3); lf = nn.CrossEntropyLoss()
    n = len(A)
    for _ in range(N_EPOCHS):
        perm = torch.randperm(n)
        for i in range(0, n, 2048):
            idx = perm[i:i + 2048]
            opt.zero_grad(); loss = lf(net(A[idx]), B[idx]); loss.backward(); opt.step()
    with torch.no_grad():
        out['dnn'] = net(torch.tensor((Xte - mu) / sd, dtype=torch.float32)).argmax(1).numpy()
    out['_train_s'] = round(t1 - t0, 1); out['_dnn_s'] = round(time.time() - t1, 1)
    return out

def score(yte, pred):
    yte = np.asarray(yte); pred = np.asarray(pred)
    out = {'acc': float(accuracy_score(yte, pred)),
           'macro_f1': float(f1_score(yte, pred, average='macro', zero_division=0)),
           'weighted_f1': float(f1_score(yte, pred, average='weighted', zero_division=0)),
           'per_class_recall': {}}
    for c in np.unique(yte):
        m = (yte == c)
        out['per_class_recall'][str(int(c))] = round(float(recall_score(m, (pred == c), zero_division=0)), 4)
    return out

def dup_counts(Xtr, Xte):
    htr = set(pd.util.hash_pandas_object(Xtr, index=False).tolist())
    hte = pd.util.hash_pandas_object(Xte, index=False)
    hit = hte.isin(htr)
    return int(hit.sum()), int(len(hte))

def strict_idx(X, seed):
    h = pd.util.hash_pandas_object(X, index=False).values
    codes, uniq = pd.factorize(h, sort=False)
    first = np.zeros(len(codes), dtype=bool)
    seen = set()
    for i, g in enumerate(codes):
        if g not in seen:
            seen.add(g); first[i] = True
    keep = np.where(first)[0]
    gk = codes[keep]
    rng = np.random.RandomState(seed)
    ug = np.unique(gk).copy(); rng.shuffle(ug)
    ncut = int(len(ug) * 0.8)
    trg = set(ug[:ncut].tolist())
    mtr = np.array([g in trg for g in gk])
    return keep[mtr], keep[~mtr]

def protocols(X, ybin, ntr_official):
    n = len(X); idx = np.arange(n)
    if ntr_official:
        yield 'official', 0, idx[:ntr_official], idx[ntr_official:]
    for s in SEEDS:
        perm = np.random.RandomState(1000 + s).permutation(n)
        cut = int(n * 0.8)
        yield 'random80', s, perm[:cut], perm[cut:]
    skf = StratifiedKFold(5, shuffle=True, random_state=0)
    for f, (a, b) in enumerate(skf.split(idx, ybin)):
        yield 'stratified5cv', f, a, b
    for s in SEEDS:
        a, b = strict_idx(X, s)
        yield 'strict-group', s, a, b

def run_dataset(name, X, ybin, ymc, mc_names, ntr_official):
    recs = []
    Xnp = X.values; ybin = np.asarray(ybin); ymc = np.asarray(ymc)
    for proto, rep, itr, ite in protocols(X, ybin, ntr_official):
        Xtr, Xte = Xnp[itr], Xnp[ite]
        nd, nt = dup_counts(pd.DataFrame(Xtr), pd.DataFrame(Xte))
        base = {'dataset': name, 'protocol': proto, 'repeat': int(rep),
                'n_train': int(len(itr)), 'n_test': int(len(ite)),
                'dup_test': nd, 'dup_pct': round(100.0 * nd / max(1, nt), 2)}
        for task, yall in [('binary', ybin), ('multiclass', ymc)]:
            ytr, yte = yall[itr], yall[ite]
            try:
                kk = 2 if task == 'binary' else len(mc_names)
                pr = fit_predict(Xtr, ytr, Xte, 100 + rep, kk)
            except Exception as e:
                r = dict(base); r['task'] = task; r['error'] = str(e)[:180]; recs.append(r); continue
            for mname in ['rf', 'dnn']:
                r = dict(base); r['task'] = task; r['model'] = mname
                r.update(score(yte, pr[mname]))
                recs.append(r)
            print('  [%s|%s|r%d|%s] ntr=%d nte=%d dup=%.1f%% rf_acc=%.4f rf_F1m=%.4f dnn_acc=%.4f dnn_F1m=%.4f' % (
                name, proto, rep, task, len(itr), len(ite), base['dup_pct'],
                recs[-2]['acc'], recs[-2]['macro_f1'], recs[-1]['acc'], recs[-1]['macro_f1']), flush=True)
    return recs, mc_names

def main():
    allrecs = {}; meta = {}
    for nm, loader in [('NSL-KDD', load_nsl), ('UNSW-NB15', load_unsw)]:
        t0 = time.time()
        X, ybin, ymc, mc_names, ntr = loader()
        print('== %s: %d rows x %d features, classes binary=%s, multi=%d' % (
            nm, X.shape[0], X.shape[1], sorted(np.unique(ybin).tolist()), len(mc_names)), flush=True)
        recs, names = run_dataset(nm, X, ybin, ymc, mc_names, ntr)
        allrecs[nm] = recs
        meta[nm] = {'n_rows': int(X.shape[0]), 'n_features': int(X.shape[1]),
                    'multiclass_labels': names, 'official_train_n': ntr,
                    'multiclass_sizes': {k: int(v) for k, v in pd.Series(ymc).value_counts().items()},
                    'binary_sizes': {k: int(v) for k, v in pd.Series(ybin).value_counts().items()},
                    'elapsed_s': round(time.time() - t0, 1)}
        print('== %s done in %.0fs' % (nm, time.time() - t0), flush=True)
    with open(os.path.join(OUT, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump({'results': allrecs, 'meta': meta}, f, indent=1)
    print('WROTE', os.path.join(OUT, 'results.json'))

if __name__ == '__main__':
    main()
