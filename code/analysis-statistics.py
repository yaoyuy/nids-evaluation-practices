# -*- coding: utf-8 -*-
"""
05-统计脚本.py  —  nids-review 项目统计与出图

用法（在 D:\dswork\nids-review 目录下）：
    python 05-统计脚本.py

它会读取 03-编码表.csv，生成：
    output/tables.md     所有表格（Markdown，可直接贴进论文）
    figures/fig_*.png    所有图（300 dpi）
    output/check.txt     数据质量检查报告（先看这个！）

依赖：pandas numpy matplotlib scipy（本机已装，无需 pip install）
"""

import os
import sys
import itertools
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# ---------- 路径 ----------
BASE = os.path.dirname(os.path.abspath(__file__))
CSV_IN = os.path.join(BASE, '03-编码表.csv')
OUT_DIR = os.path.join(BASE, 'output')
FIG_DIR = os.path.join(BASE, 'figures')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

# ---------- 中文字体（Windows 自带，防止方块） ----------
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 120
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# ---------- 字段取值域（改这里能改图例顺序） ----------
FIELDS = {
    'dataset_version':       (['yes', 'no'], '说明数据集版本/获取日期'),
    'dataset_outdated':      (['yes', 'no'], '数据集过时(>5年)'),
    'split_protocol':        (['random', 'temporal', 'grouped', 'kfold', 'unspecified'], '划分协议'),
    'split_reported':        (['yes', 'no'], '报告划分细节'),
    'code_public':           (['yes', 'no'], '公开代码'),
    'hyperparams_public':    (['yes', 'partial', 'no'], '公开超参数'),
    'runs_reported':         (['yes', 'no'], '报告多次运行'),
    'ablation':              (['yes', 'no'], '消融实验'),
    'compute_reported':      (['yes', 'no'], '报告计算成本'),
    'leakage_discussed':     (['yes', 'no'], '讨论数据泄漏'),
    'only_accuracy':         (['yes', 'no'], '只报 Accuracy'),
    'same_protocol_compare': (['yes', 'no', 'unclear'], '同协议比较基线'),
    'imbalance_handled':     (['yes', 'no', 'mentioned'], '处理类别不平衡'),
}

TRANSPARENCY_FIELDS = ['code_public', 'hyperparams_public', 'runs_reported',
                       'ablation', 'compute_reported', 'leakage_discussed']


# ============================================================
#  读数据 + 清洗
# ============================================================
def load():
    if not os.path.exists(CSV_IN):
        sys.exit('[ERROR] Coding sheet not found in this folder. Expected 03-编码表.csv next to this script.')
    df = pd.read_csv(CSV_IN, encoding='utf-8-sig', dtype=str)
    df.columns = [c.strip() for c in df.columns]
    if 'paper_id' in df.columns:
        df = df[df['paper_id'].astype(str).str.match(r'^P\d+$', na=False)]
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.lower()
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
    fix = {'y': 'yes', 'n': 'no', 'true': 'yes', 'false': 'no', 'nan': '',
           'random split': 'random', 'stratified random': 'random',
           'cross-validation': 'kfold', 'cv': 'kfold', '5-fold': 'kfold',
           '10-fold': 'kfold', 'time-based': 'temporal', 'chronological': 'temporal',
           'group': 'grouped', 'by-attack': 'grouped', 'by-source': 'grouped'}
    for c in df.columns:
        df[c] = df[c].replace(fix)
    return df


