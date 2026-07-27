# Camstar Ontology vs Physical DB Schema Validation Report

This report validates the current ontology definitions against the physical database structure (derived from CSV files).

## Module Validation Summary

| Module | Classes Checked | Missing Physical Tables | Missing FK Properties | Type Mismatches | Missing Relationships | Logical-only Rels | Missing Regular Fields |
|---|---|---|---|---|---|---|---|
| Product Modeling | 4 | 0 | 0 | 0 | 0 | 3 | 91 |
| UOMs Modeling | 2 | 0 | 0 | 0 | 0 | 2 | 8 |
| Workflow Modeling | 9 | 0 | 0 | 0 | 0 | 5 | 71 |
| alarm | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| aql_levels | 2 | 0 | 0 | 0 | 0 | 0 | 8 |
| billofprocess | 2 | 0 | 0 | 0 | 0 | 0 | 4 |
| bom | 3 | 0 | 0 | 0 | 5 | 3 | 28 |
| bonus_reasons | 2 | 0 | 2 | 0 | 4 | 1 | 9 |
| business_process | 3 | 0 | 8 | 0 | 4 | 1 | 18 |
| businessrule | 6 | 0 | 0 | 0 | 0 | 2 | 25 |
| buy_reasons | 2 | 0 | 2 | 0 | 4 | 0 | 9 |
| carrier | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| change_management | 10 | 4 | 12 | 1 | 11 | 2 | 47 |
| checklist | 5 | 0 | 0 | 0 | 1 | 3 | 19 |
| component_defect | 2 | 1 | 1 | 0 | 2 | 0 | 4 |
| computation | 2 | 0 | 0 | 0 | 0 | 0 | 9 |
| computer | 2 | 0 | 2 | 0 | 5 | 0 | 8 |
| container | 7 | 0 | 0 | 0 | 6 | 3 | 119 |
| cross_module | 42 | 0 | 43 | 0 | 73 | 30 | 279 |
| customer | 2 | 0 | 0 | 0 | 0 | 0 | 8 |
| data_transport | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| datacollection | 6 | 3 | 13 | 0 | 10 | 0 | 43 |
| delegation | 3 | 0 | 3 | 0 | 2 | 0 | 14 |
| dictionary | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| dispatch | 2 | 0 | 2 | 0 | 3 | 0 | 8 |
| disposition | 3 | 0 | 5 | 0 | 2 | 0 | 12 |
| document | 4 | 0 | 0 | 0 | 0 | 1 | 23 |
| electronic_procedure | 4 | 0 | 0 | 0 | 0 | 2 | 17 |
| employee | 3 | 0 | 0 | 0 | 0 | 0 | 15 |
| enterprise | 1 | 0 | 2 | 0 | 2 | 0 | 4 |
| erp_route | 2 | 0 | 0 | 0 | 0 | 2 | 9 |
| erpbom | 2 | 0 | 0 | 0 | 4 | 0 | 29 |
| esignature | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| factory | 2 | 0 | 0 | 0 | 0 | 2 | 18 |
| failure | 8 | 0 | 10 | 0 | 14 | 1 | 34 |
| inventory | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| issue | 3 | 0 | 2 | 0 | 5 | 0 | 12 |
| label | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| local_rework | 2 | 0 | 2 | 0 | 4 | 1 | 8 |
| loss_reason | 2 | 0 | 2 | 0 | 4 | 0 | 8 |
| maintenance | 4 | 1 | 7 | 0 | 9 | 0 | 26 |
| master_data_catalog | 2 | 0 | 1 | 0 | 2 | 0 | 15 |
| master_recipe | 2 | 0 | 8 | 0 | 7 | 1 | 8 |
| material | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| mfg_order_procedure | 4 | 0 | 6 | 0 | 10 | 0 | 14 |
| mfg_order_task_list | 1 | 0 | 4 | 0 | 5 | 0 | 5 |
| mfg_order_task_status | 1 | 0 | 0 | 0 | 1 | 0 | 6 |
| mfgcalendar | 3 | 0 | 2 | 0 | 4 | 1 | 12 |
| mfgline | 1 | 0 | 0 | 0 | 2 | 0 | 4 |
| mfgorder | 4 | 0 | 0 | 0 | 9 | 2 | 46 |
| ncr | 6 | 0 | 6 | 0 | 12 | 0 | 24 |
| notification_target | 1 | 0 | 2 | 0 | 2 | 0 | 4 |
| numbering | 2 | 0 | 2 | 0 | 6 | 1 | 8 |
| occupation | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| operation | 3 | 1 | 10 | 0 | 9 | 0 | 10 |
| organization | 10 | 0 | 0 | 0 | 2 | 4 | 41 |
| owner | 1 | 0 | 2 | 0 | 3 | 2 | 4 |
| package_creation_template | 1 | 0 | 0 | 0 | 6 | 2 | 4 |
| package_type | 1 | 0 | 0 | 0 | 1 | 0 | 4 |
| packaging | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| param | 1 | 0 | 1 | 0 | 2 | 2 | 4 |
| part | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| pause_reason | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| pause_reason_group | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| phase_template | 1 | 0 | 1 | 0 | 6 | 3 | 4 |
| phase_template_disposition | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| physical_location | 2 | 0 | 2 | 0 | 2 | 0 | 8 |
| physical_position | 1 | 0 | 1 | 0 | 1 | 0 | 4 |
| plan_template | 1 | 0 | 1 | 0 | 6 | 3 | 4 |
| plan_template_disposition | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| print_queue | 1 | 0 | 1 | 0 | 2 | 0 | 3 |
| printer_label_definition | 1 | 0 | 1 | 0 | 4 | 0 | 3 |
| priority_code | 1 | 0 | 2 | 0 | 3 | 1 | 5 |
| priority_level | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| process_list | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| process_model_template | 1 | 0 | 2 | 0 | 5 | 2 | 8 |
| process_object_template | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| process_timer | 1 | 0 | 4 | 0 | 3 | 0 | 6 |
| process_timer_type | 1 | 0 | 0 | 0 | 1 | 0 | 4 |
| product_conversion_plan | 1 | 0 | 2 | 0 | 3 | 0 | 5 |
| product_family | 1 | 0 | 0 | 0 | 2 | 0 | 8 |
| product_type | 1 | 0 | 2 | 0 | 3 | 0 | 4 |
| production_process | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| qty_adjust_reason | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| qty_adjust_reason_group | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| quality | 15 | 0 | 41 | 0 | 26 | 4 | 86 |
| quality_resolution_code | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| recipe | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| recipe_list | 1 | 0 | 0 | 0 | 0 | 0 | 5 |
| recurring_date_req | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| regulatory_agency | 1 | 0 | 2 | 0 | 2 | 0 | 4 |
| regulatory_report_type | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| release_reason | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| removal_reason | 1 | 0 | 1 | 0 | 2 | 0 | 5 |
| remove_difference_reason | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| replace_reason | 1 | 0 | 0 | 0 | 1 | 0 | 5 |
| res_status_code_group | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| res_status_reason_group | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| resource | 2 | 1 | 1 | 0 | 0 | 1 | 1 |
| resource_bom | 1 | 0 | 2 | 0 | 2 | 1 | 5 |
| resource_family | 1 | 0 | 10 | 0 | 11 | 0 | 18 |
| resource_group | 1 | 0 | 0 | 0 | 2 | 0 | 7 |
| resource_layout | 1 | 0 | 0 | 0 | 1 | 0 | 7 |
| resource_material_part | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| resource_status_code | 1 | 0 | 2 | 0 | 3 | 0 | 13 |
| resource_status_model | 1 | 0 | 1 | 0 | 2 | 0 | 2 |
| resource_status_reason | 1 | 0 | 1 | 0 | 2 | 0 | 5 |
| resource_type | 1 | 0 | 3 | 0 | 4 | 0 | 4 |
| response_set | 1 | 0 | 1 | 0 | 0 | 0 | 4 |
| returned_equipment_action | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| rework | 3 | 1 | 7 | 0 | 6 | 2 | 9 |
| rework_reason | 1 | 0 | 2 | 0 | 3 | 1 | 4 |
| rework_reason_group | 1 | 0 | 1 | 0 | 2 | 1 | 4 |
| role | 1 | 0 | 0 | 0 | 0 | 0 | 4 |
| role_permissions | 1 | 0 | 0 | 0 | 0 | 0 | 5 |
| rollup_reason | 1 | 0 | 1 | 0 | 2 | 1 | 4 |
| rollup_reason_group | 1 | 0 | 1 | 0 | 2 | 2 | 4 |
| salesorder | 1 | 0 | 3 | 0 | 5 | 0 | 4 |
| sampling | 6 | 0 | 0 | 0 | 0 | 5 | 30 |
| scale | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| scale_group | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| scale_status_code | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| scale_status_reason | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| scheduled_business_rule | 1 | 0 | 3 | 0 | 3 | 0 | 27 |
| scheduling_route | 1 | 0 | 3 | 0 | 3 | 0 | 7 |
| scrap | 3 | 2 | 1 | 0 | 2 | 0 | 6 |
| scrap_reason | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| sell_reason | 1 | 0 | 1 | 0 | 2 | 1 | 4 |
| sell_reason_group | 1 | 0 | 1 | 0 | 2 | 1 | 4 |
| setup | 1 | 0 | 3 | 0 | 3 | 0 | 8 |
| setup_access | 1 | 0 | 0 | 0 | 1 | 0 | 4 |
| setup_maint | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| shift | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| shipment_destination | 1 | 0 | 5 | 0 | 4 | 0 | 6 |
| shipment_destination_group | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| shipping_reason | 1 | 0 | 2 | 0 | 3 | 2 | 4 |
| shipping_reason_group | 1 | 0 | 1 | 0 | 2 | 2 | 4 |
| spec | 6 | 0 | 0 | 0 | 0 | 6 | 82 |
| start_reasons | 1 | 0 | 3 | 0 | 3 | 0 | 4 |
| substitution_reason | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| supplier | 3 | 2 | 1 | 0 | 2 | 0 | 6 |
| switching_rules | 4 | 0 | 0 | 0 | 0 | 0 | 20 |
| task_list | 1 | 0 | 7 | 0 | 0 | 0 | 9 |
| tda | 1 | 0 | 3 | 0 | 1 | 0 | 9 |
| tda_maint | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| tda_reason | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| team | 1 | 0 | 1 | 0 | 2 | 1 | 4 |
| terminal | 1 | 0 | 0 | 0 | 1 | 0 | 4 |
| thruput_req | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| timer | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| tool | 5 | 1 | 7 | 0 | 5 | 0 | 19 |
| tool_family | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| tool_group | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| tool_plan | 1 | 0 | 1 | 0 | 2 | 0 | 4 |
| tooling | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| training_plan | 6 | 0 | 0 | 0 | 0 | 2 | 26 |
| triage_spec | 2 | 0 | 2 | 0 | 4 | 0 | 8 |
| workcenter | 1 | 0 | 2 | 0 | 4 | 0 | 4 |

---

## Detailed Reports by Module

### 🟨 Module: `Product Modeling` (94 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Product` | `ProductParams` | `HAS_PARAMETER` |
| `Product` | `ProductStockLevel` | `HAS_STOCK_LEVEL` |
| `ProductStockLevel` | `Product` | `BELONGS_TO_PRODUCT` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 91

| Class | Field Name | Physical DataType |
|---|---|---|
| `Product` | `MaterialAccumulateExposure` | `-7` |
| `Product` | `StdStartChildQty` | `8` |
| `Product` | `MfgOrderRequired` | `-7` |
| `Product` | `MaterialMaxReturns` | `4` |
| `Product` | `MaterialThawingDuration` | `8` |
| `Product` | `MaterialExposureDuration` | `8` |
| `Product` | `Frequency` | `12` |
| `Product` | `ERPProductFamily` | `12` |
| `Product` | `OutsourceTag` | `12` |
| `Product` | `Platform` | `12` |
| ... and 81 more | | |


---

