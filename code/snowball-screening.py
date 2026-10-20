
# -*- coding: utf-8 -*-
"""34 - Snowball screening: apply the SAME automatic screening rules to the
citation-snowball candidates, to measure how many eligible studies the
OpenAlex keyword search may have missed."""
import os, io, csv, json, importlib.util, collections
BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'data', 'snowball')
OUT = os.path.join(BASE, 'output', 'snowball')
os.makedirs(OUT, exist_ok=True)

spec = importlib.util.spec_from_file_location('s13', os.path.join(BASE, '13-自动初筛.py'))
m13 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m13)
decide = m13.decide

PREPRINT = ('arxiv', 'preprint', 'research square', 'ssrn', 'biorxiv', 'medrxiv', 'techrxiv')

def load(p):
    with io.open(p, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

rows = load(os.path.join(D, 'candidates-snowball-new.csv'))
cnt = collections.Counter()
kept = []
for r in rows:
    try:
        y = int(r.get('year') or 0)
    except Exception:
        y = 0
    if y < 2019 or y > 2025:
        cnt['OUT_OF_WINDOW'] += 1; continue
    ven = (r.get('venue') or '').lower()
    if any(p in ven for p in PREPRINT):
        cnt['PREPRINT_VENUE'] += 1; continue
    cat, why = decide({'title': r.get('title') or '', 'abstract': r.get('abstract') or ''})
    cnt['DECIDE_' + cat] += 1
    if cat in ('include', 'maybe'):
        kept.append(dict(r, screen=cat, reason=why))

print('TOTAL NEW CANDIDATES', len(rows))
for k, v in sorted(cnt.items()):
    print('   %-22s %d' % (k, v))
print('KEPT (include+maybe):', len(kept))
inc = [k for k in kept if k['screen'] == 'include']
print('   include only:', len(inc))
byyear = collections.Counter(k['year'] for k in kept)
print('   by year:', dict(sorted(byyear.items())))
byven = collections.Counter((k['venue'] or '') for k in kept)
print('   top venues:')
for v, c in byven.most_common(12):
    print('      %-52s %d' % (v[:52], c))

with io.open(os.path.join(OUT, 'snowball-screened.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(kept[0].keys()) if kept else ['x'])
    w.writeheader()
    for k in kept: w.writerow(k)

print()
print('--- include-list (screen=include), newest first ---')
for k in sorted(inc, key=lambda x: -int(x['year'])):
    print('%s | %s | %s' % (k['year'], (k['venue'] or '')[:34], (k['title'] or '')[:96]))
print()
print('--- maybe (first 25) ---')
for k in sorted([x for x in kept if x['screen']=='maybe'], key=lambda x: -int(x['year']))[:25]:
    print('%s | %s | %s' % (k['year'], (k['venue'] or '')[:30], (k['title'] or '')[:90]))
print('JSONMETA', json.dumps({'total_new': len(rows), 'kept': len(kept), 'include': len(inc), 'maybe': len(kept)-len(inc), 'counts': dict(cnt)}))
