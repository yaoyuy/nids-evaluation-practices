
# -*- coding: utf-8 -*-
"""22 - Publication-quality figure for the verification experiment (Fig. 6)."""
import os, io, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
FIGD = os.path.join(BASE, 'figures')
RES = os.path.join(BASE, 'output', 'exp', 'results.json')
os.makedirs(FIGD, exist_ok=True)

INK = '#1a1a1a'; GREY_D = '#4d4d4d'; GREY_M = '#8c8c8c'; GREY_L = '#c9c9c9'; GREY_XL = '#ececec'
SIGNAL = '#2f6f9f'; ACCENT = '#c0504d'; WARN = '#e0a33e'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7, 'axes.labelsize': 7, 'axes.titlesize': 7.5,
    'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5, 'legend.fontsize': 6.5,
    'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
    'xtick.major.size': 2.2, 'ytick.major.size': 2.2,
    'axes.edgecolor': INK, 'text.color': INK, 'axes.labelcolor': INK,
    'xtick.color': INK, 'ytick.color': INK,
    'savefig.dpi': 600, 'figure.dpi': 150, 'pdf.fonttype': 42, 'ps.fonttype': 42,
})

def mm(x): return x / 25.4

def save(fig, name):
    p = os.path.join(FIGD, name)
    fig.savefig(p, dpi=600, facecolor='white')
    plt.close(fig)
    print('[SAVE] %s (%d bytes)' % (name, os.path.getsize(p)))

def panel(ax, letter):
    ax.text(-0.17, 1.03, letter, transform=ax.transAxes, fontsize=8,
            fontweight='bold', va='bottom', ha='left', color=INK)

def clean(ax, grid=True):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    if grid:
        ax.yaxis.grid(True, color=GREY_XL, linewidth=0.5, zorder=0)
        ax.set_axisbelow(True)

def agg(R, ds, proto, task, model, key):
    v = [r[key] for r in R[ds] if r['protocol'] == proto and r['task'] == task and r['model'] == model]
    if not v: return None
    return float(np.mean(v)), float(np.min(v)), float(np.max(v)), len(v)

d = json.load(io.open(RES, encoding='utf-8'))
R = d['results']; M = d['meta']

fig = plt.figure(figsize=(mm(145), mm(58)))
gs = fig.add_gridspec(1, 3, width_ratios=[1.20, 0.88, 0.96], wspace=0.48,
                      left=0.070, right=0.995, top=0.885, bottom=0.215)

PROTO_LBL = {'official': 'Official\nsplit', 'random80': 'Random\n80/20',
             'stratified5cv': 'Stratified\n5-fold', 'strict-group': 'Strict\n(grouped)'}
RF_C = SIGNAL; DNN_C = '#9dbfd6'

def bars(ax, ds, protos, title, ylim):
    x = np.arange(len(protos)); w = 0.34
    for j, (model, col, hatch, lbl) in enumerate([('rf', RF_C, '', 'Random forest'),
                                                  ('dnn', DNN_C, '///', 'Neural network')]):
        means = []; lo = []; hi = []; reps = []
        for pr in protos:
            a = agg(R, ds, pr, 'binary', model, 'macro_f1')
            means.append(a[0]); lo.append(a[1]); hi.append(a[2]); reps.append(a[3])
        err = [[me - l for me, l in zip(means, lo)], [h - me for me, h in zip(means, hi)]]
        ax.bar(x + (j - 0.5) * w, means, w, color=col, edgecolor=INK, linewidth=0.5, hatch=hatch,
               label=lbl, zorder=3, error_kw=dict(elinewidth=0.6, capsize=1.4, ecolor=INK))
        # exact values are given in Table 4; no in-figure value labels (they collide at this width)
        _ = reps
    ax.set_xticks(x); ax.set_xticklabels([PROTO_LBL[p] for p in protos])
    ax.tick_params(axis='x', labelsize=6.0)
    ax.set_ylim(*ylim); ax.set_title(title, pad=4); clean(ax)

ax1 = fig.add_subplot(gs[0, 0])
bars(ax1, 'NSL-KDD', ['official', 'random80', 'stratified5cv', 'strict-group'],
     'NSL-KDD, binary', (0.70, 1.075))
ax1.set_ylabel('Macro-F1')
ax1.axhline(0.7694, color=GREY_M, linewidth=0.6, linestyle=':', zorder=1)
ax1.legend(frameon=False, loc='upper left', handlelength=1.1, borderpad=0.15,
           handletextpad=0.5, labelspacing=0.25)
ax1.annotate('', xy=(0.86, 0.885), xytext=(0.12, 0.885),
             arrowprops=dict(arrowstyle='-|>', color=ACCENT, linewidth=0.8))
ax1.text(0.49, 0.897, '+0.227', ha='center', va='bottom', fontsize=6, color=ACCENT)
panel(ax1, 'a')

ax2 = fig.add_subplot(gs[0, 1])
bars(ax2, 'UNSW-NB15', ['random80', 'stratified5cv', 'strict-group'],
     'UNSW-NB15, binary', (0.88, 0.985))
ax2.axhline(0.9533, color=GREY_M, linewidth=0.6, linestyle=':', zorder=1)
ax2.text(2.46, 0.9555, 'random 80/20 level', ha='right', va='bottom', fontsize=5.4, color=GREY_D)
panel(ax2, 'b')

ax3 = fig.add_subplot(gs[0, 2])
labels = M['NSL-KDD']['multiclass_labels']
CLS = [l for l in labels if l != 'other']
def recall(proto, model, li):
    vals = []
    for r in R['NSL-KDD']:
        if r['protocol'] == proto and r['task'] == 'multiclass' and r['model'] == model:
            pcr = r['per_class_recall']
            if str(li) in pcr: vals.append(pcr[str(li)])
    return float(np.mean(vals)) if vals else None
for i, c in enumerate(CLS):
    li = labels.index(c)
    for model, mk, col, dx in [('rf', 'o', RF_C, -0.13), ('dnn', '^', DNN_C, 0.13)]:
        a = recall('official', model, li); b = recall('random80', model, li)
        if a is None or b is None: continue
        ax3.plot([i + dx, i + dx], [a, b], color=GREY_L, linewidth=0.6, zorder=2)
        ax3.plot([i + dx], [a], marker=mk, markersize=3.4, markerfacecolor='white',
                 markeredgecolor=INK, markeredgewidth=0.6, zorder=4)
        ax3.plot([i + dx], [b], marker=mk, markersize=3.4, color=col,
                 markeredgecolor=INK, markeredgewidth=0.5, zorder=4)
ax3.set_xticks(np.arange(len(CLS)))
ax3.set_xticklabels([c.capitalize() for c in CLS])
ax3.set_ylim(-0.05, 1.42)
ax3.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax3.set_ylabel('Recall')
ax3.set_title('NSL-KDD, per-class recall', pad=4)
clean(ax3)
ax3.plot([], [], marker='o', markersize=3.2, markerfacecolor='white', markeredgecolor=INK,
         linestyle='None', label='Official split')
ax3.plot([], [], marker='o', markersize=3.2, color=SIGNAL, markeredgecolor=INK,
         linestyle='None', label='Random 80/20, RF')
ax3.plot([], [], marker='^', markersize=3.2, color=DNN_C, markeredgecolor=INK,
         linestyle='None', label='Random 80/20, NN')
ax3.legend(frameon=False, loc='upper left', ncol=1, handlelength=0.9,
           borderpad=0.2, labelspacing=0.28, handletextpad=0.4)
panel(ax3, 'c')

save(fig, 'fig6_verification.png')
print('[INFO] done')
