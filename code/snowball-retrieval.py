# -*- coding: utf-8 -*-
"""33-引文滚雪球.py
Backward + forward citation snowballing from the 93 included studies, as a second
search strand and a coverage check on the single-database (OpenAlex) search.
Outputs data/snowball/*.csv and prints ASCII counts.
"""
import os, csv, sys, json, time, re, urllib.request, urllib.error, urllib.parse, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'data', 'snowball')
os.makedirs(OUT, exist_ok=True)
MAIL = 'mailto=research@example.org'
UA = {'User-Agent': 'snowball/1.0 ' + MAIL}
SEL = 'id,doi,title,publication_year,cited_by_count,primary_location,open_access,abstract_inverted_index'
BATCH_SEED = 20
BATCH_ID = 50

def get(url, tries=4):
    for t in range(tries):
        try:
            r = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(r, timeout=60) as f:
                return json.loads(f.read().decode('utf-8', 'ignore'))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(2 + 3 * t); continue
            return {'_err': e.code, '_url': url[:120]}
        except Exception as e:
            time.sleep(2 + 2 * t)
    return {'_err': 'retry-exhausted', '_url': url[:120]}

def abstract_text(inv):
    if not inv: return ''
    pos = {}
    for w, ps in inv.items():
        for p in ps: pos[p] = w
    return ' '.join(pos[k] for k in sorted(pos))[:4000]

def venue_of(w):
    pl = w.get('primary_location') or {}
    src = pl.get('source') or {}
    return src.get('display_name') or ''

def pid_num(pid):
    return int(pid[1:]) if pid[1:].isdigit() else None

# ---------------- 1. the 93 included studies ----------------
PILOT = {
    'P01': '10.1109/access.2021.3056614', 'P02': '10.1155/2020/8890306',
    'P03': '10.1109/access.2022.3182333', 'P04': '10.1109/access.2023.3266979',
    'P05': '10.1109/access.2020.2972627', 'P07': '10.1109/access.2022.3206425',
    'P09': '10.3390/app12167986',          'P10': '10.1016/j.procs.2020.03.367',
}
def build_corpus():
    coded = [r['paper_id'] for r in csv.DictReader(open(os.path.join(BASE, '03-编码表.csv'), encoding='utf-8-sig'))]
    dl = {int(r['sample_no']): r for r in csv.DictReader(open(os.path.join(BASE, 'data', 'download-log.csv'), encoding='utf-8-sig'))}
    out = []
    for pid in coded:
        if pid in PILOT:
            out.append({'paper_id': pid, 'doi': PILOT[pid], 'title': ''})
        else:
            n = pid_num(pid)
            row = dl.get(n) if n else None
            out.append({'paper_id': pid, 'doi': (row or {}).get('doi') or '', 'title': (row or {}).get('title') or ''})
    return out

# ---------------- 2. resolve incl uded studies to OpenAlex ----------------
def resolve(corpus):
    seeds, miss = [], []
    for i, r in enumerate(corpus):
        w = None
        if r['doi']:
            w = get('https://api.openalex.org/works/doi:%s?select=id,title,referenced_works,cited_by_count&%s'
                    % (urllib.parse.quote(r['doi'].lower()), MAIL))
            if '_err' in w or not w or not w.get('id'): w = None
        if w is None and r['title']:
            q = get('https://api.openalex.org/works?filter=title.search:%s&per-page=1&select=id,title,referenced_works&%s'
                    % (urllib.parse.quote(r['title'][:180]), MAIL))
            if isinstance(q, dict) and q.get('results'): w = q['results'][0]
        if w and w.get('id'):
            seeds.append({'paper_id': r['paper_id'], 'wid': w['id'].rsplit('/', 1)[-1],
                          'title': w.get('title') or r['title'], 'n_ref': len(w.get('referenced_works') or []),
                          'refs': w.get('referenced_works') or []})
        else:
            miss.append(r)
        if (i + 1) % 20 == 0: print('  resolved %d/%d' % (i + 1, len(corpus)), flush=True)
    print('[RESOLVE] %d of %d resolved, %d unresolved' % (len(seeds), len(corpus), len(miss)), flush=True)
    json.dump([m['paper_id'] for m in miss], open(os.path.join(OUT, 'unresolved.json'), 'w'))
    return seeds

# ---------------- 3. backward ----------------
def backward(seeds):
    cnt = collections.Counter(); where = {}
    for s in seeds:
        for w in s['refs']:
            k = w.rsplit('/', 1)[-1]; cnt[k] += 1; where.setdefault(k, []).append(s['paper_id'])
    print('[BACKWARD] %d unique referenced works' % len(cnt), flush=True)
    return cnt, where

