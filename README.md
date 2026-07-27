# Siemens Opcenter MES (Camstar) 本体知识图谱 & Graph-RAG 智能协作平台

> **基于 Siemens Opcenter Execution (Camstar) 建模逻辑的全栈知识图谱、数字孪生场景规划及 Graph-RAG 智能协作问答系统。**

本平台是一个专为制造执行系统 (MES) 领域设计的全栈知识图谱与智能问答应用。系统将 Camstar 的建模对象（如在制品 Container、工序 Spec、工作中心 WorkCenter、工艺路线 Workflow 等）映射为本体图谱（Ontology Graph），并利用 **Neo4j 图数据库**进行存储。前端采用最新的 **AntV G6 v5** 提供高性能的可视化拓扑呈现，并整合 **DeepSeek LLM** 与 **ChromaDB 本地向量库**，构建出支持行业/产品线隔离的 **Graph-RAG 智能问答**与**数字化场景工坊 (Scenario Studio & Planner)**。

---

## 🌟 核心特性与业务价值

### 1. 全面的 MES 核心本体建模 (31+ 模块)

* **业务域覆盖**：全面覆盖 Workflow (工艺路线)、Operation (工序交易)、Spec (规范)、WorkCenter (工作中心)、Product (产品及家族)、Quality (品质事件/CAPA)、BOM/ERPBOM、Resource (资源/机台)、Employee/Role (人员与角色) 以及全新的 **SPC (统计过程控制)** 等核心物理与逻辑建模对象。
* **物理一致性对齐**：本体严格遵循物理数据库定义。通过 `docs/Database_Tables.csv` (CDO列表) 与 `docs/Database_Fields.csv` (字段定义) 作为唯一事实来源开展映射。字段自动转为 camelCase 驼峰命名，外键字段规范化映射为 `Navigation` 类型。

### 2. 行业/产品线隔离与参数化支持

* **多行业隔离**：支持新能源电池 (Battery)、汽车装配 (Automotive)、通用制造 (General) 等多条典型产品线/行业的配置，系统默认以 `general` (通用/基准) 行业作为缺省配置。
* **场景与参数对齐**：各行业的预设场景、AI Planner 生成规则、RAG 问答背景等均与当前选定的行业进行强关联，实现真正的参数化与定制化。
* **通用场景融合**：在 Scenario Studio 与 Planner 中，提供“是否包含通用场景”的选择开关，用户可在查看特定行业场景的同时，平滑地叠加基准场景作为参考，数据在本地 `localStorage` 进行持久化存储。

### 3. Graph-RAG 流式智能问答 (RAG Co-Pilot)

* **流式 SSE 交互**：问答助手采用 Server-Sent Events (SSE) 协议，实现 DeepSeek 模型超低延迟的流式文字打字机输出。
* **智能图谱检索**：深度集成 Neo4j Cypher 拓扑关系检索与 ChromaDB 向量语义匹配。问答引擎自动解析用户提问，提取本体节点关键字，从 Neo4j 中拉取局部子图定义注入 Prompt，大幅降低大模型的幻觉率。
* **原生节点提及 (@Mention)**：聊天输入框支持键入 `@` 字符触发实时联想下拉，允许模糊搜索图谱中的 399+ 个类节点。选中后插入 `[[ClassName]]` 特征标记，指引问答引擎优先提取该类在图谱中的邻居子图及字段语义。

### 4. 数字化场景工坊 & AI Planner

* **双步法工艺规划**：AI Planner 会依据现场痛点推荐由『Step 1: 触发 - 业务事件』和『Step 2: 校验 - 动作拦截』组成的规范化控制链，并配合 SQL 规则进行业务防错演示。
* **拓扑自愈机制 (Twin Healing)**：当用户生成的场景步骤中包含的实体类 (Twins) 在真实图谱中存在孤立或未连接状态时，系统会基于 Neo4j 自动运行最短路径自愈算法，将桥接类（如 Resource, Spec, WipMessageDefMgr 等）自动提取并融入 Twins 列表，确保蓝图的物理连接性为 100%。

### 5. 极致渲染与性能优化

