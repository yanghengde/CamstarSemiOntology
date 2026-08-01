/** Runtime language switching and editable ontology labels. */
(() => {
    "use strict";

    const STORAGE_LANGUAGE = "camstar_ui_language_v1";
    const STORAGE_DISPLAY = "camstar_ontology_display_mode_v1";
    const BUCKETS = { property_description: "propertyDescriptions", node_description: "nodeDescriptions" };
    const UI = {
        "zh-CN": {
            settings: "平台设置", close: "关闭", language: "界面语言", languageHint: "切换后当前页面立即生效。",
            chinese: "简体中文", english: "English", displayMode: "属性显示方式", displayHint: "节点名和关系名始终显示技术原名；此设置仅控制属性显示。",
            translated: "仅显示当前语言", bilingual: "双语 + 技术原名", original: "仅显示技术原名",
            general: "语言与显示", nodeContent: "节点与属性描述", selectNode: "搜索并选择节点", nodeSearch: "搜索节点名称或描述…",
            nodeDescription: "节点描述", descriptionZh: "中文描述", descriptionEn: "英文描述", nodeProperties: "属性描述",
            selectNodeHint: "从左侧选择节点后编辑节点描述和属性描述。",
            search: "搜索名称、所属类或翻译…", originalName: "技术原名", chineseTranslation: "中文描述",
            englishTranslation: "英文描述", save: "保存", saved: "已保存并即时更新", saving: "保存中…",
            reset: "恢复默认", empty: "没有匹配的内容", loadMore: "加载更多", customized: "已自定义",
            catalogHint: "统一管理界面语言、节点与属性描述翻译及行业配置；修改后即时生效。",
            searchPlaceholder: "搜索类名、属性…", classes: "类", attributes: "属性", relations: "关系",
            queryBuilder: "查询构建", industrySettings: "行业设置", graphSettings: "平台设置",
            graphImport: "图谱导入", importTitle: "导入物理结构", importHelp: "分别选择表定义 CSV 和字段定义 CSV。现有节点作为已审核业务对象；新 CDO 默认不导入，必须人工勾选确认。",
            databaseType: "描述来源数据库", descriptionColumn: "描述",
            tableCsv: "表定义 CSV", fieldCsv: "字段定义 CSV", analyzeImport: "分析文件", analyzing: "分析中…",
            importSearch: "搜索候选 CDO…", allStatuses: "全部状态", approvedStatus: "已审核", reviewStatus: "待审核", excludedStatus: "建议排除",
            importApply: "导入已选业务对象", importing: "导入中…", importSelected: "已选择", importConfirm: "确定导入已选择的业务对象吗？本次操作只增量合并，不会删除现有节点。",
            syncDescriptions: "同步当前节点", syncingDescriptions: "同步中…", syncDone: "描述同步完成",
            moduleLegend: "模块图例", searchModule: "搜索模块…", nodeDetail: "节点详情",
            propertyList: "属性列表", relationship: "关系", addContext: "加入上下文", off: "关闭",
            exportGraph: "导出图谱", fitCanvas: "适应", sqlAssistant: "SQL 助手",
            loadingGraph: "正在加载本体图谱…", returnGraph: "返回图谱", industryList: "行业列表",
            newIndustry: "新建行业", editIndustry: "编辑行业信息", saveSettings: "保存设置",
            industryPage: "行业设置", industryId: "行业唯一 ID", industryName: "行业名称", industryIcon: "行业图标",
            industryColor: "代表色彩", industryDescription: "行业建模场景描述", resetForm: "重置",
            promptTitle: "关系建模 AI 提示词", copyPrompt: "复制当前提示词", tipsTitle: "提示说明",
            industryIdPlaceholder: "例如：semiconductor、automotive", industryNamePlaceholder: "例如：半导体制造、汽车零部件",
            industryDescriptionPlaceholder: "描述该行业的 MES 建模特征，例如 WIP 跟踪、批次追溯或设备配方下发",
            industryTip1: "1. 设置完成后，点击“保存设置”会写入系统产品线配置。",
            industryTip2: "2. 返回图谱后，新行业会立即出现在产品线下拉框中；关系 Wiki 将按行业独立存储。",
            industryTip3: "3. 右侧 AI 提示词提供 MES 行业上下文，可用于快速生成规范的本体关系 Wiki。",
        },
        "en-US": {
            settings: "Platform Settings", close: "Close", language: "Interface language", languageHint: "Changes take effect on this page immediately.",
            chinese: "简体中文", english: "English", displayMode: "Property display", displayHint: "Node and relationship names always use technical names. This setting only controls properties.",
            translated: "Current language only", bilingual: "Bilingual + technical name", original: "Technical name only",
            general: "Language & Display", nodeContent: "Node & Property Descriptions", selectNode: "Search and select a node", nodeSearch: "Search node name or description…",
            nodeDescription: "Node Description", descriptionZh: "Chinese description", descriptionEn: "English description", nodeProperties: "Property Descriptions",
            selectNodeHint: "Select a node on the left to edit node and property descriptions.",
            search: "Search name, owner, or translation…", originalName: "Technical name", chineseTranslation: "Chinese description",
            englishTranslation: "English description", save: "Save", saved: "Saved and updated instantly", saving: "Saving…",
            reset: "Restore default", empty: "No matching content", loadMore: "Load more", customized: "Customized",
            catalogHint: "Manage interface language, node and property descriptions, and industry configuration in one place. Changes take effect immediately.",
            searchPlaceholder: "Search classes or properties…", classes: "Classes", attributes: "Properties", relations: "Relations",
            queryBuilder: "Query Builder", industrySettings: "Industry Settings", graphSettings: "Platform Settings",
            graphImport: "Graph Import", importTitle: "Import Physical Structure", importHelp: "Select the table and field definition CSV files. Existing nodes are reviewed business objects; new CDOs stay unchecked until manually approved.",
            databaseType: "Description database", descriptionColumn: "Description",
            tableCsv: "Table CSV", fieldCsv: "Field CSV", analyzeImport: "Analyze Files", analyzing: "Analyzing…",
            importSearch: "Search candidate CDOs…", allStatuses: "All statuses", approvedStatus: "Reviewed", reviewStatus: "Review", excludedStatus: "Suggested exclusion",
            importApply: "Import Selected Objects", importing: "Importing…", importSelected: "Selected", importConfirm: "Import the selected business objects? This incrementally merges data and does not delete existing nodes.",
            syncDescriptions: "Sync Current Node", syncingDescriptions: "Syncing…", syncDone: "Descriptions synchronized",
            moduleLegend: "Module Legend", searchModule: "Search modules…", nodeDetail: "Node Details",
            propertyList: "Properties", relationship: "Relationships", addContext: "Add Context", off: "Off",
            exportGraph: "Export Graph", fitCanvas: "Fit", sqlAssistant: "SQL Assistant",
            loadingGraph: "Loading ontology graph…", returnGraph: "Back to Graph", industryList: "Industry List",
            newIndustry: "New Industry", editIndustry: "Edit Industry", saveSettings: "Save Settings",
            industryPage: "Industry Settings", industryId: "Unique Industry ID", industryName: "Industry Name", industryIcon: "Industry Icon",
            industryColor: "Brand Color", industryDescription: "Industry Modeling Scenario", resetForm: "Reset",
            promptTitle: "Relationship Modeling AI Prompt", copyPrompt: "Copy Prompt", tipsTitle: "Notes",
            industryIdPlaceholder: "e.g. semiconductor, automotive", industryNamePlaceholder: "e.g. Semiconductor Manufacturing, Automotive Parts",
            industryDescriptionPlaceholder: "Describe MES modeling characteristics such as WIP tracking, lot traceability, or equipment recipe delivery",
            industryTip1: "1. Click “Save Settings” to write the completed settings to the product-line configuration.",
            industryTip2: "2. The new industry appears immediately in the product-line selector. Relationship Wikis are stored separately by industry.",
            industryTip3: "3. The AI prompt provides MES industry context for quickly generating standardized ontology relationship Wikis.",
        },
    };

    const EXACT_EN = new Map(Object.entries({
        "查询构建器": "Query Builder", "临时模式": "Temporary", "清空": "Clear", "已选对象": "Selected Objects",
        "在主图中点击对象，确认物理关联后生成 SQL": "Click objects in the graph, verify physical joins, and generate SQL",
        "请从右侧主图选择对象": "Select objects from the graph", "选择对象后，将在这里展示经过物理外键验证的 Join 路径": "Verified physical foreign-key join paths appear here after selecting objects",
        "查询关系预览": "Relationship Preview", "等待选择": "Waiting", "查看关系": "View Relationship", "适应": "Fit",
        "已选对象": "Selected", "中间对象": "Bridge", "未连接": "Disconnected", "SQL 骨架": "SQL Skeleton",
        "复制": "Copy", "已复制": "Copied", "在助手中继续": "Continue in Assistant", "节点详情": "Node Details", "属性列表": "Properties",
        "点击关系线选中并查看物理 JOIN 条件": "Click a relationship to inspect its physical JOIN condition",
        "-- 请选择至少一个查询对象": "-- Select at least one query object",
        "关系": "Relationships", "加入上下文": "Add Context", "关注": "Follow", "关闭": "Close", "中文名": "Chinese Name",
        "模块": "Module", "描述": "Description", "图上邻居": "Graph Neighbors", "完整关系": "All Relationships",
        "属性名": "Property", "类型": "Type", "它引用的对象 →": "References →", "被何处引用 ←": "Referenced By ←",
        "暂无属性": "No properties", "暂无关系": "No relationships", "加载中...": "Loading...", "行业设置": "Industry Settings",
        "模块图例": "Module Legend", "关系聚焦模式": "Relationship Focus Mode", "切换布局": "Switch Layout",
        "适配画布": "Fit Canvas", "切换 Combo 聚合": "Toggle Module Grouping", "导出图谱": "Export Graph",
        "离线 HTML (交互式)": "Offline HTML (interactive)", "SQL 助手": "SQL Assistant", "上下文对象": "Context Objects",
        "尚未添加已知对象": "No known objects added", "查看物理字段": "View Physical Fields", "时间范围模板": "Time Range Template",
        "工序产出": "Operation Throughput", "历史会话": "History", "新建会话": "New Session", "删除当前会话": "Delete Session",
        "暂无历史会话": "No session history", "暂无消息": "No messages", "发送": "Send", "生成 Wiki": "Generate Wiki",
        "编辑": "Edit", "取消": "Cancel", "保存": "Save", "支持 Markdown 格式": "Markdown supported", "加载 Wiki...": "Loading Wiki...",
        "SQL 关联示例": "SQL Join Example", "Relationship 用法": "Relationship Usage", "暂无 Relationship 用法 Wiki": "No Relationship usage Wiki yet",
        "行业列表": "Industry List", "＋ 新建行业": "+ New Industry", "编辑行业信息": "Edit Industry", "返回图谱": "Back to Graph",
        "重置": "Reset", "保存设置": "Save Settings", "复制当前提示词": "Copy Prompt", "提示说明": "Notes",
        "无描述": "No description", "新建行业": "New Industry", "正在加载本体图谱...": "Loading ontology graph...",
    }));

    const TOKEN_ZH = {
        name: "名称", description: "描述", notes: "备注", type: "类型", status: "状态", id: "标识", icon: "图标",
        is: "是否", enabled: "启用", frozen: "冻结", locked: "锁定", instance: "实例", change: "变更", history: "历史",
        created: "创建", updated: "更新", start: "开始", end: "结束", time: "时间", date: "日期", count: "数量",
        total: "总计", default: "默认", first: "首个", last: "最后", current: "当前", value: "值", code: "代码",
        object: "对象", category: "类别", class: "类", property: "属性", relationship: "关系", field: "字段",
        workflow: "工作流", step: "步骤", operation: "工序", spec: "规范", product: "产品", container: "容器",
        resource: "资源", material: "物料", factory: "工厂", line: "产线", mfg: "制造", order: "工单",
        employee: "员工", role: "角色", owner: "所有者", team: "团队", group: "组", family: "系列",
        setup: "设置", access: "访问", base: "基础", revision: "版本", process: "过程", plan: "计划",
        template: "模板", document: "文档", tool: "工装", carrier: "载具", supplier: "供应商", vendor: "供应商",
        location: "位置", physical: "物理", source: "来源", target: "目标", ref: "引用", has: "包含", uses: "使用",
        with: "关联", from: "来源", to: "目标", data: "数据", collection: "采集", list: "列表", entry: "条目",
        wip: "在制品", bom: "物料清单", erp: "ERP", uom: "计量单位", yield: "良率", reason: "原因",
    };

    let state = {
        language: localStorage.getItem(STORAGE_LANGUAGE) || "zh-CN",
        displayMode: localStorage.getItem(STORAGE_DISPLAY) || "translated",
        revision: 0,
        translations: { nodeDescriptions: {}, propertyDescriptions: {} },
    };
    let readyPromise = null;
    let activeCatalogKind = "general";
    let catalogOffset = 0;
    let catalogTotal = 0;
    let catalogSearchTimer = null;
    let importAnalysis = null;
    const exactTextSources = new WeakMap();

    function t(key) {
        return UI[state.language]?.[key] || UI["zh-CN"][key] || key;
    }

    function splitWords(identifier) {
        return String(identifier || "").replace(/[_\-.]+/g, " ").split(/\s+/).flatMap((part) =>
            part.match(/[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+/g) || [part]
        ).filter(Boolean);
    }

    function defaultZh(identifier) {
        return splitWords(identifier).map((word) => TOKEN_ZH[word.toLowerCase()] || word).join("");
    }

    function defaultEn(identifier) {
        const acronyms = new Set(["api", "bom", "cdo", "eco", "erp", "id", "mes", "spc", "sql", "uom", "wip"]);
        return splitWords(identifier).map((word) => acronyms.has(word.toLowerCase())
            ? word.toUpperCase()
            : word[0].toUpperCase() + word.slice(1).toLowerCase()
        ).join(" ");
    }

    function entity(kind, key, options = {}) {
        const original = String(options.original ?? key ?? "");
        return original;
    }

    function description(className, fallback = "") {
        const override = state.translations.nodeDescriptions?.[className] || {};
        return state.language === "en-US"
            ? (override.en || fallback || "")
            : (override.zh || fallback || "");
    }

    function propertyDescription(key, fallback = "") {
        const override = state.translations.propertyDescriptions?.[key] || {};
        return state.language === "en-US"
            ? (override.en || fallback || "")
            : (override.zh || fallback || "");
    }

    function applyDom(root = document) {
        document.documentElement.lang = state.language;
        document.title = state.language === "zh-CN"
            ? (document.body?.dataset.page === "industry" ? "行业与产品线设置 | Siemens Opcenter" : "Opcenter 本体图谱浏览器 | Siemens MES")
            : (document.body?.dataset.page === "industry" ? "Industry & Product Line Settings | Siemens Opcenter" : "Opcenter Ontology Explorer | Siemens MES");
        root.querySelectorAll?.("[data-i18n]").forEach((element) => {
            element.textContent = t(element.dataset.i18n);
        });
        root.querySelectorAll?.("[data-i18n-placeholder]").forEach((element) => {
            element.placeholder = t(element.dataset.i18nPlaceholder);
        });
        root.querySelectorAll?.("[data-i18n-title]").forEach((element) => {
            const value = t(element.dataset.i18nTitle);
            element.title = value;
            if (element.hasAttribute("aria-label")) element.setAttribute("aria-label", value);
        });
        document.querySelectorAll(".i18n-language-select").forEach((select) => { select.value = state.language; });
        document.querySelectorAll(".i18n-display-select").forEach((select) => { select.value = state.displayMode; });
        applyExactText(root);
    }

    function applyExactText(root) {
        const processText = (textNode) => {
            const parent = textNode.parentElement;
            if (!parent || /^(SCRIPT|STYLE|TEXTAREA|PRE|CODE|OPTION)$/.test(parent.tagName) || parent.closest(".i18n-settings-dialog")) return;
            let source = exactTextSources.get(textNode);
            const current = textNode.nodeValue || "";
            const trimmed = current.trim();
            if (!source && EXACT_EN.has(trimmed)) {
                source = { text: trimmed, prefix: current.slice(0, current.indexOf(trimmed)), suffix: current.slice(current.indexOf(trimmed) + trimmed.length) };
                exactTextSources.set(textNode, source);
            }
            if (!source) return;
            const value = state.language === "en-US" ? (EXACT_EN.get(source.text) || source.text) : source.text;
            const next = source.prefix + value + source.suffix;
            if (textNode.nodeValue !== next) textNode.nodeValue = next;
        };
        if (root?.nodeType === Node.TEXT_NODE) {
            processText(root);
            return;
        }
        const walker = document.createTreeWalker(root || document.body, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) processText(node);
    }

    async function fetchConfig(force = false) {
        const response = await fetch(`/api/i18n${force ? `?t=${Date.now()}` : ""}`, { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const payload = await response.json();
        const changed = Number(payload.revision || 0) !== state.revision;
        state.revision = Number(payload.revision || 0);
        state.translations = payload.translations || { nodeDescriptions: {}, propertyDescriptions: {} };
        if (changed) dispatchChange("remote");
        return state;
    }

    function dispatchChange(reason) {
        applyDom();
        window.dispatchEvent(new CustomEvent("camstar:i18n-change", {
            detail: { reason, language: state.language, displayMode: state.displayMode, revision: state.revision },
        }));
    }

    function setPreferences({ language, displayMode }) {
        if (language && UI[language]) {
            state.language = language;
            localStorage.setItem(STORAGE_LANGUAGE, language);
        }
        if (["translated", "bilingual", "original"].includes(displayMode)) {
            state.displayMode = displayMode;
            localStorage.setItem(STORAGE_DISPLAY, displayMode);
        }
        dispatchChange("preferences");
    }

    function createSettingsModal() {
        if (document.getElementById("i18nSettingsModal")) return;
        const modal = document.createElement("div");
        modal.id = "i18nSettingsModal";
        modal.className = "i18n-settings-modal i18n-settings-hidden";
        modal.innerHTML = `
            <div class="i18n-settings-dialog" role="dialog" aria-modal="true" aria-labelledby="i18nSettingsTitle">
                <header class="i18n-settings-header">
                    <div><h2 id="i18nSettingsTitle"></h2><p class="i18n-settings-subtitle"></p></div>
                    <button type="button" class="icon-btn i18n-settings-close" aria-label="Close">×</button>
                </header>
                <div class="i18n-settings-layout">
                    <nav class="i18n-settings-nav">
                        <button type="button" class="active" data-i18n-section="general"></button>
                        <button type="button" data-i18n-section="content"></button>
                        <button type="button" data-i18n-section="import"></button>
                        <button type="button" data-i18n-section="industry"></button>
                    </nav>
                    <main class="i18n-settings-content">
                        <section class="i18n-general-section">
                            <div class="i18n-setting-card">
                                <label class="i18n-setting-label" for="i18nLanguageSelect"></label>
                                <p class="i18n-setting-help i18n-language-hint"></p>
                                <select id="i18nLanguageSelect" class="i18n-form-control i18n-language-select">
                                    <option value="zh-CN">简体中文</option><option value="en-US">English</option>
                                </select>
                            </div>
                        </section>
                        <section class="i18n-node-section" hidden>
                            <div class="i18n-node-toolbar">
                                <input type="search" id="i18nNodeSearch" class="i18n-form-control" />
                                <span id="i18nNodeCount"></span>
                            </div>
                            <div class="i18n-node-workspace">
                                <aside class="i18n-node-browser">
                                    <div id="i18nNodeList" class="i18n-node-list"></div>
                                    <button type="button" id="i18nLoadMore" class="i18n-load-more"></button>
                                </aside>
                                <div id="i18nNodeEditor" class="i18n-node-editor">
                                    <div class="i18n-node-editor-empty"></div>
                                </div>
                            </div>
                        </section>
                        <section class="i18n-industry-section" hidden>
                            <iframe id="i18nIndustryFrame" class="i18n-industry-frame"
                                title="行业设置" loading="lazy"></iframe>
                        </section>
                        <section class="i18n-import-section" hidden>
                            <div class="i18n-import-heading">
                                <h3></h3><p></p>
                            </div>
                            <div class="i18n-import-files">
                                <label><span data-import-label="database"></span><select id="i18nImportDatabase" class="i18n-form-control"><option value="oracle">Oracle</option><option value="sqlserver">SQL Server</option></select></label>
                                <label><span data-import-label="tables"></span><input id="i18nTablesCsv" type="file" accept=".csv,text/csv" /></label>
                                <label><span data-import-label="fields"></span><input id="i18nFieldsCsv" type="file" accept=".csv,text/csv" /></label>
                                <button type="button" id="i18nAnalyzeImport" class="i18n-primary-action"></button>
                            </div>
                            <div id="i18nImportResult" class="i18n-import-result" hidden>
                                <div id="i18nImportWarning" class="i18n-import-warning" hidden></div>
                                <div id="i18nImportSummary" class="i18n-import-summary"></div>
                                <div class="i18n-import-toolbar">
                                    <input id="i18nImportSearch" type="search" class="i18n-form-control" />
                                    <select id="i18nImportStatus" class="i18n-form-control">
                                        <option value="all"></option><option value="approved"></option><option value="review"></option><option value="excluded"></option>
                                    </select>
                                </div>
                                <div class="i18n-import-list-head"><span></span><span>CDO</span><span data-import-head="description"></span><span>Workspace</span><span>属性 / 关系</span><span>判断</span></div>
                                <div id="i18nImportCandidates" class="i18n-import-candidates"></div>
                                <div class="i18n-import-footer">
                                    <span id="i18nImportSelected"></span>
                                    <button type="button" id="i18nApplyImport" class="i18n-primary-action"></button>
                                </div>
                            </div>
                        </section>
                    </main>
                </div>
                <div id="i18nToast" class="i18n-toast" aria-live="polite"></div>
            </div>`;
        document.body.appendChild(modal);

        modal.querySelector(".i18n-settings-close").addEventListener("click", closeSettings);
        modal.addEventListener("mousedown", (event) => { if (event.target === modal) closeSettings(); });
        modal.querySelector("#i18nLanguageSelect").addEventListener("change", (event) => {
            setPreferences({ language: event.target.value });
            updateSettingsText();
            if (activeCatalogKind === "content") loadNodeCatalog(true);
        });
        modal.querySelectorAll("[data-i18n-section]").forEach((button) => {
            button.addEventListener("click", () => selectSettingsSection(button.dataset.i18nSection));
        });
        modal.querySelector("#i18nNodeSearch").addEventListener("input", () => {
            clearTimeout(catalogSearchTimer);
            catalogSearchTimer = setTimeout(() => loadNodeCatalog(true), 250);
        });
        modal.querySelector("#i18nLoadMore").addEventListener("click", () => loadNodeCatalog(false));
        modal.querySelector("#i18nAnalyzeImport").addEventListener("click", analyzeGraphImport);
        modal.querySelector("#i18nApplyImport").addEventListener("click", applyGraphImport);
        modal.querySelector("#i18nImportSearch").addEventListener("input", renderImportCandidates);
        modal.querySelector("#i18nImportStatus").addEventListener("change", renderImportCandidates);
        modal.querySelector("#i18nImportDatabase").addEventListener("change", (event) => window._setSqlDialect?.(event.target.value));
        updateSettingsText();
    }

    function updateSettingsText() {
        const modal = document.getElementById("i18nSettingsModal");
        if (!modal) return;
        modal.querySelector("#i18nSettingsTitle").textContent = t("settings");
        modal.querySelector(".i18n-settings-subtitle").textContent = t("catalogHint");
        modal.querySelector(".i18n-settings-close").title = t("close");
        const labels = { general: "general", content: "nodeContent", import: "graphImport", industry: "industrySettings" };
        modal.querySelectorAll("[data-i18n-section]").forEach((button) => { button.textContent = t(labels[button.dataset.i18nSection]); });
        modal.querySelector("#i18nIndustryFrame").title = t("industrySettings");
        modal.querySelector("label[for='i18nLanguageSelect']").textContent = t("language");
        modal.querySelector(".i18n-language-hint").textContent = t("languageHint");
        modal.querySelector("#i18nNodeSearch").placeholder = t("nodeSearch");
        modal.querySelector("#i18nLoadMore").textContent = t("loadMore");
        modal.querySelector("#i18nLanguageSelect").value = state.language;
        modal.querySelector(".i18n-import-heading h3").textContent = t("importTitle");
        modal.querySelector(".i18n-import-heading p").textContent = t("importHelp");
        modal.querySelector('[data-import-label="tables"]').textContent = t("tableCsv");
        modal.querySelector('[data-import-label="fields"]').textContent = t("fieldCsv");
        modal.querySelector('[data-import-label="database"]').textContent = t("databaseType");
        modal.querySelector('[data-import-head="description"]').textContent = t("descriptionColumn");
        modal.querySelector("#i18nAnalyzeImport").textContent = t("analyzeImport");
        modal.querySelector("#i18nImportSearch").placeholder = t("importSearch");
        const statusOptions = modal.querySelector("#i18nImportStatus").options;
        ["allStatuses", "approvedStatus", "reviewStatus", "excludedStatus"].forEach((key, index) => { statusOptions[index].textContent = t(key); });
        modal.querySelector("#i18nApplyImport").textContent = t("importApply");
        if (importAnalysis) { renderImportSummary(); renderImportCandidates(); }
        const emptyEditor = modal.querySelector(".i18n-node-editor-empty");
        if (emptyEditor) emptyEditor.textContent = t("selectNodeHint");
    }

    function openSettings() {
        createSettingsModal();
        updateSettingsText();
        document.getElementById("i18nSettingsModal").classList.remove("i18n-settings-hidden");
        document.body.classList.add("i18n-settings-open");
    }

    function closeSettings() {
        document.getElementById("i18nSettingsModal")?.classList.add("i18n-settings-hidden");
        document.body.classList.remove("i18n-settings-open");
    }

    function selectSettingsSection(section) {
        activeCatalogKind = section;
        const modal = document.getElementById("i18nSettingsModal");
        modal.querySelectorAll("[data-i18n-section]").forEach((button) => button.classList.toggle("active", button.dataset.i18nSection === section));
        modal.querySelector(".i18n-general-section").hidden = section !== "general";
        modal.querySelector(".i18n-node-section").hidden = section !== "content";
        modal.querySelector(".i18n-import-section").hidden = section !== "import";
        modal.querySelector(".i18n-industry-section").hidden = section !== "industry";
        modal.querySelector(".i18n-settings-content").classList.toggle("industry-active", section === "industry");
        if (section === "content") loadNodeCatalog(true);
        if (section === "import") {
            modal.querySelector("#i18nImportDatabase").value = window._getSqlDialect?.()
                || document.getElementById("globalSqlDialect")?.value || "oracle";
        }
        if (section === "industry") {
            const frame = modal.querySelector("#i18nIndustryFrame");
            if (!frame.src) {
                const query = new URLSearchParams(window.location.search);
                const productLine = query.get("product_line")
                    || localStorage.getItem("selected_product_line")
                    || "general";
                const target = new URL("/static/industry.html", window.location.origin);
                target.searchParams.set("embedded", "1");
                target.searchParams.set("product_line", productLine);
                frame.src = target.href;
            }
        }
    }

    function importStatusLabel(status) {
        return t(status === "approved" ? "approvedStatus" : status === "excluded" ? "excludedStatus" : "reviewStatus");
    }

    async function responseError(response) {
        try {
            const payload = await response.json();
            return typeof payload.detail === "string" ? payload.detail : `HTTP ${response.status}`;
        } catch (_) { return `HTTP ${response.status}`; }
    }

    async function analyzeGraphImport() {
        const tables = document.getElementById("i18nTablesCsv").files[0];
        const fields = document.getElementById("i18nFieldsCsv").files[0];
        if (!tables || !fields) { showToast(`${t("tableCsv")} / ${t("fieldCsv")}`, true); return; }
        const button = document.getElementById("i18nAnalyzeImport");
        button.disabled = true; button.textContent = t("analyzing");
        const form = new FormData(); form.append("tables", tables); form.append("fields", fields);
        form.append("database", document.getElementById("i18nImportDatabase").value);
        try {
            const response = await fetch("/api/ontology-import/analyze", { method: "POST", body: form });
            if (!response.ok) throw new Error(await responseError(response));
            importAnalysis = await response.json();
            document.getElementById("i18nImportResult").hidden = false;
            const warning = document.getElementById("i18nImportWarning");
            warning.textContent = importAnalysis.descriptionWarning || "";
            warning.hidden = !importAnalysis.descriptionWarning;
            renderImportSummary(); renderImportCandidates();
        } catch (error) { showToast(error.message, true); }
        finally { button.disabled = false; button.textContent = t("analyzeImport"); }
    }

    function renderImportSummary() {
        if (!importAnalysis) return;
        const target = document.getElementById("i18nImportSummary");
        const summary = importAnalysis.summary;
        const items = [
            [t("classes"), summary.tables], [t("attributes"), summary.fields],
            [t("approvedStatus"), summary.approved], [t("reviewStatus"), summary.review],
            [t("excludedStatus"), summary.excluded],
            [t("descriptionColumn"), summary.described],
        ];
        target.replaceChildren(...items.map(([label, value]) => {
            const card = document.createElement("div");
            const strong = document.createElement("strong"); strong.textContent = value;
            const span = document.createElement("span"); span.textContent = label;
            card.append(strong, span); return card;
        }));
    }

    function renderImportCandidates() {
        if (!importAnalysis) return;
        const search = document.getElementById("i18nImportSearch").value.trim().toLowerCase();
        const status = document.getElementById("i18nImportStatus").value;
        const rows = importAnalysis.candidates.filter((item) =>
            (!search || `${item.className} ${item.workspace} ${item.reason}`.toLowerCase().includes(search)) &&
            (status === "all" || item.status === status)
        );
        const list = document.getElementById("i18nImportCandidates"); list.replaceChildren();
        rows.forEach((item) => {
            const row = document.createElement("label"); row.className = `i18n-import-candidate status-${item.status}`;
            const checkbox = document.createElement("input"); checkbox.type = "checkbox"; checkbox.checked = Boolean(item.selected);
            checkbox.addEventListener("change", () => { item.selected = checkbox.checked; updateImportSelected(); });
            const name = document.createElement("strong"); name.textContent = item.className; name.title = item.className;
            const description = document.createElement("span"); description.className = "i18n-import-description";
            description.textContent = state.language === "zh-CN"
                ? (item.descriptionZh || item.descriptionEn || "—")
                : (item.descriptionEn || item.descriptionZh || "—");
            description.title = description.textContent;
            const workspace = document.createElement("span"); workspace.textContent = item.workspace || "—";
            const counts = document.createElement("span"); counts.textContent = `${item.propertyCount} / ${item.relationshipCount}`;
            const decision = document.createElement("span"); decision.className = "i18n-import-decision";
            const badge = document.createElement("em"); badge.textContent = importStatusLabel(item.status);
            const reason = document.createElement("small"); reason.textContent = item.reason; reason.title = item.reason;
            decision.append(badge, reason); row.append(checkbox, name, description, workspace, counts, decision); list.appendChild(row);
        });
        if (!rows.length) list.innerHTML = `<div class="i18n-catalog-empty">${t("empty")}</div>`;
        updateImportSelected();
    }

    function updateImportSelected() {
        if (!importAnalysis) return;
        const count = importAnalysis.candidates.filter((item) => item.selected).length;
        document.getElementById("i18nImportSelected").textContent = `${t("importSelected")}: ${count}`;
        document.getElementById("i18nApplyImport").disabled = count === 0;
    }

    async function applyGraphImport() {
        if (!importAnalysis || !window.confirm(t("importConfirm"))) return;
        const selected = importAnalysis.candidates.filter((item) => item.selected).map((item) => item.className);
        const button = document.getElementById("i18nApplyImport");
        button.disabled = true; button.textContent = t("importing");
        try {
            const response = await fetch("/api/ontology-import/apply", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ importId: importAnalysis.importId, selected }),
            });
            if (!response.ok) throw new Error(await responseError(response));
            const result = await response.json();
            showToast(`${t("saved")}: ${result.classes} ${t("classes")}, ${result.relationships} ${t("relations")}`);
            setTimeout(() => window.location.reload(), 900);
        } catch (error) { showToast(error.message, true); button.disabled = false; button.textContent = t("importApply"); }
    }

    async function loadNodeCatalog(reset) {
        const list = document.getElementById("i18nNodeList");
        const search = document.getElementById("i18nNodeSearch").value.trim();
        if (reset) { catalogOffset = 0; list.innerHTML = `<div class="i18n-catalog-loading">${t("loadingGraph")}</div>`; }
        const offset = reset ? 0 : catalogOffset;
        try {
            const response = await fetch(`/api/i18n/catalog?search=${encodeURIComponent(search)}&offset=${offset}&limit=80`, { cache: "no-store" });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const payload = await response.json();
            if (reset) list.replaceChildren();
            payload.items.forEach((item) => list.appendChild(createNodeResult(item)));
            catalogOffset = offset + payload.items.length;
            catalogTotal = payload.total;
            document.getElementById("i18nNodeCount").textContent = `${Math.min(catalogOffset, catalogTotal)} / ${catalogTotal}`;
            document.getElementById("i18nLoadMore").hidden = catalogOffset >= catalogTotal;
            if (!payload.items.length && reset) list.innerHTML = `<div class="i18n-catalog-empty">${t("empty")}</div>`;
        } catch (error) {
            list.innerHTML = `<div class="i18n-catalog-empty">${error.message}</div>`;
        }
    }

    function createNodeResult(item) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "i18n-node-result";
        button.dataset.key = item.key;
        const name = document.createElement("strong"); name.textContent = item.original;
        const meta = document.createElement("small");
        meta.textContent = `${item.owner || ""} · ${item.propertyCount || 0} ${t("attributes")}`;
        button.append(name, meta);
        if (item.customized) {
            const badge = document.createElement("em");
            badge.textContent = t("customized");
            button.appendChild(badge);
        }
        button.addEventListener("click", () => loadNodeEditor(item.key, button));
        return button;
    }

    async function loadNodeEditor(className, selectedButton) {
        document.querySelectorAll(".i18n-node-result.active").forEach((item) => item.classList.remove("active"));
        selectedButton?.classList.add("active");
        const editor = document.getElementById("i18nNodeEditor");
        editor.innerHTML = `<div class="i18n-catalog-loading">${t("loadingGraph")}</div>`;
        try {
            const response = await fetch(`/api/i18n/node/${encodeURIComponent(className)}`, { cache: "no-store" });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            renderNodeEditor(await response.json());
        } catch (error) {
            editor.innerHTML = `<div class="i18n-catalog-empty">${error.message}</div>`;
        }
    }

    function renderNodeEditor(node) {
        const editor = document.getElementById("i18nNodeEditor");
        editor.replaceChildren();
        const header = document.createElement("div"); header.className = "i18n-node-editor-header";
        const title = document.createElement("h3"); title.textContent = node.original;
        const subtitle = document.createElement("span"); subtitle.textContent = node.owner || "";
        const sync = document.createElement("button"); sync.type = "button"; sync.className = "i18n-sync-description";
        sync.innerHTML = `${window.AppIcons?.svg("refresh", { size: 13 }) || ""}<span>${t("syncDescriptions")}</span>`;
        sync.addEventListener("click", () => syncNodeDescriptions(node.key, sync));
        header.append(title, subtitle, sync);
        const descriptionCard = document.createElement("section"); descriptionCard.className = "i18n-description-card";
        descriptionCard.innerHTML = `
            <h4>${t("nodeDescription")}</h4>
            <div class="i18n-description-field">
                <label>${t("descriptionZh")}</label>
                <textarea class="i18n-form-control" data-description="zh"></textarea>
            </div>
            <div class="i18n-description-field">
                <label>${t("descriptionEn")}</label>
                <textarea class="i18n-form-control" data-description="en"></textarea>
            </div>
            <button type="button" class="i18n-row-save i18n-description-save">${t("save")}</button>`;
        descriptionCard.querySelector('[data-description="zh"]').value = node.descriptionZh || "";
        descriptionCard.querySelector('[data-description="en"]').value = node.descriptionEn || "";
        descriptionCard.querySelector("button").addEventListener("click", (event) => saveTranslation(
            "node_description", node.key,
            descriptionCard.querySelector('[data-description="zh"]').value,
            descriptionCard.querySelector('[data-description="en"]').value,
            event.currentTarget,
        ));
        const propertiesTitle = document.createElement("h4");
        propertiesTitle.className = "i18n-properties-title";
        propertiesTitle.textContent = `${t("nodeProperties")} (${node.properties.length})`;
        const head = document.createElement("div"); head.className = "i18n-catalog-head";
        [t("originalName"), t("chineseTranslation"), t("englishTranslation"), ""].forEach((value) => { const span = document.createElement("span"); span.textContent = value; head.appendChild(span); });
        const list = document.createElement("div"); list.className = "i18n-property-editor-list";
        node.properties.forEach((item) => list.appendChild(createPropertyRow(item)));
        editor.append(header, descriptionCard, propertiesTitle, head, list);
    }

    async function syncNodeDescriptions(className, button) {
        button.disabled = true;
        const label = button.querySelector("span"); if (label) label.textContent = t("syncingDescriptions");
        try {
            const response = await fetch("/api/i18n/sync-descriptions", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ className, database: window._getSqlDialect?.() || "oracle" }),
            });
            if (!response.ok) throw new Error(await responseError(response));
            const result = await response.json();
            await fetchConfig(true); dispatchChange("translation");
            showToast(result.warning || `${t("syncDone")}: ${result.updated}/${result.matched}`, Boolean(result.warning));
            await loadNodeEditor(className, document.querySelector(`.i18n-node-result[data-key="${CSS.escape(className)}"]`));
        } catch (error) {
            showToast(error.message, true); button.disabled = false; if (label) label.textContent = t("syncDescriptions");
        }
    }

    function createPropertyRow(item) {
        const row = document.createElement("div"); row.className = "i18n-catalog-row";
        const identity = document.createElement("div"); identity.className = "i18n-catalog-identity";
        const name = document.createElement("strong"); name.textContent = item.original;
        const source = document.createElement("small");
        source.textContent = item.dataType || "String";
        source.title = item.dataType || "";
        identity.append(name, source);
        const zh = document.createElement("textarea"); zh.className = "i18n-form-control i18n-property-description-input"; zh.value = item.descriptionZh || ""; zh.lang = "zh-CN"; zh.rows = 2;
        const en = document.createElement("textarea"); en.className = "i18n-form-control i18n-property-description-input"; en.value = item.descriptionEn || ""; en.lang = "en"; en.rows = 2;
        const save = document.createElement("button"); save.type = "button"; save.className = "i18n-row-save"; save.textContent = t("save");
        save.addEventListener("click", () => saveTranslation("property_description", item.key, zh.value, en.value, save));
        row.append(identity, zh, en, save);
        return row;
    }

    async function saveTranslation(kind, key, zh, en, button) {
        button.disabled = true; button.textContent = t("saving");
        try {
            const response = await fetch("/api/i18n/translation", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ kind, key, zh, en }) });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const payload = await response.json();
            const bucket = state.translations[BUCKETS[kind]];
            if (payload.translation) bucket[key] = payload.translation; else delete bucket[key];
            state.revision = payload.revision;
            dispatchChange("translation");
            showToast(t("saved"));
        } catch (error) { showToast(error.message, true); }
        finally { button.disabled = false; button.textContent = t("save"); }
    }

    function showToast(message, isError = false) {
        const toast = document.getElementById("i18nToast");
        if (!toast) return;
        toast.textContent = message; toast.classList.toggle("error", isError); toast.classList.add("visible");
        clearTimeout(showToast.timer); showToast.timer = setTimeout(() => toast.classList.remove("visible"), 2400);
    }

    async function init() {
        if (readyPromise) return readyPromise;
        readyPromise = (async () => {
            try { await fetchConfig(); } catch (error) { console.warn("Translations unavailable", error); }
            createSettingsModal();
            applyDom();
            document.querySelectorAll("#btnSettings, [data-open-i18n-settings]").forEach((button) => button.addEventListener("click", openSettings));
            window.addEventListener("keydown", (event) => { if (event.key === "Escape") closeSettings(); });
            window.addEventListener("camstar:sql-dialect-change", (event) => {
                const selector = document.getElementById("i18nImportDatabase");
                if (selector && event.detail?.dialect) selector.value = event.detail.dialect;
            });
            const observer = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    mutation.addedNodes.forEach((node) => applyExactText(node));
                }
            });
            observer.observe(document.body, { childList: true, subtree: true });
            window.setInterval(async () => {
                if (document.hidden) return;
                try { await fetchConfig(true); } catch (_) {}
            }, 5000);
            return state;
        })();
        return readyPromise;
    }

    window.CamstarI18n = {
        init, t, entity, description, propertyDescription, applyDom, openSettings, closeSettings, setPreferences,
        get language() { return state.language; },
        get displayMode() { return state.displayMode; },
        get revision() { return state.revision; },
        exact(text) { return state.language === "en-US" ? (EXACT_EN.get(text) || text) : text; },
    };
})();