def check_quality(df, lines):
    lines.append('# 数据质量检查报告')
    lines.append('')
    lines.append('样本量 N = **' + str(len(df)) + '** 篇')
    if len(df) < 60:
        lines.append('')
        lines.append('> WARNING: N < 60，说服力不足。目标 80-150。')
    lines.append('')
    lines.append('## 缺失值统计')
    lines.append('')
    lines.append('| 字段 | 空值数 | 空值率 |')
    lines.append('| --- | --- | --- |')
    for c in df.columns:
        n_empty = int((df[c].astype(str).str.strip() == '').sum())
        if n_empty > 0:
            lines.append('| ' + c + ' | ' + str(n_empty) + ' | ' + format(100.0 * n_empty / len(df), '.1f') + '% |')
    lines.append('')
    lines.append('## 非法取值（不在预定义域内）')
    lines.append('')
    bad = False
    for c in FIELDS:
        domain = FIELDS[c][0]
        if c not in df.columns:
            lines.append('- [缺失列] ' + c + ' 整列不存在')
            bad = True
            continue
        vals = df[c].astype(str).str.strip()
        vals = vals[(vals != '') & (vals != 'nan')]
        illegal = sorted(set(vals) - set(domain))
        if illegal:
            lines.append('- ' + c + ' 出现非法值：' + str(illegal) + '（合法值：' + str(domain) + '）')
            bad = True
    if not bad:
        lines.append('全部字段取值合法。')
    lines.append('')
    lines.append('## 年份分布')
    lines.append('')
    if 'year' in df.columns and df['year'].notna().any():
        yc = df['year'].value_counts().sort_index()
        lines.append('| 年份 | 篇数 |')
        lines.append('| --- | --- |')
        for y in yc.index:
            lines.append('| ' + str(int(y)) + ' | ' + str(int(yc[y])) + ' |')
    else:
        lines.append('year 列全为空。')
    lines.append('')
    return lines



# ============================================================
#  描述性统计
# ============================================================
def freq_table(df, col, domain):
    s = df[col].astype(str).str.strip() if col in df.columns else pd.Series([], dtype=str)
    s = s[(s != '') & (s != 'nan')]
    counts = s.value_counts()
    total = len(s)
    rows = []
    for v in domain:
        n = int(counts.get(v, 0))
        rows.append((v, n, 100.0 * n / total if total else 0.0))
    for v in counts.index:
        if v not in domain:
            n = int(counts[v])
            rows.append((v, n, 100.0 * n / total if total else 0.0))
    return rows, total


def make_table(df, lines):
    lines.append('# 描述性统计表')
    lines.append('')
    lines.append('N = ' + str(len(df)))
    lines.append('')
    for col in FIELDS:
        if col not in df.columns:
            continue
        domain, label = FIELDS[col]
        rows, total = freq_table(df, col, domain)
        if total == 0:
            continue
        lines.append('## ' + label + ' (' + col + ')')
        lines.append('')
        lines.append('| 取值 | 篇数 | 占比 |')
        lines.append('| --- | --- | --- |')
        for v, n, pc in rows:
            lines.append('| ' + v + ' | ' + str(n) + ' | ' + format(pc, '.1f') + '% |')
        lines.append('| **合计** | **' + str(total) + '** | 100% |')
        lines.append('')
    return lines


# ============================================================
#  交叉表 + 卡方
# ============================================================
def crosstab_test(df, row_col, col_col, lines, min_n=5):
    if row_col not in df.columns or col_col not in df.columns:
        return
    d = df[[row_col, col_col]].copy()
    d[row_col] = d[row_col].astype(str).str.strip()
    d[col_col] = d[col_col].astype(str).str.strip()
    d = d[(d[row_col] != '') & (d[row_col] != 'nan') &
          (d[col_col] != '') & (d[col_col] != 'nan')]
    if len(d) < 10:
        return
    ct = pd.crosstab(d[row_col], d[col_col])
    if ct.shape[0] < 2 or ct.shape[1] < 2:
        return
    lines.append('### ' + row_col + ' x ' + col_col)
    lines.append('')
    lines.append('| | ' + ' | '.join(str(c) for c in ct.columns) + ' |')
    lines.append('| --- | ' + ' | '.join(['---'] * ct.shape[1]) + ' |')
    for idx in ct.index:
        row = ct.loc[idx]
        lines.append('| **' + str(idx) + '** | ' + ' | '.join(str(v) for v in row.values) + ' |')
    lines.append('')
    if ct.values.min() < min_n:
        lines.append('> 注意：存在频数 < ' + str(min_n) + ' 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。')
        lines.append('')
    try:
        chi2, p, dof, expected = chi2_contingency(ct)
        sig = '（显著）' if p < 0.05 else '（不显著）'
        lines.append('卡方检验：chi2 = ' + format(chi2, '.3f') + ', dof = ' + str(dof) +
                     ', p = ' + format(p, '.4f') + ' ' + sig)
    except Exception as e:
        lines.append('卡方检验失败：' + str(e))
    lines.append('')


