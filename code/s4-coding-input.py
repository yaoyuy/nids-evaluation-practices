# -*- coding: utf-8 -*-
"""
17-紧凑编码输入.py  v4 -- 把每篇 PDF 压成一段可直接判定的证据摘要

v4 变更（降噪）：
  1) 参考文献页的命中不再展示（只在没有正文命中时才展示，并标 REF），
     因为参考文献里的 github / doi 链接是最主要的误判来源。
  2) CODE 组不再匹配裸 http(s)://，只匹配代码托管站与 availability 措辞。
  3) COMPUTE 组不再匹配裸 parameters / cpu / gpu，只匹配硬件型号、耗时数值、参数量数值。
  4) LEAK 组去掉 generaliz / shortcut 这类噪声词。
  5) ABLATE 组去掉 component analysis / sensitivity analysis（大量误命中）。
  6) 新增页眉页脚过滤（含期刊名 + doi + 页码的行）。
  7) 新增 SPLIT 强信号组 SPLIT2，只抓"比例 + 训练/测试"同句。

用法:
    python 17-紧凑编码输入.py            # 每 10 篇一批
    python 17-紧凑编码输入.py 15
输出: output/code-input/batch-NN.txt
"""
import os, re, sys, io, csv

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data')
OUT  = os.path.join(BASE, 'output', 'code-input')
SRC  = os.path.join(DATA, 'raw-search', 'sample-frame.csv')

MIN_BYTES = 30000
SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9(\[])')
MAXLEN = 260
TOPN = 3

REF_HEAD = re.compile(r'^\s*(references|bibliography|reference list)\s*$', re.I | re.M)
AVAIL_HEAD = re.compile(
    r'(data|code|software|source code)\s*(and\s*\w+\s*)?availabilit', re.I)

DATASET_RX = re.compile(
    r'(NSL[- ]?KDD|KDD ?Cup ?.?99|KDD99|CICIDS ?2017|CIC-?IDS ?2017|CICIDS ?2018|'
    r'UNSW[- ]?NB ?15|CIC-?DDoS ?2019|CICDDoS ?2019|Bot[- ]?IoT|TON_?IoT|ToN[- ]?IoT|'
    r'CIC[- ]?IoT ?2023|CICIoT ?2023|CICIDS ?2019|ISCX|AWID|Kyoto ?2006|'
    r'Edge[- ]?IIoTset|IoT[- ]?23)', re.I)

METRIC_RX = re.compile(
    r'\b(accuracy|precision|recall|f1[- ]?score|f-measure|auc|roc auc|false alarm|'
    r'detection rate|tpr|fpr|tnr|mcc|g-mean)\b', re.I)

URL_RX = re.compile(r'https?://[^\s,;)\]]+')

# 页眉页脚：期刊名 + 页码 + doi 之类
HEADER_RX = re.compile(
    r'(https?://doi\.org|www\.|Journal|VOLUME|Vol\.|No\.\s*\d|ISSN|Received|Accepted|'
    r'Published|©|Copyright|Page \d+ of \d+|\|\s*\d+\s*\|)', re.I)