# ---------------- 4. forward ----------------
def forward(seeds):
    ids = [s['wid'] for s in seeds]
    cnt = collections.Counter(); where = collections.defaultdict(list)
    for i in range(0, len(ids), BATCH_SEED):
        grp = ids[i:i + BATCH_SEED]
        page = 1
        while True:
            u = ('https://api.openalex.org/works?filter=cites:%s&per-page=200&page=%d&select=id,doi,title,publication_year,cited_by_count,primary_location,open_access,abstract_inverted_index&%s'
                 % ('|'.join(grp), page, MAIL))
            j = get(u)
            if '_err' in j:
                print('   fwd batch %d page %d ERR %s' % (i, page, j['_err']), flush=True); break
            res = j.get('results') or []
            for w in res:
                cnt[w['id'].rsplit('/', 1)[-1]] += 1
            if len(res) < 200: break
            page += 1
            if page > 60: break
        print('  forward batch %d/%d done, unique so far %d' % (i + BATCH_SEED, len(ids), len(cnt)), flush=True)
    return cnt, where

# ---------------- 5. fetch metadata by id ----------------
def fetch_by_ids(ids):
    rows = []
    for i in range(0, len(ids), BATCH_ID):
        grp = ids[i:i + BATCH_ID]
        u = ('https://api.openalex.org/works?filter=openalex_id:%s&per-page=%d&select=%s&%s'
             % ('|'.join(grp), BATCH_ID, SEL, MAIL))
        j = get(u)
        if '_err' in j:
            print('   meta batch %d ERR %s' % (i, j['_err']), flush=True); continue
        for w in (j.get('results') or []):
            rows.append(w)
        if (i // BATCH_ID) % 10 == 0:
            print('   meta %d/%d' % (i, len(ids)), flush=True)
    return rows

def main():
    t0 = time.time()
    corpus = build_corpus()
    print('[CORPUS] %d coded studies (%d with DOI)' % (len(corpus), sum(1 for c in corpus if c['doi'])), flush=True)
    seeds = resolve(corpus)
    bcnt, _ = backward(seeds)
    fcnt, _ = forward(seeds)
    allids = sorted(set(bcnt) | set(fcnt))
    seed_ids = set(s['wid'] for s in seeds)
    allids = [i for i in allids if i not in seed_ids]
    print('[UNION] %d unique neighbour works (%d backward, %d forward)' % (len(allids), len(bcnt), len(fcnt)), flush=True)
    meta = fetch_by_ids(allids)
    print('[META] fetched %d/%d' % (len(meta), len(allids)), flush=True)
    # exclude anything already in the original candidate pool
    pool = set()
    for r in csv.DictReader(open(os.path.join(BASE, 'data', 'raw-search', 'candidates-raw.csv'), encoding='utf-8-sig')):
        if r.get('openalex_id'): pool.add(r['openalex_id'].rsplit('/', 1)[-1])
        if r.get('doi'): pool.add(r['doi'].lower().replace('https://doi.org/', ''))
    rows = []
    for w in meta:
        k = w['id'].rsplit('/', 1)[-1]
        doi = (w.get('doi') or '').lower().replace('https://doi.org/', '')
        in_pool = (k in pool) or (doi and doi in pool)
        rows.append({'openalex_id': k, 'doi': doi, 'title': w.get('title') or '', 'year': w.get('publication_year') or '',
                     'venue': venue_of(w), 'cited_by': w.get('cited_by_count') or 0,
                     'is_oa': 1 if (w.get('is_oa') or (w.get('open_access') or {}).get('is_oa')) else 0,
                     'in_original_pool': 1 if in_pool else 0,
                     'n_backward_links': bcnt.get(k, 0), 'n_forward_links': fcnt.get(k, 0),
                     'abstract': abstract_text(w.get('abstract_inverted_index'))})
    with open(os.path.join(OUT, 'candidates-snowball.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wr.writeheader()
        for r in rows: wr.writerow(r)
    new = [r for r in rows if not r['in_original_pool']]
    print('[POOL] %d already in original pool, %d NEW' % (len(rows) - len(new), len(new)), flush=True)
    with open(os.path.join(OUT, 'candidates-snowball-new.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wr.writeheader()
        for r in new: wr.writerow(r)
    json.dump({'n_seeds_resolved': len(seeds), 'n_backward_unique': len(bcnt), 'n_forward_unique': len(fcnt),
               'n_union': len(allids), 'n_fetched': len(meta), 'n_in_original_pool': len(rows) - len(new),
               'n_new': len(new), 'elapsed_s': round(time.time() - t0, 1)},
              open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
    print('[DONE] %.0fs' % (time.time() - t0), flush=True)

if __name__ == '__main__':
    main()
