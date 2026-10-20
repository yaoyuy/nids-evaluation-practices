# -*- coding: utf-8 -*-
"""
09 - Full-text keyword scanner for the NIDS evaluation-practice review.

WHAT IT DOES
  Reads every PDF in data/, splits the text into sentences, and writes one
  report per paper into output/scan/. Each report shows ONLY the sentences
  relevant to each of the 19 coding columns, with page numbers.

WHY
  A 15-page paper needs 4-5 pages of reading to code. This script cuts that
  to about 30 lines of text per paper, so a paper takes 3-4 minutes instead
  of 10-15. It does NOT decide anything - every judgement is still yours.

USAGE
  1. Put the PDFs into data/  (any filename: P01.pdf, p01_masser.pdf, ...)
  2. Run:  python 09-全文扫描助手.py
  3. Read output/scan/<name>.txt

REQUIREMENTS
  pip install pymupdf      (already installed on this machine)
"""

import os
import re
import sys

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        print('[FATAL] pymupdf is not installed. Run: pip install pymupdf')
        sys.exit(1)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, 'data')
OUT_DIR = os.path.join(BASE, 'output', 'scan')

# ------------------------------------------------------------------
# keyword groups: one per coding column that needs evidence
# each entry is (column_name, [regex patterns], hint_for_reader)
# ------------------------------------------------------------------
GROUPS = [
    ('DATASET', [
        r'\bCICIDS?[- ]?2017\b', r'\bCIC-IDS[- ]?2017\b', r'\bNSL[- ]?KDD\b',
        r'\bKDD[- ]?Cup[- ]?99\b', r'\bUNSW[- ]?NB15\b', r'\bBot[- ]?IoT\b',
        r'\bTON[-_ ]?IoT\b', r'\bEdge[- ]?IIoTset\b', r'\bCIC[- ]?DDoS\b',
        r'\bCICIDS?2018\b', r'\bCSE[- ]?CIC[- ]?IDS\b', r'\bKDDTest\+',
        r'\bInSDN\b', r'\b5G[- ]?NIDD\b', r'\bAWD\b',
        r'downloaded from', r'available at', r'obtained from',
    ], 'which dataset, and did they say which version / download date?'),

    ('SPLIT PROTOCOL  [most important column]', [
        r'train(ing)?[- ]?(and|/|&)[- ]?test', r'\bsplit\b', r'\bsplitting\b',
        r'randomly (divided|selected|chosen|partitioned|sampled)',
        r'random_state', r'\bseed\b', r'\bshuffl', r'\bk[- ]?fold\b',
        r'cross[- ]?validat', r'\bhold[- ]?out\b', r'\bstratified\b',
        r'chronological', r'\btemporal\b', r'time[- ]?(based|ordered|series)',
        r'\bby day\b', r'\bper day\b', r'\bgroup(ed)? by\b', r'leave[- ]one[- ]out',
        r'\b(80|70|60|75|90|50)\s?%',
        r'training (set|data)', r'test(ing)? (set|data)',
    ], 'RANDOM / TEMPORAL / GROUP / not stated. Reporting a ratio is NOT reporting a protocol.'),

    ('CODE AVAILABILITY', [
        r'github', r'gitlab', r'bitbucket', r'zenodo', r'figshare', r'codeocean',
        r'source code', r'code (is|are) (available|publicly)', r'publicly available',
        r'upon (reasonable )?request', r'on request', r'data availability',
        r'code availability', r'supplementary (material|file)',
    ], 'Only a clickable link counts as YES. upon-request = NO.'),

    ('HYPERPARAMETERS', [
        r'learning rate', r'\blr\b', r'batch size', r'\bepochs?\b', r'optimizer',
        r'\bAdam\b', r'\bSGD\b', r'\bRMSprop\b', r'dropout',
        r'hidden (units|layers|size)', r'activation function', r'kernel size',
        r'number of (layers|filters)',
    ], 'enough detail for someone else to rebuild the model?'),

    ('RUNS / VARIANCE', [
        r'\bruns?\b', r'\bseeds?\b', r'averag(e|ed) (over|of)', r'repeat(ed)?',
        r'\u00b1', r'\bstd\b', r'standard deviation', r'\bvariance\b',
        r'confidence interval', r'\bmean\b', r'multiple times',
    ], 'single number with no +- and no seed = NO'),

    ('ABLATION', [
        r'ablation', r'\bw/o\b', r'without (the )?(proposed|attention|module)',
        r'contribution of', r'effect of (each|the) (component|module|layer)',
    ], 'did they isolate what actually helps?'),

    ('COMPUTE COST', [
        r'\bGPU\b', r'\bCPU\b', r'\bTPU\b', r'NVIDIA', r'RTX', r'Tesla', r'GeForce',
        r'\bA100\b', r'\bV100\b', r'training time', r'\bhours?\b', r'\bminutes?\b',
        r'\bRAM\b', r'\bIntel\b', r'\bAMD\b', r'inference time', r'latency',
    ], 'can a reader estimate the reproduction cost?'),

    ('LEAKAGE / GENERALISATION', [
        r'\bleakage\b', r'\bleak\b', r'\boverlap\b', r'\bduplicat', r'\bbias(ed)?\b',
        r'generalis', r'generaliz', r'unseen', r'unknown attack', r'zero[- ]day',
        r'same distribution', r'distribution shift', r'overestimat', r'optimistic',
        r'threats? to validity', r'limitation',
    ], 'do they acknowledge that their split may inflate results?'),

    ('METRICS REPORTED', [
        r'\baccuracy\b', r'\bF1\b', r'F1[- ]score', r'F[- ]measure', r'\bprecision\b',
        r'\brecall\b', r'\bAUC\b', r'\bROC\b', r'\bFPR\b', r'\bFAR\b',
        r'false (positive|alarm) rate', r'detection rate', r'\bDR\b', r'\bMCC\b',
        r'confusion matrix', r'\bkappa\b',
    ], 'is Accuracy the ONLY metric in the main table?'),

    ('CLASS IMBALANCE', [
        r'\bSMOTE\b', r'oversampl', r'undersampl', r'\bresampl', r'class weight',
        r'imbalanc', r'\bADASYN\b', r'cost[- ]sensitive', r'weighted loss',
    ], 'did they handle it, or just mention it?'),

    ('COMPARISON FAIRNESS', [
        r'compared (with|to)', r'baseline', r'state[- ]of[- ]the[- ]art', r'\bSOTA\b',
        r'same (settings|conditions|protocol|split)', r're[- ]implement', r'reproduc',
    ], 'did they compare under the SAME split protocol?'),
]

