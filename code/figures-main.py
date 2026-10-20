# -*- coding: utf-8 -*-
"""
21-出版级绘图.py  --  publication-grade figures for the NIDS review

Reads 03-编码表.csv (93 coded studies after the P123 exclusion) and writes figures/ into:
  fig1_prisma.png            study flow (PRISMA 2020 style)
  fig2_transparency.png      hero: reporting-profile of all coded studies
  fig3_split_protocol.png    train/test splitting protocol distribution
  fig4_dataset.png           dataset usage + persistence of KDD99 family
  fig5_by_split_reporting.png transparency conditional on split reporting

Does NOT modify the coding sheet or any number used in 05-统计脚本.py.
"""
import os
import re
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_IN = os.path.join(BASE, '03-编码表.csv')
FIG_DIR = os.path.join(BASE, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# ---- typography: journal-ready ----
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7,
    'axes.labelsize': 7,
    'axes.titlesize': 7.5,
    'xtick.labelsize': 6.5,
    'ytick.labelsize': 6.5,
    'legend.fontsize': 6.5,
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.major.size': 2.2,
    'ytick.major.size': 2.2,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
    'savefig.dpi': 600,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

# ---- restrained palette: neutral / signal / accent ----
INK    = '#1a1a1a'
GREY_D = '#4d4d4d'
GREY_M = '#8c8c8c'
GREY_L = '#c9c9c9'
GREY_XL= '#ececec'
SIGNAL = '#2f6f9f'   # reported / adequate
ACCENT = '#c0504d'   # not reported / inadequate  (the finding)
WARN   = '#e0a33e'

def mm(x):
    return x / 25.4

def save(fig, name):
    p = os.path.join(FIG_DIR, name)
    fig.savefig(p, dpi=600, facecolor='white')
    plt.close(fig)
    print('[OK] %s  %.0f KB' % (name, os.path.getsize(p) / 1024.0))

def panel(ax, letter, x=-0.13, y=1.10):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=8,
            fontweight='bold', va='top', ha='left', color=INK)

# ============================================================
#  load
# ============================================================
df = pd.read_csv(CSV_IN, encoding='utf-8-sig', dtype=str)
df.columns = [c.strip() for c in df.columns]
df = df[df['paper_id'].astype(str).str.match(r'^P\d+$')].copy()
for c in df.columns:
    df[c] = df[c].astype(str).str.strip()
N = len(df)
print('[INFO] N = %d coded studies' % N)

def pct(k):
    return 100.0 * k / N

# ============================================================
#  Figure 1 -- PRISMA-style study flow
# ============================================================
def fig_prisma():
    fig, ax = plt.subplots(figsize=(mm(160), mm(120)))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')

    MX, MW, MH = 2.0, 50.0, 10.5     # main column: left edge, width, height
    SX, SW = 62.0, 36.0              # side column: left edge, width
    boxes = [
        (79.0, 'Records identified from OpenAlex\nQ1: 2,033    Q2: 413', GREY_XL),
        (64.0, 'Records after duplicate removal\nn = 2,241', GREY_L),
        (49.0, 'Records passing title/abstract screening\nn = 2,029', GREY_L),
        (34.0, 'Random sample for full-text retrieval\nn = 180  (seed 20261018)', GREY_L),
        (19.0, 'Full texts obtained\nn = 91  (50.6%)', GREY_L),
        (4.0,  'Studies coded\nn = 93', SIGNAL),
    ]
    for y, txt, fc in boxes:
        b = FancyBboxPatch((MX, y), MW, MH, boxstyle='round,pad=0.3,rounding_size=1.0',
                           linewidth=0.6, edgecolor=GREY_D,
                           facecolor=fc, alpha=1.0 if fc != SIGNAL else 0.20)
        ax.add_patch(b)
        ax.text(MX + MW / 2, y + MH / 2, txt, ha='center', va='center',
                fontsize=6.0, color=INK, linespacing=1.5)
    for i in range(len(boxes) - 1):
        y0 = boxes[i][0]; y1 = boxes[i + 1][0] + MH
        ax.annotate('', xy=(MX + MW / 2, y1 + 0.4), xytext=(MX + MW / 2, y0 - 0.4),
                    arrowprops=dict(arrowstyle='-|>', linewidth=0.6, color=GREY_D,
                                    shrinkA=0, shrinkB=0))
    # side exclusions, aligned with the stage they belong to
    side = [
        (49.0, 'Excluded at title/abstract  (n = 212)\nno ML method 113\noff-topic 58  |  review 40  |  non-research 1'),
        (19.0, 'Not retrieved  (n = 89)\npublisher access blocked or paywalled'),
        (4.0,  'Excluded after full text  (n = 6)\nreviews 3  |  retracted 2  |  no public dataset 1'),
    ]
    for y, txt in side:
        b = FancyBboxPatch((SX, y), SW, MH, boxstyle='round,pad=0.3,rounding_size=1.0',
                           linewidth=0.5, edgecolor=GREY_M, facecolor=GREY_XL)
        ax.add_patch(b)
        ax.text(SX + SW / 2, y + MH / 2, txt, ha='center', va='center',
                fontsize=5.4, color=GREY_D, linespacing=1.5)
        ax.annotate('', xy=(SX - 0.4, y + MH / 2), xytext=(MX + MW + 0.4, y + MH / 2),
                    arrowprops=dict(arrowstyle='-|>', linewidth=0.5, color=GREY_M,
                                    linestyle=(0, (2, 1.6)), shrinkA=0, shrinkB=0))
    save(fig, 'fig1_prisma.png')

