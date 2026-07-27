# Phase 15: AQL Levels, Sampling & Customer Modeling Alignment Plan

Based on the physical database tables and fields defined in `Database_Tables.csv` and `Database_Fields.csv`, we have analyzed the structural anomalies, class casing/naming mismatches, and missing target FK tables in the **AQL Levels Modeling** (aql_levels), **Sampling Modeling** (sampling), **Switching Rules Modeling** (switching_rules), and **Customer Modeling** (customer) modules.

We propose the following reorganization and alignment to bring validation errors/warnings for these four modules to exactly **0**:

## User Review Required

> [!IMPORTANT]
> **Modeling 3 Missing Physical Revision Base Classes**:
> To support COMPLETE revision-controlled physical validation and eliminate warnings, we will introduce **3 missing physical base classes** directly in `cross_module_ontology.json`:
> 1. `SampleTestBase` (CdoId: 1430) - Revision controller for `SampleTest`.
> 2. `SampleDataPointBase` (CdoId: 1428) - Revision controller for `SampleDataPoint`.
> 3. `SwitchingRuleBase` (CdoId: 1436) - Revision controller for `SwitchingRule`.
> *(Note: `SamplingPlanBase` is already defined in `cross_module_ontology.json` but is missing properties/relationships which we will define).*

> [!IMPORTANT]
> **Renaming 4 Detail Table Subentities (Adding suffix 's')**:
> Physically in Camstar, subentity list items are named with plural suffix `s`. We will rename the following 4 classes and all their references to achieve exact physical table name alignment:
> 1. `SampleSizeDetail` ➔ **`SampleSizeDetails`** (CdoId: 1442) in `aql_levels`
> 2. `SamplingPlanDetail` ➔ **`SamplingPlanDetails`** (CdoId: 1435) in `sampling`
> 3. `LotSizeDetail` ➔ **`LotSizeDetails`** (CdoId: 1426) in `sampling`
> 4. `SwitchingRuleDetail` ➔ **`SwitchingRuleDetails`** (CdoId: 1438) in `switching_rules`

> [!IMPORTANT]
> **Correcting Casing Mismatches (Email ➔ EMail)**:
> In the physical database schema, the email CDOs are named with capital `M` in `EMail`. We will rename the following classes in `switching_rules_ontology.json` to resolve casing mismatches:
> - `EmailDistribution` ➔ **`EMailDistribution`**
> - `EmailMessage` ➔ **`EMailMessage`**
> - And we will rename property `email` to **`emailAddress`** and `contactName` to **`customerContactName`** in `CustomerContact` class to align with `EmailAddress` and `CustomerContactName` physical columns.

---

## Open Questions

> [!NOTE]
> **Deprecating Duplicate Logical AQL Class**:
> Currently in `sampling_ontology.json`, a logical `AQL` class is defined. However, the actual physical table is `AQLLevel` (modeled in `aql_levels_ontology.json`). We will delete the redundant logical `AQL` class and redirect all its properties and relationships to point directly to `AQLLevel`.

---

## Proposed Changes

### [Cross Module] Component

#### [MODIFY] [cross_module_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/cross_module_ontology.json)
- **Add 3 New Physical Classes** in the `classes` array:
  * **`SampleTestBase`** (CdoId: 1430):
    - Properties: `name` (String, required), `description` (String), `isFrozen` (Boolean), `changeHistory` (`Navigation` -> `ChangeStatus`), `setupAccess` (`Navigation` -> `SetupAccess`), `revOfRcd` (`Navigation` -> `SampleTest`).
  * **`SampleDataPointBase`** (CdoId: 1428):
    - Properties: `name` (String, required), `description` (String), `isFrozen` (Boolean), `changeHistory` (`Navigation` -> `ChangeStatus`), `setupAccess` (`Navigation` -> `SetupAccess`), `revOfRcd` (`Navigation` -> `SampleDataPoint`).
  * **`SwitchingRuleBase`** (CdoId: 1436):
    - Properties: `name` (String, required), `description` (String), `isFrozen` (Boolean), `changeHistory` (`Navigation` -> `ChangeStatus`), `setupAccess` (`Navigation` -> `SetupAccess`), `revOfRcd` (`Navigation` -> `SwitchingRule`).
