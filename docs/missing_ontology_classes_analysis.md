# Opcenter 本体与物理数据库 CDO 覆盖度分析报告

> **数据源**: `Database_Tables.csv` vs `wiki_kb/*.json`
> **整体统计**:
> - **物理数据库总 CDO 表数**: 1149 个
> - **已建模本体类数**: 363 个
> - **未直接建模 CDO 数**: 858 个
> - **本体覆盖度 (Coverage)**: 31.59%

---

## 📌 为什么有 800+ 个 CDO 表未在本体中建模？

未被建模的 CDO 绝大多数**不属于业务知识图谱建模的核心范围**。在一个高质量的制造本体模型（Ontology）中，我们关注的是**业务对象、核心配置及它们之间的业务关联**，而不是数据库底层的物理实现表。

我们将这些未建模的 CDO 分为四大类，并进行了详细审计：

| 分类 | 数量 | 解释与说明 | 建议处理方式 |
|------|------|------------|--------------|
| **1. 历史与交易日志 (History & Logs)** | 293 | MES 运行时的交易历史记录（如 `AssignmentHistory`, `AssociateHistory` 等）。 | **无需建模**。本体是静态知识图谱，不包含运行时的流水账数据。 |
| **2. 物理桥接表与子实体 (Bridge & Subentities)** | 98 | 数据库中用于实现多对多关系的桥接表或一对多子实体（如 `CAPAAdditionalOrganizations`, `ActivityPlanPrerequisites` 等）。 | **通过关系（Edge）建模**。在本体中，桥接表直接简化为两个核心类之间的 `ONTOLOGY_RELATION` 边，无需单独建立类节点。 |
| **3. UI 与系统运维表 (UI & System)** | 49 | UI 菜单、系统会话、导入导出日志、用户常量等运维辅助表（如 `ActiveUserSession`, `ActionsMenu`, `ButtonLabel`）。 | **无需建模**。与制造业务过程和工艺无关。 |
| **4. 潜在的核心建模类 (Core Modeling)** | 418 | **真正值得关注的核心配置 CDO**。这是可能缺失的业务建模对象，例如 `Activity`（活动）、`ActivityTemplate`（活动模板）等。 | **按需补充建模**。需逐个甄别，对核心业务配置类补充 JSON 模式。 |

---

## 🔍 潜在缺失核心建模类审计 (Core Modeling Classes — 共 418 个)

这是本次审计的**核心重点**。我们在未建模对象中，筛选出了属于物理 CDO 但在本体中完全缺失的制造相关类。以下为排名前 30 的核心 CDO 列表：

| CDO类名 | 物理ID | 推荐处理建议 |
|---------|--------|--------------|
| `ActionCategory` | `1418` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `ActionDef` | `1355` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `ActionRule` | `1356` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `Activity` | `1155` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `ActivityEventFailures` | `1290` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `ActivityNewProcessObjects` | `1306` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `ActivityPlan` | `1156` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `ActivityPlanEventLots` | `1294` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `ActivityTemplate` | `1151` | 🚨 **业务流程/执行动作 (Workflow/Action)**：建议在 `workflow_ontology.json` 中补充其作为核心步骤动作。 |
| `AlarmDefinition` | `272` | 建议按需补充，作为配置对象引入。 |
| `AlarmDefinitionTextVariables` | `273` | 建议按需补充，作为配置对象引入。 |
| `ApprovalDecision` | `1249` | 建议按需补充，作为配置对象引入。 |
| `ApprovalDecisionList` | `1234` | 建议按需补充，作为配置对象引入。 |
| `ApprovalRoutingInfo` | `1246` | 建议按需补充，作为配置对象引入。 |
| `ApprovalSheet` | `1236` | 建议按需补充，作为配置对象引入。 |
| `ApprovalSheetEntry` | `1231` | 建议按需补充，作为配置对象引入。 |
| `ApprovalSheetTemplate` | `1232` | 建议按需补充，作为配置对象引入。 |
| `AssignedMaintReq` | `1019` | 🔧 **设备维护/需求**：建议与 `maintenance_ontology.json` 进行关联。 |
| `AttachedDocs` | `1094` | 建议按需补充，作为配置对象引入。 |
| `BOMBase` | `696` | 建议按需补充，作为配置对象引入。 |
| `BOMMaterialListItemSub` | `689963047` | 建议按需补充，作为配置对象引入。 |
| `BillType` | `695` | 建议按需补充，作为配置对象引入。 |
| `Bin` | `368` | 建议按需补充，作为配置对象引入。 |
| `BusinessProcessSpecBase` | `1460` | 建议按需补充，作为配置对象引入。 |
| `BusinessProcessWorkflowBase` | `1462` | 建议按需补充，作为配置对象引入。 |
| `BusinessRuleDataHandlers` | `1121` | 建议按需补充，作为配置对象引入。 |
| `BusinessRuleParameterValues` | `1181` | 建议按需补充，作为配置对象引入。 |
| `CAPACurrentCrossRefs` | `1188` | 建议按需补充，作为配置对象引入。 |
| `CIOAttribute` | `673185819` | 建议按需补充，作为配置对象引入。 |
| `CIOBinding` | `673185830` | 建议按需补充，作为配置对象引入。 |

> [!NOTE]
> 完整列表详见本地诊断文件或在此基础上进行精细化审查。

---

## 🛠️ 后续步骤与演进建议

1. **维持“简明本体”设计理念 (Recommended)**
   * **不要**将历史表和物理桥接表引入本体，这会让图谱极度混乱并退化为普通的数据库表关系图。
   * 继续用 `ONTOLOGY_RELATION` 代替物理桥接表，使图谱保持极佳的可读性。

2. **按业务阶段补充“潜在核心建模类”**
   * **Phase 1 (高优)**: 补充 `Activity` 和 `ActivityTemplate` 类，因为当前图谱中存在它们作为“悬空引用（Dangling Target）”。
   * **Phase 2 (中优)**: 补充 SPC 统计质量控制相关的核心类（如 `SPCChartDef` 等），并与 `DataCollectionDef` 进行结合。
   * **Phase 3 (按需)**: 审查其他 unmodeled 核心配置对象，根据生产业务的变化添加新 JSON 模式文件。