### 🟨 Module: `UOMs Modeling` (10 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `isUOMConversion` | `Product` | `PARENT_PRODUCT` |
| `isUOMConversion` | `ProductFamily` | `PARENT_PRODUCT_FAMILY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `UOM` | `IconId` | `4` |
| `UOM` | `CDOTypeId` | `4` |
| `UOM` | `UOMId` | `1` |
| `UOM` | `UOMName` | `12` |
| `UOM` | `ChangeCount` | `4` |
| `isUOMConversion` | `ChangeCount` | `4` |
| `isUOMConversion` | `isUOMConversionId` | `1` |
| `isUOMConversion` | `CDOTypeId` | `4` |


---

### 🟨 Module: `Workflow Modeling` (76 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Workflow` | `ProcessingGate` | `HAS_GATE` |
| `Workflow` | `CollectionGate` | `HAS_GATE` |
| `Workflow` | `CycleTimeGate` | `HAS_GATE` |
| `Workflow` | `WIPMsgDetails` | `HAS_WIP_MESSAGE` |
| `WorkflowStep` | `WIPMsgDetails` | `HAS_STEP_WIP_MESSAGE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 71

| Class | Field Name | Physical DataType |
|---|---|---|
| `Workflow` | `CDOTypeId` | `4` |
| `Workflow` | `IconId` | `4` |
| `Workflow` | `WorkflowRevision` | `12` |
| `Workflow` | `WorkflowId` | `1` |
| `Workflow` | `ChangeCount` | `4` |
| `Workflow` | `Image` | `12` |
| `WorkflowStep` | `isSchdRouteStepName` | `12` |
| `WorkflowStep` | `isRouteStepName` | `12` |
| `WorkflowStep` | `WorkflowStepName` | `12` |
| `WorkflowStep` | `WorkflowStepId` | `1` |
| ... and 61 more | | |


---

### 🟨 Module: `alarm` (3 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `AlarmDef` (设备报警定义)
- `AlarmLog` (报警发生记录)
- `AlarmAction` (报警联动动作)


---

### 🟨 Module: `aql_levels` (8 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `AQLLevel` | `AQLLevelId` | `1` |
| `AQLLevel` | `CDOTypeId` | `4` |
| `AQLLevel` | `ChangeCount` | `4` |
| `AQLLevel` | `AQLLevelName` | `12` |
| `SampleSizeDetails` | `SampleSizeDetailsId` | `1` |
| `SampleSizeDetails` | `CDOTypeId` | `4` |
| `SampleSizeDetails` | `ChangeCount` | `4` |
| `SampleSizeDetails` | `ExportImportKey` | `12` |


---

### 🟨 Module: `billofprocess` (4 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `BillOfProcess` | `IconId` | `4` |
| `BillOfProcess` | `BillOfProcessId` | `1` |
| `BillOfProcessOverride` | `BillOfProcessOverrideName` | `12` |
| `BillOfProcessOverride` | `BillOfProcessOverrideId` | `1` |


---

### 🟨 Module: `bom` (36 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `BOM` | `BOMBase` | `BOMBaseId` |
| `BOM` | `ChangeStatus` | `ChangeHistoryId` |
| `BOM` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `ProductMaterialListItem` | `isImage` | `isImageId` |
| `TDA` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `BOM` | `TDA` | `HAS_TDA` |
| `TDA` | `Container` | `TRACES_CONTAINER` |
| `TDA` | `ProductMaterialListItem` | `ASSIGNED_TO_ITEM` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 28

| Class | Field Name | Physical DataType |
|---|---|---|
| `BOM` | `BOMId` | `1` |
| `BOM` | `IconId` | `4` |
| `BOM` | `BOMRevision` | `12` |
| `BOM` | `ChangeCount` | `4` |
| `BOM` | `CDOTypeId` | `4` |
| `ProductMaterialListItem` | `isProductDescription` | `12` |
| `ProductMaterialListItem` | `ES_ValidateBulkUID` | `4` |
| `ProductMaterialListItem` | `ES_ValidateIssueTool` | `4` |
| `ProductMaterialListItem` | `EffectiveFromDateGMT` | `93` |
| `ProductMaterialListItem` | `EffectiveThruDateGMT` | `93` |
| ... and 18 more | | |


---

### 🟨 Module: `bonus_reasons` (16 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `BonusReason` | `SetupAccessId` | `SetupAccess` |
| `BonusReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `BonusReason` | `SetupAccess` | `SetupAccessId` |
| `BonusReason` | `ChangeStatus` | `ChangeHistoryId` |
| `BonusReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `BonusReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `BonusReasonGroup` | `BonusReason` | `HAS_ENTRY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 9

| Class | Field Name | Physical DataType |
|---|---|---|
| `BonusReason` | `CDOTypeId` | `4` |
| `BonusReason` | `BonusReasonName` | `12` |
| `BonusReason` | `BonusReasonId` | `1` |
| `BonusReason` | `ChangeCount` | `4` |
| `BonusReasonGroup` | `BonusReasonGroupName` | `12` |
| `BonusReasonGroup` | `BonusReasonGroupId` | `1` |
| `BonusReasonGroup` | `EntryType` | `12` |
| `BonusReasonGroup` | `ChangeCount` | `4` |
| `BonusReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `business_process` (31 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `BusinessProcessWorkflow` | `BusinessProcessWorkflowBaseId` | `BusinessProcessWorkflowBase` |
| `BusinessProcessWorkflow` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |
| `BusinessProcessWorkflow` | `FirstStepId` | `WorkflowStep` |
| `BusinessProcessSpec` | `MoveStdValidationId` | `BusinessRule` |
| `BusinessProcessSpec` | `BusinessProcessSpecBaseId` | `BusinessProcessSpecBase` |
| `BusinessProcessSpec` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |
| `BPSpecBizRuleTxnMap` | `BusinessProcessSpecId` | `BusinessProcessSpec` |
| `BPSpecBizRuleTxnMap` | `BusinessRuleId` | `BusinessRule` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `BusinessProcessWorkflow` | `ChangeStatus` | `ChangeHistoryId` |
| `BusinessProcessWorkflow` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `BusinessProcessSpec` | `ChangeStatus` | `ChangeHistoryId` |
| `BusinessProcessSpec` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `BPSpecBizRuleTxnMap` | `Spec` | `REFERENCES_SPEC` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 18

| Class | Field Name | Physical DataType |
|---|---|---|
| `BusinessProcessWorkflow` | `CDOTypeId` | `4` |
| `BusinessProcessWorkflow` | `BusinessProcessWorkflowId` | `1` |
| `BusinessProcessWorkflow` | `ChangeCount` | `4` |
| `BusinessProcessWorkflow` | `Status` | `4` |
| `BusinessProcessSpec` | `LockInstances` | `-7` |
| `BusinessProcessSpec` | `AssignApprovers` | `-7` |
| `BusinessProcessSpec` | `StepIcon` | `12` |
| `BusinessProcessSpec` | `CDOTypeId` | `4` |
| `BusinessProcessSpec` | `BusinessProcessSpecId` | `1` |
| `BusinessProcessSpec` | `ChangeCount` | `4` |
| ... and 8 more | | |


---

### 🟨 Module: `businessrule` (27 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `BusinessRule` | `BizRuleParameter` | `HAS_PARAMETER` |
| `BusinessRule` | `Spec` | `ASSIGNED_TO_SPEC` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 25

| Class | Field Name | Physical DataType |
|---|---|---|
| `BusinessRule` | `BusinessRuleName` | `12` |
| `BusinessRule` | `CDOTypeId` | `4` |
| `BusinessRule` | `BusinessRuleId` | `1` |
| `BusinessRule` | `ChangeCount` | `4` |
| `BusinessRuleData` | `CDOTypeId` | `4` |
| `BusinessRuleData` | `BusinessRuleDataId` | `1` |
| `BusinessRuleData` | `ChangeCount` | `4` |
| `BusinessRuleData` | `BusinessRuleDataName` | `12` |
| `BizRuleParameter` | `ExportImportKey` | `12` |
| `BizRuleParameter` | `ValueExpression` | `12` |
| ... and 15 more | | |


---

### 🟨 Module: `buy_reasons` (15 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `BuyReason` | `SetupAccessId` | `SetupAccess` |
| `BuyReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `BuyReason` | `SetupAccess` | `SetupAccessId` |
| `BuyReason` | `ChangeStatus` | `ChangeHistoryId` |
| `BuyReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `BuyReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 9

| Class | Field Name | Physical DataType |
|---|---|---|
| `BuyReason` | `CDOTypeId` | `4` |
| `BuyReason` | `BuyReasonId` | `1` |
| `BuyReason` | `ChangeCount` | `4` |
| `BuyReason` | `BuyReasonName` | `12` |
| `BuyReasonGroup` | `BuyReasonGroupId` | `1` |
| `BuyReasonGroup` | `ChangeCount` | `4` |
| `BuyReasonGroup` | `BuyReasonGroupName` | `12` |
| `BuyReasonGroup` | `EntryType` | `12` |
| `BuyReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `carrier` (5 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Carrier` (载具)
- `CarrierFamily` (载具族)
- `CarrierGroup` (载具组)
- `CarrierStatusCode` (载具状态代码)
- `CarrierStatusReason` (载具状态原因)


---

### 🟨 Module: `change_management` (77 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ChangeMgtSpec` (变更管理规范)
- `ChangeMgtWorkflow` (变更管理工作流)
- `ChangePackageStatus` (变更包状态)
- `ApprovalRouting` (审批路由)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ChangePackage` | `AuthorId` | `Employee` |
| `ChangePackage` | `OwnerRoleId` | `RoleDef` |
| `ChangePackage` | `CurrentStatusId` | `TrackableObjectCurrentStatus` |
| `ChangePackage` | `PackageCreationTemplateId` | `PackageCreationTemplate` |
| `ChangePackage` | `PackageTypeId` | `PackageType` |
| `ChangePackage` | `CollaboratorDataId` | `CollaboratorData` |
| `CollaboratorEntry` | `ParentId` | `CollaboratorTemplate` |
| `CollaboratorEntry` | `DelegationTaskId` | `DelegationTask` |
| `CollaboratorEntry` | `CompletedById` | `Employee` |
| `CollaboratorEntry` | `AssignedCollaboratorId` | `Employee` |
| `CollaboratorEntry` | `CollaboratorId` | `Employee` |
| `CollaboratorEntry` | `RoleId` | `RoleDef` |

#### ⚠️ Property Type Mismatches
| Class | Field Name | Physical Type | Ontology Type |
|---|---|---|---|
| `ChangePackage` | `OwnerId` | `FK (Navigation)` | `String` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ChangeMgtApplication` | `ChangeStatus` | `ChangeHistoryId` |
| `ChangePackage` | `Employee` | `AuthorId` |
| `ChangePackage` | `Employee` | `OwnerId` |
| `ChangePackage` | `RoleDef` | `OwnerRoleId` |
| `ChangePackage` | `PackageCreationTemplate` | `PackageCreationTemplateId` |
| `ChangePackage` | `PackageType` | `PackageTypeId` |
| `ChangePackageReason` | `ChangeStatus` | `ChangeHistoryId` |
| `ChangePackagePriority` | `ChangeStatus` | `ChangeHistoryId` |
| `CollaboratorTemplate` | `ChangeStatus` | `ChangeHistoryId` |
| `CollaboratorEntry` | `CollaboratorTemplate` | `ParentId` |
| `CollaboratorEntry` | `RoleDef` | `RoleId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Product` | `ChangePackage` | `AFFECTED_BY` |
| `Workflow` | `ChangePackage` | `AFFECTED_BY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 47

| Class | Field Name | Physical DataType |
|---|---|---|
| `ChangeMgtApplication` | `ChangeCount` | `4` |
| `ChangeMgtApplication` | `ChangeMgtApplicationId` | `1` |
| `ChangeMgtApplication` | `ChangeMgtApplicationName` | `12` |
| `ChangeMgtApplication` | `CDOTypeId` | `4` |
| `ChangePackage` | `LockAllModelingInstances` | `-7` |
| `ChangePackage` | `AuthorName` | `12` |
| `ChangePackage` | `CPImportStatus` | `4` |
| `ChangePackage` | `ExportRequestDate` | `93` |
| `ChangePackage` | `SourceSystemName` | `12` |
| `ChangePackage` | `CreationDateGMT` | `93` |
| ... and 37 more | | |


---

### 🟨 Module: `checklist` (23 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ChecklistEntry` | `RoleDef` | `LastCompletedByRoleId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ChecklistTemplate` | `ChecklistEntry` | `HAS_ENTRY` |
| `ChecklistEntry` | `ChecklistTemplate` | `BELONGS_TO_TEMPLATE` |
| `Checklist` | `ChecklistTemplate` | `BELONGS_TO_TEMPLATE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 19

| Class | Field Name | Physical DataType |
|---|---|---|
| `ChecklistTemplate` | `IconId` | `4` |
| `ChecklistTemplate` | `Status` | `4` |
| `ChecklistTemplate` | `ChecklistTemplateId` | `1` |
| `ChecklistTemplate` | `ECO` | `12` |
| `ChecklistTemplateBase` | `ChecklistTemplateBaseId` | `1` |
| `ChecklistTemplateBase` | `ChecklistTemplateName` | `12` |
| `ChecklistEntry` | `LastCompletedOn` | `93` |
| `ChecklistEntry` | `LastCompletedOnGMT` | `93` |
| `ChecklistEntry` | `UserComments` | `12` |
| `ChecklistEntry` | `ChecklistEntryId` | `1` |
| ... and 9 more | | |


---

### 🟨 Module: `component_defect` (8 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `CompDefectReason` (组件缺陷原因)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `CompDefectReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `CompDefectReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `CompDefectReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `CompDefectReasonGroup` | `ChangeCount` | `4` |
| `CompDefectReasonGroup` | `CompDefectReasonGroupId` | `1` |
| `CompDefectReasonGroup` | `CompDefectReasonGroupName` | `12` |
| `CompDefectReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `computation` (9 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 9

| Class | Field Name | Physical DataType |
|---|---|---|
| `Computation` | `CDOTypeId` | `4` |
| `Computation` | `ComputationId` | `1` |
| `Computation` | `ComputationName` | `12` |
| `Computation` | `ChangeCount` | `4` |
| `ComputationParamSpec` | `ChangeCount` | `4` |
| `ComputationParamSpec` | `ComputationParamSpecName` | `12` |
| `ComputationParamSpec` | `ComputationParamSpecId` | `1` |
| `ComputationParamSpec` | `CDOTypeId` | `4` |
| `ComputationParamSpec` | `ExportImportKey` | `12` |


---

### 🟨 Module: `computer` (15 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Computer` | `SetupAccessId` | `SetupAccess` |
| `ComputerGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Computer` | `SetupAccess` | `SetupAccessId` |
| `Computer` | `ChangeStatus` | `ChangeHistoryId` |
| `Computer` | `UIVirtualPage` | `DefaultPageId` |
| `ComputerGroup` | `ChangeStatus` | `ChangeHistoryId` |
| `ComputerGroup` | `SetupAccess` | `SetupAccessId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `Computer` | `ChangeCount` | `4` |
| `Computer` | `CDOTypeId` | `4` |
| `Computer` | `ComputerId` | `1` |
| `Computer` | `ComputerName` | `12` |
| `ComputerGroup` | `ChangeCount` | `4` |
| `ComputerGroup` | `ComputerGroupId` | `1` |
| `ComputerGroup` | `CDOTypeId` | `4` |
| `ComputerGroup` | `ComputerGroupName` | `12` |


---

### 🟨 Module: `container` (128 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Container` | `isInventoryLocation` | `isInventoryLocationId` |
| `ChangeStatusReason` | `ChangeStatus` | `ChangeHistoryId` |
| `ContainerDefectReason` | `ChangeStatus` | `ChangeHistoryId` |
| `ContDefectReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |
| `ContainerGroup` | `ChangeStatus` | `ChangeHistoryId` |
| `ContainerAutoHoldReq` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Container` | `ChangeStatusReason` | `HAS_CHANGE_STATUS_REASON` |
| `ContDefectReasonGroup` | `ContainerDefectReason` | `HAS_ENTRY` |
| `ContainerGroup` | `Container` | `HAS_ENTRY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 119

| Class | Field Name | Physical DataType |
|---|---|---|
| `Container` | `ReferenceContainerName` | `12` |
| `Container` | `MoveInQty` | `8` |
| `Container` | `MoveInQty2` | `8` |
| `Container` | `ParentName` | `12` |
| `Container` | `MaterialWithdrawalDate` | `93` |
| `Container` | `MaterialTotalReturns` | `4` |
| `Container` | `MaterialExposureOffset` | `8` |
| `Container` | `MaterialTotalExposure` | `8` |
| `Container` | `ES_PCBNumber` | `4` |
| `Container` | `ES_PrimarySerialNumber` | `12` |
| ... and 109 more | | |


---

### 🟨 Module: `cross_module` (425 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ChangeStatus` | `ParentId` | `` |
| `WIPMsgDefMgr` | `SetupAccessId` | `SetupAccess` |
| `WIPMsgDefMgr` | `WIPMsgEntityId` | `` |
| `WIPMsgDefMgr` | `AllKeyId` | `WIPMsgKey` |
| `WIPMsgDefMgr` | `ParentId` | `` |
| `StepSchedulingDetail` | `StepId` | `WorkflowStep` |
| `TxnDetails` | `ReworkReasonId` | `ReworkReason` |
| `TxnDetails` | `NewOwnerId` | `Owner` |
| `TxnDetails` | `ToContainerLevelId` | `ContainerLevel` |
| `ES_MfgOrderReassignPlan` | `SetupAccessId` | `SetupAccess` |
| `ES_MfgOrderReassignPlan` | `ES_SetupAccessId` | `SetupAccess` |
| `isRecipePlan` | `ES_DocumentId` | `Document` |
| `ES_CADInstructions` | `ES_CADInstructionsBaseId` | `ES_CADInstructionsBase` |
| `ES_CADInstructions` | `ViewerId` | `DocumentViewer` |
| `ES_CADInstructions` | `AttachmentHolderId` | `DocAttachments` |
| `isImage` | `ViewerId` | `DocumentViewer` |
| `isImage` | `AttachmentHolderId` | `DocAttachments` |
| `isImage` | `isImageBaseId` | `isImageBase` |
| `ES_NPIJob` | `ES_NPIJobBaseId` | `ES_NPIJobBase` |
| `ES_NPIJob` | `ES_CADDocumentId` | `Document` |
| `ES_NPIJob` | `ES_CADLayersId` | `ES_CADLayers` |
| `ES_NPIJob` | `ES_CADPrimaryId` | `ES_CADPrimary` |
| `ES_NPIJob` | `ES_CADInstructionsId` | `ES_CADInstructions` |
| `isAutoStartSettings` | `isDefectMappingId` | `isDefectMapping` |
| `ES_Settings` | `ES_PCBToolBarConfigId` | `ES_ProdClientUIConfig` |
| `ES_Settings` | `ES_InformationBarConfigId` | `ES_ProdClientUIConfig` |
| `ES_Settings` | `ES_DefectGridConfigId` | `ES_ProdClientUIConfig` |
| `ES_Settings` | `ES_CommandBarConfigId` | `ES_ProdClientUIConfig` |
| `ES_Settings` | `ES_BoxGridConfigId` | `ES_ProdClientUIConfig` |
| `ES_Settings` | `ES_DefaultQtyAdjustReasonId` | `QtyAdjustReason` |
| `ES_Settings` | `ES_DefaultHoldReasonId` | `HoldReason` |
| `ES_Settings` | `ES_DefaultReworkReasonId` | `ReworkReason` |
| `ES_Settings` | `ES_DefaultLossReasonId` | `LossReason` |
| `ES_Settings` | `ES_SubstitutionReasonId` | `SubstitutionReason` |
| `ShopFloorSettings` | `isDefectMappingId` | `isDefectMapping` |
| `ShopFloorSettings` | `OwnerId` | `Owner` |
| `ShopFloorSettings` | `ProductTypeId` | `ProductType` |
| `ShopFloorSettings` | `StartReasonId` | `StartReason` |
| `ShopFloorSettings` | `WorkflowId` | `Workflow` |
| `ShopFloorSettings` | `LevelId` | `ContainerLevel` |
| `UIVirtualPage` | `DeveloperPersonalizationId` | `UIPersonalization` |
| `UIVirtualPage` | `CreatedById` | `Employee` |
| `PrinterLabelDefinitionBase` | `RevOfRcdId` | `PrinterLabelDefinition` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ChangeStatus` | `Employee` | `UserId` |
| `WIPMsgDefMgr` | `SetupAccess` | `SetupAccessId` |
| `WIPMsgDefMgr` | `WIPMsgKey` | `AllKeyId` |
| `WIPMsgDefMgr` | `ChangeStatus` | `ChangeHistoryId` |
| `StepSchedulingDetail` | `WorkflowStep` | `StepId` |
| `WIPMsgKey` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `TxnDetails` | `ReworkReason` | `ReworkReasonId` |
| `TxnDetails` | `Owner` | `NewOwnerId` |
| `TxnDetails` | `ContainerLevel` | `ToContainerLevelId` |
| `WorkflowBase` | `Workflow` | `RevOfRcdId` |
| `ERPRouteBase` | `ERPRoute` | `RevOfRcdId` |
| `ProductBase` | `Product` | `RevOfRcdId` |
| `BOMBase` | `BOM` | `RevOfRcdId` |
| `ERPBOMBase` | `ERPBOM` | `RevOfRcdId` |
| `BillOfProcessBase` | `BillOfProcess` | `RevOfRcdId` |
| `SpecBase` | `Spec` | `RevOfRcdId` |
| `ES_MfgOrderReassignPlan` | `SetupAccess` | `SetupAccessId` |
| `ES_MfgOrderReassignPlan` | `SetupAccess` | `ES_SetupAccessId` |
| `ES_MfgOrderReassignPlan` | `ChangeStatus` | `ChangeHistoryId` |
| `SamplingPlanBase` | `SamplingPlan` | `RevOfRcdId` |
| `EmailGroup` | `DataTransport` | `EmailTransportId` |
| `isRecipePlan` | `Document` | `ES_DocumentId` |
| `ES_AddressPool` | `NumberingRule` | `NumberingRuleId` |
| `ES_CADInstructions` | `DocumentViewer` | `ViewerId` |
| `ES_CADInstructions` | `DocAttachments` | `AttachmentHolderId` |
| `ES_CADInstructions` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `isImage` | `DocumentViewer` | `ViewerId` |
| `isImage` | `DocAttachments` | `AttachmentHolderId` |
| `isImage` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `ES_NPIJob` | `Document` | `ES_CADDocumentId` |
| `ES_NPIJob` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `ES_NPIJob` | `ES_CADInstructions` | `ES_CADInstructionsId` |
| `isAutoStartSettings` | `Workflow` | `isWorkflowId` |
| `isAutoStartSettings` | `Owner` | `isOwnerId` |
| `isAutoStartSettings` | `ContainerLevel` | `isLevelId` |
| `isAutoStartSettings` | `StartReason` | `isStartReasonId` |
| `isAutoStartSettings` | `ChangeStatus` | `ChangeHistoryId` |
| `isAutoStartSettings` | `ProductType` | `ProductTypeId` |
| `isAutoStartSettings` | `ProductType` | `isProductTypeId` |
| `isAutoStartSettings` | `SetupAccess` | `SetupAccessId` |
| `ES_DisplayOptions` | `SetupAccess` | `SetupAccessId` |
| `ES_DisplayOptions` | `ChangeStatus` | `ChangeHistoryId` |
| `ES_Settings` | `QtyAdjustReason` | `ES_DefaultQtyAdjustReasonId` |
| `ES_Settings` | `SetupAccess` | `SetupAccessId` |
| `ES_Settings` | `ChangeStatus` | `ChangeHistoryId` |
| `ES_Settings` | `HoldReason` | `ES_DefaultHoldReasonId` |
| `ES_Settings` | `ReworkReason` | `ES_DefaultReworkReasonId` |
| `ES_Settings` | `LossReason` | `ES_DefaultLossReasonId` |
| `ES_Settings` | `SubstitutionReason` | `ES_SubstitutionReasonId` |
| `isOEESettings` | `ChangeStatus` | `ChangeHistoryId` |
| `isOEESettings` | `SetupAccess` | `SetupAccessId` |
| `SignalRConfiguration` | `ChangeStatus` | `ChangeHistoryId` |
| `SmartScanRule` | `ChangeStatus` | `ChangeHistoryId` |
| `ShopFloorSettings` | `Owner` | `OwnerId` |
| `ShopFloorSettings` | `ProductType` | `ProductTypeId` |
| `ShopFloorSettings` | `StartReason` | `StartReasonId` |
| `ShopFloorSettings` | `Workflow` | `WorkflowId` |
| `ShopFloorSettings` | `ChangeStatus` | `ChangeHistoryId` |
| `ShopFloorSettings` | `ContainerLevel` | `LevelId` |
| `UIVirtualPage` | `SetupAccess` | `SetupAccessId` |
| `UIVirtualPage` | `ChangeStatus` | `ChangeHistoryId` |
| `UIVirtualPage` | `Employee` | `CreatedById` |
| `UIPreference` | `SetupAccess` | `SetupAccessId` |
| `UIPreference` | `ChangeStatus` | `ChangeHistoryId` |
| `PrinterLabelDefinitionBase` | `PrinterLabelDefinition` | `RevOfRcdId` |
| `DocumentBase` | `Document` | `RevOfRcdId` |
| `ElectronicProcedureBase` | `ElectronicProcedure` | `RevOfRcdId` |
| `TaskListBase` | `TaskList` | `RevOfRcdId` |
| `RecipeListBase` | `RecipeList` | `RevOfRcdId` |
| `DataCollectionDefBase` | `DataCollectionDef` | `RevOfRcdId` |
| `SampleTestBase` | `SampleTest` | `RevOfRcdId` |
| `SampleDataPointBase` | `SampleDataPoint` | `RevOfRcdId` |
| `SwitchingRuleBase` | `SwitchingRule` | `RevOfRcdId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `TDA` | `Container` | `TRACES_CONTAINER` |
| `TDA` | `ProductMaterialListItem` | `ASSIGNED_TO_ITEM` |
| `BillOfProcessOverride` | `Product` | `TARGETS_PRODUCT` |
| `BillOfProcessOverride` | `Factory` | `TARGETS_FACTORY` |
| `Team` | `Employee` | `HAS_MEMBER` |
| `WorkCenter` | `Team` | `REQUIRES_TEAM` |
| `CAPA` | `Document` | `HAS_ATTACHMENT` |
| `CAPA` | `NonconformanceReport` | `RESOLVES_NCR` |
| `BillOfProcessOverride` | `Team` | `OVERRIDES_TRAINING_TEAM` |
| `ChangePackage` | `BusinessProcessSpec` | `FOLLOWS_PROCESS_SPEC` |
| `ChangePackage` | `BusinessProcessWorkflow` | `FOLLOWS_PROCESS_WORKFLOW` |
| `EventDispositionHistoryDetail` | `EventLotHistoryDetail` | `BELONGS_TO_HISTORY_DETAIL` |
| `Spec` | `ContainerAutoHoldReq` | `HAS_CONTAINER_AUTO_HOLD_REQ` |
| `TaskItem` | `ChecklistTemplate` | `USES_CHECKLIST` |
| `EventClassificationSpecMap` | `Spec` | `HAS_SPEC` |
| `CategoryMap` | `Owner` | `HAS_OWNER` |
| `EventClassificationSpecMap` | `Owner` | `HAS_OWNER` |
| `PackageCreationTemplate` | `Owner` | `HAS_PACKAGE_OWNER` |
| `PackageCreationTemplate` | `Workflow` | `HAS_WORKFLOW` |
| `ComputationParamSpec` | `Param` | `REFERENCES_PARAM` |
| `BizRuleParameter` | `Param` | `REFERENCES_PARAM` |
| `PhaseTemplate` | `ChecklistTemplate` | `HAS_CHECKLIST` |
| `PlanTemplate` | `ChecklistTemplate` | `HAS_CHECKLIST` |
| `LabelTxnMap` | `PrinterLabelDefinitionBase` | `USES_LABEL_DEFINITION_BASE` |
| `PackageCreationTemplate` | `PriorityCode` | `HAS_PRIORITY` |
| `Spec` | `LabelTxnMap` | `HAS_LABEL_MAP` |
| `SampleTestBase` | `SetupAccess` | `HAS_SETUP_ACCESS` |
| `SampleDataPointBase` | `SetupAccess` | `HAS_SETUP_ACCESS` |
| `SwitchingRuleBase` | `SetupAccess` | `HAS_SETUP_ACCESS` |
| `SamplingPlanBase` | `SetupAccess` | `HAS_SETUP_ACCESS` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 279

| Class | Field Name | Physical DataType |
|---|---|---|
| `ChangeStatus` | `CreationUsername` | `12` |
| `ChangeStatus` | `CreationDate` | `93` |
| `ChangeStatus` | `CreationDateGMT` | `93` |
| `ChangeStatus` | `CDOTypeId` | `4` |
| `ChangeStatus` | `ChangeStatusId` | `1` |
| `ChangeStatus` | `CurrentStatus` | `4` |
| `ChangeStatus` | `Control` | `4` |
| `ChangeStatus` | `LastChangeDate` | `93` |
| `ChangeStatus` | `LastChangeDateGMT` | `93` |
| `ChangeStatus` | `ChangeCount` | `4` |
| ... and 269 more | | |


---

### 🟨 Module: `customer` (8 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `Customer` | `CustomerName` | `12` |
| `Customer` | `CustomerId` | `1` |
| `Customer` | `ChangeCount` | `4` |
| `Customer` | `CDOTypeId` | `4` |
| `CustomerContact` | `CustomerContactId` | `1` |
| `CustomerContact` | `CDOTypeId` | `4` |
| `CustomerContact` | `ChangeCount` | `4` |
| `CustomerContact` | `ExportImportKey` | `12` |


---

### 🟨 Module: `data_transport` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `DataTransport` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `DataTransport` | `SetupAccess` | `SetupAccessId` |
| `DataTransport` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `DataTransport` | `CDOTypeId` | `4` |
| `DataTransport` | `DataTransportId` | `1` |
| `DataTransport` | `ChangeCount` | `4` |
| `DataTransport` | `DataTransportName` | `12` |


---

### 🟨 Module: `datacollection` (69 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `DataPointCollectionDef` (数据点采集定义)
- `DataLimit` (数据限制)
- `DataCollectionHistory` (数据采集历史)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `DataCollectionDef` | `DataCollectionDefBaseId` | `DataCollectionDefBase` |
| `DataCollectionDef` | `SetupAccessId` | `SetupAccess` |
| `DataCollectionDef` | `isDefectReasonGroupId` | `isDefectReasonGroup` |
| `DataPoint` | `FailureResourceStatusReasonId` | `ResourceStatusReason` |
| `DataPoint` | `FailureResourceStatusCodeId` | `ResourceStatusCode` |
| `DataPoint` | `FailureHoldReasonId` | `HoldReason` |
| `DataPoint` | `isDefectReasonId` | `isDefectReason` |
| `DataPoint` | `ObjectGroupId` | `` |
| `DataPoint` | `DataCollectionDefId` | `DataPointCollectionGroup` |
| `DataPoint` | `UOMId` | `UOM` |
| `DataPointCollectionGroup` | `DataPointCollectionId` | `DataPointCollection` |
| `DataPointCollectionGroup` | `LastEnteredById` | `Employee` |
| `DataPointCollectionGroup` | `LastEnteredByRoleId` | `RoleDef` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `DataCollectionDef` | `DataCollectionDefBase` | `DataCollectionDefBaseId` |
| `DataCollectionDef` | `SetupAccess` | `SetupAccessId` |
| `DataCollectionDef` | `ChangeStatus` | `ChangeHistoryId` |
| `DataCollectionDef` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `DataPoint` | `ResourceStatusReason` | `FailureResourceStatusReasonId` |
| `DataPoint` | `ResourceStatusCode` | `FailureResourceStatusCodeId` |
| `DataPoint` | `DataPointCollectionGroup` | `DataCollectionDefId` |
| `DataPoint` | `UOM` | `UOMId` |
| `DataPointCollectionGroup` | `Employee` | `LastEnteredById` |
| `DataPointCollectionGroup` | `RoleDef` | `LastEnteredByRoleId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 43

| Class | Field Name | Physical DataType |
|---|---|---|
| `DataCollectionDef` | `CDOTypeId` | `4` |
| `DataCollectionDef` | `DataCollectionDefId` | `1` |
| `DataCollectionDef` | `DataCollectionDefRevision` | `12` |
| `DataCollectionDef` | `ChangeCount` | `4` |
| `DataPoint` | `isRequireDefectReason` | `-7` |
| `DataPoint` | `QueryName` | `12` |
| `DataPoint` | `QueryType` | `4` |
| `DataPoint` | `ListFieldExpression` | `12` |
| `DataPoint` | `DisplayMode` | `4` |
| `DataPoint` | `ObjectSelValType` | `4` |
| ... and 33 more | | |


---

### 🟨 Module: `delegation` (19 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `DelegateTaskHistory` | `HistoryId` | `` |
| `DelegateTaskHistory` | `HistoryMainlineId` | `HistoryMainline` |
| `DelegateTaskHistory` | `TxnId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `DelegationReasonCode` | `ChangeStatus` | `ChangeHistoryId` |
| `DelegationTask` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 14

| Class | Field Name | Physical DataType |
|---|---|---|
| `DelegationReasonCode` | `CDOTypeId` | `4` |
| `DelegationReasonCode` | `DelegationReasonCodeId` | `1` |
| `DelegationReasonCode` | `ChangeCount` | `4` |
| `DelegationReasonCode` | `DelegationReasonCodeName` | `12` |
| `DelegationTask` | `StartDateGMT` | `93` |
| `DelegationTask` | `CDOTypeId` | `4` |
| `DelegationTask` | `DelegationTaskId` | `1` |
| `DelegationTask` | `ChangeCount` | `4` |
| `DelegationTask` | `DelegationTaskName` | `12` |
| `DelegationTask` | `EndDateGMT` | `93` |
| ... and 4 more | | |


---

### 🟨 Module: `dictionary` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Dictionary` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Dictionary` | `SetupAccess` | `SetupAccessId` |
| `Dictionary` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `Dictionary` | `DictionaryName` | `12` |
| `Dictionary` | `DictionaryId` | `1` |
| `Dictionary` | `ChangeCount` | `4` |
| `Dictionary` | `CDOTypeId` | `4` |


---

### 🟨 Module: `dispatch` (13 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `DispatchRule` | `SetupAccessId` | `SetupAccess` |
| `DispatchDetail` | `DispatchRuleId` | `DispatchRule` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `DispatchRule` | `SetupAccess` | `SetupAccessId` |
| `DispatchRule` | `ChangeStatus` | `ChangeHistoryId` |
| `DispatchDetail` | `DispatchRule` | `DispatchRuleId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `DispatchRule` | `CDOTypeId` | `4` |
| `DispatchRule` | `DispatchRuleId` | `1` |
| `DispatchRule` | `ChangeCount` | `4` |
| `DispatchRule` | `DispatchRuleName` | `12` |
| `DispatchDetail` | `CDOTypeId` | `4` |
| `DispatchDetail` | `DispatchDetailId` | `1` |
| `DispatchDetail` | `ChangeCount` | `4` |
| `DispatchDetail` | `ExportImportKey` | `12` |


---

### 🟨 Module: `disposition` (19 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Disposition` | `SetupAccessId` | `SetupAccess` |
| `EventDisposition` | `ParentId` | `EventLot` |
| `EventDispositionHistoryDetail` | `HistoryDetailsId` | `EventLogHistoryDetail` |
| `EventDispositionHistoryDetail` | `HistoryId` | `` |
| `EventDispositionHistoryDetail` | `TxnId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Disposition` | `SetupAccess` | `SetupAccessId` |
| `Disposition` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 12

| Class | Field Name | Physical DataType |
|---|---|---|
| `Disposition` | `DispositionId` | `1` |
| `Disposition` | `ChangeCount` | `4` |
| `Disposition` | `DispositionName` | `12` |
| `Disposition` | `CDOTypeId` | `4` |
| `EventDisposition` | `CDOTypeId` | `4` |
| `EventDisposition` | `EventDispositionId` | `1` |
| `EventDisposition` | `ChangeCount` | `4` |
| `EventDisposition` | `ExportImportKey` | `12` |
| `EventDispositionHistoryDetail` | `CDOTypeId` | `4` |
| `EventDispositionHistoryDetail` | `EventDispositionHistoryDetaiId` | `1` |
| ... and 2 more | | |


---

### 🟨 Module: `document` (24 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `DocumentEntry` | `DocumentBase` | `HAS_BASE_VERSION` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 23

| Class | Field Name | Physical DataType |
|---|---|---|
| `Document` | `ES_IsJSON` | `-7` |
| `Document` | `ES_IsEDIF` | `-7` |
| `Document` | `ES_MountingTechnology` | `12` |
| `Document` | `CDOTypeId` | `4` |
| `Document` | `DocumentId` | `1` |
| `Document` | `DocumentRevision` | `12` |
| `Document` | `ChangeCount` | `4` |
| `Document` | `XShareContainerType` | `12` |
| `Document` | `XShareContainerName` | `12` |
| `Document` | `XShareParentFolder` | `12` |
| ... and 13 more | | |


---

### 🟨 Module: `electronic_procedure` (19 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `TaskList` | `TaskItem` | `HAS_TASK` |
| `TaskItem` | `TaskList` | `BELONGS_TO_TASK_LIST` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 17

| Class | Field Name | Physical DataType |
|---|---|---|
| `ElectronicProcedure` | `ElectronicProcedureRevision` | `12` |
| `ElectronicProcedure` | `CDOTypeId` | `4` |
| `ElectronicProcedure` | `ElectronicProcedureId` | `1` |
| `ElectronicProcedure` | `ChangeCount` | `4` |
| `EProcedureDetail` | `CDOTypeId` | `4` |
| `EProcedureDetail` | `EProcedureDetailId` | `1` |
| `EProcedureDetail` | `ChangeCount` | `4` |
| `EProcedureDetail` | `ExportImportKey` | `12` |
| `TaskList` | `CDOTypeId` | `4` |
| `TaskList` | `TaskListId` | `1` |
| ... and 7 more | | |


---

### 🟨 Module: `employee` (15 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 15

| Class | Field Name | Physical DataType |
|---|---|---|
| `Employee` | `ES_UseContainerList` | `4` |
| `Employee` | `CDOTypeId` | `4` |
| `Employee` | `EmployeeId` | `1` |
| `Employee` | `EmployeeName` | `12` |
| `Employee` | `UserComment` | `12` |
| `Employee` | `ChangeCount` | `4` |
| `Employee` | `FilterTagsSession` | `-10` |
| `EmployeeLoginInfo` | `CDOTypeId` | `4` |
| `EmployeeLoginInfo` | `EmployeeLoginInfoId` | `1` |
| `EmployeeLoginInfo` | `ChangeCount` | `4` |
| ... and 5 more | | |


---

### 🟨 Module: `enterprise` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Enterprise` | `SetupAccessId` | `SetupAccess` |
| `Enterprise` | `ChangeStatusId` | `ChangeStatus` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Enterprise` | `SetupAccess` | `SetupAccessId` |
| `Enterprise` | `ChangeStatus` | `ChangeStatusId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `Enterprise` | `CDOTypeId` | `4` |
| `Enterprise` | `EnterpriseId` | `1` |
| `Enterprise` | `EnterpriseName` | `12` |
| `Enterprise` | `ChangeCount` | `4` |


---

### 🟨 Module: `erp_route` (11 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ERPRoute` | `RouteStep` | `HAS_ROUTE_STEP` |
| `RouteStep` | `ERPRoute` | `BELONGS_TO_ERP_ROUTE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 9

| Class | Field Name | Physical DataType |
|---|---|---|
| `ERPRoute` | `CDOTypeId` | `4` |
| `ERPRoute` | `ERPRouteId` | `1` |
| `ERPRoute` | `ERPRouteRevision` | `12` |
| `ERPRoute` | `ChangeCount` | `4` |
| `RouteStep` | `ES_StartVirtualSN` | `-7` |
| `RouteStep` | `CDOTypeId` | `4` |
| `RouteStep` | `RouteStepId` | `1` |
| `RouteStep` | `ChangeCount` | `4` |
| `RouteStep` | `ExportImportKey` | `12` |


---

### 🟨 Module: `erpbom` (33 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ERPBOM` | `ERPBOMBase` | `ERPBOMBaseId` |
| `ERPBOM` | `ChangeStatus` | `ChangeHistoryId` |
| `ERPBOM` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `BOMMaterialListItem` | `isImage` | `isImageId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 29

| Class | Field Name | Physical DataType |
|---|---|---|
| `ERPBOM` | `ChangeCount` | `4` |
| `ERPBOM` | `IconId` | `4` |
| `ERPBOM` | `ERPBOMRevision` | `12` |
| `ERPBOM` | `Status` | `4` |
| `ERPBOM` | `ERPBOMId` | `1` |
| `ERPBOM` | `CDOTypeId` | `4` |
| `BOMMaterialListItem` | `ES_PCBSide` | `4` |
| `BOMMaterialListItem` | `isProductDescription` | `12` |
| `BOMMaterialListItem` | `ES_MountingTechnology` | `4` |
| `BOMMaterialListItem` | `ES_ValidateBulkUID` | `4` |
| ... and 19 more | | |


---

### 🟨 Module: `esignature` (3 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `SignatureRule` (电子签名规则)
- `SignatureRole` (签字权限角色)
- `SignatureLog` (电子签名审计日志)


---

### 🟨 Module: `factory` (20 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Factory` | `ReplaceReason` | `HAS_REPLACEMENT_REASON` |
| `Factory` | `RemoveDifferenceReason` | `HAS_ISSUE_DIFF_REASON` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 18

| Class | Field Name | Physical DataType |
|---|---|---|
| `Site` | `CDOTypeId` | `4` |
| `Site` | `SiteId` | `1` |
| `Site` | `ChangeCount` | `4` |
| `Site` | `SiteName` | `12` |
| `Factory` | `ES_DefaultRevision` | `12` |
| `Factory` | `ES_RequireNPIJob` | `-7` |
| `Factory` | `ES_UniqueSerialNumbers` | `-7` |
| `Factory` | `ES_UseContainerList` | `4` |
| `Factory` | `ES_UseContainerNameForSN` | `-7` |
| `Factory` | `ES_MdmGUID` | `12` |
| ... and 8 more | | |


---

### 🟨 Module: `failure` (59 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `FailureMode` | `SetupAccessId` | `SetupAccess` |
| `FailureModeGroup` | `SetupAccessId` | `SetupAccess` |
| `NCRFailureType` | `SetupAccessId` | `SetupAccess` |
| `FailureSeverity` | `SetupAccessId` | `SetupAccess` |
| `FailureActionType` | `SetupAccessId` | `SetupAccess` |
| `FailureActionTypeGroup` | `SetupAccessId` | `SetupAccess` |
| `EventFailure` | `EventDataId` | `EventDisposition` |
| `EventFailure` | `FailureSeverityId` | `FailureSeverity` |
| `EventFailureAction` | `ParentId` | `EventFailureCause` |
| `EventFailureAction` | `ActionOwnerId` | `Employee` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `FailureMode` | `SetupAccess` | `SetupAccessId` |
| `FailureMode` | `ChangeStatus` | `ChangeHistoryId` |
| `FailureModeGroup` | `SetupAccess` | `SetupAccessId` |
| `FailureModeGroup` | `ChangeStatus` | `ChangeHistoryId` |
| `NCRFailureType` | `SetupAccess` | `SetupAccessId` |
| `NCRFailureType` | `ChangeStatus` | `ChangeHistoryId` |
| `FailureSeverity` | `SetupAccess` | `SetupAccessId` |
| `FailureSeverity` | `ChangeStatus` | `ChangeHistoryId` |
| `FailureActionType` | `SetupAccess` | `SetupAccessId` |
| `FailureActionType` | `ChangeStatus` | `ChangeHistoryId` |
| `FailureActionTypeGroup` | `SetupAccess` | `SetupAccessId` |
| `FailureActionTypeGroup` | `ChangeStatus` | `ChangeHistoryId` |
| `EventFailure` | `EventDisposition` | `EventDataId` |
| `EventFailureAction` | `Employee` | `ActionOwnerId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `EventFailure` | `EventFailureAction` | `HAS_FAILURE_ACTION` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 34

| Class | Field Name | Physical DataType |
|---|---|---|
| `FailureMode` | `CDOTypeId` | `4` |
| `FailureMode` | `FailureModeId` | `1` |
| `FailureMode` | `ChangeCount` | `4` |
| `FailureMode` | `FailureModeName` | `12` |
| `FailureModeGroup` | `FailureModeGroupName` | `12` |
| `FailureModeGroup` | `CDOTypeId` | `4` |
| `FailureModeGroup` | `FailureModeGroupId` | `1` |
| `FailureModeGroup` | `ChangeCount` | `4` |
| `NCRFailureType` | `CDOTypeId` | `4` |
| `NCRFailureType` | `ChangeCount` | `4` |
| ... and 24 more | | |


---

### 🟨 Module: `inventory` (3 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Warehouse` (车间线边库)
- `Locator` (储位/货架)
- `InventoryBalance` (库存结存)


---

### 🟨 Module: `issue` (19 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `IssueReason` | `SetupAccessId` | `SetupAccess` |
| `IssueDifferenceReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `IssueReason` | `SetupAccess` | `SetupAccessId` |
| `IssueReason` | `ChangeStatus` | `ChangeHistoryId` |
| `IssueDifferenceReason` | `SetupAccess` | `SetupAccessId` |
| `IssueDifferenceReason` | `ChangeStatus` | `ChangeHistoryId` |
| `IssueCondition` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 12

| Class | Field Name | Physical DataType |
|---|---|---|
| `IssueReason` | `ChangeCount` | `4` |
| `IssueReason` | `IssueReasonId` | `1` |
| `IssueReason` | `IssueReasonName` | `12` |
| `IssueReason` | `CDOTypeId` | `4` |
| `IssueDifferenceReason` | `ChangeCount` | `4` |
| `IssueDifferenceReason` | `IssueDifferenceReasonName` | `12` |
| `IssueDifferenceReason` | `IssueDifferenceReasonId` | `1` |
| `IssueDifferenceReason` | `CDOTypeId` | `4` |
| `IssueCondition` | `ChangeCount` | `4` |
| `IssueCondition` | `IssueConditionId` | `1` |
| ... and 2 more | | |


---

### 🟨 Module: `label` (3 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Label` (标签定义)
- `LabelFormat` (标签格式)
- `Printer` (打印机终端)


---

### 🟨 Module: `local_rework` (15 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `LocalReworkReason` | `SetupAccessId` | `SetupAccess` |
| `LocalReworkReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `LocalReworkReason` | `SetupAccess` | `SetupAccessId` |
| `LocalReworkReason` | `ChangeStatus` | `ChangeHistoryId` |
| `LocalReworkReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `LocalReworkReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `LocalReworkReasonGroup` | `LocalReworkReason` | `HAS_ENTRY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `LocalReworkReason` | `CDOTypeId` | `4` |
| `LocalReworkReason` | `LocalReworkReasonId` | `1` |
| `LocalReworkReason` | `ChangeCount` | `4` |
| `LocalReworkReason` | `LocalReworkReasonName` | `12` |
| `LocalReworkReasonGroup` | `LocalReworkReasonGroupId` | `1` |
| `LocalReworkReasonGroup` | `ChangeCount` | `4` |
| `LocalReworkReasonGroup` | `LocalReworkReasonGroupName` | `12` |
| `LocalReworkReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `loss_reason` (14 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `LossReason` | `SetupAccessId` | `SetupAccess` |
| `LossReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `LossReason` | `SetupAccess` | `SetupAccessId` |
| `LossReason` | `ChangeStatus` | `ChangeHistoryId` |
| `LossReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `LossReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `LossReason` | `CDOTypeId` | `4` |
| `LossReason` | `LossReasonName` | `12` |
| `LossReason` | `LossReasonId` | `1` |
| `LossReason` | `ChangeCount` | `4` |
| `LossReasonGroup` | `LossReasonGroupId` | `1` |
| `LossReasonGroup` | `ChangeCount` | `4` |
| `LossReasonGroup` | `LossReasonGroupName` | `12` |
| `LossReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `maintenance` (43 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `DateReq` (维护日期需求)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `MaintenanceClass` | `SetupAccessId` | `SetupAccess` |
| `MaintenanceReason` | `SetupAccessId` | `SetupAccess` |
| `MaintenanceReq` | `SetupAccessId` | `SetupAccess` |
| `MaintenanceReq` | `MaintenanceReqBaseId` | `MaintenanceReqBase` |
| `MaintenanceReq` | `DataCollectionDefBaseId` | `` |
| `MaintenanceReq` | `DataCollectionDefId` | `DataCollectionDef` |
| `MaintenanceReq` | `BOMBaseId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MaintenanceClass` | `SetupAccess` | `SetupAccessId` |
| `MaintenanceClass` | `ChangeStatus` | `ChangeHistoryId` |
| `MaintenanceReason` | `SetupAccess` | `SetupAccessId` |
| `MaintenanceReason` | `ChangeStatus` | `ChangeHistoryId` |
| `MaintenanceReq` | `SetupAccess` | `SetupAccessId` |
| `MaintenanceReq` | `ChangeStatus` | `ChangeHistoryId` |
| `MaintenanceReq` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `MaintenanceReq` | `ESigRequirement` | `ESigRequirementId` |
| `MaintenanceReq` | `ResourceBOM` | `BOMId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 26

| Class | Field Name | Physical DataType |
|---|---|---|
| `MaintenanceClass` | `MaintenanceClassId` | `1` |
| `MaintenanceClass` | `CDOTypeId` | `4` |
| `MaintenanceClass` | `MaintenanceClassName` | `12` |
| `MaintenanceClass` | `ChangeCount` | `4` |
| `MaintenanceReason` | `MaintenanceReasonName` | `12` |
| `MaintenanceReason` | `MaintenanceReasonId` | `1` |
| `MaintenanceReason` | `CDOTypeId` | `4` |
| `MaintenanceReason` | `ChangeCount` | `4` |
| `MaintenanceReq` | `CalculatedEndDate` | `93` |
| `MaintenanceReq` | `FirstMaintDateDue` | `93` |
| ... and 16 more | | |


---

### 🟨 Module: `master_data_catalog` (18 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `MasterDataCatalogDtl` | `MasterDataCatalogId` | `MasterDataCatalog` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MasterDataCatalog` | `ChangeStatus` | `ChangeHistoryId` |
| `MasterDataCatalogDtl` | `MasterDataCatalog` | `MasterDataCatalogId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 15

| Class | Field Name | Physical DataType |
|---|---|---|
| `MasterDataCatalog` | `MasterDataCatalogId` | `1` |
| `MasterDataCatalog` | `ChangeCount` | `4` |
| `MasterDataCatalog` | `MasterDataCatalogName` | `12` |
| `MasterDataCatalog` | `CDOTypeId` | `4` |
| `MasterDataCatalogDtl` | `ChangeCount` | `4` |
| `MasterDataCatalogDtl` | `ApprovalWorkflowControlled` | `-7` |
| `MasterDataCatalogDtl` | `MasterDataCatalogDtlId` | `1` |
| `MasterDataCatalogDtl` | `ExportImportKey` | `12` |
| `MasterDataCatalogDtl` | `MasterDataCatalogDtlName` | `12` |
| `MasterDataCatalogDtl` | `Comments` | `12` |
| ... and 5 more | | |


---

### 🟨 Module: `master_recipe` (24 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `MasterRecipe` | `MasterRecipeBaseId` | `MasterRecipeBase` |
| `MasterRecipe` | `SetupAccessId` | `SetupAccess` |
| `MasterRecipe` | `RecipeProductBaseId` | `` |
| `MasterRecipe` | `WorkflowBaseId` | `` |
| `MasterRecipeDetail` | `MasterRecipeId` | `MasterRecipe` |
| `MasterRecipeDetail` | `TaskListBaseId` | `` |
| `MasterRecipeDetail` | `SpecBaseId` | `` |
| `MasterRecipeDetail` | `SpecId` | `Spec` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MasterRecipe` | `SetupAccess` | `SetupAccessId` |
| `MasterRecipe` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `MasterRecipe` | `ChangeStatus` | `ChangeHistoryId` |
| `MasterRecipe` | `PrinterLabelDefinition` | `PrinterLabelDefinitionId` |
| `MasterRecipeDetail` | `MasterRecipe` | `MasterRecipeId` |
| `MasterRecipeDetail` | `RecipeList` | `TaskListId` |
| `MasterRecipeDetail` | `Spec` | `SpecId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `MasterRecipeDetail` | `TaskList` | `REFERENCES_TASKLIST` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `MasterRecipe` | `CDOTypeId` | `4` |
| `MasterRecipe` | `MasterRecipeId` | `1` |
| `MasterRecipe` | `ChangeCount` | `4` |
| `MasterRecipeDetail` | `ChangeCount` | `4` |
| `MasterRecipeDetail` | `MasterRecipeDetailId` | `1` |
| `MasterRecipeDetail` | `SubSequence` | `4` |
| `MasterRecipeDetail` | `CDOTypeId` | `4` |
| `MasterRecipeDetail` | `ExportImportKey` | `12` |


---

### 🟨 Module: `material` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Material` (原材料)


---

### 🟨 Module: `mfg_order_procedure` (30 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `MfgOrderProcedure` | `MfgOrderProcedureBaseId` | `MfgOrderProcedureBase` |
| `MfgOrderProcedureDetail` | `MfgOrderProcedureId` | `MfgOrderProcedure` |
| `MfgOrderProcedureDetail` | `MfgOrderTaskListBaseId` | `` |
| `MfgOrderProcedureDetail` | `MfgOrderTaskListId` | `MfgOrderTaskList` |
| `MfgOrderTaskList` | `MfgOrderTaskListBaseId` | `MfgOrderTaskListBase` |
| `MfgOrderTaskList` | `isImageId` | `isImage` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MfgOrderProcedure` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `MfgOrderProcedure` | `OrderStatus` | `CompletedOrderStatusId` |
| `MfgOrderProcedure` | `ChangeStatus` | `ChangeHistoryId` |
| `MfgOrderProcedureDetail` | `MfgOrderProcedure` | `MfgOrderProcedureId` |
| `MfgOrderTaskList` | `isImage` | `isImageId` |
| `MfgOrderTaskList` | `ChangeStatus` | `ChangeHistoryId` |
| `MfgOrderTaskList` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `MfgOrderTaskList` | `MfgOrderTaskList` | `PrerequisiteTaskListId` |
| `MfgOrderTaskList` | `ResourceGroup` | `WorkstationGroupId` |
| `MfgOrderTaskStatus` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 14

| Class | Field Name | Physical DataType |
|---|---|---|
| `MfgOrderProcedure` | `ChangeCount` | `4` |
| `MfgOrderProcedure` | `MfgOrderProcedureId` | `1` |
| `MfgOrderProcedure` | `CDOTypeId` | `4` |
| `MfgOrderProcedureDetail` | `ChangeCount` | `4` |
| `MfgOrderProcedureDetail` | `CDOTypeId` | `4` |
| `MfgOrderProcedureDetail` | `MfgOrderProcedureDetailName` | `12` |
| `MfgOrderProcedureDetail` | `MfgOrderProcedureDetailId` | `1` |
| `MfgOrderTaskList` | `ChangeCount` | `4` |
| `MfgOrderTaskList` | `CDOTypeId` | `4` |
| `MfgOrderTaskList` | `MfgOrderTaskListId` | `1` |
| ... and 4 more | | |


---

### 🟨 Module: `mfg_order_task_list` (14 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `MfgOrderTaskList` | `MfgOrderTaskListBaseId` | `MfgOrderTaskListBase` |
| `MfgOrderTaskList` | `isImageId` | `isImage` |
| `MfgOrderTaskList` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |
| `MfgOrderTaskList` | `PrerequisiteTaskListId` | `MfgOrderTaskList` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MfgOrderTaskList` | `isImage` | `isImageId` |
| `MfgOrderTaskList` | `ChangeStatus` | `ChangeHistoryId` |
| `MfgOrderTaskList` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `MfgOrderTaskList` | `MfgOrderTaskList` | `PrerequisiteTaskListId` |
| `MfgOrderTaskList` | `ResourceGroup` | `WorkstationGroupId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `MfgOrderTaskList` | `ChangeCount` | `4` |
| `MfgOrderTaskList` | `CDOTypeId` | `4` |
| `MfgOrderTaskList` | `Instruction` | `12` |
| `MfgOrderTaskList` | `ReportInstruction` | `12` |
| `MfgOrderTaskList` | `MfgOrderTaskListId` | `1` |


---

### 🟨 Module: `mfg_order_task_status` (7 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MfgOrderTaskStatus` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 6

| Class | Field Name | Physical DataType |
|---|---|---|
| `MfgOrderTaskStatus` | `MfgOrderTaskStatusName` | `12` |
| `MfgOrderTaskStatus` | `TaskComplete` | `-7` |
| `MfgOrderTaskStatus` | `TaskFailed` | `-7` |
| `MfgOrderTaskStatus` | `ChangeCount` | `4` |
| `MfgOrderTaskStatus` | `CDOTypeId` | `4` |
| `MfgOrderTaskStatus` | `MfgOrderTaskStatusId` | `1` |


---

### 🟨 Module: `mfgcalendar` (19 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Shift` | `SetupAccessId` | `SetupAccess` |
| `CalendarShift` | `MfgCalendarId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MfgCalendar` | `SetupAccess` | `SetupAccessId` |
| `MfgCalendar` | `ChangeStatus` | `ChangeHistoryId` |
| `Shift` | `SetupAccess` | `SetupAccessId` |
| `Shift` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `MfgCalendar` | `CalendarShift` | `HAS_SHIFT` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 12

| Class | Field Name | Physical DataType |
|---|---|---|
| `MfgCalendar` | `MfgCalendarName` | `12` |
| `MfgCalendar` | `CDOTypeId` | `4` |
| `MfgCalendar` | `ChangeCount` | `4` |
| `MfgCalendar` | `MfgCalendarId` | `1` |
| `Shift` | `ShiftId` | `1` |
| `Shift` | `ShiftName` | `12` |
| `Shift` | `ChangeCount` | `4` |
| `Shift` | `CDOTypeId` | `4` |
| `CalendarShift` | `CalendarShiftId` | `1` |
| `CalendarShift` | `ChangeCount` | `4` |
| ... and 2 more | | |


---

### 🟨 Module: `mfgline` (6 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MfgLine` | `ChangeStatus` | `ChangeHistoryId` |
| `MfgLine` | `SetupAccess` | `SetupAccessId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `MfgLine` | `ChangeCount` | `4` |
| `MfgLine` | `MfgLineId` | `1` |
| `MfgLine` | `CDOTypeId` | `4` |
| `MfgLine` | `MfgLineName` | `12` |


---

### 🟨 Module: `mfgorder` (57 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `MfgOrder` | `isRecipePlan` | `isRecipePlanId` |
| `MfgOrder` | `ES_AddressPool` | `ES_CustomAddressPoolId` |
| `MfgOrder` | `ES_AddressPool` | `ES_IMEIAddressPoolId` |
| `MfgOrder` | `ES_AddressPool` | `ES_MACAddressPoolId` |
| `MfgOrder` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `MfgOrder` | `ChangeStatus` | `ChangeStatusId` |
| `OrderType` | `ChangeStatus` | `ChangeHistoryId` |
| `OrderStatus` | `ChangeStatus` | `ChangeHistoryId` |
| `MfgOrderMaterialListItem` | `isImage` | `isImageId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `MfgOrder` | `ProductType` | `HAS_DEFAULT_PRODUCT_TYPE` |
| `MfgOrderMaterialListItem` | `MfgOrder` | `BELONGS_TO_ORDER` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 46

| Class | Field Name | Physical DataType |
|---|---|---|
| `MfgOrder` | `PISO` | `12` |
| `MfgOrder` | `OriginalCompletionPlan` | `12` |
| `MfgOrder` | `RMANumber` | `12` |
| `MfgOrder` | `OriginalPMDemandDate` | `93` |
| `MfgOrder` | `PMDemandDate` | `93` |
| `MfgOrder` | `RSDCommitment` | `12` |
| `MfgOrder` | `OriginalShipPlanAndRBWCommit` | `12` |
| `MfgOrder` | `CompletionPlan` | `12` |
| `MfgOrder` | `ReworkId` | `12` |
| `MfgOrder` | `ProjectCode` | `12` |
| ... and 36 more | | |


---

### 🟨 Module: `ncr` (42 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `NCRCauseCode` | `SetupAccessId` | `SetupAccess` |
| `NCRCauseCodeGroup` | `SetupAccessId` | `SetupAccess` |
| `NCRFailureCode` | `SetupAccessId` | `SetupAccess` |
| `NCRFailureCodeGroup` | `SetupAccessId` | `SetupAccess` |
| `NCRResolutionCode` | `SetupAccessId` | `SetupAccess` |
| `NCRResolutionCodeGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `NCRCauseCode` | `SetupAccess` | `SetupAccessId` |
| `NCRCauseCode` | `ChangeStatus` | `ChangeHistoryId` |
| `NCRCauseCodeGroup` | `SetupAccess` | `SetupAccessId` |
| `NCRCauseCodeGroup` | `ChangeStatus` | `ChangeHistoryId` |
| `NCRFailureCode` | `SetupAccess` | `SetupAccessId` |
| `NCRFailureCode` | `ChangeStatus` | `ChangeHistoryId` |
| `NCRFailureCodeGroup` | `SetupAccess` | `SetupAccessId` |
| `NCRFailureCodeGroup` | `ChangeStatus` | `ChangeHistoryId` |
| `NCRResolutionCode` | `SetupAccess` | `SetupAccessId` |
| `NCRResolutionCode` | `ChangeStatus` | `ChangeHistoryId` |
| `NCRResolutionCodeGroup` | `SetupAccess` | `SetupAccessId` |
| `NCRResolutionCodeGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 24

| Class | Field Name | Physical DataType |
|---|---|---|
| `NCRCauseCode` | `CDOTypeId` | `4` |
| `NCRCauseCode` | `NCRCauseCodeId` | `1` |
| `NCRCauseCode` | `NCRCauseCodeName` | `12` |
| `NCRCauseCode` | `ChangeCount` | `4` |
| `NCRCauseCodeGroup` | `CDOTypeId` | `4` |
| `NCRCauseCodeGroup` | `ChangeCount` | `4` |
| `NCRCauseCodeGroup` | `NCRCauseCodeGroupName` | `12` |
| `NCRCauseCodeGroup` | `NCRCauseCodeGroupId` | `1` |
| `NCRFailureCode` | `NCRFailureCodeId` | `1` |
| `NCRFailureCode` | `ChangeCount` | `4` |
| ... and 14 more | | |


---

### 🟨 Module: `notification_target` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `NotificationTarget` | `SetupAccessId` | `SetupAccess` |
| `NotificationTarget` | `ChangeStatusId` | `ChangeStatus` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `NotificationTarget` | `SetupAccess` | `SetupAccessId` |
| `NotificationTarget` | `ChangeStatus` | `ChangeStatusId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `NotificationTarget` | `CDOTypeId` | `4` |
| `NotificationTarget` | `NotificationTargetId` | `1` |
| `NotificationTarget` | `NotificationTargetName` | `12` |
| `NotificationTarget` | `ChangeCount` | `4` |


---

### 🟨 Module: `numbering` (17 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `NumberingRule` | `SetupAccessId` | `SetupAccess` |
| `DynamicNumberingRule` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `NumberingRule` | `SetupAccess` | `SetupAccessId` |
| `NumberingRule` | `ChangeStatus` | `ChangeHistoryId` |
| `DynamicNumberingRule` | `SetupAccess` | `SetupAccessId` |
| `DynamicNumberingRule` | `DynamicNumberingRule` | `ResolvedNumberingRuleId` |
| `DynamicNumberingRule` | `DynamicNumberingRule` | `NewDynamicNumberingRuleId` |
| `DynamicNumberingRule` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `NumberingRule` | `DynamicNumberingRule` | `MIGRATES_TO_DYNAMIC` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `NumberingRule` | `NumberingRuleId` | `1` |
| `NumberingRule` | `CDOTypeId` | `4` |
| `NumberingRule` | `ChangeCount` | `4` |
| `NumberingRule` | `NumberingRuleName` | `12` |
| `DynamicNumberingRule` | `DynamicNumberingRuleName` | `12` |
| `DynamicNumberingRule` | `CDOTypeId` | `4` |
| `DynamicNumberingRule` | `DynamicNumberingRuleId` | `1` |
| `DynamicNumberingRule` | `ChangeCount` | `4` |


---

### 🟨 Module: `occupation` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Occupation` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Occupation` | `SetupAccess` | `SetupAccessId` |
| `Occupation` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `Occupation` | `OccupationId` | `1` |
| `Occupation` | `CDOTypeId` | `4` |
| `Occupation` | `ChangeCount` | `4` |
| `Occupation` | `OccupationName` | `12` |


---

### 🟨 Module: `operation` (30 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `DisallowedTxn` (禁用事务)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ContainerLevel` | `ChildContainerNumberingRuleId` | `NumberingRule` |
| `ContainerLevel` | `SetupAccessId` | `SetupAccess` |
| `ContainerLevel` | `ES_ParentSNRuleId` | `NumberingRule` |
| `ContainerLevel` | `ES_ChildSNRuleId` | `NumberingRule` |
| `Operation` | `SetupAccessId` | `SetupAccess` |
| `Operation` | `ES_isDefectReasonGroupId` | `isDefectReasonGroup` |
| `Operation` | `ES_DisplayOptionsId` | `ES_DisplayOptions` |
| `Operation` | `QtyAdjustReasonId` | `QtyAdjustGroup` |
| `Operation` | `ChangeStatusId` | `ChangeStatus` |
| `Operation` | `AutoAdjustReasonId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ContainerLevel` | `SetupAccess` | `SetupAccessId` |
| `ContainerLevel` | `UIPreference` | `UIPreferenceId` |
| `ContainerLevel` | `ChangeStatus` | `ChangeHistoryId` |
| `ContainerLevel` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `Operation` | `SetupAccess` | `SetupAccessId` |
| `Operation` | `ES_DisplayOptions` | `ES_DisplayOptionsId` |
| `Operation` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `Operation` | `ChangeStatus` | `ChangeStatusId` |
| `Operation` | `TrainingRequirementGroup` | `TrainingReqGroupId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 10

| Class | Field Name | Physical DataType |
|---|---|---|
| `ContainerLevel` | `ES_LevelType` | `4` |
| `ContainerLevel` | `CDOTypeId` | `4` |
| `ContainerLevel` | `ContainerLevelId` | `1` |
| `ContainerLevel` | `ContainerLevelName` | `12` |
| `ContainerLevel` | `ChangeCount` | `4` |
| `Operation` | `ES_NPIDocumentView` | `12` |
| `Operation` | `CDOTypeId` | `4` |
| `Operation` | `OperationId` | `1` |
| `Operation` | `OperationName` | `12` |
| `Operation` | `ChangeCount` | `4` |


---

### 🟨 Module: `organization` (47 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `CategoryMap` | `RoleDef` | `RoleId` |
| `EventClassificationSpecMap` | `RoleDef` | `RoleId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Organization` | `CategoryMap` | `HAS_CATEGORY_MAP` |
| `Organization` | `NotificationEvent` | `HAS_NOTIFICATION` |
| `Organization` | `QualityProcessingMap` | `HAS_QUALITY_PROCESSING` |
| `CategoryMap` | `ApprovalSheetMap` | `HAS_APPROVAL_SHEET` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 41

| Class | Field Name | Physical DataType |
|---|---|---|
| `Organization` | `IconId` | `4` |
| `Organization` | `OrganizationName` | `12` |
| `Organization` | `CDOTypeId` | `4` |
| `Organization` | `OrganizationId` | `1` |
| `Organization` | `ChangeCount` | `4` |
| `CategoryMap` | `ExportImportKey` | `12` |
| `CategoryMap` | `CDOTypeId` | `4` |
| `CategoryMap` | `CategoryMapId` | `1` |
| `CategoryMap` | `ChangeCount` | `4` |
| `ApprovalSheetMap` | `ExportImportKey` | `12` |
| ... and 31 more | | |


---

### 🟨 Module: `owner` (11 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Owner` | `SetupAccessId` | `SetupAccess` |
| `Owner` | `ChangeStatusId` | `ChangeStatus` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Owner` | `SetupAccess` | `SetupAccessId` |
| `Owner` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `Owner` | `ChangeStatus` | `ChangeStatusId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `CategoryMap` | `Owner` | `HAS_OWNER` |
| `EventClassificationSpecMap` | `Owner` | `HAS_OWNER` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `Owner` | `CDOTypeId` | `4` |
| `Owner` | `OwnerId` | `1` |
| `Owner` | `OwnerName` | `12` |
| `Owner` | `ChangeCount` | `4` |


---

### 🟨 Module: `package_creation_template` (12 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PackageCreationTemplate` | `Employee` | `PackageOwnerId` |
| `PackageCreationTemplate` | `ChangeStatus` | `ChangeHistoryId` |
| `PackageCreationTemplate` | `RoleDef` | `OwnerRoleId` |
| `PackageCreationTemplate` | `ChangePackagePriority` | `PackagePriorityCodeId` |
| `PackageCreationTemplate` | `ChangePackageReason` | `PackageCreationReasonId` |
| `PackageCreationTemplate` | `BusinessProcessWorkflow` | `WorkflowId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `PackageCreationTemplate` | `Workflow` | `HAS_WORKFLOW` |
| `PackageCreationTemplate` | `Owner` | `HAS_PACKAGE_OWNER` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `PackageCreationTemplate` | `CDOTypeId` | `4` |
| `PackageCreationTemplate` | `PackageCreationTemplateId` | `1` |
| `PackageCreationTemplate` | `ChangeCount` | `4` |
| `PackageCreationTemplate` | `PackageCreationTemplateName` | `12` |


---

### 🟨 Module: `package_type` (5 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PackageType` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `PackageType` | `CDOTypeId` | `4` |
| `PackageType` | `PackageTypeName` | `12` |
| `PackageType` | `PackageTypeId` | `1` |
| `PackageType` | `ChangeCount` | `4` |


---

### 🟨 Module: `packaging` (3 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Box` (包装箱)
- `Pallet` (栈板)
- `PackingRule` (包装规则)


---

### 🟨 Module: `param` (9 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Param` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Param` | `ChangeStatus` | `ChangeHistoryId` |
| `Param` | `SetupAccess` | `SetupAccessId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ComputationParamSpec` | `Param` | `REFERENCES_PARAM` |
| `BizRuleParameter` | `Param` | `REFERENCES_PARAM` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `Param` | `ParamName` | `12` |
| `Param` | `ParamId` | `1` |
| `Param` | `CDOTypeId` | `4` |
| `Param` | `ChangeCount` | `4` |


---

### 🟨 Module: `part` (8 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `PartFamily` (设备资源族)
- `PartFamilyIdealCycle` (族理想节拍)
- `Part` (设备/工位资源)
- `PartIdealCycle` (设备理想节拍)
- `ResourceParam` (资源参数)
- `DowntimeSchedule` (停机排程)
- `PartEmployee` (设备操作员工)
- `PartPMStatus` (设备PM状态)


---

### 🟨 Module: `pause_reason` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `PauseReason` (暂停原因)


---

### 🟨 Module: `pause_reason_group` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `PauseReasonGroup` (暂停原因分组)


---

### 🟨 Module: `phase_template` (14 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `PhaseTemplate` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PhaseTemplate` | `SetupAccess` | `SetupAccessId` |
| `PhaseTemplate` | `RoleDef` | `AssigneeRoleId` |
| `PhaseTemplate` | `ChangeStatus` | `ChangeHistoryId` |
| `PhaseTemplate` | `Employee` | `AssigneeId` |
| `PhaseTemplate` | `DocumentSet` | `DocumentSetId` |
| `PhaseTemplate` | `Checklist` | `ChecklistId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `PhaseTemplate` | `ChecklistTemplate` | `HAS_CHECKLIST` |
| `PhaseTemplate` | `BusinessRule` | `HAS_ON_START_RULE` |
| `PhaseTemplate` | `BusinessRule` | `HAS_ON_COMPLETE_RULE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `PhaseTemplate` | `PhaseTemplateId` | `1` |
| `PhaseTemplate` | `CDOTypeId` | `4` |
| `PhaseTemplate` | `ChangeCount` | `4` |
| `PhaseTemplate` | `PhaseTemplateName` | `12` |


---

### 🟨 Module: `phase_template_disposition` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `PhaseTemplateDisposition` (处置阶段模板)


---

### 🟨 Module: `physical_location` (12 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `PhysicalLocation` | `SetupAccessId` | `` |
| `PhysicalLocationPosition` | `PhysicalLocationId` | `PhysicalLocation` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PhysicalLocation` | `ChangeStatus` | `ChangeHistoryId` |
| `PhysicalLocationPosition` | `PhysicalLocation` | `PhysicalLocationId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `PhysicalLocation` | `CDOTypeId` | `4` |
| `PhysicalLocation` | `PhysicalLocationId` | `1` |
| `PhysicalLocation` | `ChangeCount` | `4` |
| `PhysicalLocation` | `PhysicalLocationName` | `12` |
| `PhysicalLocationPosition` | `ExportImportKey` | `12` |
| `PhysicalLocationPosition` | `CDOTypeId` | `4` |
| `PhysicalLocationPosition` | `PhysicalLocationPositionId` | `1` |
| `PhysicalLocationPosition` | `ChangeCount` | `4` |


---

### 🟨 Module: `physical_position` (6 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `PhysicalPosition` | `SetupAccessId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PhysicalPosition` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `PhysicalPosition` | `PhysicalPositionName` | `12` |
| `PhysicalPosition` | `CDOTypeId` | `4` |
| `PhysicalPosition` | `ChangeCount` | `4` |
| `PhysicalPosition` | `PhysicalPositionId` | `1` |


---

### 🟨 Module: `plan_template` (14 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `PlanTemplate` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PlanTemplate` | `SetupAccess` | `SetupAccessId` |
| `PlanTemplate` | `RoleDef` | `AssigneeRoleId` |
| `PlanTemplate` | `ChangeStatus` | `ChangeHistoryId` |
| `PlanTemplate` | `Employee` | `AssigneeId` |
| `PlanTemplate` | `DocumentSet` | `DocumentSetId` |
| `PlanTemplate` | `Checklist` | `ChecklistId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `PlanTemplate` | `ChecklistTemplate` | `HAS_CHECKLIST` |
| `PlanTemplate` | `BusinessRule` | `HAS_ON_START_RULE` |
| `PlanTemplate` | `BusinessRule` | `HAS_ON_COMPLETE_RULE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `PlanTemplate` | `PlanTemplateId` | `1` |
| `PlanTemplate` | `CDOTypeId` | `4` |
| `PlanTemplate` | `ChangeCount` | `4` |
| `PlanTemplate` | `PlanTemplateName` | `12` |


---

### 🟨 Module: `plan_template_disposition` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `PlanTemplateDisposition` (处置计划模板)


---

### 🟨 Module: `print_queue` (6 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `PrintQueue` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PrintQueue` | `SetupAccess` | `SetupAccessId` |
| `PrintQueue` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 3

| Class | Field Name | Physical DataType |
|---|---|---|
| `PrintQueue` | `CDOTypeId` | `4` |
| `PrintQueue` | `ChangeCount` | `4` |
| `PrintQueue` | `PrintQueueName` | `12` |


---

### 🟨 Module: `printer_label_definition` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `PrinterLabelDefinition` | `PrinterLabelDefinitionBaseId` | `PrinterLabelDefinitionBase` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PrinterLabelDefinition` | `PrinterLabelDefinitionBase` | `PrinterLabelDefinitionBaseId` |
| `PrinterLabelDefinition` | `SetupAccess` | `SetupAccessId` |
| `PrinterLabelDefinition` | `ChangeStatus` | `ChangeHistoryId` |
| `PrinterLabelDefinition` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 3

| Class | Field Name | Physical DataType |
|---|---|---|
| `PrinterLabelDefinition` | `CDOTypeId` | `4` |
| `PrinterLabelDefinition` | `ChangeCount` | `4` |
| `PrinterLabelDefinition` | `PrinterLabelDefinitionId` | `1` |


---

### 🟨 Module: `priority_code` (11 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `PriorityCode` | `SetupAccessId` | `SetupAccess` |
| `PriorityCode` | `ChangeStatusId` | `ChangeStatus` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PriorityCode` | `SetupAccess` | `SetupAccessId` |
| `PriorityCode` | `ChangeStatus` | `ChangeStatusId` |
| `PriorityCode` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `PackageCreationTemplate` | `PriorityCode` | `HAS_PRIORITY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `PriorityCode` | `CDOTypeId` | `4` |
| `PriorityCode` | `PriorityCodeId` | `1` |
| `PriorityCode` | `PriorityCodeName` | `12` |
| `PriorityCode` | `RelativePriority` | `4` |
| `PriorityCode` | `ChangeCount` | `4` |


---

### 🟨 Module: `priority_level` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `PriorityLevel` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `PriorityLevel` | `SetupAccess` | `SetupAccessId` |
| `PriorityLevel` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `PriorityLevel` | `PriorityLevelName` | `12` |
| `PriorityLevel` | `CDOTypeId` | `4` |
| `PriorityLevel` | `PriorityLevelId` | `1` |
| `PriorityLevel` | `ChangeCount` | `4` |


---

### 🟨 Module: `process_list` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ProcessList` (流程任务清单)


---

### 🟨 Module: `process_model_template` (17 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ProcessModelTemplate` | `ProcessModelTemplateBaseId` | `ProcessModelTemplateBase` |
| `ProcessModelTemplate` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ProcessModelTemplate` | `SetupAccess` | `SetupAccessId` |
| `ProcessModelTemplate` | `Employee` | `AssigneeId` |
| `ProcessModelTemplate` | `RoleDef` | `AssigneeRoleId` |
| `ProcessModelTemplate` | `ChangeStatus` | `ChangeHistoryId` |
| `ProcessModelTemplate` | `DocumentSet` | `DocumentSetId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ProcessModelTemplate` | `BusinessRule` | `HAS_ON_START_RULE` |
| `ProcessModelTemplate` | `BusinessRule` | `HAS_ON_COMPLETE_RULE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `ProcessModelTemplate` | `ProcessModelTemplateId` | `1` |
| `ProcessModelTemplate` | `CDOTypeId` | `4` |
| `ProcessModelTemplate` | `ChangeCount` | `4` |
| `ProcessModelTemplate` | `Revision` | `12` |
| `ProcessModelTemplate` | `EffectiveFromDate` | `93` |
| `ProcessModelTemplate` | `EffectiveFromDateGMT` | `93` |
| `ProcessModelTemplate` | `EffectiveThruDate` | `93` |
| `ProcessModelTemplate` | `EffectiveThruDateGMT` | `93` |


---

### 🟨 Module: `process_object_template` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ProcessObjectTemplate` (流程对象模板)


---

### 🟨 Module: `process_timer` (13 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ProcessTimer` | `ProcessTimerBaseId` | `ProcessTimerBase` |
| `ProcessTimer` | `ProcessTimerTypeId` | `ProcessTimerType` |
| `ProcessTimer` | `ProcessTimerMinTimeDtlId` | `ProcessTimerDtl` |
| `ProcessTimer` | `ProcessTimerMaxTimeDtlId` | `ProcessTimerDtl` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ProcessTimer` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `ProcessTimer` | `ChangeStatus` | `ChangeHistoryId` |
| `ProcessTimer` | `ProcessTimerType` | `ProcessTimerTypeId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 6

| Class | Field Name | Physical DataType |
|---|---|---|
| `ProcessTimer` | `ProcessTimerId` | `1` |
| `ProcessTimer` | `CDOTypeId` | `4` |
| `ProcessTimer` | `MinWarningTime` | `8` |
| `ProcessTimer` | `MinWarningTimeColor` | `12` |
| `ProcessTimer` | `ChangeCount` | `4` |
| `ProcessTimer` | `TimerType` | `4` |


---

### 🟨 Module: `process_timer_type` (5 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ProcessTimerType` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ProcessTimerType` | `CDOTypeId` | `4` |
| `ProcessTimerType` | `ProcessTimerTypeId` | `1` |
| `ProcessTimerType` | `ChangeCount` | `4` |
| `ProcessTimerType` | `ProcessTimerTypeName` | `12` |


---

### 🟨 Module: `product_conversion_plan` (10 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ProductConversionPlan` | `StartProductId` | `Product` |
| `ProductConversionPlan` | `StartProductBaseId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ProductConversionPlan` | `ChangeStatus` | `ChangeHistoryId` |
| `ProductConversionPlan` | `SetupAccess` | `SetupAccessId` |
| `ProductConversionPlan` | `Product` | `StartProductId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `ProductConversionPlan` | `UseStartProductWorkflow` | `-7` |
| `ProductConversionPlan` | `CDOTypeId` | `4` |
| `ProductConversionPlan` | `ProductConversionPlanName` | `12` |
| `ProductConversionPlan` | `ProductConversionPlanId` | `1` |
| `ProductConversionPlan` | `ChangeCount` | `4` |


---

### 🟨 Module: `product_family` (10 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ProductFamily` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `ProductFamily` | `ChangeStatus` | `ChangeStatusId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `ProductFamily` | `ES_UniqueSerialNumbers` | `-7` |
| `ProductFamily` | `isRegisterContainers` | `4` |
| `ProductFamily` | `ES_UseContainerNameForSN` | `-7` |
| `ProductFamily` | `ES_UseProductionClientBoxMode` | `-7` |
| `ProductFamily` | `CDOTypeId` | `4` |
| `ProductFamily` | `ProductFamilyId` | `1` |
| `ProductFamily` | `ProductFamilyName` | `12` |
| `ProductFamily` | `ChangeCount` | `4` |


---

### 🟨 Module: `product_type` (9 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ProductType` | `SetupAccessId` | `SetupAccess` |
| `ProductType` | `ChangeStatusId` | `ChangeStatus` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ProductType` | `SetupAccess` | `SetupAccessId` |
| `ProductType` | `ChangeStatus` | `ChangeStatusId` |
| `ProductType` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ProductType` | `CDOTypeId` | `4` |
| `ProductType` | `ProductTypeId` | `1` |
| `ProductType` | `ProductTypeName` | `12` |
| `ProductType` | `ChangeCount` | `4` |


---

### 🟨 Module: `production_process` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ProductionProcess` (电子规程)


---

### 🟨 Module: `qty_adjust_reason` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `QtyAdjustReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `QtyAdjustReason` | `SetupAccess` | `SetupAccessId` |
| `QtyAdjustReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `QtyAdjustReason` | `CDOTypeId` | `4` |
| `QtyAdjustReason` | `QtyAdjustReasonName` | `12` |
| `QtyAdjustReason` | `QtyAdjustReasonId` | `1` |
| `QtyAdjustReason` | `ChangeCount` | `4` |


---

### 🟨 Module: `qty_adjust_reason_group` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `QtyAdjustReasonGroup` (数量调整原因分组)


---

### 🟨 Module: `quality` (157 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `NCRDefectData` | `ParentId` | `EventLot` |
| `NCRDefectData` | `ActualComponentIssueId` | `IssueActualsHistory` |
| `NonconformanceReport` | `PreventiveActionCommentsId` | `NCRComments` |
| `NonconformanceReport` | `CorrectiveActionCommentsId` | `NCRComments` |
| `NonconformanceReport` | `FailureInvestigationCommentsId` | `NCRComments` |
| `NonconformanceReport` | `ChargeToStepId` | `WorkflowStep` |
| `NonconformanceReport` | `ContainerId` | `Container` |
| `NonconformanceReport` | `NCRFailureTypeId` | `NCRFailureType` |
| `NonconformanceReport` | `NCRCauseCodeGroupId` | `NCRCauseCodeGroup` |
| `NonconformanceReport` | `NCRCauseCodeId` | `NCRCauseCode` |
| `NonconformanceReport` | `LastRevTxnId` | `` |
| `NonconformanceReport` | `TaskId` | `TaskItem` |
| `NonconformanceReport` | `EscalatedEventId` | `` |
| `NonconformanceReport` | `EscalatedById` | `Employee` |
| `HoldReason` | `SetupAccessId` | `SetupAccess` |
| `HoldReason` | `ChangeStatusId` | `ChangeStatus` |
| `CARSeverity` | `SetupAccessId` | `SetupAccess` |
| `Classification` | `SetupAccessId` | `SetupAccess` |
| `SubClassification` | `SetupAccessId` | `SetupAccess` |
| `CommentType` | `SetupAccessId` | `SetupAccess` |
| `DocAttachments` | `ParentId` | `` |
| `RiskAssessment` | `ParentId` | `` |
| `CAPACustomData` | `ParentId` | `` |
| `EventData` | `ReportFiledWithFDAId` | `EventCheckBoxFieldData` |
| `EventData` | `ReportSourceId` | `EventCheckBoxFieldData` |
| `EventData` | `EventTypeId` | `EventCheckBoxFieldData` |
| `EventData` | `AdverseEventId` | `EventCheckBoxFieldData` |
| `EventData` | `DeviceAvailableId` | `EventCheckBoxFieldData` |
| `EventData` | `DeviceEvaluatedId` | `EventCheckBoxFieldData` |
| `EventData` | `DeviceOperatorId` | `EventCheckBoxFieldData` |
| `EventData` | `DeviceReturnedId` | `EventCheckBoxFieldData` |
| `EventData` | `HealthProfessionalId` | `EventCheckBoxFieldData` |
| `EventData` | `ProductProblemId` | `EventCheckBoxFieldData` |
| `EventData` | `EventCustomDataId` | `EventCustomData` |
| `EventData` | `FailureInvestigationCommentsId` | `NCRComments` |
| `EventData` | `PreventiveActionCommentsId` | `NCRComments` |
| `EventData` | `CorrectiveActionCommentsId` | `NCRComments` |
| `ProcessModel` | `SetupAccessId` | `SetupAccess` |
| `ProcessModel` | `ParentId` | `` |
| `ProcessModel` | `DataPointCollectionId` | `DataPointCollection` |
| `Checklist` | `ParentId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `NCRDefectData` | `Container` | `ContainerId` |
| `NCRDefectData` | `Product` | `ProductId` |
| `NonconformanceReport` | `DocAttachments` | `AttachmentsId` |
| `NonconformanceReport` | `NonconformanceReport` | `RelatedNonconformanceId` |
| `NonconformanceReport` | `WorkflowStep` | `ChargeToStepId` |
| `NonconformanceReport` | `Container` | `ContainerId` |
| `NonconformanceReport` | `NCRFailureType` | `NCRFailureTypeId` |
| `NonconformanceReport` | `NCRCauseCodeGroup` | `NCRCauseCodeGroupId` |
| `NonconformanceReport` | `TaskItem` | `TaskId` |
| `NonconformanceReport` | `Employee` | `EscalatedById` |
| `CAPA` | `RoleDef` | `RoleId` |
| `HoldReason` | `SetupAccess` | `SetupAccessId` |
| `HoldReason` | `ChangeStatus` | `ChangeStatusId` |
| `HoldReason` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `CARSeverity` | `SetupAccess` | `SetupAccessId` |
| `CARSeverity` | `ChangeStatus` | `ChangeHistoryId` |
| `Classification` | `SetupAccess` | `SetupAccessId` |
| `Classification` | `ChangeStatus` | `ChangeHistoryId` |
| `SubClassification` | `SetupAccess` | `SetupAccessId` |
| `SubClassification` | `ChangeStatus` | `ChangeHistoryId` |
| `CommentType` | `SetupAccess` | `SetupAccessId` |
| `CommentType` | `ChangeStatus` | `ChangeHistoryId` |
| `Event` | `RoleDef` | `RoleId` |
| `ProcessModel` | `SetupAccess` | `SetupAccessId` |
| `ProcessModel` | `RoleDef` | `AssigneeRoleId` |
| `ProcessModel` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `NonconformanceReport` | `NCRDefectData` | `CONTAINS_DEFECT` |
| `CAPA` | `NonconformanceReport` | `RESOLVES_NCR` |
| `EventData` | `Customer` | `REPORTING_CUSTOMER` |
| `EventData` | `Customer` | `CONTACT_CUSTOMER` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 86

| Class | Field Name | Physical DataType |
|---|---|---|
| `NCRDefectData` | `CDOTypeId` | `4` |
| `NCRDefectData` | `ChangeCount` | `4` |
| `NCRDefectData` | `ExportImportKey` | `12` |
| `NonconformanceReport` | `CloseDateGMT` | `93` |
| `NonconformanceReport` | `CreationDateGMT` | `93` |
| `NonconformanceReport` | `CDOTypeId` | `4` |
| `NonconformanceReport` | `ChangeCount` | `4` |
| `NonconformanceReport` | `NonconformanceReportName` | `12` |
| `NonconformanceReport` | `EscalationDate` | `93` |
| `NonconformanceReport` | `EscalationDateGMT` | `93` |
| ... and 76 more | | |


---

### 🟨 Module: `quality_resolution_code` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `QualityResolutionCode` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `QualityResolutionCode` | `SetupAccess` | `SetupAccessId` |
| `QualityResolutionCode` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `QualityResolutionCode` | `QualityResolutionCodeId` | `1` |
| `QualityResolutionCode` | `CDOTypeId` | `4` |
| `QualityResolutionCode` | `ChangeCount` | `4` |
| `QualityResolutionCode` | `QualityResolutionCodeName` | `12` |


---

### 🟨 Module: `recipe` (2 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Recipe` (设备配方)
- `RecipeParameter` (配方参数)


---

### 🟨 Module: `recipe_list` (5 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `RecipeList` | `CDOTypeId` | `4` |
| `RecipeList` | `RecipeListId` | `1` |
| `RecipeList` | `ChangeCount` | `4` |
| `RecipeList` | `ECO` | `12` |
| `RecipeList` | `TargetContainerPlannedQty` | `12` |


---

### 🟨 Module: `recurring_date_req` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `RecurringDateReq` (周期性维护要求)


---

### 🟨 Module: `regulatory_agency` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `RegulatoryAgency` | `SetupAccessId` | `SetupAccess` |
| `RegulatoryAgency` | `DecisionTreePageFlowId` | `UIPageFlow` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `RegulatoryAgency` | `SetupAccess` | `SetupAccessId` |
| `RegulatoryAgency` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `RegulatoryAgency` | `RegulatoryAgencyName` | `12` |
| `RegulatoryAgency` | `ChangeCount` | `4` |
| `RegulatoryAgency` | `CDOTypeId` | `4` |
| `RegulatoryAgency` | `RegulatoryAgencyId` | `1` |


---

### 🟨 Module: `regulatory_report_type` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `RegulatoryReportType` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `RegulatoryReportType` | `SetupAccess` | `SetupAccessId` |
| `RegulatoryReportType` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `RegulatoryReportType` | `ChangeCount` | `4` |
| `RegulatoryReportType` | `RegulatoryReportTypeId` | `1` |
| `RegulatoryReportType` | `RegulatoryReportTypeName` | `12` |
| `RegulatoryReportType` | `CDOTypeId` | `4` |


---

### 🟨 Module: `release_reason` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ReleaseReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ReleaseReason` | `SetupAccess` | `SetupAccessId` |
| `ReleaseReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ReleaseReason` | `ReleaseReasonName` | `12` |
| `ReleaseReason` | `ChangeCount` | `4` |
| `ReleaseReason` | `CDOTypeId` | `4` |
| `ReleaseReason` | `ReleaseReasonId` | `1` |


---

### 🟨 Module: `removal_reason` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `RemovalReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `RemovalReason` | `SetupAccess` | `SetupAccessId` |
| `RemovalReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `RemovalReason` | `RemovalType` | `4` |
| `RemovalReason` | `RemovalReasonId` | `1` |
| `RemovalReason` | `ChangeCount` | `4` |
| `RemovalReason` | `RemovalReasonName` | `12` |
| `RemovalReason` | `CDOTypeId` | `4` |


---

### 🟨 Module: `remove_difference_reason` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `RemoveDifferenceReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `RemoveDifferenceReason` | `SetupAccess` | `SetupAccessId` |
| `RemoveDifferenceReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `RemoveDifferenceReason` | `RemoveDifferenceReasonId` | `1` |
| `RemoveDifferenceReason` | `ChangeCount` | `4` |
| `RemoveDifferenceReason` | `RemoveDifferenceReasonName` | `12` |
| `RemoveDifferenceReason` | `CDOTypeId` | `4` |


---

### 🟨 Module: `replace_reason` (6 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ReplaceReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `ReplaceReason` | `CDOTypeId` | `4` |
| `ReplaceReason` | `ReplaceReasonId` | `1` |
| `ReplaceReason` | `ChangeCount` | `4` |
| `ReplaceReason` | `ReplaceReasonName` | `12` |
| `ReplaceReason` | `IsScrapRemoved` | `-7` |


---

### 🟨 Module: `res_status_code_group` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ResStatusCodeGroup` (资源状态代码分组)


---

### 🟨 Module: `res_status_reason_group` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResStatusReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResStatusReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `ResStatusReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResStatusReasonGroup` | `ResStatusReasonGroupName` | `12` |
| `ResStatusReasonGroup` | `ResStatusReasonGroupId` | `1` |
| `ResStatusReasonGroup` | `CDOTypeId` | `4` |
| `ResStatusReasonGroup` | `ChangeCount` | `4` |


---

### 🟨 Module: `resource` (4 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Resource` (设备资源)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResourceLogs` | `LogsId` | `` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ResourceLogs` | `UOM` | `USES_UOM` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 1

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceLogs` | `FieldId` | `4` |


---

### 🟨 Module: `resource_bom` (10 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResourceBOM` | `ResourceBOMBaseId` | `ResourceBOMBase` |
| `ResourceBOM` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResourceBOM` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `ResourceBOM` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ResourceBOM` | `ProductType` | `HAS_DEFAULT_TYPE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceBOM` | `ECO` | `12` |
| `ResourceBOM` | `CDOTypeId` | `4` |
| `ResourceBOM` | `ResourceBOMId` | `1` |
| `ResourceBOM` | `ChangeCount` | `4` |
| `ResourceBOM` | `Status` | `4` |


---

### 🟨 Module: `resource_family` (39 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResourceFamily` | `SetupAccessId` | `SetupAccess` |
| `ResourceFamily` | `JobNotificationEmailGroupId` | `EmailGroup` |
| `ResourceFamily` | `isOEESettingsId` | `isOEESettings` |
| `ResourceFamily` | `isProductId` | `Product` |
| `ResourceFamily` | `isMfgOrderId` | `MfgOrder` |
| `ResourceFamily` | `isTrainingReqGroupId` | `TrainingRequirementGroup` |
| `ResourceFamily` | `isPrintQueueId` | `PrintQueue` |
| `ResourceFamily` | `isVendorId` | `Vendor` |
| `ResourceFamily` | `ResourceStatusModelId` | `ResourceStatusModel` |
| `ResourceFamily` | `UIPreferenceId` | `UIPreference` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResourceFamily` | `SetupAccess` | `SetupAccessId` |
| `ResourceFamily` | `EmailGroup` | `JobNotificationEmailGroupId` |
| `ResourceFamily` | `isOEESettings` | `isOEESettingsId` |
| `ResourceFamily` | `Product` | `isProductId` |
| `ResourceFamily` | `MfgOrder` | `isMfgOrderId` |
| `ResourceFamily` | `TrainingRequirementGroup` | `isTrainingReqGroupId` |
| `ResourceFamily` | `PrintQueue` | `isPrintQueueId` |
| `ResourceFamily` | `Vendor` | `isVendorId` |
| `ResourceFamily` | `ChangeStatus` | `ChangeHistoryId` |
| `ResourceFamily` | `ResourceStatusModel` | `ResourceStatusModelId` |
| `ResourceFamily` | `UIPreference` | `UIPreferenceId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 18

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceFamily` | `ObjectCategory` | `12` |
| `ResourceFamily` | `ObjectType` | `12` |
| `ResourceFamily` | `isCarrierThruputRecordingMode` | `4` |
| `ResourceFamily` | `isReuseTrackingContainer` | `-7` |
| `ResourceFamily` | `isUsePosition` | `4` |
| `ResourceFamily` | `isSingleMfgOrder` | `4` |
| `ResourceFamily` | `isSingleProduct` | `4` |
| `ResourceFamily` | `isVendorSerialNumber` | `12` |
| `ResourceFamily` | `isVendorModel` | `12` |
| `ResourceFamily` | `ResourceFamilyName` | `12` |
| ... and 8 more | | |


---

### 🟨 Module: `resource_group` (9 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResourceGroup` | `SetupAccess` | `SetupAccessId` |
| `ResourceGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 7

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceGroup` | `ObjectCategory` | `12` |
| `ResourceGroup` | `ObjectType` | `12` |
| `ResourceGroup` | `isSMTResources` | `-7` |
| `ResourceGroup` | `ResourceGroupName` | `12` |
| `ResourceGroup` | `ResourceGroupId` | `1` |
| `ResourceGroup` | `ChangeCount` | `4` |
| `ResourceGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `resource_layout` (8 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResourceLayout` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 7

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceLayout` | `LayoutHeight` | `4` |
| `ResourceLayout` | `ResourceLayoutId` | `1` |
| `ResourceLayout` | `ChangeCount` | `4` |
| `ResourceLayout` | `ResourceLayoutName` | `12` |
| `ResourceLayout` | `CDOTypeId` | `4` |
| `ResourceLayout` | `LayoutWidth` | `4` |
| `ResourceLayout` | `BackgroundFilename` | `12` |


---

### 🟨 Module: `resource_material_part` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ResourceMaterialPart` (资源物料部件)


---

### 🟨 Module: `resource_status_code` (18 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResourceStatusCode` | `SetupAccessId` | `SetupAccess` |
| `ResourceStatusCode` | `ResourceStatusReasonsId` | `ResStatusReasonGroup` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResourceStatusCode` | `SetupAccess` | `SetupAccessId` |
| `ResourceStatusCode` | `ChangeStatus` | `ChangeHistoryId` |
| `ResourceStatusCode` | `ResStatusReasonGroup` | `ResourceStatusReasonsId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 13

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceStatusCode` | `isOrder` | `4` |
| `ResourceStatusCode` | `isOEELossCategory` | `4` |
| `ResourceStatusCode` | `CDOTypeId` | `4` |
| `ResourceStatusCode` | `NextTxnType` | `4` |
| `ResourceStatusCode` | `ResourceStatusCodeId` | `1` |
| `ResourceStatusCode` | `ChangeCount` | `4` |
| `ResourceStatusCode` | `ResourceStatusCodeName` | `12` |
| `ResourceStatusCode` | `ResourceState` | `4` |
| `ResourceStatusCode` | `Availability` | `4` |
| `ResourceStatusCode` | `ResourceCDOTypeName` | `12` |
| ... and 3 more | | |


---

### 🟨 Module: `resource_status_model` (5 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResourceStatusModel` | `InitStatusCodesId` | `ResourceStatusCodeGroup` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResourceStatusModel` | `SetupAccess` | `SetupAccessId` |
| `ResourceStatusModel` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 2

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceStatusModel` | `ResourceStatusModelName` | `12` |
| `ResourceStatusModel` | `ResourceStatusModelId` | `1` |


---

### 🟨 Module: `resource_status_reason` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResourceStatusReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResourceStatusReason` | `SetupAccess` | `SetupAccessId` |
| `ResourceStatusReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceStatusReason` | `CDOTypeId` | `4` |
| `ResourceStatusReason` | `ResourceStatusReasonName` | `12` |
| `ResourceStatusReason` | `ResourceStatusReasonId` | `1` |
| `ResourceStatusReason` | `ChangeCount` | `4` |
| `ResourceStatusReason` | `ResourceCDOTypeName` | `12` |


---

### 🟨 Module: `resource_type` (11 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResourceType` | `SetupAccessId` | `SetupAccess` |
| `ResourceType` | `ResourceStatusModelId` | `ResourceStatusModel` |
| `ResourceType` | `UIPreferenceId` | `UIPreference` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ResourceType` | `SetupAccess` | `SetupAccessId` |
| `ResourceType` | `ResourceStatusModel` | `ResourceStatusModelId` |
| `ResourceType` | `ChangeStatus` | `ChangeHistoryId` |
| `ResourceType` | `UIPreference` | `UIPreferenceId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResourceType` | `ResourceTypeId` | `1` |
| `ResourceType` | `ChangeCount` | `4` |
| `ResourceType` | `ResourceTypeName` | `12` |
| `ResourceType` | `CDOTypeId` | `4` |


---

### 🟨 Module: `response_set` (5 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ResponseSet` | `SetupAccessId` | `SetupAccess` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ResponseSet` | `ResponseSetId` | `1` |
| `ResponseSet` | `CDOTypeId` | `4` |
| `ResponseSet` | `ChangeCount` | `4` |
| `ResponseSet` | `ResponseSetName` | `12` |


---

### 🟨 Module: `returned_equipment_action` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ReturnedEquipmentAction` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ReturnedEquipmentAction` | `SetupAccess` | `SetupAccessId` |
| `ReturnedEquipmentAction` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ReturnedEquipmentAction` | `ReturnedEquipmentActionName` | `12` |
| `ReturnedEquipmentAction` | `CDOTypeId` | `4` |
| `ReturnedEquipmentAction` | `ReturnedEquipmentActionId` | `1` |
| `ReturnedEquipmentAction` | `ChangeCount` | `4` |


---

### 🟨 Module: `rework` (25 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ReworkPath` (返工工艺路线)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ReworkReason` | `SetupAccessId` | `SetupAccess` |
| `ReworkReason` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |
| `ReworkStatus` | `CurrentStatusId` | `CurrentStatus` |
| `ReworkStatus` | `LastRevTxnId` | `` |
| `ReworkStatus` | `ReEntryStepId` | `WorkflowStep` |
| `ReworkStatus` | `ReworkReasonId` | `ReworkReason` |
| `ReworkStatus` | `EndReworkStepId` | `WorkflowStep` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ReworkReason` | `SetupAccess` | `SetupAccessId` |
| `ReworkReason` | `ChangeStatus` | `ChangeHistoryId` |
| `ReworkReason` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `ReworkStatus` | `WorkflowStep` | `ReEntryStepId` |
| `ReworkStatus` | `ReworkReason` | `ReworkReasonId` |
| `ReworkStatus` | `WorkflowStep` | `EndReworkStepId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Container` | `ReworkStatus` | `HAS_REWORK_STATUS` |
| `Container` | `ReworkReason` | `REWORKED_DUE_TO` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 9

| Class | Field Name | Physical DataType |
|---|---|---|
| `ReworkReason` | `CDOTypeId` | `4` |
| `ReworkReason` | `ReworkReasonId` | `1` |
| `ReworkReason` | `IconId` | `4` |
| `ReworkReason` | `ReworkReasonName` | `12` |
| `ReworkReason` | `ChangeCount` | `4` |
| `ReworkStatus` | `CDOTypeId` | `4` |
| `ReworkStatus` | `ReworkStatusId` | `1` |
| `ReworkStatus` | `ChangeCount` | `4` |
| `ReworkStatus` | `ExportImportKey` | `12` |


---

### 🟨 Module: `rework_reason` (10 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ReworkReason` | `SetupAccessId` | `SetupAccess` |
| `ReworkReason` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ReworkReason` | `SetupAccess` | `SetupAccessId` |
| `ReworkReason` | `ChangeStatus` | `ChangeHistoryId` |
| `ReworkReason` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ReworkReasonGroup` | `ReworkReason` | `HAS_ENTRY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ReworkReason` | `CDOTypeId` | `4` |
| `ReworkReason` | `ReworkReasonId` | `1` |
| `ReworkReason` | `ReworkReasonName` | `12` |
| `ReworkReason` | `ChangeCount` | `4` |


---

### 🟨 Module: `rework_reason_group` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ReworkReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ReworkReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `ReworkReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ReworkReasonGroup` | `ReworkReason` | `HAS_ENTRY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ReworkReasonGroup` | `ReworkReasonGroupId` | `1` |
| `ReworkReasonGroup` | `ReworkReasonGroupName` | `12` |
| `ReworkReasonGroup` | `ChangeCount` | `4` |
| `ReworkReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `role` (4 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `RoleDef` | `RoleName` | `12` |
| `RoleDef` | `CDOTypeId` | `4` |
| `RoleDef` | `RoleId` | `1` |
| `RoleDef` | `ChangeCount` | `4` |


---

### 🟨 Module: `role_permissions` (5 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 5

| Class | Field Name | Physical DataType |
|---|---|---|
| `RolePermission` | `CDOTypeId` | `4` |
| `RolePermission` | `RolePermissionId` | `1` |
| `RolePermission` | `ChangeCount` | `4` |
| `RolePermission` | `RolePermissionName` | `12` |
| `RolePermission` | `ExportImportKey` | `12` |


---

### 🟨 Module: `rollup_reason` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `RollupReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `RollupReason` | `SetupAccess` | `SetupAccessId` |
| `RollupReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `RollupReasonGroup` | `RollupReason` | `HAS_ENTRY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `RollupReason` | `ChangeCount` | `4` |
| `RollupReason` | `RollupReasonName` | `12` |
| `RollupReason` | `RollupReasonId` | `1` |
| `RollupReason` | `CDOTypeId` | `4` |


---

### 🟨 Module: `rollup_reason_group` (9 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `RollupReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `RollupReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `RollupReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `RollupReasonGroup` | `RollupReason` | `HAS_ENTRY` |
| `RollupReasonGroup` | `RollupReasonGroup` | `HAS_SUBGROUP` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `RollupReasonGroup` | `RollupReasonGroupId` | `1` |
| `RollupReasonGroup` | `ChangeCount` | `4` |
| `RollupReasonGroup` | `RollupReasonGroupName` | `12` |
| `RollupReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `salesorder` (12 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `SalesOrder` | `SetupAccessId` | `SetupAccess` |
| `SalesOrder` | `ChangeStatusId` | `ChangeStatus` |
| `SalesOrder` | `ProductBaseId` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `SalesOrder` | `SetupAccess` | `SetupAccessId` |
| `SalesOrder` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `SalesOrder` | `ChangeStatus` | `ChangeStatusId` |
| `SalesOrder` | `UOM` | `UOM2Id` |
| `SalesOrder` | `UOM` | `UOMId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `SalesOrder` | `CDOTypeId` | `4` |
| `SalesOrder` | `SalesOrderId` | `1` |
| `SalesOrder` | `SalesOrderName` | `12` |
| `SalesOrder` | `ChangeCount` | `4` |


---

### 🟨 Module: `sampling` (35 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `SamplingPlanDetails` | `SpecBase` | `HAS_SPEC_BASE` |
| `SamplingPlanDetails` | `SampleTestBase` | `HAS_BASE_VERSION` |
| `SamplingPlanDetails` | `SwitchingRuleBase` | `HAS_SWITCHING_RULE_BASE` |
| `SamplingPlan` | `SpecBase` | `HAS_SPEC_BASE` |
| `SamplingPlan` | `SwitchingRuleBase` | `HAS_SWITCHING_RULE_BASE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 30

| Class | Field Name | Physical DataType |
|---|---|---|
| `SamplingPlan` | `SamplingPlanId` | `1` |
| `SamplingPlan` | `CDOTypeId` | `4` |
| `SamplingPlan` | `ChangeCount` | `4` |
| `SamplingPlan` | `IconId` | `4` |
| `SamplingPlan` | `SampleSizeBasedOnStartQty` | `-7` |
| `SamplingPlanDetails` | `Sequence` | `4` |
| `SamplingPlanDetails` | `SamplingPlanDetailsId` | `1` |
| `SamplingPlanDetails` | `CDOTypeId` | `4` |
| `SamplingPlanDetails` | `ChangeCount` | `4` |
| `SamplingPlanDetails` | `InspectAll` | `-7` |
| ... and 20 more | | |


---

### 🟨 Module: `scale` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Scale` (称重设备)


---

### 🟨 Module: `scale_group` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ScaleGroup` (称重组)


---

### 🟨 Module: `scale_status_code` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ScaleStatusCode` (称重设备状态代码)


---

### 🟨 Module: `scale_status_reason` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ScaleStatusReason` (称重设备状态变更原因)


---

### 🟨 Module: `scheduled_business_rule` (33 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ScheduledBusinessRule` | `SetupAccessId` | `SetupAccess` |
| `ScheduledBusinessRule` | `OnExecute` | `BusinessRule` |
| `ScheduledBusinessRule` | `ExecutionContext` | `` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ScheduledBusinessRule` | `SetupAccess` | `SetupAccessId` |
| `ScheduledBusinessRule` | `BusinessRule` | `OnExecute` |
| `ScheduledBusinessRule` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 27

| Class | Field Name | Physical DataType |
|---|---|---|
| `ScheduledBusinessRule` | `LockGUID` | `12` |
| `ScheduledBusinessRule` | `DayOfMonth` | `4` |
| `ScheduledBusinessRule` | `ScheduledBusinessRuleName` | `12` |
| `ScheduledBusinessRule` | `DueTime` | `93` |
| `ScheduledBusinessRule` | `DueTimeGMT` | `93` |
| `ScheduledBusinessRule` | `RecurrencePattern` | `4` |
| `ScheduledBusinessRule` | `RecurrenceFrequency` | `4` |
| `ScheduledBusinessRule` | `DayOfWeek` | `4` |
| `ScheduledBusinessRule` | `MonthOfYear` | `4` |
| `ScheduledBusinessRule` | `IsLastDayOfMonth` | `-7` |
| ... and 17 more | | |


---

### 🟨 Module: `scheduling_route` (13 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `SchedulingRoute` | `SchedulingRouteBaseId` | `SchedulingRouteBase` |
| `SchedulingRoute` | `SetupAccessId` | `SetupAccess` |
| `SchedulingRoute` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `SchedulingRoute` | `SetupAccess` | `SetupAccessId` |
| `SchedulingRoute` | `ChangeStatus` | `ChangeHistoryId` |
| `SchedulingRoute` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 7

| Class | Field Name | Physical DataType |
|---|---|---|
| `SchedulingRoute` | `CDOTypeId` | `4` |
| `SchedulingRoute` | `SchedulingRouteId` | `1` |
| `SchedulingRoute` | `ChangeCount` | `4` |
| `SchedulingRoute` | `ECO` | `12` |
| `SchedulingRoute` | `Revision` | `12` |
| `SchedulingRoute` | `Status` | `4` |
| `SchedulingRoute` | `ERPItem` | `12` |


---

### 🟨 Module: `scrap` (11 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `CostCenter` (成本中心)
- `ScrapLog` (报废核算记录)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ScrapReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ScrapReason` | `SetupAccess` | `SetupAccessId` |
| `ScrapReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 6

| Class | Field Name | Physical DataType |
|---|---|---|
| `ScrapReason` | `CDOTypeId` | `4` |
| `ScrapReason` | `ScrapReasonId` | `1` |
| `ScrapReason` | `ChangeCount` | `4` |
| `ScrapReason` | `Description` | `12` |
| `ScrapReason` | `IconId` | `4` |
| `ScrapReason` | `ScrapReasonName` | `12` |


---

### 🟨 Module: `scrap_reason` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ScrapReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ScrapReason` | `SetupAccess` | `SetupAccessId` |
| `ScrapReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ScrapReason` | `CDOTypeId` | `4` |
| `ScrapReason` | `ScrapReasonId` | `1` |
| `ScrapReason` | `ChangeCount` | `4` |
| `ScrapReason` | `ScrapReasonName` | `12` |


---

### 🟨 Module: `sell_reason` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `SellReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `SellReason` | `SetupAccess` | `SetupAccessId` |
| `SellReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `SellReasonGroup` | `SellReason` | `HAS_ENTRY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `SellReason` | `CDOTypeId` | `4` |
| `SellReason` | `SellReasonId` | `1` |
| `SellReason` | `SellReasonName` | `12` |
| `SellReason` | `ChangeCount` | `4` |


---

### 🟨 Module: `sell_reason_group` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `SellReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `SellReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `SellReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `SellReasonGroup` | `SellReason` | `HAS_ENTRY` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `SellReasonGroup` | `SellReasonGroupId` | `1` |
| `SellReasonGroup` | `ChangeCount` | `4` |
| `SellReasonGroup` | `SellReasonGroupName` | `12` |
| `SellReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `setup` (14 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Setup` | `SetupBaseId` | `SetupBase` |
| `Setup` | `SetupAccessId` | `SetupAccess` |
| `Setup` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Setup` | `SetupAccess` | `SetupAccessId` |
| `Setup` | `ChangeStatus` | `ChangeHistoryId` |
| `Setup` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `Setup` | `CDOTypeId` | `4` |
| `Setup` | `SetupId` | `1` |
| `Setup` | `Status` | `4` |
| `Setup` | `SetupRevision` | `12` |
| `Setup` | `StdSetupLaborTime` | `8` |
| `Setup` | `StdSetupTime` | `8` |
| `Setup` | `ChangeCount` | `4` |
| `Setup` | `ECO` | `12` |


---

### 🟨 Module: `setup_access` (5 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `SetupAccess` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `SetupAccess` | `ChangeCount` | `4` |
| `SetupAccess` | `CDOTypeId` | `4` |
| `SetupAccess` | `SetupAccessName` | `12` |
| `SetupAccess` | `SetupAccessRefId` | `1` |


---

### 🟨 Module: `setup_maint` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `SetupMaint` (换线维护)


---

### 🟨 Module: `shift` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Shift` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Shift` | `SetupAccess` | `SetupAccessId` |
| `Shift` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `Shift` | `ShiftId` | `1` |
| `Shift` | `ShiftName` | `12` |
| `Shift` | `ChangeCount` | `4` |
| `Shift` | `CDOTypeId` | `4` |


---

### 🟨 Module: `shipment_destination` (15 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ShipmentDestination` | `SetupAccessId` | `SetupAccess` |
| `ShipmentDestination` | `FactoryId` | `Factory` |
| `ShipmentDestination` | `LocationId` | `Location` |
| `ShipmentDestination` | `CustomerId` | `Customer` |
| `ShipmentDestination` | `RemoteSiteId` | `Site` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ShipmentDestination` | `SetupAccess` | `SetupAccessId` |
| `ShipmentDestination` | `Factory` | `FactoryId` |
| `ShipmentDestination` | `ChangeStatus` | `ChangeHistoryId` |
| `ShipmentDestination` | `Site` | `RemoteSiteId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 6

| Class | Field Name | Physical DataType |
|---|---|---|
| `ShipmentDestination` | `CDOTypeId` | `4` |
| `ShipmentDestination` | `ShipmentDestinationName` | `12` |
| `ShipmentDestination` | `ChangeCount` | `4` |
| `ShipmentDestination` | `RemoteContainerStatus` | `4` |
| `ShipmentDestination` | `ShipmentDestinationId` | `1` |
| `ShipmentDestination` | `LocalContainerStatus` | `4` |


---

### 🟨 Module: `shipment_destination_group` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ShipmentDestinationGrp` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ShipmentDestinationGrp` | `SetupAccess` | `SetupAccessId` |
| `ShipmentDestinationGrp` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ShipmentDestinationGrp` | `ShipmentDestinationGrpName` | `12` |
| `ShipmentDestinationGrp` | `CDOTypeId` | `4` |
| `ShipmentDestinationGrp` | `ShipmentDestinationGrpId` | `1` |
| `ShipmentDestinationGrp` | `ChangeCount` | `4` |


---

### 🟨 Module: `shipping_reason` (11 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ShippingReason` | `SetupAccessId` | `SetupAccess` |
| `ShippingReason` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ShippingReason` | `SetupAccess` | `SetupAccessId` |
| `ShippingReason` | `ChangeStatus` | `ChangeHistoryId` |
| `ShippingReason` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ShippingReasonGroup` | `ShippingReason` | `HAS_ENTRY` |
| `Container` | `ShippingReason` | `SHIPPED_DUE_TO` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ShippingReason` | `CDOTypeId` | `4` |
| `ShippingReason` | `ShippingReasonId` | `1` |
| `ShippingReason` | `ShippingReasonName` | `12` |
| `ShippingReason` | `ChangeCount` | `4` |


---

### 🟨 Module: `shipping_reason_group` (9 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ShippingReasonGroup` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ShippingReasonGroup` | `SetupAccess` | `SetupAccessId` |
| `ShippingReasonGroup` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `ShippingReasonGroup` | `ShippingReason` | `HAS_ENTRY` |
| `ShippingReasonGroup` | `ShippingReasonGroup` | `HAS_SUBGROUP` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ShippingReasonGroup` | `ShippingReasonGroupId` | `1` |
| `ShippingReasonGroup` | `ChangeCount` | `4` |
| `ShippingReasonGroup` | `ShippingReasonGroupName` | `12` |
| `ShippingReasonGroup` | `CDOTypeId` | `4` |


---

### 🟨 Module: `spec` (88 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Spec` | `SpecParams` | `HAS_PARAMETER` |
| `Spec` | `ESigReqTxnMap` | `HAS_ESIG_MAP` |
| `Spec` | `BPSpecBizRuleTxnMap` | `HAS_BIZ_RULE_MAP` |
| `SpecParams` | `Spec` | `BELONGS_TO_SPEC` |
| `ESigReqTxnMap` | `Spec` | `BELONGS_TO_SPEC` |
| `BPSpecBizRuleTxnMap` | `Spec` | `BELONGS_TO_SPEC` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 82

| Class | Field Name | Physical DataType |
|---|---|---|
| `Spec` | `AutoComponentIssue` | `-7` |
| `Spec` | `AutoClose` | `-7` |
| `Spec` | `VerifyMfgLine` | `-7` |
| `Spec` | `VerifyYieldLimits` | `-7` |
| `Spec` | `AutoDisassociate` | `-7` |
| `Spec` | `RecordTDADetailsHistory` | `-7` |
| `Spec` | `ES_CloseParentContainers` | `-7` |
| `Spec` | `ES_AutoOpenInstructions` | `-7` |
| `Spec` | `isRecordCarrierThruput` | `-7` |
| `Spec` | `isValidateCarrierMaintenance` | `-7` |
| ... and 72 more | | |


---

### 🟨 Module: `start_reasons` (10 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `StartReason` | `SetupAccessId` | `SetupAccess` |
| `StartReason` | `ChangeStatusId` | `ChangeStatus` |
| `StartReason` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `StartReason` | `SetupAccess` | `SetupAccessId` |
| `StartReason` | `ChangeStatus` | `ChangeStatusId` |
| `StartReason` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `StartReason` | `CDOTypeId` | `4` |
| `StartReason` | `StartReasonId` | `1` |
| `StartReason` | `StartReasonName` | `12` |
| `StartReason` | `ChangeCount` | `4` |


---

### 🟨 Module: `substitution_reason` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `SubstitutionReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `SubstitutionReason` | `SetupAccess` | `SetupAccessId` |
| `SubstitutionReason` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `SubstitutionReason` | `ChangeCount` | `4` |
| `SubstitutionReason` | `SubstitutionReasonId` | `1` |
| `SubstitutionReason` | `SubstitutionReasonName` | `12` |
| `SubstitutionReason` | `CDOTypeId` | `4` |


---

### 🟨 Module: `supplier` (11 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `VendorMaterial` (供应商物料映射)
- `ReceivingLog` (收货入库记录)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Vendor` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Vendor` | `SetupAccess` | `SetupAccessId` |
| `Vendor` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 6

| Class | Field Name | Physical DataType |
|---|---|---|
| `Vendor` | `IconId` | `4` |
| `Vendor` | `Description` | `12` |
| `Vendor` | `VendorId` | `1` |
| `Vendor` | `VendorName` | `12` |
| `Vendor` | `ChangeCount` | `4` |
| `Vendor` | `CDOTypeId` | `4` |


---

### 🟨 Module: `switching_rules` (20 issues/warnings)

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 20

| Class | Field Name | Physical DataType |
|---|---|---|
| `SwitchingRule` | `ChangeCount` | `4` |
| `SwitchingRule` | `IconId` | `4` |
| `SwitchingRule` | `CDOTypeId` | `4` |
| `SwitchingRule` | `SwitchingRuleId` | `1` |
| `SwitchingRuleDetails` | `SwitchingRuleDetailsId` | `1` |
| `SwitchingRuleDetails` | `CDOTypeId` | `4` |
| `SwitchingRuleDetails` | `ChangeCount` | `4` |
| `SwitchingRuleDetails` | `ExportImportKey` | `12` |
| `EMailDistribution` | `EMailDistributionName` | `12` |
| `EMailDistribution` | `IconId` | `4` |
| ... and 10 more | | |


---

### 🟨 Module: `task_list` (16 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `TaskList` | `TaskListBaseId` | `TaskListBase` |
| `TaskList` | `SetupAccessId` | `SetupAccess` |
| `TaskList` | `PrerequisiteTaskListId` | `TaskList` |
| `TaskList` | `WorkstationId` | `ResourceDef` |
| `TaskList` | `WorkstationGroupId` | `ResourceGroup` |
| `TaskList` | `WIPMsgDefMgrId` | `WIPMsgDefMgr` |
| `TaskList` | `isImageId` | `isImage` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 9

| Class | Field Name | Physical DataType |
|---|---|---|
| `TaskList` | `CDOTypeId` | `4` |
| `TaskList` | `TaskListId` | `1` |
| `TaskList` | `ChangeCount` | `4` |
| `TaskList` | `IconId` | `4` |
| `TaskList` | `ECO` | `12` |
| `TaskList` | `ExecutionMode` | `4` |
| `TaskList` | `TaskListRevision` | `12` |
| `TaskList` | `Status` | `4` |
| `TaskList` | `ReportInstruction` | `12` |


---

### 🟨 Module: `tda` (13 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `TDA` | `DocumentSetId` | `DocumentSet` |
| `TDA` | `SetupAccessId` | `SetupAccess` |
| `TDA` | `ReasonId` | `TDAReason` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `TDA` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 9

| Class | Field Name | Physical DataType |
|---|---|---|
| `TDA` | `EffectiveThruDate` | `93` |
| `TDA` | `EffectiveFromDate` | `93` |
| `TDA` | `TDAName` | `12` |
| `TDA` | `CDOTypeId` | `4` |
| `TDA` | `TDAId` | `1` |
| `TDA` | `EffectiveThruDateGMT` | `93` |
| `TDA` | `Status` | `4` |
| `TDA` | `EffectiveFromDateGMT` | `93` |
| `TDA` | `ChangeCount` | `4` |


---

### 🟨 Module: `tda_maint` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `TDAMaint` (培训需求维护)


---

### 🟨 Module: `tda_reason` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `TDAReason` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `TDAReason` | `ChangeStatus` | `ChangeHistoryId` |
| `TDAReason` | `SetupAccess` | `SetupAccessId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `TDAReason` | `ChangeCount` | `4` |
| `TDAReason` | `TDAReasonId` | `1` |
| `TDAReason` | `CDOTypeId` | `4` |
| `TDAReason` | `TDAReasonName` | `12` |


---

### 🟨 Module: `team` (8 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `Team` | `SetupAccessId` | `SetupAccess` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Team` | `SetupAccess` | `SetupAccessId` |
| `Team` | `ChangeStatus` | `ChangeHistoryId` |

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `Team` | `Employee` | `HAS_MEMBER` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `Team` | `TeamName` | `12` |
| `Team` | `TeamId` | `1` |
| `Team` | `ChangeCount` | `4` |
| `Team` | `CDOTypeId` | `4` |


---

### 🟨 Module: `terminal` (5 issues/warnings)

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `Terminal` | `ChangeStatus` | `ChangeHistoryId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `Terminal` | `TerminalName` | `12` |
| `Terminal` | `CDOTypeId` | `4` |
| `Terminal` | `TerminalId` | `1` |
| `Terminal` | `ChangeCount` | `4` |


---

### 🟨 Module: `thruput_req` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ThruputReq` (吞吐量要求)


---

### 🟨 Module: `timer` (3 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `TimerDef` (时效定义)
- `ActiveTimer` (激活的计时器)
- `TimerAction` (超时动作)


---

### 🟨 Module: `tool` (32 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Tool` (工装/工具)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `A_ToolPlan` | `DocumentSetId` | `DocumentSet` |
| `A_ToolPlanDetails` | `ToolPlanId` | `ToolPlan` |
| `ES_ToolPlanMatrix` | `SetupAccessId` | `SetupAccess` |
| `ES_ToolPlanMatrixDetails` | `ES_ToolPlanMatrixId` | `ES_ToolPlanMatrix` |
| `ES_ToolPlanMatrixDetails` | `ResourceId` | `ResourceDef` |
| `ES_ToolPlanMatrixDetails` | `SpecBaseId` | `` |
| `ES_ToolPlanMatrixDetails` | `SpecId` | `Spec` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `A_ToolPlan` | `ChangeStatus` | `ChangeHistoryId` |
| `A_ToolPlan` | `DocumentSet` | `DocumentSetId` |
| `ES_ToolPlanMatrix` | `SetupAccess` | `SetupAccessId` |
| `ES_ToolPlanMatrix` | `ChangeStatus` | `ChangeHistoryId` |
| `ES_ToolPlanMatrixDetails` | `Spec` | `SpecId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 19

| Class | Field Name | Physical DataType |
|---|---|---|
| `A_ToolPlan` | `CDOTypeId` | `4` |
| `A_ToolPlan` | `ToolPlanName` | `12` |
| `A_ToolPlan` | `ToolPlanId` | `1` |
| `A_ToolPlan` | `ChangeCount` | `4` |
| `A_ToolPlanDetails` | `ItemName` | `12` |
| `A_ToolPlanDetails` | `MinRequired` | `4` |
| `A_ToolPlanDetails` | `ChangeCount` | `4` |
| `A_ToolPlanDetails` | `ToolPlanDetailsId` | `1` |
| `A_ToolPlanDetails` | `CDOTypeId` | `4` |
| `A_ToolPlanDetails` | `MaxRequired` | `4` |
| ... and 9 more | | |


---

### 🟨 Module: `tool_family` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ToolFamily` (工具家族)


---

### 🟨 Module: `tool_group` (1 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `ToolGroup` (工具组)


---

### 🟨 Module: `tool_plan` (7 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `ToolPlan` | `DocumentSetId` | `DocumentSet` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `ToolPlan` | `ChangeStatus` | `ChangeHistoryId` |
| `ToolPlan` | `DocumentSet` | `DocumentSetId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `ToolPlan` | `CDOTypeId` | `4` |
| `ToolPlan` | `ToolPlanName` | `12` |
| `ToolPlan` | `ToolPlanId` | `1` |
| `ToolPlan` | `ChangeCount` | `4` |


---

### 🟨 Module: `tooling` (3 issues/warnings)

#### ❌ Missing Physical Tables (Ontology defines them but they don't exist in DB)
- `Tool` (工装/刀具)
- `ToolGroup` (工装组)
- `ToolStatus` (工装状态)


---

### 🟨 Module: `training_plan` (28 issues/warnings)

#### ℹ️ Logical-only Relationships (Defined in ontology, but no direct FK or bridge table in DB)
| Source Class | Target Class | Relation Name |
|---|---|---|
| `TrainingPlanDetail` | `TrainingRequirementBase` | `REQUIRES_REQUISITE_BASE` |
| `TrainingRequirement` | `DocumentBase` | `HAS_SOP_DOC_BASE` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 26

| Class | Field Name | Physical DataType |
|---|---|---|
| `TrainingPlan` | `TrainingPlanName` | `12` |
| `TrainingPlan` | `CDOTypeId` | `4` |
| `TrainingPlan` | `TrainingPlanId` | `1` |
| `TrainingPlan` | `ChangeCount` | `4` |
| `TrainingPlanDetail` | `CDOTypeId` | `4` |
| `TrainingPlanDetail` | `TrainingPlanDetailId` | `1` |
| `TrainingPlanDetail` | `ChangeCount` | `4` |
| `TrainingPlanDetail` | `ExportImportKey` | `12` |
| `TrainingRequirement` | `CDOTypeId` | `4` |
| `TrainingRequirement` | `TrainingRequirementId` | `1` |
| ... and 16 more | | |


---

### 🟨 Module: `triage_spec` (14 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `TriageSpec` | `SetupAccessId` | `SetupAccess` |
| `TriageSpecDetail` | `TriageSpecId` | `TriageSpec` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `TriageSpec` | `SetupAccess` | `SetupAccessId` |
| `TriageSpec` | `ChangeStatus` | `ChangeHistoryId` |
| `TriageSpecDetail` | `TriageSpec` | `TriageSpecId` |
| `TriageSpecDetail` | `RoleDef` | `RoleId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 8

| Class | Field Name | Physical DataType |
|---|---|---|
| `TriageSpec` | `TriageSpecName` | `12` |
| `TriageSpec` | `TriageSpecId` | `1` |
| `TriageSpec` | `CDOTypeId` | `4` |
| `TriageSpec` | `ChangeCount` | `4` |
| `TriageSpecDetail` | `TriageSpecDetailId` | `1` |
| `TriageSpecDetail` | `CDOTypeId` | `4` |
| `TriageSpecDetail` | `TriageSpecDetailName` | `12` |
| `TriageSpecDetail` | `ExportImportKey` | `12` |


---

### 🟨 Module: `workcenter` (10 issues/warnings)

#### ❌ Missing Navigation Properties (Physical FK exists but property is missing)
| Class | Field Name | Target Physical Table |
|---|---|---|
| `WorkCenter` | `SetupAccessId` | `SetupAccess` |
| `WorkCenter` | `ChangeStatusId` | `ChangeStatus` |

#### ❌ Missing Relationships (Physical FK/bridge exists but no relationship defined)
| Source Class | Target Class | Physical FK Field |
|---|---|---|
| `WorkCenter` | `SetupAccess` | `SetupAccessId` |
| `WorkCenter` | `WIPMsgDefMgr` | `WIPMsgDefMgrId` |
| `WorkCenter` | `ChangeStatus` | `ChangeStatusId` |
| `WorkCenter` | `TrainingRequirementGroup` | `TrainingReqGroupId` |

#### ⚠️ Missing Regular Fields (Physical fields not in ontology - Optional/For Review)
Total missing physical data fields: 4

| Class | Field Name | Physical DataType |
|---|---|---|
| `WorkCenter` | `CDOTypeId` | `4` |
| `WorkCenter` | `WorkCenterId` | `1` |
| `WorkCenter` | `WorkCenterName` | `12` |
| `WorkCenter` | `ChangeCount` | `4` |


---

