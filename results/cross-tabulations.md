# 描述性统计表

N = 93

## 说明数据集版本/获取日期 (dataset_version)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 2 | 2.2% |
| no | 91 | 97.8% |
| **合计** | **93** | 100% |

## 数据集过时(>5年) (dataset_outdated)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 80 | 86.0% |
| no | 13 | 14.0% |
| **合计** | **93** | 100% |

## 划分协议 (split_protocol)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| random | 11 | 11.8% |
| temporal | 1 | 1.1% |
| grouped | 1 | 1.1% |
| kfold | 15 | 16.1% |
| unspecified | 65 | 69.9% |
| **合计** | **93** | 100% |

## 报告划分细节 (split_reported)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 25 | 26.9% |
| no | 68 | 73.1% |
| **合计** | **93** | 100% |

## 公开代码 (code_public)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 2 | 2.2% |
| no | 91 | 97.8% |
| **合计** | **93** | 100% |

## 公开超参数 (hyperparams_public)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 37 | 39.8% |
| partial | 31 | 33.3% |
| no | 25 | 26.9% |
| **合计** | **93** | 100% |

## 报告多次运行 (runs_reported)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 11 | 11.8% |
| no | 82 | 88.2% |
| **合计** | **93** | 100% |

## 消融实验 (ablation)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 17 | 18.3% |
| no | 76 | 81.7% |
| **合计** | **93** | 100% |

## 报告计算成本 (compute_reported)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 51 | 54.8% |
| no | 42 | 45.2% |
| **合计** | **93** | 100% |

## 讨论数据泄漏 (leakage_discussed)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 3 | 3.2% |
| no | 90 | 96.8% |
| **合计** | **93** | 100% |

## 只报 Accuracy (only_accuracy)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 3 | 3.2% |
| no | 90 | 96.8% |
| **合计** | **93** | 100% |

## 同协议比较基线 (same_protocol_compare)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 31 | 33.3% |
| no | 49 | 52.7% |
| unclear | 13 | 14.0% |
| **合计** | **93** | 100% |

## 处理类别不平衡 (imbalance_handled)

| 取值 | 篇数 | 占比 |
| --- | --- | --- |
| yes | 41 | 44.1% |
| no | 36 | 38.7% |
| mentioned | 16 | 17.2% |
| **合计** | **93** | 100% |

# 交叉表与卡方检验

### dataset_version x dataset_outdated

| | no | yes |
| --- | --- | --- |
| **no** | 12 | 79 |
| **yes** | 1 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.206, dof = 1, p = 0.6495 （不显著）

### dataset_version x split_protocol

| | grouped | kfold | random | temporal | unspecified |
| --- | --- | --- | --- | --- | --- |
| **no** | 1 | 15 | 9 | 1 | 65 |
| **yes** | 0 | 0 | 2 | 0 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 15.237, dof = 4, p = 0.0042 （显著）

### dataset_version x split_reported

| | no | yes |
| --- | --- | --- |
| **no** | 68 | 23 |
| **yes** | 0 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 2.408, dof = 1, p = 0.1207 （不显著）

### dataset_version x code_public

| | no | yes |
| --- | --- | --- |
| **no** | 89 | 2 |
| **yes** | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_version x hyperparams_public

| | no | partial | yes |
| --- | --- | --- | --- |
| **no** | 25 | 31 | 35 |
| **yes** | 0 | 0 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 3.094, dof = 2, p = 0.2129 （不显著）

### dataset_version x runs_reported

| | no | yes |
| --- | --- | --- |
| **no** | 80 | 11 |
| **yes** | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_version x ablation

| | no | yes |
| --- | --- | --- |
| **no** | 74 | 17 |
| **yes** | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_version x compute_reported

| | no | yes |
| --- | --- | --- |
| **no** | 41 | 50 |
| **yes** | 1 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_version x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **no** | 88 | 3 |
| **yes** | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_version x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 88 | 3 |
| **yes** | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_version x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 48 | 13 | 30 |
| **yes** | 1 | 0 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.459, dof = 2, p = 0.7950 （不显著）

### dataset_version x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 15 | 36 | 40 |
| **yes** | 1 | 0 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 2.085, dof = 2, p = 0.3525 （不显著）

### dataset_outdated x split_protocol

| | grouped | kfold | random | temporal | unspecified |
| --- | --- | --- | --- | --- | --- |
| **no** | 0 | 5 | 2 | 0 | 6 |
| **yes** | 1 | 10 | 9 | 1 | 59 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 6.378, dof = 4, p = 0.1726 （不显著）