# ============================================================
#  Cohen's kappa（一致性检验）
# ============================================================
def cohen_kappa(a, b):
    """a, b 是两个编码者/两次编码的标签列表，长度相同。返回 kappa。"""
    a = [str(x).strip().lower() for x in a]
    b = [str(x).strip().lower() for x in b]
    if len(a) != len(b) or len(a) == 0:
        raise ValueError('两个列表长度必须相同且非空')
    n = len(a)
    labels = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / float(n)
    pe = 0.0
    for lab in labels:
        pa = sum(1 for x in a if x == lab) / float(n)
        pb = sum(1 for x in b if x == lab) / float(n)
        pe += pa * pb
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)


def kappa_report(lines):
    lines.append('# 编码一致性（Cohen kappa）')
    lines.append('')
    lines.append('用法：准备两个 CSV，coder_A.csv 和 coder_B.csv，都只含被复核的那 20 篇，')
    lines.append('列名与 03-编码表.csv 相同。脚本会自动找这两个文件并逐字段算 kappa。')
    lines.append('')
    fa = os.path.join(BASE, 'coder_A.csv')
    fb = os.path.join(BASE, 'coder_B.csv')
    if not (os.path.exists(fa) and os.path.exists(fb)):
        lines.append('（未找到 coder_A.csv / coder_B.csv，跳过。）')
        lines.append('')
        return lines
    A = pd.read_csv(fa, encoding='utf-8-sig', dtype=str)
    B = pd.read_csv(fb, encoding='utf-8-sig', dtype=str)
    if 'paper_id' not in A.columns or 'paper_id' not in B.columns:
        lines.append('两个文件都必须有 paper_id 列。')
        return lines
    M = A.merge(B, on='paper_id', suffixes=('_A', '_B'))
    lines.append('复核篇数：' + str(len(M)))
    lines.append('')
    lines.append('| 字段 | kappa | 一致性等级 |')
    lines.append('| --- | --- | --- |')
    for col in FIELDS:
        ca, cb = col + '_A', col + '_B'
        if ca not in M.columns or cb not in M.columns:
            continue
        try:
            k = cohen_kappa(M[ca].tolist(), M[cb].tolist())
        except Exception:
            continue
        if k >= 0.81:
            lvl = 'almost perfect'
        elif k >= 0.61:
            lvl = 'substantial'
        elif k >= 0.41:
            lvl = 'moderate'
        elif k >= 0.21:
            lvl = 'fair'
        else:
            lvl = 'slight/poor'
        lines.append('| ' + col + ' | ' + format(k, '.3f') + ' | ' + lvl + ' |')
    lines.append('')
    return lines



# ============================================================
#  出图
# ============================================================
def savefig(fig, name):
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path)
    plt.close(fig)
    return path


