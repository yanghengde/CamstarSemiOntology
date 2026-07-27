# Camstar 本体驱动 ETL 系统开发指南

> **版本**: v1.0  
> **目标**: 以本体论为核心，驱动 Camstar MES 数据的结构化抽取与目标库建设  
> **技术栈**: Neo4j · Python · SQL Server · LLM (本体辅助生成)

---

## 目录

1. [整体架构](#1-整体架构)
2. [阶段一：建立 Camstar 本体](#2-阶段一建立-camstar-本体)
3. [阶段二：本体驱动目标库设计](#3-阶段二本体驱动目标库设计)
4. [阶段三：本体驱动 ETL 开发](#4-阶段三本体驱动-etl-开发)
5. [LLM 辅助本体构建策略](#5-llm-辅助本体构建策略)
6. [数据流与增量同步设计](#6-数据流与增量同步设计)
7. [目录结构与代码规范](#7-目录结构与代码规范)
8. [里程碑与验收标准](#8-里程碑与验收标准)
9. [风险与注意事项](#9-风险与注意事项)

---

## 1. 整体架构

### 1.1 设计哲学

本项目采用 **Ontology-Driven Data Integration（本体驱动数据集成）** 模式：

```
本体（Ontology）= 系统唯一事实来源（Single Source of Truth）

本体 ──驱动──► 目标库 DDL（建表结构）
本体 ──驱动──► ETL 映射逻辑（字段对应）
本体 ──驱动──► 数据质量规则（约束验证）
本体 ──驱动──► 分析查询模板（端到端分析）
```

### 1.2 数据流全景

```
┌─────────────────────────────────────────────────────────────────┐
│                  Camstar MES (源系统)                            │
│                                                                  │
│  Studio 建模结构    SQL Server DB          API/Transaction文档   │
│  ·WorkflowDef      ·Workflows             ·Transaction语义      │
│  ·OperationDef     ·ContainerHistory      ·字段说明             │
│  ·ESpecDef         ·DCHistory                                   │
│                    ·AuditLog                                     │
└────────┬────────────────┬────────────────────────┬─────────────┘
         │                │                        │
    Studio导出         SQL抽取                 文档解析
    + LLM理解          + 表结构扫描            + LLM语义提取
         │                │                        │
         └────────────────┴────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              【阶段一】Camstar 本体层 (Neo4j)                     │
│                                                                  │
│  OntologyClass ── OntologyProperty ── OntologyRelationship      │
│                                                                  │
│  ConfigEntity        EventEntity          MetricEntity          │
│  ·WorkflowDef        ·MoveEvent           ·YieldRecord          │
│  ·StepDef            ·MeasureEvent        ·CycleTimeRecord      │
│  ·ESpecDef           ·ChangeEvent         ·QualityRecord        │
│  ·ResourceDef        ·DowntimeEvent       ·EfficiencyRecord     │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 本体驱动
              ┌────────────┴────────────┐
              ▼                         ▼
┌─────────────────────┐    ┌────────────────────────────────────┐
│  【阶段二】目标库     │    │  【阶段三】ETL Pipeline             │
│  DDL 自动生成        │    │                                    │
│                      │    │  全量加载 → 增量同步 → 聚合计算    │
│  ont_WorkflowDef     │    │  Python + SQLAlchemy              │
│  ont_StepDef         │    │  调度: Airflow / Windows Task     │
│  ont_MoveEvent       │    │                                    │
│  ont_YieldRecord     │    └────────────────────────────────────┘
│  ...                 │
└─────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      分析层（端到端分析）                         │
│                                                                  │
│  变更对质量的影响分析   产品效率对比分析   质量根因追溯           │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 技术栈选型

| 组件 | 技术 | 用途 |
|---|---|---|
| 本体存储 | Neo4j 5.x | 存储本体类/属性/关系 |
| 本体格式 | OWL/Turtle (via n10s) | 标准化导出/导入 |
| LLM 辅助 | Claude / GPT-4 + Wiki | 本体草稿生成 |
| ETL 引擎 | Python 3.11 + SQLAlchemy | 数据抽取与加载 |
| 源数据库 | SQL Server (Camstar DB) | 原始数据 |
| 目标数据库 | SQL Server (Ontology DB) | 按本体建设的目标库 |
| 调度 | Apache Airflow / Task Scheduler | 增量同步调度 |
| 验证 | Great Expectations | 数据质量校验 |

---

## 2. 阶段一：建立 Camstar 本体

### 2.1 本体三层结构

```
Layer 1: 配置本体（Config Ontology）
  → 描述 Camstar 的"设计结构"：工艺、规格、资源、产品
  → 来源：Studio 建模界面 + SQL 配置表

Layer 2: 事件本体（Event Ontology）
  → 描述 Camstar 的"发生了什么"：流转、采集、变更、停机
  → 来源：ContainerHistory / DCHistory / AuditLog

Layer 3: 指标本体（Metric Ontology）
  → 描述"结果如何"：良率、节拍、质量指数
  → 来源：聚合计算，非直接抽取
```

### 2.2 本体类完整定义

#### 配置层类

| 类名 | 中文 | 核心属性 | 对应 Camstar 对象 |
|---|---|---|---|
| `WorkflowDef` | 工艺路线 | name, revision, effectiveDate | Workflow Definition |
| `StepDef` | 工步 | name, sequence, stepType | Workflow Step |
| `OperationDef` | 工序 | name, description, operationType | Operation Definition |
| `ProductDef` | 产品 | name, revision, productType | Product Definition |
| `ProductFamily` | 产品族 | name | Product Family |
| `ResourceDef` | 资源/设备 | name, resourceType, capacity | Resource Definition |
| `ResourceGroup` | 资源组/产线 | name, lineId | Resource Group |
| `DataCollectionDef` | 采集计划 | name, dcType | Data Collection Definition |
| `ESpecDef` | 参数规格 | name, dataType, lowLimit, highLimit, uom | E-Spec Definition |
| `BOMDef` | 物料清单 | name, revision | BOM Definition |
| `ContainerDef` | 容器定义 | name, uom | Container Definition |

#### 事件层类

| 类名 | 中文 | 核心属性 | 来源表 |
|---|---|---|---|
| `MoveEvent` | 流转事件 | eventId, moveType(IN/OUT), ts, qty | ContainerHistory |
| `MeasureEvent` | 测量事件 | eventId, value, inSpec, ts | DCHistory |
| `ChangeEvent` | 变更事件 | eventId, objectType, fieldName, oldVal, newVal, ts | AuditLog |
| `DowntimeEvent` | 停机事件 | eventId, reason, startTs, endTs, durationMin | DowntimeLog |

#### 指标层类

| 类名 | 中文 | 核心属性 | 计算逻辑 |
|---|---|---|---|
| `YieldRecord` | 良率记录 | date, yieldRate, scrapQty, ncmQty | MoveEvent 聚合 |
| `CycleTimeRecord` | 节拍记录 | date, avgSec, minSec, maxSec | MoveIn-MoveOut 配对 |
| `QualityRecord` | 质量记录 | date, passRate, cpk | MeasureEvent 聚合 |
| `EfficiencyRecord` | 效率记录 | date, oee, throughput, utilRate | MoveEvent + Downtime 聚合 |

### 2.3 本体关系完整定义

```
配置层关系（结构关系）：
WorkflowDef  ──[HAS_STEP {sequence}]──►  StepDef
StepDef      ──[USES]──►                 OperationDef
StepDef      ──[ASSIGNED_TO]──►          ResourceDef
StepDef      ──[COLLECTS]──►             DataCollectionDef
StepDef      ──[NEXT_STEP {condition}]── StepDef          ← 路由关系
DataCollectionDef ──[HAS_SPEC]──►        ESpecDef
WorkflowDef  ──[APPLIES_TO]──►           ProductDef
ProductDef   ──[BELONGS_TO]──►           ProductFamily
ProductDef   ──[HAS_BOM]──►              BOMDef
BOMDef       ──[HAS_COMPONENT {qty}]──►  ProductDef
ResourceDef  ──[LOCATED_IN]──►           ResourceGroup

变更关系（因果链核心）：
ConfigEntity ──[CHANGED_BY {ts, author}]──► ChangeEvent
ChangeEvent  ──[PRECEDED {windowDays}]──►   MetricEntity  ← 变更前后对比

事件→配置关系（定位关系）：
MoveEvent    ──[AT_STEP]──►    StepDef
MoveEvent    ──[RAN_ON]──►     ResourceDef
MoveEvent    ──[FOR_PRODUCT]──► ProductDef
MeasureEvent ──[MEASURES]──►   ESpecDef
MeasureEvent ──[AT_STEP]──►    StepDef

指标→维度关系（分析维度）：
MetricEntity ──[ON_LINE]──►      ResourceGroup
MetricEntity ──[FOR_PRODUCT]──►  ProductDef
MetricEntity ──[AT_STEP]──►      StepDef
```

### 2.4 Neo4j 本体初始化脚本

```cypher
// ── 创建约束 ──
CREATE CONSTRAINT FOR (n:WorkflowDef)        REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:StepDef)            REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT FOR (n:OperationDef)       REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:ProductDef)         REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:ResourceDef)        REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:ESpecDef)           REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:DataCollectionDef)  REQUIRE n.name IS UNIQUE;

// ── 创建本体元数据节点（描述类本身） ──
CREATE (:OntologyClass {
    name: 'WorkflowDef',
    layer: 'Config',
    chineseName: '工艺路线',
    sourceTable: 'Workflows',
    description: 'Camstar工艺路线定义，包含一组有序的工步'
});

CREATE (:OntologyClass {
    name: 'ESpecDef',
    layer: 'Config',
    chineseName: '参数规格',
    sourceTable: 'ESpecs',
    description: '定义工步数据采集的参数规格，含上下限'
});

// ── 示例：建立本体类层级关系 ──
MATCH (wf:OntologyClass {name:'WorkflowDef'})
MATCH (st:OntologyClass {name:'StepDef'})
CREATE (wf)-[:ONTOLOGY_RELATION {
    name: 'HAS_STEP',
    cardinality: 'ONE_TO_MANY',
    ordered: true,
    orderField: 'sequence'
}]->(st);
```

### 2.5 从 SQL Server 自动探索本体

```python
# ontology_explorer.py
# 用途：扫描 Camstar SQL Server，自动发现表结构，辅助本体建立

import pyodbc
import pandas as pd
from neo4j import GraphDatabase

CAMSTAR_TABLES = [
    'Workflows', 'WorkflowSteps', 'Operations',
    'Products', 'ProductFamilies', 'ProductRevisions',
    'Resources', 'ResourceGroups', 'ResourceCapabilities',
    'DataCollections', 'ESpecs',
    'ContainerHistory', 'DataCollectionHistory',
    'AuditLog', 'YieldHistory'
]

def scan_table_schema(conn, table_name: str) -> pd.DataFrame:
    """扫描指定表的字段结构，作为本体属性的来源"""
    return pd.read_sql(f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            CHARACTER_MAXIMUM_LENGTH,
            NUMERIC_PRECISION
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
    """, conn)

def scan_foreign_keys(conn) -> pd.DataFrame:
    """扫描外键关系，辅助发现本体关系"""
    return pd.read_sql("""
        SELECT
            fk.name                         AS fk_name,
            tp.name                         AS parent_table,
            cp.name                         AS parent_column,
            tr.name                         AS referenced_table,
            cr.name                         AS referenced_column
        FROM sys.foreign_keys fk
        JOIN sys.tables        tp ON fk.parent_object_id      = tp.object_id
        JOIN sys.tables        tr ON fk.referenced_object_id  = tr.object_id
        JOIN sys.foreign_key_columns fkc ON fk.object_id     = fkc.constraint_object_id
        JOIN sys.columns       cp ON fkc.parent_column_id    = cp.column_id
                                  AND cp.object_id           = tp.object_id
        JOIN sys.columns       cr ON fkc.referenced_column_id = cr.column_id
                                  AND cr.object_id           = tr.object_id
        WHERE tp.name IN ({})
    """.format(','.join(f"'{t}'" for t in CAMSTAR_TABLES)), conn)

def export_schema_for_llm(conn) -> str:
    """生成给 LLM 的结构摘要，用于本体草稿生成"""
    output = []
    for table in CAMSTAR_TABLES:
        schema = scan_table_schema(conn, table)
        cols = ', '.join(schema['COLUMN_NAME'].tolist())
        output.append(f"Table: {table}\nColumns: {cols}\n")
    return '\n'.join(output)
```

---

## 3. 阶段二：本体驱动目标库设计

### 3.1 设计原则

- 每个本体类对应一张目标表，表名前缀 `ont_`
- 所有表包含 `_source_id`（Camstar原始主键）和 `_loaded_at`（加载时间戳）
- 外键关系严格对应本体的对象属性（ObjectProperty）
- 指标表额外包含维度外键，便于分析查询

### 3.2 DDL 自动生成器

```python
# ddl_generator.py
# 从 Neo4j 本体自动生成目标库 DDL

from neo4j import GraphDatabase

TYPE_MAP = {
    'String':   'NVARCHAR(200)',
    'Text':     'NVARCHAR(MAX)',
    'Integer':  'INT',
    'Float':    'DECIMAL(18,6)',
    'Boolean':  'BIT',
    'DateTime': 'DATETIME',
    'Date':     'DATE'
}

def generate_ddl_from_ontology(driver) -> str:
    """读取 Neo4j 本体，生成 SQL Server DDL"""
    ddl_statements = []

    with driver.session() as session:
        # 查询所有本体类及其属性
        classes = session.run("""
            MATCH (c:OntologyClass)
            OPTIONAL MATCH (c)-[:HAS_PROPERTY]->(p:OntologyProperty)
            RETURN c.name AS class_name,
                   c.layer AS layer,
                   collect({
                       name: p.name,
                       dataType: p.dataType,
                       required: p.required
                   }) AS properties
            ORDER BY c.layer, c.name
        """)

        for record in classes:
            class_name = record['class_name']
            properties = record['properties']

            cols = [f"    {class_name.lower()}_id  NVARCHAR(200) PRIMARY KEY"]
            for prop in properties:
                if not prop['name']:
                    continue
                sql_type = TYPE_MAP.get(prop['dataType'], 'NVARCHAR(200)')
                nullable = '' if prop.get('required') else ' NULL'
                cols.append(f"    {prop['name'].lower():<30} {sql_type}{nullable}")

            # 标准审计列
            cols.append("    _source_id    NVARCHAR(200) NULL")
            cols.append("    _loaded_at    DATETIME      NOT NULL DEFAULT GETDATE()")

            ddl = (
                f"-- {class_name} ({record['layer']} Layer)\n"
                f"CREATE TABLE ont_{class_name} (\n"
                + ',\n'.join(cols)
                + "\n);\n"
            )
            ddl_statements.append(ddl)

        # 查询外键关系
        relations = session.run("""
            MATCH (from:OntologyClass)-[r:ONTOLOGY_RELATION]->(to:OntologyClass)
            WHERE r.cardinality IN ['MANY_TO_ONE', 'ONE_TO_ONE']
            RETURN from.name AS from_class,
                   to.name   AS to_class,
                   r.name    AS rel_name
        """)

        fk_statements = []
        for rel in relations:
            fk = (
                f"ALTER TABLE ont_{rel['from_class']} "
                f"ADD CONSTRAINT fk_{rel['from_class']}_{rel['to_class']} "
                f"FOREIGN KEY ({rel['to_class'].lower()}_id) "
                f"REFERENCES ont_{rel['to_class']} ({rel['to_class'].lower()}_id);"
            )
            fk_statements.append(fk)

    return '\n\n'.join(ddl_statements) + '\n\n-- Foreign Keys\n' + '\n'.join(fk_statements)
```

### 3.3 目标库核心表结构（手工验证版）

```sql
-- ════════════════════════════════
-- 配置层
-- ════════════════════════════════

CREATE TABLE ont_WorkflowDef (
    workflow_id      NVARCHAR(200) PRIMARY KEY,
    name             NVARCHAR(200) NOT NULL,
    revision         NVARCHAR(50),
    effective_date   DATE,
    description      NVARCHAR(MAX),
    _source_id       NVARCHAR(200),
    _loaded_at       DATETIME DEFAULT GETDATE()
);

CREATE TABLE ont_StepDef (
    step_id          NVARCHAR(200) PRIMARY KEY,  -- {workflow_id}::{step_name}
    workflow_id      NVARCHAR(200) NOT NULL REFERENCES ont_WorkflowDef(workflow_id),
    name             NVARCHAR(200) NOT NULL,
    sequence         INT NOT NULL,
    operation_id     NVARCHAR(200),
    resource_id      NVARCHAR(200),
    _source_id       NVARCHAR(200),
    _loaded_at       DATETIME DEFAULT GETDATE()
);

CREATE TABLE ont_ESpecDef (
    espec_id         NVARCHAR(200) PRIMARY KEY,
    name             NVARCHAR(200) NOT NULL,
    dc_id            NVARCHAR(200),
    data_type        NVARCHAR(50),
    low_limit        DECIMAL(18,6),
    high_limit       DECIMAL(18,6),
    uom              NVARCHAR(50),
    _source_id       NVARCHAR(200),
    _loaded_at       DATETIME DEFAULT GETDATE()
);

-- ════════════════════════════════
-- 事件层
-- ════════════════════════════════

CREATE TABLE ont_MoveEvent (
    event_id         NVARCHAR(200) PRIMARY KEY,
    container_name   NVARCHAR(200) NOT NULL,
    move_type        NVARCHAR(10)  NOT NULL,  -- MoveIn / MoveOut
    step_id          NVARCHAR(200) REFERENCES ont_StepDef(step_id),
    resource_id      NVARCHAR(200),
    product_id       NVARCHAR(200),
    event_ts         DATETIME     NOT NULL,
    qty              DECIMAL(18,4),
    shift_name       NVARCHAR(50),
    _loaded_at       DATETIME DEFAULT GETDATE()
);

CREATE TABLE ont_MeasureEvent (
    event_id         NVARCHAR(200) PRIMARY KEY,
    container_name   NVARCHAR(200) NOT NULL,
    espec_id         NVARCHAR(200) REFERENCES ont_ESpecDef(espec_id),
    step_id          NVARCHAR(200) REFERENCES ont_StepDef(step_id),
    data_value       DECIMAL(18,6),
    in_spec          BIT          NOT NULL,
    measure_ts       DATETIME     NOT NULL,
    _loaded_at       DATETIME DEFAULT GETDATE()
);

CREATE TABLE ont_ChangeEvent (
    change_id        NVARCHAR(200) PRIMARY KEY,
    object_type      NVARCHAR(100) NOT NULL,
    object_name      NVARCHAR(200) NOT NULL,
    field_name       NVARCHAR(100),
    old_value        NVARCHAR(MAX),
    new_value        NVARCHAR(MAX),
    change_ts        DATETIME     NOT NULL,
    author           NVARCHAR(100),
    reason           NVARCHAR(MAX),
    _loaded_at       DATETIME DEFAULT GETDATE()
);

-- ════════════════════════════════
-- 指标层
-- ════════════════════════════════

CREATE TABLE ont_YieldRecord (
    record_id        NVARCHAR(200) PRIMARY KEY,
    record_date      DATE         NOT NULL,
    line_name        NVARCHAR(100),
    product_id       NVARCHAR(200),
    step_id          NVARCHAR(200),
    shift_name       NVARCHAR(50),
    input_qty        DECIMAL(18,4),
    output_qty       DECIMAL(18,4),
    scrap_qty        DECIMAL(18,4),
    ncm_qty          DECIMAL(18,4),
    yield_rate       DECIMAL(8,6),  -- 0.000000 ~ 1.000000
    _loaded_at       DATETIME DEFAULT GETDATE()
);

CREATE TABLE ont_CycleTimeRecord (
    record_id        NVARCHAR(200) PRIMARY KEY,
    record_date      DATE         NOT NULL,
    step_id          NVARCHAR(200),
    product_id       NVARCHAR(200),
    line_name        NVARCHAR(100),
    avg_cycle_sec    DECIMAL(10,2),
    min_cycle_sec    DECIMAL(10,2),
    max_cycle_sec    DECIMAL(10,2),
    sample_count     INT,
    _loaded_at       DATETIME DEFAULT GETDATE()
);
```

---

## 4. 阶段三：本体驱动 ETL 开发

### 4.1 ETL 元数据配置（本体映射表）

```python
# etl_config.py
# 本体类 → ETL 映射配置，驱动整个数据加载逻辑

ONTOLOGY_ETL_MAP = {

    # ── 配置层 ──
    "WorkflowDef": {
        "type": "direct",
        "source_query": """
            SELECT
                Name              AS workflow_id,
                Name              AS name,
                Revision          AS revision,
                EffectiveDate     AS effective_date,
                Description       AS description,
                CAST(WorkflowId AS VARCHAR) AS _source_id
            FROM Workflows
        """,
        "target_table": "ont_WorkflowDef",
        "merge_key":    "workflow_id",
        "incremental":  False
    },

    "StepDef": {
        "type": "direct",
        "source_query": """
            SELECT
                wf.Name + '::' + ws.Name     AS step_id,
                wf.Name                      AS workflow_id,
                ws.Name                      AS name,
                ws.StepSequence              AS sequence,
                op.Name                      AS operation_id,
                r.Name                       AS resource_id,
                CAST(ws.StepId AS VARCHAR)   AS _source_id
            FROM WorkflowSteps ws
            JOIN Workflows   wf ON ws.WorkflowId  = wf.WorkflowId
            JOIN Operations  op ON ws.OperationId = op.OperationId
            LEFT JOIN Resources r ON ws.ResourceId = r.ResourceId
        """,
        "target_table": "ont_StepDef",
        "merge_key":    "step_id",
        "incremental":  False
    },

    "MoveEvent": {
        "type": "direct",
        "source_query": """
            SELECT
                CAST(HistoryId AS VARCHAR)   AS event_id,
                ContainerName                AS container_name,
                EventType                    AS move_type,
                WorkflowName + '::' + StepName AS step_id,
                ResourceName                 AS resource_id,
                ProductName                  AS product_id,
                EventTime                    AS event_ts,
                Qty                          AS qty,
                ShiftName                    AS shift_name
            FROM ContainerHistory
            WHERE EventType IN ('MoveIn', 'MoveOut')
            AND EventTime > :last_loaded
        """,
        "target_table":      "ont_MoveEvent",
        "merge_key":         "event_id",
        "incremental":       True,
        "incremental_field": "event_ts",
        "watermark_key":     "move_event_watermark"
    },

    "MeasureEvent": {
        "type": "direct",
        "source_query": """
            SELECT
                CAST(dc.HistoryId AS VARCHAR)     AS event_id,
                dc.ContainerName                  AS container_name,
                dc.ESpecName                      AS espec_id,
                dc.WorkflowName+'::'+dc.StepName  AS step_id,
                dc.DataValue                      AS data_value,
                CASE WHEN dc.DataValue BETWEEN es.LowLimit AND es.HighLimit
                     THEN 1 ELSE 0 END            AS in_spec,
                dc.CollectionTime                 AS measure_ts
            FROM DataCollectionHistory dc
            LEFT JOIN ESpecs es ON dc.ESpecName = es.Name
            WHERE dc.CollectionTime > :last_loaded
        """,
        "target_table":      "ont_MeasureEvent",
        "merge_key":         "event_id",
        "incremental":       True,
        "incremental_field": "measure_ts",
        "watermark_key":     "measure_event_watermark"
    },

    "YieldRecord": {
        "type": "aggregation",
        "aggregation_fn": "compute_yield_records",
        "target_table":   "ont_YieldRecord",
        "merge_key":      "record_id"
    },

    "CycleTimeRecord": {
        "type": "aggregation",
        "aggregation_fn": "compute_cycletime_records",
        "target_table":   "ont_CycleTimeRecord",
        "merge_key":      "record_id"
    }
}
```

### 4.2 ETL 引擎核心代码

```python
# etl_engine.py

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class OntologyETLEngine:
    def __init__(self, src_conn_str: str, tgt_conn_str: str):
        self.src = create_engine(src_conn_str)
        self.tgt = create_engine(tgt_conn_str)

    def get_watermark(self, key: str) -> datetime:
        """读取增量水位线"""
        with self.tgt.connect() as conn:
            result = conn.execute(text(
                "SELECT watermark FROM etl_watermarks WHERE entity_key = :key"
            ), {"key": key}).fetchone()
            return result[0] if result else datetime(2020, 1, 1)

    def set_watermark(self, key: str, ts: datetime):
        """更新增量水位线"""
        with self.tgt.connect() as conn:
            conn.execute(text("""
                MERGE etl_watermarks AS target
                USING (SELECT :key AS entity_key, :ts AS watermark) AS src
                ON target.entity_key = src.entity_key
                WHEN MATCHED THEN UPDATE SET watermark = src.watermark
                WHEN NOT MATCHED THEN INSERT (entity_key, watermark)
                    VALUES (src.entity_key, src.watermark);
            """), {"key": key, "ts": ts})
            conn.commit()

    def upsert(self, df: pd.DataFrame, table: str, merge_key: str):
        """MERGE 方式写入目标库"""
        if df.empty:
            return
        tmp_table = f"#tmp_{table}"
        df.to_sql(tmp_table, self.tgt, if_exists='replace', index=False)

        cols = ', '.join(df.columns)
        update_cols = ', '.join(
            f"t.{c} = s.{c}" for c in df.columns if c != merge_key
        )
        with self.tgt.connect() as conn:
            conn.execute(text(f"""
                MERGE {table} AS t
                USING {tmp_table} AS s ON t.{merge_key} = s.{merge_key}
                WHEN MATCHED THEN UPDATE SET {update_cols}
                WHEN NOT MATCHED THEN INSERT ({cols}) VALUES ({cols});
            """))
            conn.commit()

    def run_entity(self, entity_name: str):
        """执行单个本体类的 ETL"""
        from etl_config import ONTOLOGY_ETL_MAP
        cfg = ONTOLOGY_ETL_MAP[entity_name]
        logger.info(f"Running ETL for: {entity_name}")

        if cfg['type'] == 'direct':
            params = {}
            if cfg.get('incremental'):
                watermark = self.get_watermark(cfg['watermark_key'])
                params['last_loaded'] = watermark

            df = pd.read_sql(text(cfg['source_query']), self.src, params=params)
            self.upsert(df, cfg['target_table'], cfg['merge_key'])

            if cfg.get('incremental') and not df.empty:
                new_watermark = df[cfg['incremental_field']].max()
                self.set_watermark(cfg['watermark_key'], new_watermark)

        elif cfg['type'] == 'aggregation':
            from aggregations import compute_yield_records, compute_cycletime_records
            fn = {'compute_yield_records': compute_yield_records,
                  'compute_cycletime_records': compute_cycletime_records}[cfg['aggregation_fn']]
            df = fn(self.src)
            self.upsert(df, cfg['target_table'], cfg['merge_key'])

        logger.info(f"  → Loaded {len(df) if not df.empty else 0} rows")

    def run_full_load(self):
        """全量初始化（顺序按依赖关系）"""
        ordered = [
            # 配置层（先父后子）
            'WorkflowDef', 'OperationDef', 'ResourceDef',
            'ProductDef', 'DataCollectionDef', 'ESpecDef', 'StepDef',
            # 事件层
            'ChangeEvent', 'DowntimeEvent', 'MoveEvent', 'MeasureEvent',
            # 指标层
            'YieldRecord', 'CycleTimeRecord'
        ]
        for entity in ordered:
            self.run_entity(entity)

    def run_incremental(self):
        """增量同步（每小时/每天触发）"""
        incremental_entities = ['MoveEvent', 'MeasureEvent', 'ChangeEvent',
                                'DowntimeEvent', 'YieldRecord', 'CycleTimeRecord']
        for entity in incremental_entities:
            self.run_entity(entity)
```

### 4.3 聚合计算模块

```python
# aggregations.py

import pandas as pd
from sqlalchemy import text

def compute_cycletime_records(src_engine) -> pd.DataFrame:
    """MoveIn-MoveOut 配对，计算步骤节拍"""
    df = pd.read_sql(text("""
        SELECT
            mo.ProductName,
            mo.WorkflowName + '::' + mo.StepName  AS step_id,
            mo.LineName,
            CAST(mo.EventTime AS DATE)             AS record_date,
            DATEDIFF(SECOND, mi.EventTime, mo.EventTime) AS cycle_sec
        FROM ContainerHistory mo
        JOIN ContainerHistory mi
            ON  mo.ContainerName = mi.ContainerName
            AND mo.StepName      = mi.StepName
            AND mi.EventType     = 'MoveIn'
        WHERE mo.EventType = 'MoveOut'
    """), src_engine)

    agg = df.groupby(['product_name', 'step_id', 'line_name', 'record_date']).agg(
        avg_cycle_sec=('cycle_sec', 'mean'),
        min_cycle_sec=('cycle_sec', 'min'),
        max_cycle_sec=('cycle_sec', 'max'),
        sample_count=('cycle_sec', 'count')
    ).reset_index()

    agg['record_id'] = (
        agg['record_date'].astype(str) + '::' +
        agg['step_id'] + '::' +
        agg['product_name']
    )
    return agg

def compute_yield_records(src_engine) -> pd.DataFrame:
    """良率聚合计算"""
    df = pd.read_sql(text("""
        SELECT
            ProductName, WorkflowName+'::'+StepName AS step_id,
            LineName, ShiftName,
            CAST(EventDate AS DATE) AS record_date,
            SUM(InputQty)  AS input_qty,
            SUM(OutputQty) AS output_qty,
            SUM(ScrapQty)  AS scrap_qty,
            SUM(NCMQty)    AS ncm_qty
        FROM YieldHistory
        GROUP BY ProductName, WorkflowName, StepName, LineName, ShiftName, EventDate
    """), src_engine)

    df['yield_rate'] = df['output_qty'] / df['input_qty'].replace(0, float('nan'))
    df['record_id'] = (
        df['record_date'].astype(str) + '::' +
        df['line_name'] + '::' +
        df['product_name'] + '::' +
        df['step_id']
    )
    return df
```

---

## 5. LLM 辅助本体构建策略

### 5.1 为什么适合用 LLM + Wiki

| 传统方式 | LLM + Wiki 方式 |
|---|---|
| 人工阅读文档，逐字理解 | LLM 批量理解，输出结构化草稿 |
| 依赖专家，耗时数周 | 数小时生成初稿，人工审核 |
| 容易遗漏隐含关系 | LLM 可发现字段间潜在语义关联 |
| 文档和本体割裂 | 文档即输入，本体即输出，可溯源 |

### 5.2 LLM 本体生成工作流

```
Step 1: 文档准备
  ├── Camstar 官方 Wiki / Help 文档（PDF/HTML）
  ├── SQL Server 表结构导出（INFORMATION_SCHEMA）
  └── Studio 建模对象列表（截图或导出）
         │
         ▼
Step 2: 输入给 LLM（分批处理）
  ├── Prompt A: 从 Wiki 提取"类"定义
  ├── Prompt B: 从表结构推断"属性"定义
  └── Prompt C: 从外键和业务规则推断"关系"
         │
         ▼
Step 3: LLM 输出本体草稿（OWL/JSON/Cypher 格式）
         │
         ▼
Step 4: 人工审核
  ├── 验证类名是否准确
  ├── 验证属性类型是否正确
  └── 补充 LLM 遗漏的业务关系
         │
         ▼
Step 5: 写入 Neo4j，生成正式本体
```

### 5.3 Prompt 模板

#### Prompt A：从 Wiki 提取类定义

```
你是一个本体工程师，正在为 Camstar MES 系统建立本体。

以下是 Camstar 官方文档中关于 [WorkflowDef] 的描述：
---
{粘贴 Wiki 内容}
---

请提取以下信息，以 JSON 格式输出：
{
  "className": "类名（英文）",
  "chineseName": "中文名",
  "description": "简洁的类描述（1-2句）",
  "layer": "Config / Event / Metric 三选一",
  "dataProperties": [
    {"name": "属性名", "dataType": "String/Integer/Float/Boolean/DateTime", "required": true/false, "description": "说明"}
  ],
  "relatedClasses": ["可能关联的其他类名"]
}
```

#### Prompt B：从表结构推断属性

```
以下是 Camstar SQL Server 中 [Workflows] 表的字段结构：
---
{粘贴字段列表}
---

已知该表对应本体类 WorkflowDef。

请将每个字段映射到本体属性，输出格式：
[
  {
    "sourceColumn": "原始字段名",
    "ontologyProperty": "本体属性名（驼峰命名）",
    "dataType": "String/Integer/Float/Boolean/DateTime",
    "required": true/false,
    "semanticNote": "该字段的业务含义"
  }
]

忽略系统内部字段（如 ObjectId, LastUpdated 等审计字段）。
```

#### Prompt C：推断本体关系

```
以下是 Camstar 数据库的外键关系：
---
{粘贴外键扫描结果}
---

以及以下业务描述：
"一个 WorkflowDef 包含多个有序的 StepDef，每个 StepDef 使用一个 OperationDef 并分配给一个 ResourceDef。"

请推断本体关系，输出格式：
[
  {
    "fromClass": "源类",
    "toClass": "目标类",
    "relationName": "关系名（全大写下划线）",
    "cardinality": "ONE_TO_ONE / ONE_TO_MANY / MANY_TO_MANY",
    "attributes": ["关系上的属性，如 sequence"],
    "semanticNote": "该关系的业务含义"
  }
]
```

### 5.4 本体质量验证清单

生成本体草稿后，逐项验证：

- [ ] 每个 Camstar Modeling Object 都有对应的本体类
- [ ] 每个关键业务属性（name, revision, limit）都有映射
- [ ] 配置层类之间的结构关系完整
- [ ] 事件类都有时间戳属性（ts/eventTs）
- [ ] 指标类都有维度外键（产品/产线/步骤/日期）
- [ ] 没有孤立节点（每个类至少有一个关系）
- [ ] 关系基数（cardinality）与业务规则一致

---

## 6. 数据流与增量同步设计

### 6.1 全量 vs 增量策略

| 数据类型 | 同步策略 | 触发频率 | 说明 |
|---|---|---|---|
| 配置层（WorkflowDef等） | 全量覆盖 | 每天一次（凌晨） | 数据量小，变更少 |
| 变更事件（ChangeEvent） | 增量追加 | 每小时 | 按 ChangeTime 水位线 |
| 流转事件（MoveEvent） | 增量追加 | 每小时 | 按 EventTime 水位线 |
| 测量事件（MeasureEvent） | 增量追加 | 每小时 | 按 CollectionTime 水位线 |
| 指标层（YieldRecord等） | 增量重算 | 每天（T+1） | 按日聚合，覆盖当日 |

### 6.2 水位线管理表

```sql
-- 在目标库创建水位线管理表
CREATE TABLE etl_watermarks (
    entity_key   NVARCHAR(100) PRIMARY KEY,
    watermark    DATETIME     NOT NULL,
    last_run     DATETIME     DEFAULT GETDATE(),
    rows_loaded  INT          DEFAULT 0
);

-- 初始化水位线
INSERT INTO etl_watermarks (entity_key, watermark) VALUES
('move_event_watermark',    '2023-01-01'),
('measure_event_watermark', '2023-01-01'),
('change_event_watermark',  '2023-01-01'),
('downtime_event_watermark','2023-01-01');
```

### 6.3 调度设计（无 Airflow 版本）

```python
# scheduler.py
# 使用 Python schedule 库，适合无 Airflow 环境

import schedule
import time
from etl_engine import OntologyETLEngine

engine = OntologyETLEngine(src_conn_str=SRC_CONN, tgt_conn_str=TGT_CONN)

# 每小时增量同步事件数据
schedule.every().hour.do(engine.run_incremental)

# 每天凌晨2点全量刷新配置层
schedule.every().day.at("02:00").do(lambda: [
    engine.run_entity('WorkflowDef'),
    engine.run_entity('StepDef'),
    engine.run_entity('ESpecDef'),
    engine.run_entity('ResourceDef'),
])

# 每天凌晨3点计算指标层
schedule.every().day.at("03:00").do(lambda: [
    engine.run_entity('YieldRecord'),
    engine.run_entity('CycleTimeRecord'),
])

if __name__ == '__main__':
    print("ETL Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)
```

---

## 7. 目录结构与代码规范

```
camstar_ontology_etl/
│
├── README.md
├── requirements.txt
│
├── ontology/                      # 阶段一：本体管理
│   ├── schema/
│   │   ├── camstar_ontology.cypher    # Neo4j 本体初始化脚本
│   │   └── camstar_ontology.ttl       # OWL/Turtle 格式（n10s 导出）
│   ├── explorer/
│   │   └── ontology_explorer.py       # SQL Server 表结构扫描
│   ├── llm_prompts/
│   │   ├── prompt_class.txt           # 提取类的 Prompt 模板
│   │   ├── prompt_property.txt        # 提取属性的 Prompt 模板
│   │   └── prompt_relation.txt        # 推断关系的 Prompt 模板
│   └── validator/
│       └── ontology_validator.py      # 本体质量验证
│
├── ddl/                           # 阶段二：目标库 DDL
│   ├── generator/
│   │   └── ddl_generator.py           # 从本体自动生成 DDL
│   ├── migrations/
│   │   ├── V001__init_config_layer.sql
│   │   ├── V002__init_event_layer.sql
│   │   └── V003__init_metric_layer.sql
│   └── indexes/
│       └── create_indexes.sql
│
├── etl/                           # 阶段三：ETL 引擎
│   ├── config/
│   │   ├── etl_config.py              # 本体→ETL 映射配置
│   │   └── db_config.py               # 数据库连接配置
│   ├── extractor/
│   │   ├── config_extractor.py
│   │   ├── event_extractor.py
│   │   └── ontology_explorer.py
│   ├── aggregations/
│   │   └── aggregations.py            # 指标层聚合计算
│   ├── loader/
│   │   └── neo4j_loader.py            # 写入 Neo4j（可选）
│   ├── etl_engine.py                  # ETL 引擎核心
│   └── scheduler.py                   # 调度管理
│
├── analysis/                      # 分析查询模板
│   ├── change_impact.cypher           # 变更影响分析
│   ├── efficiency_compare.sql         # 效率对比分析
│   └── quality_trace.sql              # 质量根因追溯
│
└── tests/
    ├── test_ontology.py
    ├── test_etl_engine.py
    └── test_aggregations.py
```

---

## 8. 里程碑与验收标准

### Milestone 1：本体建立（Week 1-2）

**交付物**:
- Neo4j 本体图，包含全部 Camstar 类、属性、关系
- 本体导出文件（`.ttl` / `.cypher`）
- 本体说明文档

**验收标准**:
- [ ] 覆盖 Camstar 全部 Modeling Object（≥ 10 个配置类）
- [ ] 每个类有中英文名、来源表、核心属性
- [ ] 类之间关系完整，无孤立节点
- [ ] LLM 生成草稿 + 人工验证完成

### Milestone 2：目标库建设（Week 3）

**交付物**:
- 目标库 DDL 脚本（配置层 + 事件层 + 指标层）
- DDL 自动生成器（`ddl_generator.py`）

**验收标准**:
- [ ] 所有本体类均有对应目标表
- [ ] 外键关系与本体关系一致
- [ ] 审计列（`_source_id`, `_loaded_at`）完整
- [ ] 目标库可成功创建，无 DDL 错误

### Milestone 3：ETL 开发（Week 4-5）

**交付物**:
- ETL 引擎代码
- 全量加载脚本
- 增量同步脚本

**验收标准**:
- [ ] 全量加载成功，数据行数与源库一致（误差 < 0.1%）
- [ ] 增量同步正确，水位线更新无误
- [ ] CycleTime 计算逻辑验证（MoveIn-MoveOut 配对）
- [ ] InSpec 判断与 ESpec 上下限一致

### Milestone 4：分析验证（Week 6）

**交付物**:
- 端到端分析查询模板库
- 分析结果报告

**验收标准**:
- [ ] 变更影响分析：能查出变更前后良率变化
- [ ] 效率对比分析：能比较两产品在同线体的节拍差异
- [ ] 质量追溯：能从异常测量值追溯到步骤和设备

---

## 9. 风险与注意事项

### 9.1 技术风险

| 风险 | 影响 | 应对策略 |
|---|---|---|
| Camstar 表名因版本不同 | ETL 查询失败 | 先用 `sys.tables` 探索，再写查询 |
| MoveIn/MoveOut 配对不完整 | CycleTime 计算错误 | 增加配对成功率监控，记录孤立事件 |
| AuditLog 未开启 | 变更事件缺失 | 检查 Camstar 审计配置，备选方案用快照对比 |
| 源库大表全量抽取慢 | ETL 超时 | 按日期分批抽取，使用 NOLOCK 提示 |

### 9.2 本体建立注意事项

- **版本管理**：本体变更需版本化，不可随意修改已有类名（会影响 ETL 配置）
- **命名规范**：类名用 PascalCase（WorkflowDef），属性用 camelCase（lowLimit），关系用 UPPER_SNAKE（HAS_STEP）
- **抽象类不建表**：`ConfigEntity`、`EventEntity`、`MetricEntity` 仅为本体组织用，不生成 DDL
- **LLM 输出需人工验证**：重点验证上下限字段类型（Float vs String）和关系基数

### 9.3 ETL 注意事项

- **加载顺序**：严格按本体依赖顺序加载（父类先于子类，配置层先于事件层）
- **UPSERT 而非 INSERT**：所有加载使用 MERGE，保证幂等性，可重复执行
- **不删除历史数据**：事件层只追加，不覆盖，配置层用软删除（增加 `is_active` 列）

---

*文档生成时间：{today}*  
*下一步：按本文档进行 Milestone 1 本体建立，推荐从 Studio 建模界面截图 + SQL Server 表结构扫描开始，配合 LLM Prompt 快速生成本体草稿。*