# ============================================================
#  Figure 2 -- hero: reporting profile
# ============================================================
def fig_transparency():
    items = [
        ('Dataset version stated',      'dataset_version',      'yes'),
        ('Data-leakage risk discussed', 'leakage_discussed',    'yes'),
        ('Code publicly available',     'code_public',          'yes'),
        ('Repeated runs / variance',    'runs_reported',        'yes'),
        ('Splitting details reported',  'split_reported',       'yes'),
        ('Ablation study',              'ablation',             'yes'),
        ('Compute cost reported',       'compute_reported',     'yes'),
        ('Hyperparameters reported',    'hyperparams_public',   'yes'),
    ]
    vals = []
    for lab, col, good in items:
        k = int((df[col] == good).sum())
        vals.append((lab, k, pct(k)))
    vals.sort(key=lambda r: r[2])

    fig, ax = plt.subplots(figsize=(mm(89), mm(62)))
    y = np.arange(len(vals))
    v = [r[2] for r in vals]
    colors = [ACCENT if x < 30 else (WARN if x < 60 else SIGNAL) for x in v]
    ax.barh(y, v, height=0.62, color=colors, linewidth=0)
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in vals])
    ax.set_xlim(0, 100)
    ax.set_xlabel('Studies reporting the item (%% of %d)' % N)
    ax.axvline(50, color=GREY_M, linewidth=0.5, linestyle=(0, (2, 2)), zorder=0)
    for yi, (lab, k, p) in zip(y, vals):
        ax.text(p + 1.6, yi, '%d (%.1f%%)' % (k, p), va='center', ha='left',
                fontsize=6, color=INK)
    ax.set_ylim(-0.6, len(vals) - 0.4)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='x', color=GREY_XL, linewidth=0.5)
    ax.set_axisbelow(True)
    save(fig, 'fig2_transparency.png')

# ============================================================
#  Figure 3 -- splitting protocol
# ============================================================
def fig_split():
    order = ['random', 'kfold', 'temporal', 'grouped', 'unspecified']
    nice = {'random': 'Random hold-out', 'kfold': 'k-fold CV',
            'temporal': 'Temporal', 'grouped': 'Grouped',
            'unspecified': 'Not specified'}
    cnt = {k: int((df['split_protocol'] == k).sum()) for k in order}
    order = sorted(order, key=lambda k: cnt[k])

    fig, ax = plt.subplots(figsize=(mm(89), mm(52)))
    y = np.arange(len(order))
    v = [cnt[k] for k in order]
    colors = [ACCENT if k == 'unspecified' else SIGNAL for k in order]
    ax.barh(y, v, height=0.6, color=colors, linewidth=0)
    ax.set_yticks(y)
    ax.set_yticklabels([nice[k] for k in order])
    ax.set_xlabel('Number of studies')
    ax.set_xlim(0, max(v) * 1.22)
    for yi, k in zip(y, order):
        ax.text(cnt[k] + max(v) * 0.012, yi, '%d (%.1f%%)' % (cnt[k], pct(cnt[k])),
                va='center', ha='left', fontsize=6, color=INK)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='x', color=GREY_XL, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.annotate('only %d study each' % min(cnt['temporal'], cnt['grouped']),
                xy=(cnt['temporal'] + max(v) * 0.30, 0.5), fontsize=5.8,
                color=GREY_D, ha='left', va='center')
    save(fig, 'fig3_split_protocol.png')

# ============================================================
#  Figure 4 -- dataset usage and the persistence of KDD99
# ============================================================
def canon_ds(label):
    """Collapse the free-text dataset labels in the coding sheet onto one name."""
    k = re.sub(r'[\s_\-]', '', label).lower()
    if not k:
        return None
    if 'nsl' in k:
        return 'NSL-KDD'
    if 'kdd' in k:
        return 'KDD99'
    if 'unsw' in k:
        return 'UNSW-NB15'
    if 'cic' in k and '2017' in k:
        return 'CICIDS2017'
    if 'cic' in k and '2018' in k:
        return 'CICIDS2018'
    if 'ddos' in k:
        return 'CIC-DDoS2019'
    if 'bot' in k and 'iot' in k:
        return 'Bot-IoT'
    if 'ton' in k:
        return 'ToN-IoT'
    if 'iot23' in k or 'iot-23' in k:
        return 'IoT-23'
    return label.strip()

def study_datasets(row):
    out = set()
    for p in re.split(r'[;,]', row):
        c = canon_ds(p)
        if c:
            out.add(c)
    return out

