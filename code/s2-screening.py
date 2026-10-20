# -*- coding: utf-8 -*-
"""
13-自动初筛.py  --  第二阶段：按 02-纳入排除标准.md 对标题+摘要做自动初筛

只做"能机器判的"部分，拿不准的一律标 maybe，留给人判。
输出：
  data/raw-search/screening-auto.csv    每条一个 decision
  data/raw-search/shortlist.csv         通过初筛的候选（按可获取性排序）
控制台 ASCII。
"""
import csv, os, sys, io, re, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(BASE, 'data', 'raw-search')

SRC = os.path.join(RAW, 'candidates-raw.csv')
OUT1 = os.path.join(RAW, 'screening-auto.csv')
OUT2 = os.path.join(RAW, 'shortlist.csv')

# ---- 公开数据集白名单（I3）----
DATASETS = [
    'nsl-kdd', 'nsl kdd', 'kdd99', 'kdd cup', 'kddcup', 'kdd-99', 'kdd 99',
    'cicids', 'cic-ids', 'cse-cic', 'cicddos', 'cic-ddos',
    'unsw-nb15', 'unsw nb15', 'unsw',
    'bot-iot', 'bot_iot', 'bot iot',
    'ton_iot', 'ton-iot',
    'isax', 'iscx', 'awid', 'ciciot', 'iot-23', 'iot23',
    'nsl', 'ids2017', 'ids2018', 'ids-2017', 'ids-2018',
    'unsw-nb15', 'ctu-13', 'ctu13', 'caida', 'darknet',
    'mawilab', 'cicids2017', 'cicids2018',
]

# ---- E1 综述关键词（标题层）----
E1_TITLE = [
    'survey', 'review', 'overview', 'systematic literature', 'systematic review',
    'a taxonomy', 'state of the art', 'state-of-the-art', 'literature review',
    'meta-analysis', 'bibliometric', 'research trends', 'a comprehensive study of',
    'scoping review', 'tutorial',
]

# ---- E7 非网络流量主题（标题层）----
E7_TITLE = [
    'malware', 'phishing', 'spam', 'ransomware', 'android', 'iot firmware',
    'hdfs', 'log anomaly', 'log-based', 'binary code', 'vulnerability detection',
    'fraud detection', 'botnet detection using dns', 'url',
]

# ---- 主题关键词（I1）----
I1_KEYS = ['intrusion detection', 'intrusion', 'network intrusion', 'anomaly detection',
           'attack detection', 'nids', 'ids ', 'network security', 'traffic classification',
           'network traffic', 'ddos']

# ---- 方法关键词（I1 深度学习）----
DL_KEYS = ['deep learning', 'neural network', 'lstm', 'cnn', 'transformer', 'autoencoder',
           'gru', 'rnn', 'dnn', 'mlp', 'convolutional', 'recurrent', 'attention',
           'generative adversarial', 'gan', 'graph neural', 'gnn', 'bert', 'federated',
           'reinforcement learning', 'machine learning', 'random forest', 'xgboost',
           'svm', 'ensemble', 'stacking', 'boosting', 'resnet', 'vgg', 'inception']

# ---- 明显非研究性（E2）----
E2_TITLE = ['editorial', 'erratum', 'correction', 'retraction', 'comment on',
            'letter to the editor', 'book review', 'preface']


def low(s):
    return (s or '').lower()


def hit(keys, text):
    t = low(text)
    return [k for k in keys if k in t]


def decide(r):
    title, ab = r['title'], r['abstract']
    both = title + ' ' + ab

    # E2
    if hit(E2_TITLE, title):
        return 'exclude', 'E2 non-research'
    # E1 综述
    if hit(E1_TITLE, title):
        return 'exclude', 'E1 review/survey'
    # E7 主题不符
    e7 = hit(E7_TITLE, title)
    if e7 and not hit(['network traffic', 'intrusion detection'], title):
        return 'exclude', 'E7 off-topic(%s)' % e7[0]
    # I1 主题
    if not hit(I1_KEYS, both):
        return 'exclude', 'E7 no-ids-topic'
    # I1 方法
    if not hit(DL_KEYS, both):
        return 'exclude', 'I1 no-ml-method'
    # I3 数据集
    ds = hit(DATASETS, ab)
    if not ds:
        return 'maybe', 'I3 dataset-unclear'
    # I4 可编码性：摘要里有结果数字
    if not re.search(r'\d+\.\d+\s*%|\b9[0-9]\.\d+\b|\baccuracy\b|\bf1\b', low(ab)):
        return 'maybe', 'I4 no-result-in-abstract'
    return 'include', 'auto-pass'


def main():
    rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
    print('[LOAD] %d candidates' % len(rows))

    out, cnt = [], collections.Counter()
    for r in rows:
        d, why = decide(r)
        cnt[(d, why)] += 1
        r2 = dict(r)
        r2['auto_decision'] = d
        r2['auto_reason'] = why
        out.append(r2)

    cols = list(rows[0].keys()) + ['auto_decision', 'auto_reason']
    with open(OUT1, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in out:
            w.writerow(r)

    print()
    print('=== AUTO SCREENING RESULT ===')
    for d in ['include', 'maybe', 'exclude']:
        n = sum(1 for r in out if r['auto_decision'] == d)
        print('  %-8s %d' % (d, n))
    print()
    print('--- reason breakdown ---')
    for (d, why), n in sorted(cnt.items(), key=lambda x: -x[1]):
        print('  %-8s %-40s %d' % (d, why[:40], n))

    # shortlist：include + maybe，且优先可下载
    short = [r for r in out if r['auto_decision'] in ('include', 'maybe')]
    short.sort(key=lambda r: (-int(r['is_oa']), -(int(r['year']) if r['year'] else 0),
                              -int(r['cited_by'] or 0)))
    with open(OUT2, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in short:
            w.writerow(r)

    n_oa = sum(1 for r in short if r['is_oa'] == '1')
    n_pdf = sum(1 for r in short if r['pdf_url'])
    print()
    print('[SHORTLIST] %d rows  (is_oa=%d, has_pdf_url=%d)' % (len(short), n_oa, n_pdf))
    print('[SAVE] %s' % OUT1)
    print('[SAVE] %s' % OUT2)


if __name__ == '__main__':
    main()