- **Update relationships**:
  * Define new relationships corresponding to newly exposed physical navigation fields on base and target classes:
    - `SampleTestBase -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `SampleTestBase -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `SampleDataPointBase -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `SampleDataPointBase -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `SwitchingRuleBase -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `SwitchingRuleBase -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `SamplingPlanBase -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `SamplingPlanBase -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `SampleTest -[HAS_BASE_VERSION]-> SampleTestBase` (FK: `SampleTestBaseId`)
    - `SampleDataPoint -[HAS_BASE_VERSION]-> SampleDataPointBase` (FK: `SampleDataPointBaseId`)
    - `SwitchingRule -[HAS_BASE_VERSION]-> SwitchingRuleBase` (FK: `SwitchingRuleBaseId`)
    - `SamplingPlan -[HAS_BASE_VERSION]-> SamplingPlanBase` (FK: `SamplingPlanBaseId`)

---

### [AQL Levels] Component

#### [MODIFY] [aql_levels_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/aql_levels_ontology.json)
- **Rename Class**: `SampleSizeDetail` ➔ **`SampleSizeDetails`**.
- **Update properties for `AQLLevel`**:
  * Add property: `changeHistory` (`Navigation` -> `ChangeStatus`, physical: `ChangeHistoryId`).
- **Update properties for `SampleSizeDetails`**:
  * Add property: `aqlLevel` (`Navigation` -> `AQLLevel`, physical: `AQLLevelId`).
- **Update relationships**:
  * Rename `AQLLevel -[HAS_SAMPLE_SIZE_DETAIL]-> SampleSizeDetail` ➔ `AQLLevel -[HAS_SAMPLE_SIZE_DETAILS]-> SampleSizeDetails`.
  * Add `SampleSizeDetails -[BELONGS_TO_AQL]-> AQLLevel` (FK: `AQLLevelId`).
  * Add `AQLLevel -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`).

---

### [Sampling Modeling] Component

#### [MODIFY] [sampling_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/sampling_ontology.json)
- **Delete Class**: `AQL` (completely deprecate duplicate logical class).
- **Rename Classes**:
  * `SamplingPlanDetail` ➔ **`SamplingPlanDetails`**
  * `LotSizeDetail` ➔ **`LotSizeDetails`**
- **Update properties for `SamplingPlan`**:
  * Add missing properties:
    - `samplingPlanBase` (`Navigation` -> `SamplingPlanBase`, physical: `SamplingPlanBaseId`)
    - `wipMsgDefMgr` (`Navigation` -> `WIPMsgDefMgr`, physical: `WIPMsgDefMgrId`)
    - `specBase` (`Navigation` -> `SpecBase`, physical: `SpecBaseId`)
    - `switchingRuleBase` (`Navigation` -> `SwitchingRuleBase`, physical: `SwitchingRuleBaseId`)
- **Update properties for `SamplingPlanDetails`**:
  * Add all physical navigation properties matching direct database FKs:
    - `aqlLevel` (`Navigation` -> `AQLLevel`, physical: `AQLLevelId`)
    - `inspectionLevel` (`Navigation` -> `InspectionLevel`, physical: `InspectionLevelId`)
    - `resource` (`Navigation` -> `Resource`, physical: `ResourceId`)
    - `sampleTest` (`Navigation` -> `SampleTest`, physical: `SampleTestId`)
    - `samplingPlan` (`Navigation` -> `SamplingPlan`, physical: `SamplingPlanId`)
    - `spec` (`Navigation` -> `Spec`, physical: `SpecId`)
    - `switchingRule` (`Navigation` -> `SwitchingRule`, physical: `SwitchingRuleId`)
    - `vendor` (`Navigation` -> `Vendor`, physical: `VendorId`)
    - `vendorItem` (`Navigation` -> `VendorItem`, physical: `VendorItemId`)