* **前端差量渲染更新 (`_applyStates`)**：摒弃传统的全量重绘机制。引入状态对比缓存，每次点击仅对发生改变的节点及连线应用高亮/置灰等样式变化，点击响应时间从 300ms 骤降至 **< 30ms**。
* **大规模视口裁剪 (Viewport Culling)**：在 G6 图谱渲染中，视口之外的文字标签和阴影效果会自动裁剪并隐藏，只在 Hover 时动态加载，支持 400+ 节点、1300+ 边在低配设备上流畅无卡顿渲染。
* **UNWIND 批量数据装载**：Neo4j 数据导入完全重构为 Cypher `UNWIND` 批量装载机制。装载网络往返开销降低 99.9%，实现 1300+ 条实体边数秒内一键部署入库。

---

## 🏗️ 系统架构

系统由前端展示层、FastAPI 路由网关、本体定义层、双数据库（Neo4j 图数据库 + ChromaDB 向量数据库）及 LLM 推理引擎共同构成：

```
                              ┌─────────────────────────────────────────────────────────────┐
                              │                       前端浏览器 (Browser)                   │
                              │ ┌─────────────────┐ ┌───────────────────┐ ┌────────────────┐│
                              │ │  G6 拓扑图谱     │ │  场景工坊 / 蓝图  │ │ 问答助手       ││
                              │ │  (app.js WebGL) │ │  (studio/planner) │ │ (流式 @Mention)││
                              │ └─────────────────┘ └───────────────────┘ └────────────────┘│
                              └──────────────────────────────┬──────────────────────────────┘
                                                             │ HTTP / SSE (FastAPI Port: 5050)
                              ┌──────────────────────────────┴──────────────────────────────┐
                              │                    FastAPI Web Server (server.py)           │
                              │  /api/graph/*        /api/wiki/*      /api/scenarios/*      │
                              └───────────┬───────────────────┬───────────────────┬─────────┘
                                          │                   │                   │
                     ┌────────────────────┴───┐    ┌──────────┴──────────┐   ┌────┴───────────────┐
                     │   Neo4j 图数据库        │    │ ChromaDB 本地向量库  │   │  DeepSeek LLM API  │
                     │  (399+ 类, 1300+ 关系)  │    │ (文档章节 + 场景数据)│   │  (流式多轮对话生成)  │
                     │  规范索引: 10 大约束   │    │ 路径: data/vector_  │   │                    │
                     │                        │    │       store/ (已提交)│   │                    │
                     └────────────────────────┘    └─────────────────────┘   └────────────────────┘
```

---

## 📁 目录结构说明