GROUPS = [
    ('SPLIT',
     [r'\bsplit\b', r'\bdivid', r'hold.?out', r'cross.?valid', r'k.?fold',
      r'partition', r'training set', r'test set', r'for training', r'for testing',
      r'train(ing)? (data|set).{0,40}test'],
     [r'train.{0,80}test', r'test.{0,80}train',
      r'\d{2}\s*%\s*(of\s*)?(the\s*)?(data|dataset|samples|records|instances)',
      r'\b(80|70|60|75|90)\s*[:/]\s*(20|30|40|25|10)\b',
      r'randomly (split|divided|partitioned|selected|chosen|shuffled)',
      r'k.?fold', r'cross.?validat', r'temporal', r'chronological',
      r'group(ed)? by (attack|host|session|source)']),

    ('CODE',
     [r'github', r'gitlab', r'zenodo', r'figshare', r'bitbucket',
      r'source code', r'code (is|was|are) (publicly )?available',
      r'upon (reasonable )?request', r'available (on|at) request',
      r'code availabilit', r'data availabilit', r'open.?source'],
     [r'(github|gitlab|zenodo|figshare|bitbucket)\.com',
      r'code.{0,50}(available|released|provided|shared)',
      r'(publicly|freely) available', r'upon (reasonable )?request']),

    ('RUNS',
     [r'random[ _]seed', r'\bseeds?\b', r'\d+\s+(independent\s+)?runs',
      r'average[sd]? (of|over)', r'mean\s*(±|\+/-)', r'standard deviation',
      r'repeated\s+\d+', r'confidence interval'],
     [r'random[ _]seed', r'seeds?\s*(=|of|value|number)',
      r'\d+\s+(independent\s+)?runs', r'mean\s*(±|\+/-)',
      r'standard deviation', r'repeated\s+\d+',
      r'(average|averaged) (over|of) \d+', r'\d+\s*times.{0,30}(repeat|run)']),

    ('ABLATE',
     [r'ablation', r'we (remove|drop|exclude)',
      r'without the (module|component|attention|layer|block|branch)'],
     [r'ablation', r'without the (module|component|attention|layer|block|branch)',
      r'we (remove|drop|exclude)']),

    ('LEAK',
     [r'\bleak', r'contaminat', r'\boverlap', r'duplicat', r'same.?source',
      r'unseen (attack|host|session|class)', r'data leakage'],
     [r'\bleak', r'contaminat', r'duplicat', r'same.?source',
      r'unseen (attack|host|session)', r'train.{0,40}test.{0,40}(overlap|duplicat)']),

    ('SAME',
     [r'under the same', r'same (split|protocol|setting|condition)',
      r'as reported (in|by)', r'taken from (the )?(original|their)',
      r're-?implement', r'we (also )?(re)?(train|implement|run)(ed)? (the )?(baseline|comparison)',
      r'we constructed', r'baseline'],
     [r'under the same', r'same (split|protocol|setting|condition)',
      r're-?implement',
      r'we (also )?(re)?(train|implement|run)(ed)? (the )?(baseline|comparison)',
      r'we constructed']),

    ('COMPUTE',
     [r'nvidia|geforce|rtx|gtx|tesla|quadro',
      r'intel (core|xeon)|amd ryzen|xeon|core i\d',
      r'\d+\s*gb\s*(ram|vram|memory)',
      r'training time', r'training took', r'inference time',
      r'\d+(\.\d+)?\s*(s|sec|seconds|min|minutes|hours)\s*(of\s*)?(training|to train)',
      r'number of (trainable )?parameters', r'flops', r'\btpu\b'],
     [r'nvidia|geforce|rtx|gtx|tesla|quadro',
      r'intel (core|xeon)|amd ryzen|xeon|core i\d',
      r'\d+\s*gb\s*(ram|vram|memory)',
      r'training time', r'\d+(\.\d+)?\s*(s|sec|seconds|min|minutes|hours)',
      r'number of (trainable )?parameters', r'flops']),

    ('HYPER',
     [r'learning rate', r'\blr\b', r'batch size', r'\bepochs?\b', r'optimizer',
      r'adam|sgd|rmsprop|adagrad|adamw|nadam', r'dropout', r'hidden (layer|unit|node)',
      r'number of (neurons|units|layers)', r'activation function', r'relu|sigmoid|tanh|softmax'],
     [r'learning rate', r'batch size', r'\bepochs?\b', r'optimizer',
      r'adam|sgd|rmsprop|adagrad|adamw', r'dropout', r'hidden (layer|unit|node)',
      r'number of (neurons|units|layers)']),

    ('IMBAL',
     [r'smote', r'oversampl', r'undersampl', r'class[_ ]weight',
      r'focal loss', r'weighted loss', r'imbalanc', r'class imbalance'],
     [r'smote', r'oversampl', r'undersampl', r'class[_ ]weight', r'focal loss']),

    ('VERSION',
     [r'downloaded (from|on|in)', r'accessed (on|in)', r'version\s*[\d.]',
      r'available at http', r'corrected (version|dataset)',
      r'https?://(www\.)?(unb\.ca|research\.unsw|kaggle\.com|ieee-dataport|'
      r'cse\.csi|iscx|canadian|registry\.opendata)'],
     [r'downloaded (from|on|in)', r'accessed (on|in)', r'version\s*[\d.]',
      r'corrected (version|dataset)']),
]


def clean(t):
    t = t.replace('\u00ad', '').replace('\ufb01', 'fi').replace('\ufb02', 'fl')
    t = re.sub(r'[ \t]+', ' ', t)
    return t


def sents(text):
    text = re.sub(r'\s+', ' ', text)
    out = []
    for s in SENT.split(text):
        s = s.strip()
        if 25 <= len(s) <= 600:
            out.append(s)
    return out


def find_ref_start(doc):
    for i, p in enumerate(doc, 1):
        if REF_HEAD.search(p.get_text()):
            return i
    for i, p in enumerate(doc, 1):
        t = p.get_text()
        if re.search(r'\bReferences\b', t) and len(re.findall(r'\[\d+\]', t)) >= 5:
            return i
    return len(doc) + 1


