# Phase 16: Employee, Role & Training Modeling Alignment Plan

Based on the physical database tables and fields defined in `Database_Tables.csv` and `Database_Fields.csv`, we have analyzed the structural anomalies, class casing/naming mismatches, and missing target FK tables in the **Employee Modeling** (`employee`), **Role Modeling** (`role`), **Role Permissions Modeling** (`role_permissions`), and **Training Plan Modeling** (`training_plan`) modules.

We propose the following reorganization and alignment to bring validation errors/warnings for these four modules to exactly **0**:

## User Review Required

> [!IMPORTANT]
> **Introducing 2 Physical Classes (`TrainingRequirementBase` & `TrainingRecord`)**:
> To support COMPLETE physical database alignment and model actual MES runtime records:
> 1. We will add **`TrainingRequirementBase`** (CdoId: 965) to `cross_module_ontology.json`. This class acts as the revision base controller for the version-controlled `TrainingRequirement` class.
> 2. We will add **`TrainingRecord`** (CdoId: 975) to `training_plan_ontology.json`. This class maps directly to the physical `TrainingRecord` table, establishing the concrete runtime link between `Employee` and their completed `TrainingRequirement` qualifications.

> [!IMPORTANT]
> **Renaming Classes to Align with DB Table Names**:
> 1. **`Role` ➔ `RoleDef`** (CdoId: 914) in `role_ontology.json`.
> 2. **`RolePermissions` ➔ `RolePermission`** (CdoId: 1219) in `role_permissions_ontology.json`. We will move the duplicate `RolePermission` definition from the `role` module and unify it into `role_permissions` under a single singular class `RolePermission`.
> 3. **`TrainingReqGroup` ➔ `TrainingRequirementGroup`** (CdoId: 971) in `training_plan_ontology.json`. This resolves numerous cross-module target warnings since other files (like Spec, Operation) are already referencing `TrainingRequirementGroup`.

> [!IMPORTANT]
> **Deprecating Logical-Only `Certification` Class**:
> The `Certification` class in `employee_ontology.json` does not map to any physical database table. In a real Camstar system, qualifications are tracked via `TrainingRecord` pointing to a `TrainingRequirement`. We will delete the logical-only `Certification` class and replace it with the physical `TrainingRecord` definition.

---

## Open Questions

> [!NOTE]
> **ObjectInstanceId Type Normalization**:
> In `RolePermission`, the `ObjectInstanceId` is a generic physical FK pointing to any object instance, represented in the CSV schema as an FK but with an empty target table. In the ontology, it is currently modeled as `String`. We will change its type to `Navigation` to perfectly align with the physical schema without throwing type mismatch warnings.

---

## Proposed Changes

### [Cross Module] Component

#### [MODIFY] [cross_module_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/cross_module_ontology.json)
- **Add Physical Class** in the `classes` array:
  * **`TrainingRequirementBase`** (CdoId: 965):
    - Properties: `name` (String, maps to `TrainingRequirementName` physically, required), `description` (String), `iconId` (Integer), `revOfRcd` (`Navigation` -> `TrainingRequirement`).
- **Update relationships**:
  * Define two-way physical relationships for base versions:
    - `TrainingRequirementBase -[HAS_REV_OF_RCD]-> TrainingRequirement` (FK: `RevOfRcdId`)
    - `TrainingRequirement -[HAS_BASE_VERSION]-> TrainingRequirementBase` (FK: `TrainingRequirementBaseId`)

---

### [Employee Modeling] Component