```
CamstarOntology/
├── .env.example                 # 环境变量模板文件
├── .gitignore                   # Git 忽略配置（已配置 data/vector_store 提交追踪）
├── requirements.txt             # 项目 Python 依赖声明
├── README.md                    # 本文档
├── AGENTS.md                    # 代理开发与开发流指南（含核心工作流及规范约束）
├── CLAUDE.md                    # IDE 指令快捷参考
├── run_all_builders.py          # [NEW] 一键重建与验证本地本体的辅助脚本
├── run_etl_full.py              # MES 业务数据全量/增量 ETL 装载管线
│
├── docs/                        # 物理数据库 Schema 与设计事实文档 (只读来源)
│   ├── Database_Tables.csv      # Camstar CDO（类名）物理表映射清单
│   ├── Database_Fields.csv      # CDO 字段、数据类型及物理外键关联定义
│   └── ontology_csv_validation_report.md  # 物理一致性自动校验结果报告
│
├── data/                        # 🗄️ 系统本地持久化数据层
│   └── vector_store/            # ChromaDB 向量数据库持久化目录（已包含预构建的向量索引数据）
│       ├── chroma.sqlite3       # 向量元数据 SQLite 文件
│       └── ...                  # 向量 HNSW 索引二进制文件
│
├── src/                         # 🐍 后端核心业务源码
│   ├── ontology/                # 本体定义与管理中心
│   │   ├── wiki_kb/             # 30+ 模块本体的原始定义数据
│   │   │   ├── *_ontology.json  # 模块本体的类、属性、关系声明
│   │   │   ├── *_modeling.md    # 中英文本体建模设计原理文档
│   │   │   ├── cross_module_ontology.json  # 跨模块拓扑关联定义汇总
│   │   │   └── product_lines.json  # 行业/产品线定义数据 (Semiconductor, Battery等)
│   │   ├── loader/
│   │   │   └── neo4j_loader.py  # JSON 本体 -> Neo4j 的 UNWIND 高效批量装载器
│   │   └── wiki_manager.py      # 关系 Wiki 生成、读取与 product_lines 管理核心引擎
│   │
│   ├── qa/                      # RAG 问答与大模型交互引擎
│   │   ├── engine.py            # RAG 编排、ChromaDB 混合多路召回与对话处理
│   │   ├── graph_retriever.py   # Neo4j 拓扑子图抽取与关联路径检索器
│   │   ├── vectorizer.py        # PDF 文档解析、Overlap 切片与 ChromaDB 向量化构建器
│   │   ├── prompt_builder.py    # LLM 系统与用户 Prompt 模板组装器
│   │   └── logger.py            # 多轮对话审计日志记录器 (支持本地日期归档与查询)
│   │
│   └── etl/                     # 数据抽取与同步模块 (MES 生产数据到知识图谱)
│
├── scripts/                     # 🛠️ 运维与系统初始化脚本
│   ├── rebuild_indexes.py       # Neo4j 规范索引重建脚本 (包含 10 大全文/唯一约束索引)
│   └── validate_ontology_vs_csv.py  # 物理一致性校验器，比对物理 CSV 结构与 JSON 本体定义
│
└── web/                         # 🌐 前端 UI 与 API 宿主服务
    ├── server.py                # FastAPI 启动服务入口
    ├── shared.py                # Neo4j 驱动共享、ChromaDB 预热加载及模块类别着色配置
    └── routers/                 # API 业务模块化路由
    │   ├── graph.py             # G6 图谱拓扑、节点详情、统计信息 API
    │   ├── wiki.py              # Wiki Markdown 读写、单条/批量 AI Wiki 生成 API
    │   ├── chat.py              # 问答助手 API 与多轮对话日志查询 API
    │   └── scenarios.py         # 场景管理、场景问答RAG、AI Planner 生成与拓扑自愈 API
    └── static/                  # 静态前端资源 (AntV G6 v5, Vanilla JS, CSS3)
        ├── index.html           # 本体图谱与对话主页面
        ├── industry.html        # 行业/产品线配置管理页面
        ├── planner.html         # AI Planner 业务防错场景规划页面
        ├── studio.html          # 场景工坊展示与配置页面
        ├── logs.html            # 对话审计日志查看页面
        ├── app.js               # 图谱渲染、Combo 展开、差量动画及布局算法
        ├── chat.js              # 流式问答渲染、原生提及 (@Mention) 与节点跳转交互
        └── style.css            # 扁平蓝黑色工业质感 CSS 主题系统
```

---

## 🚀 快速开始与部署指南

对于新机器部署或者由于变更需要进行的数据迁移，可以使用以下指南快速恢复并运行整个平台。

### 1. 环境准备

确保目标机器已安装以下软件：

* **Python**: `≥ 3.10`（推荐 3.10 或 3.11）
* **Neo4j**: `≥ 5.x`（支持 Community/Enterprise 社区版及企业版均可）
* **支持 WebGL 的浏览器**: （推荐使用 Google Chrome, Microsoft Edge）

### 2. 获取源码与虚拟环境配置

```bash
# 克隆项目到本地
git clone https://github.com/yanghengde/CamstarOntology.git
cd CamstarOntology

# 创建 Python 虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux / macOS:
# source venv/bin/activate

# 升级 pip 并安装核心依赖项
pip install -r requirements.txt
```

### 3. 环境变量配置

复制并重命名配置文件：

```bash
copy .env.example .env       # Windows
# cp .env.example .env       # Linux / macOS
```

使用文本编辑器修改 `.env` 文件的值：