def availability_block(doc, ref_start):
    out = []
    for i, p in enumerate(doc, 1):
        if i >= ref_start:
            break
        t = re.sub(r'\s+', ' ', clean(p.get_text()))
        m = AVAIL_HEAD.search(t)
        if not m:
            continue
        out.append('p%d| %s' % (i, t[max(0, m.start()):max(0, m.start()) + 380]))
    return out


def score(s, bonus):
    n = 0
    for rx in bonus:
        if rx.search(s):
            n += 2
    if len(s) < 200:
        n += 1
    if HEADER_RX.search(s):
        n -= 2
    return n


def group_hits(pages, kws, bonus, ref_start):
    kws = [re.compile(p, re.I) for p in kws]
    bonus = [re.compile(p, re.I) for p in bonus]
    body, ref = [], []
    seen = set()
    for pno, ss in pages:
        after = pno >= ref_start
        for s in ss:
            if not any(rx.search(s) for rx in kws):
                continue
            k = re.sub(r'\W+', '', s[:60]).lower()
            if k in seen:
                continue
            seen.add(k)
            sc = score(s, bonus)
            (ref if after else body).append((sc, pno, s))
    body.sort(key=lambda x: -x[0])
    ref.sort(key=lambda x: -x[0])
    if body:
        return body[:TOPN], len(body) + len(ref), len(body)
    return ref[:1], len(ref), 0


def profile(path, row):
    doc = pymupdf.open(path)
    npages = len(doc)
    ref_start = find_ref_start(doc)
    pages = [(i, sents(clean(p.get_text()))) for i, p in enumerate(doc, 1)]
    body = ' '.join(s for pno, ss in pages if pno < ref_start for s in ss)

    L = []
    L.append('=' * 66)
    L.append('p%s  %s (%s)  %dpp  ref@%d'
             % (row['sample_no'], row['venue'][:36], row['year'], npages, ref_start))
    L.append('T: ' + row['title'][:130])
    L.append('DOI: ' + (row['doi'] or '-'))

    ds, seen = [], set()
    for m in DATASET_RX.finditer(body):
        k = re.sub(r'\W+', '', m.group(0)).upper()
        if k not in seen:
            seen.add(k)
            ds.append(m.group(0))
    L.append('DS: ' + (', '.join(ds[:6]) if ds else 'NONE'))

    mt, seenm = [], set()
    for m in METRIC_RX.finditer(body):
        k = m.group(0).lower()
        if k not in seenm:
            seenm.add(k)
            mt.append(k)
    L.append('MT: ' + (', '.join(mt[:7]) if mt else 'NONE'))

    urls = []
    for u in URL_RX.finditer(body):
        v = u.group(0).rstrip('.').rstrip(')')
        if 'creativecommons' in v or 'doi.org' in v:
            continue
        if v not in urls:
            urls.append(v)
    L.append('URL: ' + (' | '.join(urls[:3]) if urls else 'NONE'))

    avail = availability_block(doc, ref_start)
    if avail:
        L.append('AVAIL:')
        for a in avail[:2]:
            L.append('   ' + a[:300])

    for name, kws, bonus in GROUPS:
        hits, total, nbody = group_hits(pages, kws, bonus, ref_start)
        if not hits:
            L.append('%-7s 0   [silent]' % name)
            continue
        L.append('%-7s %d (body %d)' % (name, total, nbody))
        for sc, pno, s in hits:
            L.append('   p%-3d| %s' % (pno, s[:MAXLEN]))
    L.append('')
    doc.close()
    return '\n'.join(L)


def main():
    per = 10
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        per = int(sys.argv[1])

    rows = {int(r['sample_no']): r for r in csv.DictReader(open(SRC, encoding='utf-8-sig'))}
    files = []
    for f in os.listdir(DATA):
        if not f.lower().endswith('.pdf'):
            continue
        stem = f[:-4]
        if not stem.startswith('p') or not stem[1:].isdigit():
            continue
        n = int(stem[1:])
        if n not in rows:
            continue
        p = os.path.join(DATA, f)
        if os.path.getsize(p) < MIN_BYTES:
            continue
        files.append((n, p))
    files.sort()
    print('[FOUND] %d PDFs' % len(files))

    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.endswith('.txt'):
            os.remove(os.path.join(OUT, old))

    nb = 0
    for i in range(0, len(files), per):
        nb += 1
        chunk = files[i:i + per]
        parts = []
        for n, p in chunk:
            try:
                parts.append(profile(p, rows[n]))
            except Exception as e:
                parts.append('p%d FAILED: %s\n' % (n, e))
        out = os.path.join(OUT, 'batch-%02d.txt' % nb)
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(parts))
        print('[OK] batch-%02d.txt  %d papers  %d bytes'
              % (nb, len(chunk), os.path.getsize(out)))
    print()
    print('[DONE] %d batches' % nb)


if __name__ == '__main__':
    main()