#### [MODIFY] [employee_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/employee_ontology.json)
- **Delete Class**: `Certification` (and remove the redundant logical-only relationship `Employee -[HAS_CERTIFICATION]-> Certification`).
- **Update properties for `Employee`**:
  * Add direct physical FK properties:
    - `setupAccess` (`Navigation` -> `SetupAccess`, physical: `SetupAccessId`)
    - `esDisplayOptions` (`Navigation` -> `ES_DisplayOptions`, physical: `ES_DisplayOptionsId`)
    - `esInformationBarConfig` (`Navigation` -> `ES_ProdClientUIConfig`, physical: `ES_InformationBarConfigId`)
    - `esPCBToolBarConfig` (`Navigation` -> `ES_ProdClientUIConfig`, physical: `ES_PCBToolBarConfigId`)
    - `esDefectGridConfig` (`Navigation` -> `ES_ProdClientUIConfig`, physical: `ES_DefectGridConfigId`)
    - `esCommandBarConfig` (`Navigation` -> `ES_ProdClientUIConfig`, physical: `ES_CommandBarConfigId`)
    - `esBoxGridConfig` (`Navigation` -> `ES_ProdClientUIConfig`, physical: `ES_BoxGridConfigId`)
    - `esTrackCompleteFAI` (`Navigation`, physical: `ES_TrackCompleteFAIId`)
    - `terminologyDictionary` (`Navigation` -> `Dictionary`, physical: `TerminologyDictionaryId`)
    - `webDrillDownMenuDefinition` (`Navigation` -> `MenuDefinition`, physical: `WebDrillDownMenuDefinitionId`)
    - `webMenuDefinition` (`Navigation` -> `MenuDefinition`, physical: `WebMenuDefinitionId`)
    - `historyView` (`Navigation` -> `HistoryView`, physical: `HistoryViewId`)
    - `changeStatus` (`Navigation` -> `ChangeStatus`, physical: `ChangeStatusId`) - *Note: this renames the legacy logical `changeHistory` property to align with physical `ChangeStatusId` field name.*
    - `sessionValues` (`Navigation` -> `SessionValues`, physical: `SessionValuesId`)
    - `uiPortalProfile` (`Navigation` -> `UIPortalProfile`, physical: `UIPortalProfileId`)
    - `trainingPlan` (`Navigation` -> `TrainingPlan`, physical: `TrainingPlanId`)
    - `userProfile` (`Navigation` -> `UserProfile`, physical: `UserProfileId`)
    - `employeeLoginInfo` (`Navigation` -> `EmployeeLoginInfo`, physical: `EmployeeLoginInfoId`)
    - `portalV8MenuDefinition` (`Navigation` -> `PortalMenuDefinition`, physical: `PortalV8MenuDefinitionId`)
- **Update properties for `EmployeeLoginInfo`**:
  * Add `name` (String) property.
  * Add `employee` (`Navigation` -> `Employee`, physical: `EmployeeId`).
  * Add `changeHistory` (`Navigation` -> `ChangeStatus`, physical: `ChangeHistoryId`).
- **Update properties for `EmployeeRole`**:
  * Add `setupAccess` (`Navigation` -> `SetupAccess`, physical: `SetupAccessId`).
