# -*- coding: utf-8 -*-
"""
12-检索执行.py  --  第一阶段：从 OpenAlex 拉取候选文献元数据

只做检索与元数据收集，不做判定。
输出：data/raw-search/openalex-<query>-<date>.json   (原始，不可改)
      data/raw-search/candidates-raw.csv             (合并去重后的候选清单)
控制台输出全为 ASCII，避免 Windows GBK 控制台乱码。

注：OpenAlex 的 cursor 分页对本账号返回 401，改用 page 分页（实测可用）。
"""
import json, os, sys, io, time, csv, urllib.request, urllib.parse, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(BASE, 'data', 'raw-search')
os.makedirs(RAW, exist_ok=True)

UA = {'User-Agent': 'nids-review/1.0 (mailto:hexy@example.edu)'}
TODAY = datetime.date.today().isoformat()

# ---------- 检索式（原样写进论文 Methods） ----------
Q = {}

Q['Q1'] = ('title_and_abstract.search:'
  '("intrusion detection" OR "network intrusion" OR "network anomaly")'
  ' AND ("deep learning" OR LSTM OR CNN OR transformer OR autoencoder'
  ' OR "neural network" OR "convolutional")'
  ' AND ("NSL-KDD" OR "KDD99" OR "KDD Cup" OR "KDDCup" OR "CICIDS" OR "CIC-IDS"'
  ' OR "UNSW-NB15" OR "Bot-IoT" OR "TON_IoT" OR "CICDDoS" OR "CSE-CIC")')

Q['Q2'] = ('title_and_abstract.search:'
  '("intrusion detection" OR "network intrusion")'
  ' AND ("deep learning" OR LSTM OR CNN OR transformer OR autoencoder)'
  ' AND ("data leakage" OR "reproducibility" OR "evaluation protocol"'
  ' OR "train-test split" OR "benchmark dataset" OR "experimental setup")')

COMMON = (',from_publication_date:2019-01-01,to_publication_date:2025-12-31'
          ',type:article,language:en')

SELECT = ('id,doi,title,publication_year,type,language,'
          'primary_location,best_oa_location,open_access,'
          'abstract_inverted_index,cited_by_count,authorships')

PER_PAGE = 200
MAX_PAGES = 25          # 25 * 200 = 5000 上限，足够覆盖

def fetch_all(name, filter_str):
    out, page = [], 1
    total = None
    while page <= MAX_PAGES:
        params = {
            'filter': filter_str + COMMON,
            'per-page': str(PER_PAGE),
            'page': str(page),
            'select': SELECT,
            'mailto': 'hexy@example.edu',
        }
        url = 'https://api.openalex.org/works?' + urllib.parse.urlencode(params)
        j = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers=UA)
                with urllib.request.urlopen(req, timeout=90) as r:
                    j = json.load(r)
                break
            except Exception as e:
                if attempt == 2:
                    print('[ERR] %s page %d: %s' % (name, page, e))
                    return out, total
                time.sleep(3)
        res = j.get('results', [])
        if total is None:
            total = j['meta']['count']
            print('[%s] server says total = %d' % (name, total))
        out.extend(res)
        print('[%s] page %d -> +%d  (%d / %d)' % (name, page, len(res), len(out), total))
        if len(res) < PER_PAGE or len(out) >= total:
            break
        page += 1
        time.sleep(0.4)
    return out, total

def unabstract(inv):
    if not inv:
        return ''
    pos = {}
    for w, idxs in inv.items():
        for i in idxs:
            pos[i] = w
    if not pos:
        return ''
    return ' '.join(pos[i] for i in sorted(pos))

def main():
    all_recs, stats = {}, []
    for name, f in Q.items():
        recs, total = fetch_all(name, f)
        path = os.path.join(RAW, 'openalex-%s-%s.json' % (name, TODAY))
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump({'query': f, 'common': COMMON, 'date': TODAY,
                       'reported_total': total, 'fetched': len(recs),
                       'results': recs}, fh, ensure_ascii=False)
        print('[SAVE] %s  (%d records)' % (path, len(recs)))
        stats.append((name, total, len(recs)))
        for r in recs:
            all_recs.setdefault(r['id'], r)

    print('[TOTAL] unique after dedupe: %d' % len(all_recs))

    rows = []
    for wid, r in all_recs.items():
        oa = r.get('open_access') or {}
        bo = r.get('best_oa_location') or {}
        pl = r.get('primary_location') or {}
        src = (pl.get('source') or {})
        rows.append({
            'openalex_id': wid.rsplit('/', 1)[-1],
            'doi': (r.get('doi') or '').replace('https://doi.org/', ''),
            'title': (r.get('title') or '').strip(),
            'year': r.get('publication_year') or '',
            'venue': src.get('display_name') or '',
            'is_oa': 1 if oa.get('is_oa') else 0,
            'oa_status': oa.get('oa_status') or '',
            'pdf_url': bo.get('pdf_url') or '',
            'landing': bo.get('landing_page_url') or '',
            'cited_by': r.get('cited_by_count') or 0,
            'abstract': unabstract(r.get('abstract_inverted_index')),
            'n_authors': len(r.get('authorships') or []),
        })

    rows.sort(key=lambda x: (-(x['year'] or 0), -x['cited_by']))
    csvp = os.path.join(RAW, 'candidates-raw.csv')
    cols = ['openalex_id','doi','title','year','venue','is_oa','oa_status',
            'pdf_url','landing','cited_by','n_authors','abstract']
    with open(csvp, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print('[SAVE] %s  (%d rows)' % (csvp, len(rows)))

    n_oa  = sum(1 for r in rows if r['is_oa'])
    n_pdf = sum(1 for r in rows if r['pdf_url'])
    print('[STAT] is_oa=%d   has_pdf_url=%d   total=%d' % (n_oa, n_pdf, len(rows)))
    print()
    print('=== SEARCH LOG (paste into 01-检索式.md) ===')
    for name, total, got in stats:
        print('  %s | %s | reported=%s | fetched=%d' % (name, TODAY, total, got))
    print('  after dedupe | %d' % len(rows))

if __name__ == '__main__':
    main()