```ini
# Neo4j 图数据库连接地址及密码
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_secure_password

# DeepSeek API 密钥与端点配置 (用于问答与 Planner)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

---

## 💾 数据库迁移与数据同步指南 (部署核心)

新部署一台机器时，如何将已有的**图数据库 (Neo4j)** 和**向量数据库 (ChromaDB)** 的数据完整同步过去？

### 💡 方案 A：直接克隆免配部署 (ChromaDB 本地向量库)

为简化部署流程，系统的 ChromaDB 向量数据库（存放有 Camstar 官方文档的全部切片及场景数据，大小约 15MB 左右）已经全部被追踪并提交到了 Git 仓库中，路径为：

* `data/vector_store/`

**新机器部署时：**

* 只要通过 `git clone` 拉取了最新代码，ChromaDB 就已经存在于你的本地。
* 在运行系统时，FastAPI 后端会在后台自动读取并装载 `data/vector_store/` 内的向量索引文件，**无需重新下载 Embedding 模型或重新向量化切片**，即可直接开始 Graph-RAG 对话。
* 如果后续需要重新构建向量库，可以运行以下命令从 PDF 重新构建：
  ```bash
  python src/qa/vectorizer.py
  ```

### 💡 方案 B：从本体 JSON 极速重构 Neo4j 数据

我们不需要像传统关系型数据库那样导出一个巨大的 SQL 备份。得益于本体定义的高度可读性和装载器强大的批量合并能力，你可以随时通过几条命令在几秒内在新 Neo4j 数据库上重新生成所有的类、属性和 1300+ 条关系边。

**执行步骤：**

1. **启动 Neo4j 服务**：确保新机器上的 Neo4j 服务已启动，且已根据 `.env` 配置好用户名和密码。
2. **校验本体文件规范性**（可选）：
   ```bash
   python scripts/validate_ontology_vs_csv.py
   ```

   这会比对 `docs/` 下的 CSV 表和物理字段，检查是否存在未对齐的类型或缺失的 Navigation 属性。
3. **重建图数据库规范索引**：
   ```bash
   python scripts/rebuild_indexes.py
   ```

   *作用：在 Neo4j 中创建唯一性约束（如 `unique_ontology_class_name`、`unique_ontology_property`）以防脏数据生成，并创建全文索引以加速大模型的模糊检索。*
4. **批量 UNWIND 写入本体数据**：
   ```bash
   python src/ontology/loader/neo4j_loader.py
   ```

   *作用：解析 `src/ontology/wiki_kb/` 下的所有本体 JSON，打包通过 Cypher UNWIND 批量向 Neo4j 写入 399 个 Class 节点、4800+ 属性及关系边，全程仅需 2~3 秒。*

---

## 🏃 启动 Web 系统

一切就绪后，通过以下命令启动 FastAPI 服务器：

```bash
python web/server.py
```

* 服务器将运行在 `http://localhost:5050` 上。
* 浏览器访问 `http://localhost:5050` 即可看到主页。
* 访问 `http://localhost:5050/static/industry.html` 访问行业管理页面。
* 访问 `http://localhost:5050/static/studio.html` 访问场景工坊。
* 访问 `http://localhost:5050/static/planner.html` 访问 AI Planner。
* 访问 `http://localhost:5050/logs` 查看用户对话审计日志。

---

## 🎮 页面交互与功能使用指南

### 🌐 1. 本体知识图谱主页 (`index.html`)

* **拓扑大图渲染**：展示了系统 399 个节点和 1300 条关系边的全景。
* **Layout 布局一键切换**：支持 `Dagre (层级排列)`、`Force (力导向扩散)`、`Radial (辐射圆环)` 布局，在大图右上方可以自由切换。
* **Combo 分组聚合**：开启 Combo 模式后，节点会按 Workflow、Operation 等 31 个大类收纳到各自的分组盒子里，方便进行宏观层级的业务结构审阅。
* **邻域差量高亮**：点击任何节点（例如 `Container`），系统会在 **30ms 内**将该节点及其一阶邻边、邻近节点保持彩色高亮，将其余无关节点淡化置灰；右侧抽屉式详情面板会滑出，显示其物理 CDOName、中文名称、数据属性及入向/出向外键关联。

