# Camstar SQL 业务指标目录

本目录是自然语言 SQL 助手的确定性业务语义层。指标合同位于
`src/qa/semantic/metrics.json`，物理表、字段和 JOIN 均以
`Database_Tables.csv`、`Database_Fields.csv` 为唯一事实来源。

## 合同状态

- `approved`：度量字段和事实粒度可由物理 Schema 直接确认。
- `provisional`：表、字段和 JOIN 已确认，但冲销、返工、状态枚举或符号规则
  尚缺现场权威定义；SQL会明确展示当前采用的原始事实口径。

## 第一批指标

| 指标合同 | 中文名 | 事实表 | 度量 | 状态 |
|---|---|---|---|---|
| `container.current_detail` | 容器当前明细 | `Container` | 明细字段 | approved |
| `wip.current_qty` | 当前容器数量合计 | `Container` | `SUM(Qty)` | provisional |
| `throughput.total_qty` | 产出数量 | `ThruputHistory` | `SUM(Qty)` | provisional |
| `throughput.by_mfg_order` | 工单产出数量 | `ResourceThruputHistory` | `SUM(Qty)` | provisional |
| `throughput.by_resource` | 设备产出数量 | `ResourceThruputHistory` | `SUM(Qty)` | provisional |
| `throughput.by_operation` | 工序产出数量 | `ThruputHistory` | `SUM(Qty)` | provisional |
| `track_in.qty` | Track In数量 | `A_TrackInLotHistory` | `SUM(TrackInQty)` | approved |
| `track_out.qty` | Track Out数量 | `A_TrackOutLotHistory` | `SUM(TrackOutQty)` | approved |
| `move.event_count` | 移动事务次数 | `MoveHistory` | `COUNT(MoveHistoryId)` | approved |
| `start.qty` | 开工数量 | `StartHistoryDetail` | `SUM(Qty)` | provisional |
| `quantity_change.recorded_qty` | 数量变更记录量 | `QtyHistoryDetails` | `SUM(Qty)` | provisional |
| `split.qty` | 拆分数量 | `SplitHistoryDetails` | `SUM(Qty)` | provisional |
| `combine.qty` | 合并数量 | `CombineHistoryDetail` | `SUM(Qty)` | provisional |
| `hold.duration` | Hold持续时间 | `HoldReleaseHistoryDetail` | `SUM(HoldDuration)` | approved |
| `resource_status.change_count` | 资源状态变更次数 | `ResourceStatusHistory` | `COUNT(ResourceStatusHistoryId)` | approved |

## 强制规则

1. 历史指标必须先确定时间范围和时间字段。
2. 时间过滤使用参数化半开区间，不对时间字段执行 `TRUNC`、`CAST` 或 `CONVERT`。
3. 指标SQL只使用合同登记的事实表、物理外键和聚合表达式。
4. `provisional` 指标不推测 `ReversalStatus`、返工、状态或数量符号枚举。
5. 命中指标合同后由程序渲染SQL，不调用LLM决定表、JOIN或统计口径。
6. “良率”“一次通过率”和OEE在分子、分母及排除规则确认前不生成确定性SQL。

## 回归基线

Golden数据集位于 `src/tests/fixtures/sql_semantic_benchmark.jsonl`，共50条。
来源包括现有聊天日志中的SQL问法及依据物理Schema补齐的真实业务场景问法。
每条记录保存预期指标、事实表、时间口径、必需JOIN及静态标准SQL。