### dataset_outdated x split_reported

| | no | yes |
| --- | --- | --- |
| **no** | 7 | 6 |
| **yes** | 61 | 19 |

卡方检验：chi2 = 1.830, dof = 1, p = 0.1762 （不显著）

### dataset_outdated x code_public

| | no | yes |
| --- | --- | --- |
| **no** | 13 | 0 |
| **yes** | 78 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_outdated x hyperparams_public

| | no | partial | yes |
| --- | --- | --- | --- |
| **no** | 3 | 4 | 6 |
| **yes** | 22 | 27 | 31 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.265, dof = 2, p = 0.8758 （不显著）

### dataset_outdated x runs_reported

| | no | yes |
| --- | --- | --- |
| **no** | 10 | 3 |
| **yes** | 72 | 8 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.794, dof = 1, p = 0.3729 （不显著）

### dataset_outdated x ablation

| | no | yes |
| --- | --- | --- |
| **no** | 10 | 3 |
| **yes** | 66 | 14 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.009, dof = 1, p = 0.9238 （不显著）

### dataset_outdated x compute_reported

| | no | yes |
| --- | --- | --- |
| **no** | 0 | 13 |
| **yes** | 42 | 38 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 10.416, dof = 1, p = 0.0012 （显著）

### dataset_outdated x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **no** | 13 | 0 |
| **yes** | 77 | 3 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_outdated x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 13 | 0 |
| **yes** | 77 | 3 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### dataset_outdated x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 5 | 1 | 7 |
| **yes** | 44 | 12 | 24 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 2.915, dof = 2, p = 0.2328 （不显著）

### dataset_outdated x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 2 | 2 | 9 |
| **yes** | 14 | 34 | 32 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 4.320, dof = 2, p = 0.1153 （不显著）

### split_protocol x split_reported

| | no | yes |
| --- | --- | --- |
| **grouped** | 0 | 1 |
| **kfold** | 1 | 14 |
| **random** | 2 | 9 |
| **temporal** | 1 | 0 |
| **unspecified** | 64 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 74.917, dof = 4, p = 0.0000 （显著）

### split_protocol x code_public

| | no | yes |
| --- | --- | --- |
| **grouped** | 1 | 0 |
| **kfold** | 14 | 1 |
| **random** | 10 | 1 |
| **temporal** | 1 | 0 |
| **unspecified** | 65 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 5.444, dof = 4, p = 0.2447 （不显著）

### split_protocol x hyperparams_public

| | no | partial | yes |
| --- | --- | --- | --- |
| **grouped** | 0 | 1 | 0 |
| **kfold** | 3 | 2 | 10 |
| **random** | 2 | 3 | 6 |
| **temporal** | 0 | 1 | 0 |
| **unspecified** | 20 | 24 | 21 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 11.352, dof = 8, p = 0.1825 （不显著）

### split_protocol x runs_reported

| | no | yes |
| --- | --- | --- |
| **grouped** | 1 | 0 |
| **kfold** | 8 | 7 |
| **random** | 11 | 0 |
| **temporal** | 1 | 0 |
| **unspecified** | 61 | 4 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 21.208, dof = 4, p = 0.0003 （显著）

### split_protocol x ablation

| | no | yes |
| --- | --- | --- |
| **grouped** | 1 | 0 |
| **kfold** | 8 | 7 |
| **random** | 9 | 2 |
| **temporal** | 1 | 0 |
| **unspecified** | 57 | 8 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 10.091, dof = 4, p = 0.0389 （显著）

### split_protocol x compute_reported

| | no | yes |
| --- | --- | --- |
| **grouped** | 1 | 0 |
| **kfold** | 5 | 10 |
| **random** | 7 | 4 |
| **temporal** | 0 | 1 |
| **unspecified** | 29 | 36 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 4.409, dof = 4, p = 0.3535 （不显著）

### split_protocol x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **grouped** | 1 | 0 |
| **kfold** | 14 | 1 |
| **random** | 11 | 0 |
| **temporal** | 1 | 0 |
| **unspecified** | 63 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 1.007, dof = 4, p = 0.9088 （不显著）

### split_protocol x only_accuracy

| | no | yes |
| --- | --- | --- |
| **grouped** | 1 | 0 |
| **kfold** | 15 | 0 |
| **random** | 10 | 1 |
| **temporal** | 1 | 0 |
| **unspecified** | 63 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 1.783, dof = 4, p = 0.7755 （不显著）