### 💬 2. RAG 智能对话侧栏 (流式 + @提及)

* 在图谱右侧的问答面板输入您想了解的问题，如：`什么是 WIPMessageDefMgr 并在制品是如何挂起的？`
* 键入 `@` 字符会激活图谱实体的模糊联想菜单，选中后双括号包裹（如 `[[Container]]`），大模型会针对该实体相关的邻域知识开展精准回答。
* **智能高亮跳转**：AI 回答中的实体名（或场景 ID `[SC_281]`）在前端会自动转换成蓝色链接。点击链接，图谱会自动平滑移动视口（Focus & Pan To）到目标节点并触发高亮，实现“看图问答，问答触图”的双向交互。

### ⚙️ 3. 行业/产品线配置管理 (`industry.html`)

* 用户可在该页面定义不同的产品线/行业参数（如行业代号、名称、描述、主题颜色、显示图标）。
* 切换页面顶部的行业（如“半导体”或“新能源”），主页图谱及各子页面的所有请求都将附带 `?industry=industry_id` 参数。

### 🛠️ 4. 数字化场景工坊 (`studio.html`)

* **场景总览卡片**：列出当前行业下配置的数字化映射防错场景（如 `SC_001. 在制品MoveOut时校验Resource状态`）。
* **通用场景叠加控制**：提供一个 **“包含通用场景”** 的勾选框。如果勾选，不仅会显示当前行业专属的场景，还会把 `general` 行业的通用场景合并排序显示；如果不勾选，则只显示当前行业专有场景。此状态会自动同步到 `localStorage` 中并在刷新后保持。
* **新建场景与拓扑校验**：在此可以手动输入场景 ID、场景名称、核心业务描述，定义工步 (Step 1 触发, Step 2 校验)，声明 Twins（涉及的图元类）。点击保存后，场景定义将被序列化保存为 JSON 文件，并同步写入 ChromaDB 向量库中。

### 🤖 5. AI Planner 防错场景生成 (`planner.html`)

* **对话式业务梳理**：通过输入一段工厂实际痛点（如：`我们经常有员工在未经过培训的情况下，使用了错误的工装夹具完成了 MoveIn 交易，希望能进行拦截`），LLM 会根据本地 RAG 获取的最接近场景，并参考 Neo4j 图数据库中类与类的真实物理连接关系，为您量身规划一套双工步防错场景。
* **蓝图还原与拓扑自愈**：生成的场景会自动重画为前端的数字孪生工步卡片，并在后台通过 Neo4j 数据库自动执行自愈校验，如发现 Twins 缺失桥接关系（比如用户只写了 `Container` 和 `Resource`，但没写它们在物理表中的外键关联媒介 `Spec`），系统会自动修复并在前端卡片中进行提示。

---

## 📝 完整 REST API 接口定义

FastAPI 后端网关对外暴露了 4 大核心路由组，以下为它们的详细定义：

### 📁 1. 图谱拓扑接口 (`web/routers/graph.py`)

#### `GET /api/graph/overview`

* **功能**：获取全量图谱的节点、连线与 Combo 划分（仅传输核心元数据，传输性能优秀）。
* **响应格式**：
  ```json
  {
    "nodes": [
      { "id": "Container", "data": { "label": "Container", "chineseName": "容器", "layer": "Execution", "module": "container" } }
    ],
    "edges": [
      { "source": "Container", "target": "Spec", "data": { "label": "Spec", "cardinality": "0..1" } }
    ],
    "combos": [
      { "id": "container", "data": { "label": "Container" } }
    ]
  }
  ```

#### `GET /api/graph/class/{class_name}`

* **功能**：查询特定类节点的详细属性定义、入向和出向关联边（支持 `Cache-Control` 强缓存以提升性能）。
* **响应格式**：
  ```json
  {
    "className": "Container",
    "properties": [
      { "name": "isFrozen", "dataType": "Boolean", "description": "是否冻结" }
    ],
    "outgoing": [
      { "targetClass": "QtyDef", "relName": "uOM", "cardinality": "0..1", "description": "单位定义" }
    ],
    "incoming": []
  }
  ```