COMPILED = [(name, [re.compile(p, re.IGNORECASE) for p in pats], hint)
            for name, pats, hint in GROUPS]

MAX_HITS_PER_GROUP = 12
SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z(\[])')
MIN_CHARS = 2000


def clean(text):
    text = text.replace('\u00ad', '')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_sentences(text):
    out = []
    for p in SENT_SPLIT.split(text):
        p = p.strip()
        if len(p) < 25:
            continue
        if len(p) > 700:
            for i in range(0, len(p), 600):
                out.append(p[i:i + 600])
        else:
            out.append(p)
    return out


def scan_pdf(path):
    doc = pymupdf.open(path)
    pages = []
    for i, page in enumerate(doc):
        try:
            txt = page.get_text('text')
        except Exception:
            txt = ''
        pages.append((i + 1, split_sentences(clean(txt))))
    doc.close()
    return pages


def build_report(name, pages):
    L = []
    L.append('=' * 74)
    L.append('PAPER: ' + name)
    L.append('PAGES: ' + str(len(pages)))
    L.append('=' * 74)
    L.append('')
    L.append('How to use: read the quoted sentences under each heading, then fill')
    L.append('that column in 03-编码表.csv. The page number is shown as [pN].')
    L.append('Nothing here is a decision - every call is yours.')
    L.append('')
    summary = []
    for gname, pats, hint in COMPILED:
        hits = []
        for pno, sents in pages:
            for s in sents:
                for rx in pats:
                    if rx.search(s):
                        hits.append((pno, s))
                        break
        summary.append((gname, len(hits)))
        L.append('-' * 74)
        L.append('## ' + gname + '   (' + str(len(hits)) + ' hits)')
        L.append('   what to look for: ' + hint)
        L.append('')
        if not hits:
            L.append('   [NO HIT] No sentence in this PDF mentions any expected')
            L.append('   keyword. That is itself evidence: the paper most likely')
            L.append('   does NOT report this item at all.')
            L.append('')
            continue
        seen = set()
        shown = 0
        for pno, s in hits:
            key = s[:90].lower()
            if key in seen:
                continue
            seen.add(key)
            if shown >= MAX_HITS_PER_GROUP:
                L.append('   ... (' + str(len(hits) - shown) + ' more hits omitted)')
                break
            L.append('   [p' + str(pno) + '] ' + s)
            shown += 1
        L.append('')
    L.append('=' * 74)
    L.append('HIT SUMMARY  (a zero means the paper is silent on that item)')
    L.append('=' * 74)
    for gname, n in summary:
        L.append('   ' + str(n).rjust(4) + '  ' + gname)
    L.append('')
    return '\n'.join(L), summary


def main():
    print('[INFO] scanning PDFs in: ' + DATA_DIR)
    if not os.path.isdir(DATA_DIR):
        print('[FATAL] data/ folder does not exist.')
        return 1
    pdfs = sorted([f for f in os.listdir(DATA_DIR) if f.lower().endswith('.pdf')])
    if not pdfs:
        print('[INFO] no PDF found in data/.')
        print('       Put the papers there and run again.')
        return 0
    os.makedirs(OUT_DIR, exist_ok=True)
    ok = 0
    bad = []
    for fn in pdfs:
        path = os.path.join(DATA_DIR, fn)
        stem = os.path.splitext(fn)[0]
        try:
            pages = scan_pdf(path)
        except Exception as e:
            bad.append((fn, str(e)[:80]))
            print('[FAIL] ' + fn + ' -> ' + str(e)[:80])
            continue
        nchars = sum(len(s) for _, ss in pages for s in ss)
        if nchars < MIN_CHARS:
            bad.append((fn, 'almost no text (' + str(nchars) + ' chars) - probably a scanned image PDF'))
            print('[WARN] ' + fn + ' -> only ' + str(nchars) + ' chars, likely a scan. Skipped.')
            continue
        report, summary = build_report(stem, pages)
        outp = os.path.join(OUT_DIR, stem + '.txt')
        with open(outp, 'w', encoding='utf-8') as f:
            f.write(report)
        zero = [g for g, n in summary if n == 0]
        print('[OK] ' + fn + ' -> ' + str(len(pages)) + ' pages, '
              + str(nchars) + ' chars, ' + str(len(zero)) + ' silent section(s)')
        ok += 1
    print('')
    print('[DONE] ' + str(ok) + ' report(s) written to output/scan/')
    if bad:
        print('[NOTE] ' + str(len(bad)) + ' file(s) skipped:')
        for fn, why in bad:
            print('       - ' + fn + ' : ' + why)
    return 0


if __name__ == '__main__':
    sys.exit(main())