### split_protocol x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **grouped** | 0 | 1 | 0 |
| **kfold** | 5 | 2 | 8 |
| **random** | 7 | 2 | 2 |
| **temporal** | 1 | 0 | 0 |
| **unspecified** | 36 | 8 | 21 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 11.310, dof = 8, p = 0.1848 （不显著）

### split_protocol x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **grouped** | 0 | 0 | 1 |
| **kfold** | 4 | 1 | 10 |
| **random** | 4 | 2 | 5 |
| **temporal** | 0 | 0 | 1 |
| **unspecified** | 8 | 33 | 24 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 16.684, dof = 8, p = 0.0336 （显著）

### split_reported x code_public

| | no | yes |
| --- | --- | --- |
| **no** | 67 | 1 |
| **yes** | 24 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### split_reported x hyperparams_public

| | no | partial | yes |
| --- | --- | --- | --- |
| **no** | 20 | 25 | 23 |
| **yes** | 5 | 6 | 14 |

卡方检验：chi2 = 3.755, dof = 2, p = 0.1529 （不显著）

### split_reported x runs_reported

| | no | yes |
| --- | --- | --- |
| **no** | 64 | 4 |
| **yes** | 18 | 7 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 6.585, dof = 1, p = 0.0103 （显著）

### split_reported x ablation

| | no | yes |
| --- | --- | --- |
| **no** | 59 | 9 |
| **yes** | 17 | 8 |

卡方检验：chi2 = 3.144, dof = 1, p = 0.0762 （不显著）

### split_reported x compute_reported

| | no | yes |
| --- | --- | --- |
| **no** | 30 | 38 |
| **yes** | 12 | 13 |

卡方检验：chi2 = 0.010, dof = 1, p = 0.9215 （不显著）

### split_reported x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **no** | 66 | 2 |
| **yes** | 24 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### split_reported x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 66 | 2 |
| **yes** | 24 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### split_reported x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 37 | 9 | 22 |
| **yes** | 12 | 4 | 9 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.316, dof = 2, p = 0.8541 （不显著）

### split_reported x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 8 | 32 | 28 |
| **yes** | 8 | 4 | 13 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 9.392, dof = 2, p = 0.0091 （显著）

### code_public x hyperparams_public

| | no | partial | yes |
| --- | --- | --- | --- |
| **no** | 25 | 30 | 36 |
| **yes** | 0 | 1 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.773, dof = 2, p = 0.6793 （不显著）

### code_public x runs_reported

| | no | yes |
| --- | --- | --- |
| **no** | 80 | 11 |
| **yes** | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### code_public x ablation

| | no | yes |
| --- | --- | --- |
| **no** | 75 | 16 |
| **yes** | 1 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.062, dof = 1, p = 0.8037 （不显著）

### code_public x compute_reported

| | no | yes |
| --- | --- | --- |
| **no** | 41 | 50 |
| **yes** | 1 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### code_public x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **no** | 88 | 3 |
| **yes** | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### code_public x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 88 | 3 |
| **yes** | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### code_public x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 49 | 11 | 31 |
| **yes** | 0 | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 12.578, dof = 2, p = 0.0019 （显著）

### code_public x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 16 | 36 | 39 |
| **yes** | 0 | 0 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 2.592, dof = 2, p = 0.2736 （不显著）

### hyperparams_public x runs_reported

| | no | yes |
| --- | --- | --- |
| **no** | 20 | 5 |
| **partial** | 31 | 0 |
| **yes** | 31 | 6 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 6.443, dof = 2, p = 0.0399 （显著）

### hyperparams_public x ablation

| | no | yes |
| --- | --- | --- |
| **no** | 22 | 3 |
| **partial** | 28 | 3 |
| **yes** | 26 | 11 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 5.443, dof = 2, p = 0.0658 （不显著）

### hyperparams_public x compute_reported

| | no | yes |
| --- | --- | --- |
| **no** | 15 | 10 |
| **partial** | 14 | 17 |
| **yes** | 13 | 24 |

卡方检验：chi2 = 3.725, dof = 2, p = 0.1553 （不显著）

### hyperparams_public x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **no** | 25 | 0 |
| **partial** | 30 | 1 |
| **yes** | 35 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 1.396, dof = 2, p = 0.4975 （不显著）

### hyperparams_public x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 23 | 2 |
| **partial** | 30 | 1 |
| **yes** | 37 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 3.059, dof = 2, p = 0.2167 （不显著）