#### `GET /api/stats`

* **功能**：返回 Neo4j 中已加载的类节点总数、属性总数和关系边总数。

#### `GET /api/product-lines`

* **功能**：返回已注册的产品线/行业列表（例如：`general`、`semiconductor`、`battery` 等）。

#### `POST /api/product-lines`

* **功能**：更新或保存产品线配置文件 `product_lines.json`。

---

### 📖 2. 关系 Wiki 接口 (`web/routers/wiki.py`)

#### `GET /api/wiki/relationship`

* **功能**：读取两个实体类在特定关系边上的 Wiki 建模说明书（Markdown 格式）。
* **参数**：`source` (源类名), `rel` (关系名), `target` (目标类名), `product_line` (行业ID)

#### `POST /api/wiki/save`

* **功能**：手动修改并保存一条特定关系的 Wiki 内容。

#### `POST /api/wiki/generate-one`

* **功能**：针对某一特定关系，调用 DeepSeek 流式生成一份高质量的中英文双语建模说明书。

#### `POST /api/wiki/generate-batch`

* **功能**：启动后台任务，一键流式为图谱中所有缺失 Wiki 的关系批量进行 AI 生成，前端支持实时进度百分比及 skips/failures 计数器渲染。

---

### 🤖 3. Graph-RAG 流式问答接口 (`web/routers/chat.py`)

#### `POST /api/chat`

* **功能**：发送用户问题，开展基于图谱邻域提取的 RAG 智能流式问答。
* **参数**：
  ```json
  {
    "question": "用户输入的具体提问",
    "session_id": "可选的会话ID (用于多轮对话历史管理)",
    "product_line": "行业ID (如 battery)"
  }
  ```
* **返回**：`text/event-stream` SSE 流。结束时会返回提取到的图元关键词、提取到的类链接（以供高亮渲染）和审计 `trace_id`。

#### `POST /api/chat/clear`

* **功能**：清除特定 `session_id` 的多轮对话历史上下文。

#### `GET /api/logs`

* **功能**：查询与审计用户的多轮对话记录。支持按日期、会话 ID、关键字过滤。

---

### 🛠️ 4. 场景管理与自愈接口 (`web/routers/scenarios.py`)

#### `GET /api/scenarios`

* **功能**：获取指定行业下的所有预设防错场景。
* **参数**：
  * `industry`: 行业ID (默认 `"general"`)
  * `include_general`: 是否同时合并获取通用行业的场景卡片 (布尔值，默认 `true`)

#### `POST /api/scenarios/plan`

* **功能**：AI Planner 对话网关，接收痛点，在 Neo4j 最短路径图谱知识和 ChromaDB 场景 RAG 背景的支持下，规划防错蓝图。

#### `POST /api/scenarios/save`

* **功能**：保存或更新一个场景定义为 JSON，并同步插入 ChromaDB 向量库中。

#### `POST /api/scenarios/qa`

* **功能**：RAG 场景问答与检索网关。根据用户现场问题，在已保存的场景库中进行向量多路召回，定位相关场景 ID。
* **参数**：
  ```json
  {
    "question": "Resource 故障了在制品怎么拦截？",
    "industry": "semiconductor",
    "include_general": true
  }
  ```

#### `GET /api/scenarios/{scenario_id}`

* **功能**：根据 ID 获取特定场景的详细 JSON 配置（包含步骤、涉及的 Twins、防错 SQL 演示代码）。

#### `DELETE /api/scenarios/{scenario_id}`

* **功能**：删除一个场景，并同步将其从 ChromaDB 向量数据库中抹除。

---

## 🛡️ 系统安全性与版权申明

* **内部交流**：本项目仅限企业内部技术方案验证、MES 蓝图建模与学术性研究使用。
* **商标声明**：`Siemens`、`Opcenter`、`Camstar` 为西门子股份公司 (Siemens AG) 及其子公司的注册商标。本平台所体现的类名、字段及关联网络纯属对物理出厂表结构的本体化映射呈现。