def plot_split_protocol(df):
    if 'split_protocol' not in df.columns:
        return None
    s = df['split_protocol'].astype(str).str.strip()
    s = s[(s != '') & (s != 'nan')]
    if s.empty:
        return None
    order = ['random', 'temporal', 'grouped', 'kfold', 'unspecified']
    counts = s.value_counts()
    labels = [v for v in order if v in counts.index]
    labels += [v for v in counts.index if v not in order]
    vals = [int(counts[v]) for v in labels]
    pct = [100.0 * v / len(s) for v in vals]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(labels, vals, color='#4C72B0')
    for b, v, pc in zip(bars, vals, pct):
        ax.text(b.get_x() + b.get_width() / 2.0, b.get_height() + 0.5,
                str(v) + '\n(' + format(pc, '.1f') + '%)',
                ha='center', va='bottom', fontsize=9)
    ax.set_ylabel('Number of studies')
    ax.set_title('Train/test splitting protocol (N=' + str(len(s)) + ')')
    ax.set_ylim(0, max(vals) * 1.25 if vals else 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return savefig(fig, 'fig_split_protocol.png')


def plot_transparency(df):
    labels, vals, pcts = [], [], []
    for c in TRANSPARENCY_FIELDS:
        if c not in df.columns:
            continue
        s = df[c].astype(str).str.strip()
        s = s[(s != '') & (s != 'nan')]
        if s.empty:
            continue
        n_yes = int((s == 'yes').sum())
        labels.append(c)
        vals.append(n_yes)
        pcts.append(100.0 * n_yes / len(s))
    if not labels:
        return None
    # 反转，让第一个字段显示在最上面
    labels = labels[::-1]
    vals = vals[::-1]
    pcts = pcts[::-1]
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(labels, pcts, color='#DD8452')
    for b, pc, v in zip(bars, pcts, vals):
        ax.text(pc + 1, b.get_y() + b.get_height() / 2.0,
                format(pc, '.1f') + '% (n=' + str(v) + ')', va='center', fontsize=9)
    ax.set_xlabel('Percentage of studies reporting YES (%)')
    ax.set_xlim(0, 115)
    ax.set_title('Reporting transparency indicators (N=' + str(len(df)) + ')')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return savefig(fig, 'fig_transparency.png')


def plot_dataset_trend(df):
    if 'dataset' not in df.columns or 'year' not in df.columns:
        return None
    d = df[['dataset', 'year']].copy()
    d = d[d['year'].notna()]
    if d.empty:
        return None
    recs = []
    for i in range(len(d)):
        yr = int(d.iloc[i]['year'])
        for x in str(d.iloc[i]['dataset']).split(';'):
            x = x.strip()
            if x and x != 'nan':
                recs.append((yr, x))
    if not recs:
        return None
    E = pd.DataFrame(recs, columns=['year', 'dataset'])
    top = E['dataset'].value_counts().head(6).index.tolist()
    E = E[E['dataset'].isin(top)]
    ct = pd.crosstab(E['year'], E['dataset'])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ct.plot(kind='bar', stacked=True, ax=ax, colormap='tab10')
    ax.set_xlabel('Publication year')
    ax.set_ylabel('Number of usages')
    ax.set_title('Dataset usage over time (top ' + str(len(top)) + ' datasets)')
    ax.legend(title='Dataset', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=0)
    return savefig(fig, 'fig_dataset_trend.png')


def plot_only_accuracy_trend(df):
    if 'only_accuracy' not in df.columns or 'year' not in df.columns:
        return None
    d = df[['only_accuracy', 'year']].copy()
    d['only_accuracy'] = d['only_accuracy'].astype(str).str.strip()
    d = d[d['only_accuracy'].isin(['yes', 'no'])]
    d = d[d['year'].notna()]
    if len(d) < 10:
        return None
    ct = pd.crosstab(d['year'].astype(int), d['only_accuracy'])
    if 'yes' not in ct.columns:
        return None
    pct = ct['yes'] / ct.sum(axis=1) * 100.0
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(pct.index, pct.values, marker='o', color='#C44E52', linewidth=2)
    for x, y in zip(pct.index, pct.values):
        ax.annotate(format(y, '.0f') + '%', (x, y), textcoords='offset points',
                    xytext=(0, 8), ha='center', fontsize=8)
    ax.set_xlabel('Publication year')
    ax.set_ylabel('% of studies reporting accuracy ONLY')
    ax.set_ylim(0, max(100.0, float(pct.max()) * 1.25))
    ax.set_title('Prevalence of accuracy-only reporting over time')
    ax.grid(alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return savefig(fig, 'fig_only_accuracy_trend.png')


def plot_dataset_outdated(df):
    if 'dataset_outdated' not in df.columns:
        return None
    s = df['dataset_outdated'].astype(str).str.strip()
    s = s[s.isin(['yes', 'no'])]
    if s.empty:
        return None
    n_yes = int((s == 'yes').sum())
    n_no = int((s == 'no').sum())
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.pie([n_yes, n_no],
           labels=['Uses outdated (>5y) dataset', 'Recent datasets only'],
           autopct='%1.1f%%', colors=['#C44E52', '#55A868'], startangle=90,
           wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
    ax.set_title('Dataset recency (N=' + str(len(s)) + ')')
    return savefig(fig, 'fig_dataset_outdated.png')


def plot_split_reporting_trend(df):
    if 'split_reported' not in df.columns or 'year' not in df.columns:
        return None
    d = df.copy()
    d['year'] = pd.to_numeric(d['year'], errors='coerce')
    d = d[d['year'].notna()]
    d['split_reported'] = d['split_reported'].astype(str).str.strip()
    d = d[d['split_reported'].isin(['yes', 'no'])]
    if d.empty:
        return None
    years = sorted(d['year'].astype(int).unique())
    pct = []
    ns = []
    for y in years:
        sub = d[d['year'] == y]
        ns.append(len(sub))
        pct.append(100.0 * (sub['split_reported'] == 'yes').sum() / len(sub))
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(years, pct, marker='o', color='#C44E52', linewidth=2)
    for x, y, n in zip(years, pct, ns):
        ax.annotate(format(y, '.0f') + '%', (x, y), textcoords='offset points',
                    xytext=(0, 9), ha='center', fontsize=8)
        ax.annotate('n=' + str(n), (x, 3), ha='center', fontsize=7, color='#777777')
    ax.set_xlabel('Publication year')
    ax.set_ylabel('% of studies reporting split details')
    ax.set_ylim(0, 100)
    ax.set_title('Reporting of train/test split details over time (N=' + str(len(d)) + ')')
    ax.grid(alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return savefig(fig, 'fig_split_reporting_trend.png')


def plot_transparency_by_protocol(df):
    need = ['split_protocol', 'code_public', 'runs_reported', 'ablation', 'leakage_discussed']
    for c in need:
        if c not in df.columns:
            return None
    d = df.copy()
    for c in need:
        d[c] = d[c].astype(str).str.strip()
    d['known'] = d['split_protocol'].isin(['random', 'temporal', 'grouped', 'kfold'])
    groups = [('Protocol stated', d[d['known']]), ('Protocol not stated', d[~d['known']])]
    metrics = ['code_public', 'runs_reported', 'ablation', 'leakage_discussed']
    labels = ['Code public', 'Repeated runs', 'Ablation', 'Leakage discussed']
    if any(len(g) == 0 for _, g in groups):
        return None
    x = np.arange(len(metrics))
    w = 0.38
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for i, (name, g) in enumerate(groups):
        vals = [100.0 * (g[m] == 'yes').sum() / len(g) for m in metrics]
        pos = x + (i - 0.5) * w
        bars = ax.bar(pos, vals, w, label=name + ' (n=' + str(len(g)) + ')',
                      color=['#4C72B0', '#DD8452'][i])
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2.0, b.get_height() + 1.0,
                    format(v, '.0f') + '%', ha='center', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('% of studies reporting YES')
    ax.set_ylim(0, 100)
    ax.set_title('Transparency by whether the splitting protocol is stated')
    ax.legend(frameon=False)
    ax.grid(alpha=0.3, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return savefig(fig, 'fig_transparency_by_protocol.png')


# ============================================================
#  main
# ============================================================
def main():
    df = load()
    if len(df) == 0:
        print('')
        print('[INFO] No real data yet.')
        print('       The coding sheet only contains the EXAMPLE row, which is skipped.')
        print('       Replace it with your first real paper (paper_id = P001) and run again.')
        print('')
        sys.exit(0)

    lines = check_quality(df, [])
    with open(os.path.join(OUT_DIR, 'check.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('[1/4] Data quality check -> output/check.txt')

    tbl = make_table(df, [])
    tbl.append('# 交叉表与卡方检验')
    tbl.append('')
    keys = list(FIELDS.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            crosstab_test(df, keys[i], keys[j], tbl)
    tbl = kappa_report(tbl)
    with open(os.path.join(OUT_DIR, 'tables.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(tbl))
    print('[2/4] Statistical tables -> output/tables.md')

    figs = []
    for fn in [plot_split_protocol, plot_transparency, plot_dataset_trend,
               plot_only_accuracy_trend, plot_dataset_outdated,
               plot_split_reporting_trend, plot_transparency_by_protocol]:
        try:
            path = fn(df)
            if path:
                figs.append(path)
        except Exception as e:
            print('  [skipped] ' + fn.__name__ + ': ' + str(e))
    print('[3/4] Figures -> figures/  (' + str(len(figs)) + ' files)')

    print('')
    print('=' * 60)
    print('SUMMARY  (N = ' + str(len(df)) + ')')
    print('=' * 60)
    for c in FIELDS:
        if c not in df.columns:
            continue
        domain, label = FIELDS[c]
        rows, total = freq_table(df, c, domain)
        if total == 0:
            continue
        top = max(rows, key=lambda r: r[1])
        print('  ' + c.ljust(24) + ' top value: ' + str(top[0]).ljust(12) +
              ' ' + str(top[1]) + ' (' + format(top[2], '.1f') + '%)')
    print('')
    print('[4/4] Done. Open output/check.txt first to check for illegal values.')


if __name__ == '__main__':
    main()