LEGACY = ('NSL-KDD', 'KDD99')

def fig_dataset():
    CANON = ['NSL-KDD', 'KDD99', 'UNSW-NB15', 'CICIDS2017',
             'Bot-IoT', 'ToN-IoT', 'CICIDS2018', 'IoT-23']
    dsets = df['dataset'].apply(study_datasets)
    counts = [(name, int(dsets.apply(lambda s: name in s).sum())) for name in CANON]
    counts.sort(key=lambda r: r[1])

    fig, axes = plt.subplots(1, 2, figsize=(mm(145), mm(58)),
                             gridspec_kw={'width_ratios': [1.05, 1.0], 'wspace': 0.42})
    ax = axes[0]
    y = np.arange(len(counts))
    v = [c[1] for c in counts]
    legacy = [c[0] in ('NSL-KDD', 'KDD99') for c in counts]
    ax.barh(y, v, height=0.6, color=[ACCENT if l else SIGNAL for l in legacy], linewidth=0)
    ax.set_yticks(y)
    ax.set_yticklabels([c[0] for c in counts])
    ax.set_xlabel('Studies using the dataset')
    ax.set_xlim(0, max(v) * 1.24)
    for yi, (n_, k) in zip(y, counts):
        ax.text(k + max(v) * 0.015, yi, '%d' % k, va='center', ha='left', fontsize=6, color=INK)
    ax.set_ylim(-0.6, len(counts) - 0.4)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='x', color=GREY_XL, linewidth=0.5)
    ax.set_axisbelow(True)
    panel(ax, 'a', x=-0.34, y=1.06)

    # panel b: share of studies still using KDD99-family, by year
    df['_year'] = pd.to_numeric(df['year'], errors='coerce')
    sub = df.dropna(subset=['_year']).copy()
    sub['_year'] = sub['_year'].astype(int)
    sub['_legacy'] = sub['dataset'].apply(lambda r: bool(study_datasets(r) & set(LEGACY)))
    years = sorted(sub['_year'].unique())
    xs, ys, ns = [], [], []
    for yr in years:
        g = sub[sub['_year'] == yr]
        xs.append(yr); ns.append(len(g))
        ys.append(100.0 * g['_legacy'].sum() / len(g))
    ax2 = axes[1]
    ax2.plot(xs, ys, color=ACCENT, linewidth=1.1, marker='o', markersize=3.0,
             markerfacecolor='white', markeredgewidth=0.8, zorder=3)
    for x_, y_, n_ in zip(xs, ys, ns):
        ax2.annotate('n=%d' % n_, xy=(x_, y_), xytext=(0, 6), textcoords='offset points',
                     ha='center', fontsize=5.2, color=GREY_M)
    ax2.set_ylim(0, 108)
    ax2.set_xlabel('Publication year')
    ax2.set_ylabel('Studies using KDD99 or NSL-KDD (%)')
    ax2.set_xticks(xs)
    ax2.grid(axis='y', color=GREY_XL, linewidth=0.5)
    ax2.set_axisbelow(True)
    panel(ax2, 'b', x=-0.22, y=1.06)
    save(fig, 'fig4_dataset.png')

# ============================================================
#  Figure 5 -- transparency conditional on split reporting
# ============================================================
def fig_by_split():
    fields = [('Code public', 'code_public'),
              ('Repeated runs', 'runs_reported'),
              ('Ablation', 'ablation'),
              ('Leakage discussed', 'leakage_discussed')]
    good = df[df['split_reported'] == 'yes']
    bad = df[df['split_reported'] == 'no']
    fig, ax = plt.subplots(figsize=(mm(89), mm(56)))
    x = np.arange(len(fields))
    w = 0.36
    v1 = [100.0 * (good[c] == 'yes').sum() / max(len(good), 1) for _, c in fields]
    v2 = [100.0 * (bad[c] == 'yes').sum() / max(len(bad), 1) for _, c in fields]
    b1 = ax.bar(x - w/2, v1, w, color=SIGNAL, linewidth=0, label='Split protocol reported (n=%d)' % len(good))
    b2 = ax.bar(x + w/2, v2, w, color=GREY_L, linewidth=0, label='Split protocol not reported (n=%d)' % len(bad))
    for bars, vals in ((b1, v1), (b2, v2)):
        for r, val in zip(bars, vals):
            ax.text(r.get_x() + r.get_width()/2, val + 1.8, '%.0f' % val,
                    ha='center', va='bottom', fontsize=5.8, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels([f[0] for f in fields])
    ax.set_ylabel('Studies reporting the item (%)')
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, loc='upper right', handlelength=1.2, borderpad=0.2)
    ax.grid(axis='y', color=GREY_XL, linewidth=0.5)
    ax.set_axisbelow(True)
    save(fig, 'fig5_by_split_reporting.png')

if __name__ == '__main__':
    fig_prisma()
    fig_transparency()
    fig_split()
    fig_dataset()
    fig_by_split()
    print('[DONE] figures written to %s' % FIG_DIR)