- **Update properties for `SampleTest`**:
  * Add property: `sampleTestBase` (`Navigation` -> `SampleTestBase`, physical: `SampleTestBaseId`).
  * Add property: `wipMsgDefMgr` (`Navigation` -> `WIPMsgDefMgr`, physical: `WIPMsgDefMgrId`).
- **Update properties for `SampleDataPoint`**:
  * Add property: `sampleDataPointBase` (`Navigation` -> `SampleDataPointBase`, physical: `SampleDataPointBaseId`).
  * Add property: `wipMsgDefMgr` (`Navigation` -> `WIPMsgDefMgr`, physical: `WIPMsgDefMgrId`).
- **Update properties for `InspectionLevel`**:
  * Add property: `changeHistory` (`Navigation` -> `ChangeStatus`, physical: `ChangeHistoryId`).
- **Update properties for `LotSizeDetails`**:
  * Add property: `inspectionLevel` (`Navigation` -> `InspectionLevel`, physical: `InspectionLevelId`).
- **Update relationships**:
  * Rebuild all relationships to point to correct class names (`SamplingPlanDetails`, `LotSizeDetails`, `AQLLevel`) and add all physical FK links:
    - `SamplingPlanDetails -[BELONGS_TO_SAMPLING_PLAN]-> SamplingPlan` (FK: `SamplingPlanId`)
    - `SamplingPlanDetails -[USES_AQL]-> AQLLevel` (FK: `AQLLevelId`)
    - `SamplingPlanDetails -[USES_INSPECTION_LEVEL]-> InspectionLevel` (FK: `InspectionLevelId`)
    - `SamplingPlanDetails -[USES_RESOURCE]-> Resource` (FK: `ResourceId`)
    - `SamplingPlanDetails -[USES_SAMPLE_TEST]-> SampleTest` (FK: `SampleTestId`)
    - `SamplingPlanDetails -[ASSIGNED_SPEC]-> Spec` (FK: `SpecId`)
    - `SamplingPlanDetails -[HAS_SWITCHING_RULE]-> SwitchingRule` (FK: `SwitchingRuleId`)
    - `SamplingPlanDetails -[BELONGS_TO_VENDOR]-> Vendor` (FK: `VendorId`)
    - `SamplingPlanDetails -[BELONGS_TO_VENDOR_ITEM]-> VendorItem` (FK: `VendorItemId`)
    - `LotSizeDetails -[BELONGS_TO_INSPECTION]-> InspectionLevel` (FK: `InspectionLevelId`)
    - `SamplingPlan -[USES_AQL]-> AQLLevel` (Redirected from `AQL`)
    - `SamplingPlan -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `SamplingPlan -[HAS_WIP_MSG_DEF_MGR]-> WIPMsgDefMgr` (FK: `WIPMsgDefMgrId`)
    - `SamplingPlan -[HAS_SPEC_BASE]-> SpecBase` (FK: `SpecBaseId`)
    - `SamplingPlan -[HAS_SWITCHING_RULE_BASE]-> SwitchingRuleBase` (FK: `SwitchingRuleBaseId`)
    - `SampleTest -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `SampleTest -[HAS_WIP_MSG_DEF_MGR]-> WIPMsgDefMgr` (FK: `WIPMsgDefMgrId`)
    - `SampleTest -[HAS_AQL_REJECT_REASONS]-> LossReasonGroup` (FK: `AQLRejectReasonsId`)
    - `SampleTest -[DECREASE_BY_REJECT_COUNT_REASON]-> LossReason` (FK: `DecreaseByRejectCountReasonId`)
    - `SampleTest -[DECREASE_BY_SAMPLE_SIZE_REASON]-> LossReason` (FK: `DecreaseBySampleSizeReasonId`)
    - `SampleDataPoint -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `SampleDataPoint -[HAS_WIP_MSG_DEF_MGR]-> WIPMsgDefMgr` (FK: `WIPMsgDefMgrId`)
    - `InspectionLevel -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)