- **Update relationships**:
  * Update all relations and add 7 physical direct edges:
    - `Employee -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `Employee -[HAS_DISPLAY_OPTIONS]-> ES_DisplayOptions` (FK: `ES_DisplayOptionsId`)
    - `Employee -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeStatusId`)
    - `EmployeeLoginInfo -[BELONGS_TO_EMPLOYEE]-> Employee` (FK: `EmployeeId`)
    - `EmployeeLoginInfo -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `EmployeeRole -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `EmployeeRole -[BELONGS_TO_EMPLOYEE]-> Employee` (FK: `EmployeeId`)

---

### [Role Modeling] Component

#### [MODIFY] [role_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/role_ontology.json)
- **Rename Class**: `Role` ➔ **`RoleDef`**.
- **Update properties for `RoleDef`**:
  * `name` (String, required, maps to `RoleName` physically).
  * Add `roleType` (Integer, physical: `RoleType`).
- **Delete Class definition**: `RolePermission` (moved to `role_permissions_ontology.json`).
- **Update relationships**:
  * Update occurrences of `Role` to `RoleDef`:
    - `RoleDef -[HAS_PERMISSION]-> RolePermission` (cardinality: `ONE_TO_MANY`)
    - `EmployeeRole -[REFERENCES_ROLE]-> RoleDef` (cardinality: `MANY_TO_ONE`)
    - `RoleDef -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `RoleDef -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)

---

### [Role Permissions Modeling] Component

#### [MODIFY] [role_permissions_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/role_permissions_ontology.json)
- **Rename Class**: `RolePermissions` ➔ **`RolePermission`** (singular, matching physical table `RolePermission`).
- **Update properties for `RolePermission`**:
  * `name` (String, maps to physical `RolePermissionName`).
  * Add `role` (`Navigation` -> `RoleDef`, physical: `RoleId`, required).
  * `permissionType` (Integer).
  * `objectMetaId` (Integer).
  * `objectInstanceId` (change type from `String` to `Navigation` to resolve physical type warnings).
  * `modes` (`Navigation`, logical list).
- **Update relationships**:
  * Add relation:
    - `RolePermission -[BELONGS_TO_ROLE]-> RoleDef` (FK: `RoleId`)

---

### [Training Plan Modeling] Component

#### [MODIFY] [training_plan_ontology.json](file:///d:/Deepseek/camstar/CamstarOntology/src/ontology/wiki_kb/training_plan_ontology.json)
- **Rename Class**: `TrainingReqGroup` ➔ **`TrainingRequirementGroup`**.
- **Add Class**: **`TrainingRecord`** (CdoId: 975) representing the physical training history table.
  * Properties:
    - `employee` (`Navigation` -> `Employee`, physical: `EmployeeId`)
    - `trainingRequirement` (`Navigation` -> `TrainingRequirement`, physical: `TrainingRequirementId`)
    - `status` (`Navigation` -> `TrainingRecordStatus`, physical: `StatusId`)
    - `expirationDate` (DateTime, physical: `ExpirationDate`)
    - `permission` (Integer, physical: `Permission`)
    - `eSigRequirement` (`Navigation` -> `ESigRequirement`, physical: `ESigRequirementId`)
    - `changeHistory` (`Navigation` -> `ChangeStatus`, physical: `ChangeHistoryId`)
    - `setupAccess` (`Navigation` -> `SetupAccess`, physical: `SetupAccessId`)
- **Update properties for `TrainingPlan`**:
  * Add `setupAccess` (`Navigation` -> `SetupAccess`, physical: `SetupAccessId`).
  * Add `changeHistory` (`Navigation` -> `ChangeStatus`, physical: `ChangeHistoryId`).
- **Update properties for `TrainingPlanDetail`**:
  * Add physical navigation properties:
    - `trainingPlan` (`Navigation` -> `TrainingPlan`, physical: `TrainingPlanId`)
    - `subTrainingPlan` (`Navigation` -> `TrainingPlan`, physical: `SubTrainingPlanId`)
    - `trainingRequirement` (`Navigation` -> `TrainingRequirement`, physical: `TrainingRequirementId`)
    - `trainingRequirementBase` (`Navigation` -> `TrainingRequirementBase`, physical: `TrainingRequirementBaseId`)
- **Update properties for `TrainingRequirement`**:
  * Add physical navigation properties:
    - `setupAccess` (`Navigation` -> `SetupAccess`, physical: `SetupAccessId`)
    - `warningEmailGroup` (`Navigation` -> `EmployeeGroup`, physical: `WarningEmailGroupId`)
    - `trainingRequirementBase` (`Navigation` -> `TrainingRequirementBase`, physical: `TrainingRequirementBaseId`)
    - `wipMsgDefMgr` (`Navigation` -> `WIPMsgDefMgr`, physical: `WIPMsgDefMgrId`)
    - `sopDocBase` (`Navigation` -> `DocumentBase`, physical: `SOPDocBaseId`)
    - `sopDoc` (`Navigation` -> `Document`, physical: `SOPDocId`)
- **Update properties for `TrainingRequirementGroup`**:
  * Add `setupAccess` (`Navigation` -> `SetupAccess`, physical: `SetupAccessId`).
- **Update properties for `TrainingRecordStatus`**:
  * Add `setupAccess` (`Navigation` -> `SetupAccess`, physical: `SetupAccessId`).
- **Update relationships**:
  * Map all direct physical foreign keys and bridge connections:
    - `TrainingPlanDetail -[BELONGS_TO_PLAN]-> TrainingPlan` (FK: `TrainingPlanId`)
    - `TrainingPlanDetail -[HAS_SUB_PLAN]-> TrainingPlan` (FK: `SubTrainingPlanId`)
    - `TrainingPlanDetail -[REQUIRES_REQUISITE]-> TrainingRequirement` (FK: `TrainingRequirementId`)
    - `TrainingPlanDetail -[REQUIRES_REQUISITE_BASE]-> TrainingRequirementBase` (FK: `TrainingRequirementBaseId`)
    - `TrainingRequirement -[HAS_BASE_VERSION]-> TrainingRequirementBase` (FK: `TrainingRequirementBaseId`)
    - `TrainingRequirement -[HAS_SOP_DOC]-> Document` (FK: `SOPDocId`)
    - `TrainingRequirement -[HAS_SOP_DOC_BASE]-> DocumentBase` (FK: `SOPDocBaseId`)
    - `TrainingRequirement -[HAS_WIP_MSG_DEF_MGR]-> WIPMsgDefMgr` (FK: `WIPMsgDefMgrId`)
    - `TrainingRequirement -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `TrainingRequirementGroup -[HAS_ENTRY]-> TrainingRequirement`
    - `TrainingRequirementGroup -[HAS_SUBGROUP]-> TrainingRequirementGroup`
    - `TrainingRequirementGroup -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `TrainingRecordStatus -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `TrainingRecordStatus -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `TrainingRecord -[BELONGS_TO_EMPLOYEE]-> Employee` (FK: `EmployeeId`)
    - `TrainingRecord -[BELONGS_TO_REQUIREMENT]-> TrainingRequirement` (FK: `TrainingRequirementId`)
    - `TrainingRecord -[HAS_RECORD_STATUS]-> TrainingRecordStatus` (FK: `StatusId`)
    - `TrainingRecord -[HAS_ESIG_REQUIREMENT]-> ESigRequirement` (FK: `ESigRequirementId`)
    - `TrainingRecord -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)
    - `TrainingRecord -[HAS_SETUP_ACCESS]-> SetupAccess` (FK: `SetupAccessId`)
    - `Employee -[HAS_TRAINING_RECORD]-> TrainingRecord` (cardinality: `ONE_TO_MANY`)
    - `TrainingPlan -[HAS_CHANGE_STATUS]-> ChangeStatus` (FK: `ChangeHistoryId`)

---

## Verification Plan

### Automated Tests
- Run validation script comparing our schema mapping with the CSV table design:
  ```bash
  python C:\Users\yanghe\.gemini\antigravity-ide\brain\6c3460b2-c405-4ea1-a01d-3d5fb63292ee\scratch\validate_ontology_vs_csv.py
  ```
  Validate that warnings for `employee`, `role`, `role_permissions`, and `training_plan` drop to exactly **0**.
- Execute schema ingestion to Neo4j graph:
  ```bash
  python src/ontology/loader/neo4j_loader.py
  ```
  Ensure 100% database schema parsing and loading success.
- Run a custom verification script `verify_phase16.py` to confirm node existence and relationship connectivity in Neo4j via automated Cypher queries.

### Manual Verification
- Review the graph locally in the browser visualizer and ensure all renamed classes (e.g. `RoleDef`, `RolePermission`, `TrainingRequirementGroup`, and new physical classes `TrainingRecord`, `TrainingRequirementBase`) display correctly.