### hyperparams_public x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 16 | 3 | 6 |
| **partial** | 20 | 5 | 6 |
| **yes** | 13 | 5 | 19 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 9.846, dof = 4, p = 0.0431 （显著）

### hyperparams_public x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 5 | 14 | 6 |
| **partial** | 3 | 15 | 13 |
| **yes** | 8 | 7 | 22 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 12.282, dof = 4, p = 0.0154 （显著）

### runs_reported x ablation

| | no | yes |
| --- | --- | --- |
| **no** | 72 | 10 |
| **yes** | 4 | 7 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 13.910, dof = 1, p = 0.0002 （显著）

### runs_reported x compute_reported

| | no | yes |
| --- | --- | --- |
| **no** | 39 | 43 |
| **yes** | 3 | 8 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.897, dof = 1, p = 0.3436 （不显著）

### runs_reported x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **no** | 80 | 2 |
| **yes** | 10 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.070, dof = 1, p = 0.7919 （不显著）

### runs_reported x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 79 | 3 |
| **yes** | 11 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### runs_reported x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 46 | 11 | 25 |
| **yes** | 3 | 2 | 6 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 3.371, dof = 2, p = 0.1853 （不显著）

### runs_reported x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 12 | 35 | 35 |
| **yes** | 4 | 1 | 6 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 5.799, dof = 2, p = 0.0551 （不显著）

### ablation x compute_reported

| | no | yes |
| --- | --- | --- |
| **no** | 38 | 38 |
| **yes** | 4 | 13 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 2.934, dof = 1, p = 0.0867 （不显著）

### ablation x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **no** | 74 | 2 |
| **yes** | 16 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### ablation x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 73 | 3 |
| **yes** | 17 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.005, dof = 1, p = 0.9414 （不显著）

### ablation x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 46 | 9 | 21 |
| **yes** | 3 | 4 | 10 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 10.260, dof = 2, p = 0.0059 （显著）

### ablation x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 13 | 35 | 28 |
| **yes** | 3 | 1 | 13 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 10.742, dof = 2, p = 0.0046 （显著）

### compute_reported x leakage_discussed

| | no | yes |
| --- | --- | --- |
| **no** | 41 | 1 |
| **yes** | 49 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### compute_reported x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 40 | 2 |
| **yes** | 50 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.029, dof = 1, p = 0.8641 （不显著）

### compute_reported x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 28 | 3 | 11 |
| **yes** | 21 | 10 | 20 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 6.573, dof = 2, p = 0.0374 （显著）

### compute_reported x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 8 | 19 | 15 |
| **yes** | 8 | 17 | 26 |

卡方检验：chi2 = 2.212, dof = 2, p = 0.3309 （不显著）

### leakage_discussed x only_accuracy

| | no | yes |
| --- | --- | --- |
| **no** | 87 | 3 |
| **yes** | 3 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 0.000, dof = 1, p = 1.0000 （不显著）

### leakage_discussed x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 48 | 13 | 29 |
| **yes** | 1 | 0 | 2 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 1.687, dof = 2, p = 0.4302 （不显著）

### leakage_discussed x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 16 | 34 | 40 |
| **yes** | 0 | 2 | 1 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 1.241, dof = 2, p = 0.5378 （不显著）

### only_accuracy x same_protocol_compare

| | no | unclear | yes |
| --- | --- | --- | --- |
| **no** | 47 | 12 | 31 |
| **yes** | 2 | 1 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 1.979, dof = 2, p = 0.3717 （不显著）

### only_accuracy x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 15 | 34 | 41 |
| **yes** | 1 | 2 | 0 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 2.461, dof = 2, p = 0.2921 （不显著）

### same_protocol_compare x imbalance_handled

| | mentioned | no | yes |
| --- | --- | --- | --- |
| **no** | 8 | 26 | 15 |
| **unclear** | 4 | 3 | 6 |
| **yes** | 4 | 7 | 20 |

> 注意：存在频数 < 5 的单元格，卡方结果需谨慎（应改用 Fisher 精确检验）。

卡方检验：chi2 = 12.222, dof = 4, p = 0.0158 （显著）

# 编码一致性（Cohen kappa）

用法：准备两个 CSV，coder_A.csv 和 coder_B.csv，都只含被复核的那 20 篇，
列名与 03-编码表.csv 相同。脚本会自动找这两个文件并逐字段算 kappa。

（未找到 coder_A.csv / coder_B.csv，跳过。）
