# -*- coding: utf-8 -*-
"""
14-抽样与下载清单.py  --  第三阶段：从合格池随机抽样，生成下载任务单

为什么抽样而不是全做：
  合格池 2000+ 篇，全部编码不可能。审计型综述的标准做法是
  "从合格记录中随机抽取 N 篇"，随机种子与抽样协议写进 Methods 即可，
  这比手工挑 100 篇更不容易被质疑选择性纳入。

输出：
  data/raw-search/sample-frame.csv     抽样框（含随机顺序号）
  14-下载任务单.md                      给你照着下的清单，按可获取性分组
控制台 ASCII。
"""
import csv, os, sys, io, random, collections, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(BASE, 'data', 'raw-search')
SRC  = os.path.join(RAW, 'shortlist.csv')

SEED = 20261018
SAMPLE_N = 180
TARGET_N = 100

DONE_TITLES = [
    'rtids: a robust transformer-based approach for intrusion detection system',
    'novel two-stage deep learning model for network intrusion detection: lstm-ae',
    'bat: deep learning methods on network intrusion detection using nsl-kdd dataset',
    'cnn-lstm: hybrid deep neural network for network intrusion detection system',
    'a 1d-cnn based deep learning architecture for network intrusion detection',
    'dl-ids: extracting features using cnn-lstm hybrid network for intrusion detection system',
    'analysis of kdd-cup99, nsl-kdd and unsw-nb15 datasets using deep learning in iot',
]

def norm(t):
    t = (t or '').lower()
    t = re.sub(r'[^a-z0-9 ]+', ' ', t)
    return ' '.join(t.split())

DONE = set(norm(t) for t in DONE_TITLES)


def main():
    rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
    print('[LOAD] shortlist %d rows' % len(rows))

    by_key, dups = {}, 0
    for r in rows:
        key = (r['doi'] or '').strip().lower() or norm(r['title'])
        if not key:
            continue
        if key in by_key:
            dups += 1
            if int(r['cited_by'] or 0) > int(by_key[key]['cited_by'] or 0):
                by_key[key] = r
        else:
            by_key[key] = r
    pool = list(by_key.values())
    print('[DEDUPE] removed %d duplicates -> pool %d' % (dups, len(pool)))

    before = len(pool)
    pool = [r for r in pool if norm(r['title']) not in DONE]
    print('[DEDUPE] removed %d already-coded -> pool %d' % (before - len(pool), len(pool)))

    rnd = random.Random(SEED)
    rnd.shuffle(pool)
    sample = pool[:SAMPLE_N]
    print('[SAMPLE] seed=%d  n=%d  from pool %d' % (SEED, len(sample), len(pool)))

    for i, r in enumerate(sample, 1):
        r['sample_no'] = i
        r['can_download_now'] = 'yes' if r['pdf_url'] else ('maybe' if r['is_oa'] == '1' else 'no')

    cols = ['sample_no'] + [c for c in sample[0].keys() if c != 'sample_no']
    with open(os.path.join(RAW, 'sample-frame.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in sample:
            w.writerow(r)

    n_pdf = sum(1 for r in sample if r['pdf_url'])
    n_oa  = sum(1 for r in sample if r['is_oa'] == '1')
    print()
    print('=== SAMPLE PROFILE ===')
    print('  has direct pdf_url : %d / %d' % (n_pdf, len(sample)))
    print('  is open access     : %d / %d' % (n_oa, len(sample)))
    print('  years: %s' % collections.Counter(r['year'] for r in sample).most_common())
    print('  venues top 15:')
    for v, c in collections.Counter(r['venue'] for r in sample).most_common(15):
        print('    %-55s %d' % (v[:55], c))

    TICK = chr(96)

    L = []
    L.append('# 14 · 下载任务单（%d 篇）' % len(sample))
    L.append('')
    L.append('**生成日期**：2026-10-18　**随机种子**：%d　**合格池**：%d 篇　**抽样**：%d 篇　**目标编码**：%d 篇'
             % (SEED, len(pool), len(sample), TARGET_N))
    L.append('')
    L.append('> 这份清单是从 **%d 篇合格记录**里用固定随机种子（%d）抽出来的。' % (len(pool), SEED))
    L.append('> 抽样协议直接写进论文 Methods，比手工挑 100 篇更不容易被质疑选择性纳入。')
    L.append('>')
    L.append('> **你要做的**：按顺序下载 PDF，存成 data/pNNN.pdf（如 p011.pdf）。')
    L.append('> 下不下来就跳过，在 04-PRISMA记录表.csv 记 E9，**绝对不要用别的网站凑**。')
    L.append('>')
    L.append('> **下到 %d 篇就够**，不用下满 %d 篇。' % (TARGET_N, len(sample)))
    L.append('')
    L.append('---')
    L.append('')

    groups = [
        ('A. 开放获取，有 PDF 直链（优先做这批）',
         [r for r in sample if r['pdf_url']]),
        ('B. 标记为 OA 但无直链，需点开落地页找 PDF',
         [r for r in sample if not r['pdf_url'] and r['is_oa'] == '1']),
        ('C. 订阅制，需校园网/VPN（下不下来就标 E9）',
         [r for r in sample if not r['pdf_url'] and r['is_oa'] != '1']),
    ]

    n = 0
    for gname, grp in groups:
        L.append('## %s　（%d 篇）' % (gname, len(grp)))
        L.append('')
        if not grp:
            L.append('_（无）_')
            L.append('')
            continue
        for r in grp:
            n += 1
            doi = r['doi'] or ''
            link = ('https://doi.org/' + doi) if doi else (r['landing'] or '')
            L.append('### %03d　%s' % (n, r['title']))
            L.append('')
            L.append('- **存成**：data/p%03d.pdf' % n)
            L.append('- **期刊**：%s　**年份**：%s' % (r['venue'], r['year']))
            if doi:
                L.append('- **DOI**：%s' % doi)
            L.append('- **打开**：%s' % link)
            if r['pdf_url']:
                L.append('- **PDF 直链**：%s' % r['pdf_url'])
            L.append('- **抽样号**：%s' % r['sample_no'])
            L.append('')
        L.append('---')
        L.append('')

    L.append('## 下完之后')
    L.append('')
    L.append('跟我说一句「下载完成，共 N 篇」，我就自动跑全文扫描与证据定位，')
    L.append('然后你按 10-编码结果与依据.md 的口径逐篇判 19 列。')
    L.append('')

    md = os.path.join(BASE, '14-下载任务单.md')
    open(md, 'w', encoding='utf-8').write('\n'.join(L))
    print()
    print('[SAVE] %s  (%d bytes)' % (md, os.path.getsize(md)))
    print('[SAVE] %s' % os.path.join(RAW, 'sample-frame.csv'))


if __name__ == '__main__':
    main()