---

### [Switching Rules Modeling] Component

#### [MODIFY] [switching_rules_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/switching_rules_ontology.json)
- **Rename Classes**:
  * `SwitchingRuleDetail` ➔ **`SwitchingRuleDetails`**
  * `EmailDistribution` ➔ **`EMailDistribution`**
  * `EmailMessage` ➔ **`EMailMessage`**
- **Update properties for `SwitchingRule`**:
  * Add missing properties:
    - `switchingRuleBase` (`Navigation` -> `SwitchingRuleBase`, physical: `SwitchingRuleBaseId`)
    - `changeHistory` (`Navigation` -> `ChangeStatus`, physical: `ChangeHistoryId`)
- **Update properties for `SwitchingRuleDetails`**:
  * Add property: `switchingRule` (`Navigation` -> `SwitchingRule`, physical: `SwitchingRuleId`).
- **Update properties for `EMailDistribution`**:
  * Add property: `changeHistory` (`Navigation` -> `ChangeStatus`, physical: `ChangeHistoryId`).
- **Update properties for `EMailMessage`**:
  * Add property: `changeHistory` (`Navigation` -> `ChangeStatus`, physical: `ChangeHistoryId`).
- **Update relationships**:
  * Rename occurrences of detail and email classes in relations.
  * Add `SwitchingRuleDetails -[BELONGS_TO_RULE]-> SwitchingRule` (FK: `SwitchingRuleId`).
  * Add `SwitchingRule -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`).
  * Add `EMailDistribution -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`).
  * Add `EMailMessage -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`).

---

### [Customer Modeling] Component

#### [MODIFY] [customer_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/customer_ontology.json)
- **Update properties for `Customer`**:
  * Add missing properties:
    - `setupAccess` (`Navigation` -> `SetupAccess`, physical: `SetupAccessId`)
- **Update properties for `CustomerContact`**:
  * Add/Modify properties:
    - `customer` (`Navigation` -> `Customer`, physical: `CustomerId`)
    - Rename `email` ➔ `emailAddress` (Physical: `EmailAddress`, String)
    - Rename `contactName` ➔ `customerContactName` (Physical: `CustomerContactName`, String)
    - Add `primaryContact` (Boolean, Physical: `PrimaryContact`)
    - Add `cellPhoneNumber` (String, Physical: `CellPhoneNumber`)
- **Update relationships**:
  * Add `Customer -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`).
  * Add `Customer -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`).
  * Add `Customer -[HAS_WIP_MSG_DEF_MGR]-> WIPMsgDefMgr` (FK: `WIPMsgDefMgrId`).
  * Add `CustomerContact -[BELONGS_TO_CUSTOMER]-> Customer` (FK: `CustomerId`).

---

## Verification Plan

### Automated Tests
- Run validation script comparing our schema mapping with the CSV table design:
  ```bash
  python C:\Users\yanghe\.gemini\antigravity-ide\brain\6c3460b2-c405-4ea1-a01d-3d5fb63292ee\scratch\validate_ontology_vs_csv.py
  ```
  Validate that warnings for `aql_levels`, `sampling`, `switching_rules`, and `customer` drop to exactly **0**.
- Execute schema ingestion to Neo4j graph:
  ```bash
  python src/ontology/loader/neo4j_loader.py
  ```
  Ensure 100% database schema parsing and loading success.
- Run a custom verification script `verify_phase15.py` to confirm node existence and relationship connectivity in Neo4j via automated Cypher queries.

### Manual Verification
- Review the graph locally in the browser visualizer and ensure all renamed details classes (e.g. `SampleSizeDetails`, `LotSizeDetails`, `SamplingPlanDetails`, `SwitchingRuleDetails`) display correctly.
