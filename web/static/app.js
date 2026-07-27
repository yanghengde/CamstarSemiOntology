/**
 * Camstar Ontology Explorer – G6 v5 Graph Application
 * ────────────────────────────────────────────────────
 * Features:
 *   • Layered loading: L0 = OntologyClass overview → L1 = click to drill
 *   • Combo aggregation by module (Workflow / Operation / Spec / Other)
 *   • Siemens colour scheme
 */
(() => {
    "use strict";

    // ── Siemens Palette ──
    const COLORS = {
        workflow: { fill: "#009999", stroke: "#00B8B8", text: "#E8F0F2", comboFill: "rgba(0,153,153,0.08)", comboBorder: "rgba(0,153,153,0.3)" },
        operation: { fill: "#FF6600", stroke: "#FF8833", text: "#E8F0F2", comboFill: "rgba(255,102,0,0.08)", comboBorder: "rgba(255,102,0,0.3)" },
        spec: { fill: "#862996", stroke: "#A040B0", text: "#E8F0F2", comboFill: "rgba(134,41,150,0.08)", comboBorder: "rgba(134,41,150,0.3)" },
        workcenter: { fill: "#2E86C1", stroke: "#5DADE2", text: "#E8F0F2", comboFill: "rgba(46,134,193,0.08)", comboBorder: "rgba(46,134,193,0.3)" },
        factory: { fill: "#27AE60", stroke: "#52D68C", text: "#E8F0F2", comboFill: "rgba(39,174,96,0.08)", comboBorder: "rgba(39,174,96,0.3)" },
        mfgline: { fill: "#00897B", stroke: "#4DB6AC", text: "#E8F0F2", comboFill: "rgba(0,137,123,0.08)", comboBorder: "rgba(0,137,123,0.3)" },
        mfgcalendar: { fill: "#FF8F00", stroke: "#FFB74D", text: "#E8F0F2", comboFill: "rgba(255,143,0,0.08)", comboBorder: "rgba(255,143,0,0.3)" },
        product: { fill: "#F39C12", stroke: "#F5B041", text: "#E8F0F2", comboFill: "rgba(243,156,18,0.08)", comboBorder: "rgba(243,156,18,0.3)" },
        container: { fill: "#3498DB", stroke: "#5DADE2", text: "#E8F0F2", comboFill: "rgba(52,152,219,0.08)", comboBorder: "rgba(52,152,219,0.3)" },
        carrier: { fill: "#039BE5", stroke: "#4FC3F7", text: "#E8F0F2", comboFill: "rgba(3,155,229,0.08)", comboBorder: "rgba(3,155,229,0.3)" },
        businessrule: { fill: "#6A1B9A", stroke: "#AB47BC", text: "#E8F0F2", comboFill: "rgba(106,27,154,0.08)", comboBorder: "rgba(106,27,154,0.3)" },
        datacollection: { fill: "#9B59B6", stroke: "#AF7AC5", text: "#E8F0F2", comboFill: "rgba(155,89,182,0.08)", comboBorder: "rgba(155,89,182,0.3)" },
        quality: { fill: "#E74C3C", stroke: "#EC7063", text: "#E8F0F2", comboFill: "rgba(231,76,60,0.08)", comboBorder: "rgba(231,76,60,0.3)" },
        electronic_procedure: { fill: "#1ABC9C", stroke: "#48C9B0", text: "#E8F0F2", comboFill: "rgba(26,188,156,0.08)", comboBorder: "rgba(26,188,156,0.3)" },
        resource: { fill: "#F1C40F", stroke: "#F7DC6F", text: "#E8F0F2", comboFill: "rgba(241,196,15,0.08)", comboBorder: "rgba(241,196,15,0.3)" },
        material: { fill: "#16A085", stroke: "#48C9B0", text: "#E8F0F2", comboFill: "rgba(22,160,133,0.08)", comboBorder: "rgba(22,160,133,0.3)" },
        bom: { fill: "#673AB7", stroke: "#9575CD", text: "#E8F0F2", comboFill: "rgba(103,58,183,0.08)", comboBorder: "rgba(103,58,183,0.3)" },
        erpbom: { fill: "#7B1FA2", stroke: "#BA68C8", text: "#E8F0F2", comboFill: "rgba(123,31,162,0.08)", comboBorder: "rgba(123,31,162,0.3)" },
        employee: { fill: "#E67E22", stroke: "#EB984E", text: "#E8F0F2", comboFill: "rgba(230,126,34,0.08)", comboBorder: "rgba(230,126,34,0.3)" },
        role: { fill: "#37474F", stroke: "#78909C", text: "#E8F0F2", comboFill: "rgba(55,71,79,0.08)", comboBorder: "rgba(55,71,79,0.3)" },
        mfgorder: { fill: "#34495E", stroke: "#5D6D7E", text: "#E8F0F2", comboFill: "rgba(52,73,94,0.08)", comboBorder: "rgba(52,73,94,0.3)" },
        part: { fill: "#0277BD", stroke: "#4FC3F7", text: "#E8F0F2", comboFill: "rgba(2,119,189,0.08)", comboBorder: "rgba(2,119,189,0.3)" },
        organization: { fill: "#C62828", stroke: "#EF5350", text: "#E8F0F2", comboFill: "rgba(198,40,40,0.08)", comboBorder: "rgba(198,40,40,0.3)" },
        billofprocess: { fill: "#4527A0", stroke: "#7E57C2", text: "#E8F0F2", comboFill: "rgba(69,39,160,0.08)", comboBorder: "rgba(69,39,160,0.3)" },
        team: { fill: "#BF360C", stroke: "#FF7043", text: "#E8F0F2", comboFill: "rgba(191,54,12,0.08)", comboBorder: "rgba(191,54,12,0.3)" },
        terminal: { fill: "#00695C", stroke: "#4DB6AC", text: "#E8F0F2", comboFill: "rgba(0,105,92,0.08)", comboBorder: "rgba(0,105,92,0.3)" },
        salesorder: { fill: "#1B5E20", stroke: "#66BB6A", text: "#E8F0F2", comboFill: "rgba(27,94,32,0.08)", comboBorder: "rgba(27,94,32,0.3)" },
        maintenance: { fill: "#C0392B", stroke: "#D98880", text: "#E8F0F2", comboFill: "rgba(192,57,43,0.08)", comboBorder: "rgba(192,57,43,0.3)" },
        sampling: { fill: "#9C27B0", stroke: "#BA68C8", text: "#E8F0F2", comboFill: "rgba(156,39,176,0.08)", comboBorder: "rgba(156,39,176,0.3)" },
        document: { fill: "#607D8B", stroke: "#90A4AE", text: "#E8F0F2", comboFill: "rgba(96,125,139,0.08)", comboBorder: "rgba(96,125,139,0.3)" },
        label: { fill: "#FF9800", stroke: "#FFB74D", text: "#E8F0F2", comboFill: "rgba(255,152,0,0.08)", comboBorder: "rgba(255,152,0,0.3)" },
        tool: { fill: "#795548", stroke: "#A1887F", text: "#E8F0F2", comboFill: "rgba(121,85,72,0.08)", comboBorder: "rgba(121,85,72,0.3)" },
        change_management: { fill: "#F44336", stroke: "#E57373", text: "#E8F0F2", comboFill: "rgba(244,67,54,0.08)", comboBorder: "rgba(244,67,54,0.3)" },
        recipe: { fill: "#E91E63", stroke: "#F06292", text: "#E8F0F2", comboFill: "rgba(233,30,99,0.08)", comboBorder: "rgba(233,30,99,0.3)" },
        inventory: { fill: "#8BC34A", stroke: "#AED581", text: "#E8F0F2", comboFill: "rgba(139,195,74,0.08)", comboBorder: "rgba(139,195,74,0.3)" },
        rework: { fill: "#FF5722", stroke: "#FF8A65", text: "#E8F0F2", comboFill: "rgba(255,87,34,0.08)", comboBorder: "rgba(255,87,34,0.3)" },
        timer: { fill: "#00BCD4", stroke: "#4DD0E1", text: "#E8F0F2", comboFill: "rgba(0,188,212,0.08)", comboBorder: "rgba(0,188,212,0.3)" },
        checklist: { fill: "#5C6BC0", stroke: "#7986CB", text: "#E8F0F2", comboFill: "rgba(92,107,192,0.08)", comboBorder: "rgba(92,107,192,0.3)" },
        setup: { fill: "#7E57C2", stroke: "#9575CD", text: "#E8F0F2", comboFill: "rgba(126,87,194,0.08)", comboBorder: "rgba(126,87,194,0.3)" },
        packaging: { fill: "#8D6E63", stroke: "#A1887F", text: "#E8F0F2", comboFill: "rgba(141,110,99,0.08)", comboBorder: "rgba(141,110,99,0.3)" },
        supplier: { fill: "#3F51B5", stroke: "#5C6BC0", text: "#E8F0F2", comboFill: "rgba(63,81,181,0.08)", comboBorder: "rgba(63,81,181,0.3)" },
        esignature: { fill: "#00ACC1", stroke: "#26C6DA", text: "#E8F0F2", comboFill: "rgba(0,172,193,0.08)", comboBorder: "rgba(0,172,193,0.3)" },
        alarm: { fill: "#F50057", stroke: "#FF4081", text: "#E8F0F2", comboFill: "rgba(245,0,87,0.08)", comboBorder: "rgba(245,0,87,0.3)" },
        scrap: { fill: "#546E7A", stroke: "#78909C", text: "#E8F0F2", comboFill: "rgba(84,110,122,0.08)", comboBorder: "rgba(84,110,122,0.3)" },
        equipmentstate: { fill: "#29B6F6", stroke: "#4FC3F7", text: "#E8F0F2", comboFill: "rgba(41,182,246,0.08)", comboBorder: "rgba(41,182,246,0.3)" },
        shipping: { fill: "#827717", stroke: "#9E9D24", text: "#E8F0F2", comboFill: "rgba(130,119,23,0.08)", comboBorder: "rgba(130,119,23,0.3)" },
        environment: { fill: "#00BFA5", stroke: "#1DE9B6", text: "#E8F0F2", comboFill: "rgba(0,191,165,0.08)", comboBorder: "rgba(0,191,165,0.3)" },
        rma: { fill: "#D84315", stroke: "#F4511E", text: "#E8F0F2", comboFill: "rgba(216,67,21,0.08)", comboBorder: "rgba(216,67,21,0.3)" },
        consumable: { fill: "#FFB300", stroke: "#FFCA28", text: "#E8F0F2", comboFill: "rgba(255,179,0,0.08)", comboBorder: "rgba(255,179,0,0.3)" },
        spc: { fill: "#2979FF", stroke: "#82B1FF", text: "#E8F0F2", comboFill: "rgba(41,121,255,0.08)", comboBorder: "rgba(41,121,255,0.3)" },
        semiconductor_action_approval_esign: { fill: "#BE123C", stroke: "#FDA4AF", text: "#E8F0F2", comboFill: "rgba(190,18,60,0.08)", comboBorder: "rgba(190,18,60,0.3)" },
        semiconductor_bin_overlay: { fill: "#0369A1", stroke: "#7DD3FC", text: "#E8F0F2", comboFill: "rgba(3,105,161,0.08)", comboBorder: "rgba(3,105,161,0.3)" },
        semiconductor_cio_core: { fill: "#00695C", stroke: "#4DB6AC", text: "#E8F0F2", comboFill: "rgba(0,105,92,0.08)", comboBorder: "rgba(0,105,92,0.3)" },
        semiconductor_cio_orchestration: { fill: "#283593", stroke: "#7986CB", text: "#E8F0F2", comboFill: "rgba(40,53,147,0.08)", comboBorder: "rgba(40,53,147,0.3)" },
        semiconductor_carrier_material_tool: { fill: "#6D4C41", stroke: "#BCAAA4", text: "#E8F0F2", comboFill: "rgba(109,76,65,0.08)", comboBorder: "rgba(109,76,65,0.3)" },
        semiconductor_cio_bases: { fill: "#3949AB", stroke: "#9FA8DA", text: "#E8F0F2", comboFill: "rgba(57,73,171,0.08)", comboBorder: "rgba(57,73,171,0.3)" },
        semiconductor_foundation: { fill: "#00A6A6", stroke: "#36D1C4", text: "#E8F0F2", comboFill: "rgba(0,166,166,0.08)", comboBorder: "rgba(0,166,166,0.3)" },
        semiconductor_legacy_name_replacements: { fill: "#4F46E5", stroke: "#A5B4FC", text: "#E8F0F2", comboFill: "rgba(79,70,229,0.08)", comboBorder: "rgba(79,70,229,0.3)" },
        semiconductor_physical_resource_replacements: { fill: "#0F766E", stroke: "#5EEAD4", text: "#E8F0F2", comboFill: "rgba(15,118,110,0.08)", comboBorder: "rgba(15,118,110,0.3)" },
        semiconductor_print_interface_details: { fill: "#D97706", stroke: "#FBBF24", text: "#E8F0F2", comboFill: "rgba(217,119,6,0.08)", comboBorder: "rgba(217,119,6,0.3)" },
        semiconductor_print_pack_ship: { fill: "#5D4037", stroke: "#A1887F", text: "#E8F0F2", comboFill: "rgba(93,64,55,0.08)", comboBorder: "rgba(93,64,55,0.3)" },
        semiconductor_process_equipment: { fill: "#1565C0", stroke: "#42A5F5", text: "#E8F0F2", comboFill: "rgba(21,101,192,0.08)", comboBorder: "rgba(21,101,192,0.3)" },
        semiconductor_process_wip_details: { fill: "#0891B2", stroke: "#67E8F9", text: "#E8F0F2", comboFill: "rgba(8,145,178,0.08)", comboBorder: "rgba(8,145,178,0.3)" },
        semiconductor_quality_iqc: { fill: "#C62828", stroke: "#EF5350", text: "#E8F0F2", comboFill: "rgba(198,40,40,0.08)", comboBorder: "rgba(198,40,40,0.3)" },
        semiconductor_revision_bases: { fill: "#546E7A", stroke: "#B0BEC5", text: "#E8F0F2", comboFill: "rgba(84,110,122,0.08)", comboBorder: "rgba(84,110,122,0.3)" },
        semiconductor_scheduling_flow: { fill: "#2E7D32", stroke: "#66BB6A", text: "#E8F0F2", comboFill: "rgba(46,125,50,0.08)", comboBorder: "rgba(46,125,50,0.3)" },
        semiconductor_security_kpi_configuration: { fill: "#4338CA", stroke: "#A5B4FC", text: "#E8F0F2", comboFill: "rgba(67,56,202,0.08)", comboBorder: "rgba(67,56,202,0.3)" },
        semiconductor_service_location: { fill: "#455A64", stroke: "#90A4AE", text: "#E8F0F2", comboFill: "rgba(69,90,100,0.08)", comboBorder: "rgba(69,90,100,0.3)" },
        semiconductor_shared_support: { fill: "#00897B", stroke: "#80CBC4", text: "#E8F0F2", comboFill: "rgba(0,137,123,0.08)", comboBorder: "rgba(0,137,123,0.3)" },
        semiconductor_shipping_integration: { fill: "#AD1457", stroke: "#F06292", text: "#E8F0F2", comboFill: "rgba(173,20,87,0.08)", comboBorder: "rgba(173,20,87,0.3)" },
        semiconductor_spc_quality_details: { fill: "#A855F7", stroke: "#D8B4FE", text: "#E8F0F2", comboFill: "rgba(168,85,247,0.08)", comboBorder: "rgba(168,85,247,0.3)" },
        semiconductor_spc_yield: { fill: "#00838F", stroke: "#4DD0E1", text: "#E8F0F2", comboFill: "rgba(0,131,143,0.08)", comboBorder: "rgba(0,131,143,0.3)" },
        semiconductor_user_job_spc_configuration: { fill: "#7C3AED", stroke: "#C4B5FD", text: "#E8F0F2", comboFill: "rgba(124,58,237,0.08)", comboBorder: "rgba(124,58,237,0.3)" },
        semiconductor_wafer_experiment: { fill: "#7B1FA2", stroke: "#CE93D8", text: "#E8F0F2", comboFill: "rgba(123,31,162,0.08)", comboBorder: "rgba(123,31,162,0.3)" },
        semiconductor_wip_control: { fill: "#EF6C00", stroke: "#FFB74D", text: "#E8F0F2", comboFill: "rgba(239,108,0,0.08)", comboBorder: "rgba(239,108,0,0.3)" },
        other: { fill: "#505050", stroke: "#707070", text: "#E8F0F2", comboFill: "rgba(80,80,80,0.08)", comboBorder: "rgba(80,80,80,0.3)" },
    };

    const COMBO_LABELS = {
        workflow: "Workflow 工作流",
        operation: "Operation 工序",
        spec: "Spec 规范/参数",
        workcenter: "WorkCenter 工作中心",
        factory: "Factory 工厂模型",
        mfgline: "MfgLine 制造产线",
        mfgcalendar: "MfgCalendar 制造日历",
        product: "Product 产品物料",
        container: "Container 容器批次",
        carrier: "Carrier 载具管理",
        businessrule: "BusinessRule 业务规则",
        datacollection: "Data Collection 数据采集",
        quality: "Quality 质量",
        electronic_procedure: "E-Procedure 电子程序",
        resource: "Resource 设备资源",
        material: "Material 原材料/物料",
        bom: "BOM 物料清单",
        erpbom: "ERPBOM ERP物料清单",
        employee: "Employee 人员资质",
        role: "Role 角色权限",
        mfgorder: "MfgOrder 制造工单",
        part: "Part 设备资源",
        organization: "Organization 组织",
        billofprocess: "BillOfProcess 工艺清单",
        team: "Team 班组团队",
        salesorder: "SalesOrder 销售订单",
        maintenance: "Maintenance 维护保养",
        sampling: "Sampling 质量抽样",
        document: "Document 文档控制",
        tool: "Tool 工装工具",
        change_management: "Change Mgt 变更管理",
        recipe: "Recipe 设备配方",
        inventory: "Inventory 库存货位",
        checklist: "Checklist 检查表模板",
        setup: "Setup 换线准备",
        packaging: "Packaging 包装管理",
        spc: "SPC 统计过程控制",
        semiconductor_action_approval_esign: "Semiconductor 动作审批与电子签名",
        semiconductor_bin_overlay: "Semiconductor Bin与Overlay",
        semiconductor_cio_core: "CIO 连接与消息",
        semiconductor_cio_orchestration: "CIO 编排与派工",
        semiconductor_carrier_material_tool: "Semiconductor 载具物料工装",
        semiconductor_cio_bases: "CIO 与半导体Base",
        semiconductor_foundation: "Semiconductor 半导体基础",
        semiconductor_legacy_name_replacements: "Semiconductor 旧名称物理替代",
        semiconductor_physical_resource_replacements: "Semiconductor 物理位置与资源BOM",
        semiconductor_print_interface_details: "Semiconductor 打印与接口明细",
        semiconductor_print_pack_ship: "Semiconductor 打印包装出货",
        semiconductor_process_equipment: "Semiconductor 工艺与设备",
        semiconductor_process_wip_details: "Semiconductor 工艺与WIP明细",
        semiconductor_quality_iqc: "Semiconductor 质量与IQC",
        semiconductor_revision_bases: "Revision Base 版本基础",
        semiconductor_scheduling_flow: "Semiconductor 排程与工艺流",
        semiconductor_security_kpi_configuration: "Semiconductor 安全与KPI配置",
        semiconductor_service_location: "Semiconductor 服务与位置",
        semiconductor_shared_support: "Semiconductor 公共支撑",
        semiconductor_shipping_integration: "Semiconductor 出货与集成",
        semiconductor_spc_quality_details: "Semiconductor SPC与质量明细",
        semiconductor_spc_yield: "Semiconductor SPC与良率",
        semiconductor_user_job_spc_configuration: "Semiconductor 用户作业与SPC配置",
        semiconductor_wafer_experiment: "Semiconductor 晶圆与实验",
        semiconductor_wip_control: "Semiconductor WIP控制",
        other: "Other 其他",
    };

    // ── Globals ──
    let graph = null;
    let rawData = null;
    let comboEnabled = false;
    let relMode = false;  // Relationship focus mode
    let layoutMode = "radial";  // Current layout
    let selectedNodeId = null;   // Persistent selection
    const API = "";  // same origin
    const classDetailCache = new Map(); // Client-side cache for class detail API responses

    // ── Layout presets ──
    const LAYOUTS = {
        "dagre-tb": {
            type: "dagre",
            rankdir: "TB",
            nodesep: 50,
            ranksep: 80,
            align: undefined,
        },
        "dagre-lr": {
            type: "dagre",
            rankdir: "LR",
            nodesep: 40,
            ranksep: 100,
            align: undefined,
        },
        "force": {
            type: "force",
            preventOverlap: true,
            nodeSize: 68,
            linkDistance: 160,
            nodeStrength: -400,
            edgeStrength: 0.3,
            collideStrength: 0.8,
            alphaDecay: 0.03,
        },
        "radial": {
            type: "radial",
            unitRadius: 200,
            linkDistance: 220,
            preventOverlap: true,
            nodeSize: 80,
            nodeSpacing: 50,
            focusNode: "Workflow",
            strictRadial: false
        },
    };

    const LAYOUT_LABELS = {
        "dagre-tb": "↓ 层次纵向",
        "dagre-lr": "→ 层次横向",
        "force": "⬤ 力导向",
        "radial": "◎ 径向",
    };
    const LAYOUT_KEYS = Object.keys(LAYOUTS);

    // ══════════════════════════════════════════════════════
    //  Fetch helpers
    // ══════════════════════════════════════════════════════
    async function fetchJSON(url) {
        const res = await fetch(API + url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    }

    // ══════════════════════════════════════════════════════
    //  Build G6 graph data from API response
    // ══════════════════════════════════════════════════════
    function buildGraphData(apiData, useCombo) {
        const nodes = apiData.nodes.map((n) => {
            let mod = n.data.module || "other";
            if (!COMBO_LABELS[mod]) {
                mod = "other";
            }
            const c = COLORS[mod] || COLORS.other;
            return {
                id: n.id,
                combo: useCombo ? mod : undefined,
                style: {
                    fill: c.fill,
                    stroke: c.stroke,
                    shadowColor: c.fill,
                    zIndex: 10,
                },
                data: {
                    ...n.data,
                    module: mod,
                },
            };
        });

        const edges = apiData.edges.map((e, i) => ({
            id: `e-${i}`,
            source: e.source,
            target: e.target,
            data: {
                ...e.data,
                type: "quadratic",
                style: {
                    stroke: "rgba(0,255,185,0.25)",
                    lineWidth: 1.5,
                    endArrow: true,
                    lineDash: e.data.lineStyle === "dashed" ? [5, 5] : undefined,
                    cursor: "pointer",
                    halo: 20,
                    haloOpacity: 0,
                    haloPointerEvents: "auto",
                },
                labelText: e.data.label || "",
                labelCfg: {
                    style: {
                        fill: "rgba(0,255,185,0.6)",
                        fontSize: 9,
                        fontFamily: "Inter",
                        background: {
                            fill: "rgba(0,0,40,0.8)",
                            padding: [2, 4, 2, 4],
                            radius: 3,
                        },
                    },
                    autoRotate: true,
                },
            },
        }));

        const combos = useCombo
            ? Object.keys(COMBO_LABELS).map((key) => {
                const c = COLORS[key] || COLORS.other;
                return {
                    id: key,
                    data: {
                        label: COMBO_LABELS[key],
                        type: "rect",
                        style: {
                            fill: c.comboFill,
                            stroke: c.comboBorder,
                            lineWidth: 1.5,
                            radius: 12,
                            lineDash: [4, 4],
                        },
                        labelCfg: {
                            style: {
                                fill: c.stroke,
                                fontSize: 13,
                                fontWeight: 600,
                                fontFamily: "Inter",
                            },
                            position: "top",
                        },
                    },
                };
            })
            : [];

        return { nodes, edges, combos };
    }

    // ══════════════════════════════════════════════════════
    //  Initialise the G6 Graph
    // ══════════════════════════════════════════════════════
    function initGraph(container, data) {
        const width = container.clientWidth;
        const height = container.clientHeight;

        graph = new G6.Graph({
            container,
            width,
            height,
            autoFit: "view",
            padding: [60, 60, 60, 60],
            // ── G6 v5 高密集节点渲染性能优化配置 ──
            culling: {
                enable: true,
                cullingDebounce: 30,
            },

            // ── Node defaults ──
            node: {
                type: "circle",
                style: {
                    zIndex: 10,
                    size: (d) => ["workflow", "mfgorder", "material", "product"].includes(d.data?.module) ? 76 : 52,
                    fill: (d) => (COLORS[d.data?.module] || COLORS.other).fill,
                    stroke: (d) => (COLORS[d.data?.module] || COLORS.other).stroke,
                    lineWidth: 2,
                    labelText: (d) => d.data?.chineseName ? (d.data.label || d.id) + '\n(' + d.data.chineseName + ')' : (d.data?.label || d.id),
                    labelFill: "#E8F0F2",
                    labelFontSize: 11,
                    labelFontWeight: 500,
                    labelFontFamily: "Inter, sans-serif",
                    labelPlacement: "bottom",
                    labelOffsetY: 8,
                    iconText: (d) => (d.data?.label || d.id).substring(0, 2),
                    iconFontSize: (d) => ["workflow", "mfgorder", "material", "product"].includes(d.data?.module) ? 18 : 14,
                    iconFontWeight: 700,
                    iconFill: "#fff",
                    iconFontFamily: "Inter, sans-serif",
                    shadowBlur: 0,
                    cursor: "pointer",
                    ports: [{ placement: "center" }],
                },
                state: {
                    active: {
                        stroke: "#00FFB9",
                        lineWidth: 3,
                        shadowColor: "#00FFB9",
                        shadowBlur: 10,
                        opacity: 1,
                        zIndex: 20,
                    },
                    selected: {
                        stroke: "#FFFFFF",
                        lineWidth: 4,
                        shadowColor: "#00FFB9",
                        shadowBlur: 14,
                        lineDash: undefined,
                        opacity: 1,
                        zIndex: 20,
                    },
                    highlighted: {
                        stroke: "#00FFB9",
                        lineWidth: 4,
                        shadowColor: "#00FFB9",
                        shadowBlur: 12,
                        opacity: 1,
                        zIndex: 20,
                    },
                    inactive: {
                        opacity: 0.45,
                        labelOpacity: 0.45,
                        iconOpacity: 0.45,
                        zIndex: 2,
                    },
                },
            },

            // ── Edge defaults ──
            edge: {
                type: "quadratic",
                style: {
                    zIndex: 0,
                    stroke: "rgba(0,255,185,0.2)",
                    lineWidth: 1.0,
                    shadowBlur: 0,
                    halo: 6,
                    haloOpacity: 0,
                    haloPointerEvents: "auto",
                    endArrowSize: 6,
                    endArrow: true,
                    labelText: (d) => d.data?.label || "",
                    labelOpacity: 0,
                    labelBackgroundOpacity: 0,
                    labelFill: "rgba(0,255,185,0.55)",
                    labelFontSize: 9,
                    labelFontFamily: "Inter, sans-serif",
                    labelBackgroundFill: "rgba(0,0,40,0.85)",
                    labelPadding: [2, 4],
                    labelBackgroundRadius: 3,
                    curveOffset: 20,
                    cursor: "pointer",
                },
                state: {
                    active: {
                        stroke: "#00FFB9",
                        lineWidth: 2.5,
                        shadowColor: "#00FFB9",
                        shadowBlur: 10,
                        halo: 12,
                        haloOpacity: 0,
                        haloPointerEvents: "auto",
                        pointerEvents: "auto",
                        interactive: true,
                        zIndex: 15,
                        labelOpacity: 1,
                        labelBackgroundOpacity: 1,
                        labelFill: "#00FFB9",
                        opacity: 1,
                    },
                    activeOut: {
                        stroke: "#00FFB9",
                        lineWidth: 2.5,
                        shadowColor: "#00FFB9",
                        shadowBlur: 10,
                        labelOpacity: 1,
                        labelBackgroundOpacity: 1,
                        labelFill: "#00FFB9",
                        endArrowSize: 8,
                        halo: 12,
                        haloOpacity: 0,
                        haloPointerEvents: "auto",
                        pointerEvents: "auto",
                        interactive: true,
                        zIndex: 15,
                        opacity: 1,
                    },
                    activeIn: {
                        stroke: "#FF4081",
                        lineWidth: 2.5,
                        shadowColor: "#FF4081",
                        shadowBlur: 10,
                        labelOpacity: 1,
                        labelBackgroundOpacity: 1,
                        labelFill: "#FF4081",
                        endArrowSize: 8,
                        halo: 12,
                        haloOpacity: 0,
                        haloPointerEvents: "auto",
                        pointerEvents: "auto",
                        interactive: true,
                        zIndex: 15,
                        opacity: 1,
                    },
                    inactive: {
                        opacity: 0.4,
                        labelOpacity: 0,
                        labelBackgroundOpacity: 0,
                        halo: 0,
                        pointerEvents: "none",
                        haloPointerEvents: "none",
                        interactive: false,
                        zIndex: -2,
                    },
                },
            },

            // ── Combo defaults ──
            combo: {
                type: "rect",
                style: {
                    zIndex: -5,
                    fill: (d) => (COLORS[d.id] || COLORS.other).comboFill,
                    fillOpacity: 1,
                    stroke: (d) => (COLORS[d.id] || COLORS.other).comboBorder,
                    lineWidth: 1.5,
                    lineDash: [6, 4],
                    radius: 16,
                    labelText: (d) => COMBO_LABELS[d.id] || d.id,
                    labelFill: (d) => (COLORS[d.id] || COLORS.other).stroke,
                    labelFontSize: 13,
                    labelFontWeight: 600,
                    labelFontFamily: "Inter, sans-serif",
                    labelPlacement: "top",
                    padding: 30,
                    cursor: "pointer",
                    collapsedMarker: false,
                },
                state: {
                    active: {
                        stroke: "#00FFB9",
                        lineWidth: 2,
                        zIndex: -3,
                    },
                    inactive: {
                        opacity: 0.15,
                        pointerEvents: "none",
                    },
                },
            },

            // ── Layout ──
            layout: { ...LAYOUTS[layoutMode] },

            // ── Behaviours ──
            behaviors: [
                "drag-canvas",
                "zoom-canvas",
                {
                    type: "drag-element",
                    state: null, // Only drag the hovered node, not all 'selected' nodes
                },
                "optimize-viewport-transform",
            ],

            // ── Plugins ──
            plugins: [
                {
                    type: "minimap",
                    size: [160, 100],
                    style: {
                        position: "absolute",
                        bottom: "20px",
                        right: "20px",
                        background: "rgba(0,0,40,0.7)",
                        border: "1px solid rgba(0,153,153,0.2)",
                        borderRadius: "8px",
                    },
                },
            ],

            // ── Animation (reduced duration for snappier interactions) ──
            animation: {
                duration: 300,
                easing: "ease-out",
            },

            data,
        });

        graph.render();

        // Expose graph for chat.js linking
        window._g6Graph = graph;

        // ── Node click → select + open detail panel (or toggle off if already selected) ──
        graph.on("node:click", async (evt) => {
            const nodeId = evt.target.id;

            // Toggle off if clicking the already selected node
            if (selectedNodeId === nodeId) {
                clearSelection();
                closePanel();
                return;
            }

            selectNode(nodeId);
            if (relMode) {
                await showRelOnly(nodeId);
            } else {
                await showClassDetail(nodeId);
            }
        });

        // ── Custom tooltip: show on node hover, hide on leave ──
        const tooltip = document.getElementById("nodeTooltip");

        graph.on("node:pointerenter", (evt) => {
            const nodeId = evt.target.id;
            const nodeData = graph.getNodeData(nodeId);
            if (!nodeData || !nodeData.data) return;
            const d = nodeData.data;
            if (!(d.type === "class" || d.module)) return;

            // Only show tooltip when hovering over the circle, not the label text below
            const canvasPos = graph.getCanvasByClient({ x: evt.client.x, y: evt.client.y });
            const nodePos = graph.getElementPosition(nodeId);
            const nodeSize = nodeData.style?.size || 52;
            const radius = (typeof nodeSize === 'function'
                ? nodeSize(d)
                : typeof nodeSize === 'number' ? nodeSize : 52) / 2;
            const dx = canvasPos.x - nodePos[0];
            const dy = canvasPos.y - nodePos[1];
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist > radius + 6) return; // pointer outside the circle

            tooltip.innerHTML = `<div class="tt-title">${d.label || nodeId}</div>
                                 <div class="tt-sub">${d.chineseName || ""}</div>
                                 <div style="margin-top:4px;color:#8DA4B8;font-size:11px">${d.description || ""}</div>`;
            tooltip.classList.remove("node-tooltip-hidden");
        });

        graph.on("node:pointermove", (evt) => {
            if (tooltip.classList.contains("node-tooltip-hidden")) return;

            // Hide tooltip when pointer moves outside the circle onto the label
            const nodeId = evt.target.id;
            const nodeData = graph.getNodeData(nodeId);
            if (nodeData) {
                const canvasPos = graph.getCanvasByClient({ x: evt.client.x, y: evt.client.y });
                const nodePos = graph.getElementPosition(nodeId);
                const sizeVal = nodeData.style?.size || 52;
                const radius = (typeof sizeVal === 'number' ? sizeVal : 52) / 2;
                const dx = canvasPos.x - nodePos[0];
                const dy = canvasPos.y - nodePos[1];
                if (Math.sqrt(dx * dx + dy * dy) > radius + 6) {
                    tooltip.classList.add("node-tooltip-hidden");
                    return;
                }
            }

            const clientX = evt.client?.x ?? 0;
            const clientY = evt.client?.y ?? 0;
            tooltip.style.left = (clientX + 16) + "px";
            tooltip.style.top = (clientY - 10) + "px";
        });

        graph.on("node:pointerleave", () => {
            tooltip.classList.add("node-tooltip-hidden");
        });

        // ── Canvas click → clear selection + close panel + hide edge popup ──
        // (skip if an edge was just clicked — guard prevents race condition)
        let edgeClickGuard = false;

        graph.on("canvas:click", () => {
            if (edgeClickGuard) { edgeClickGuard = false; return; }
            clearSelection();
            closePanel();
            hideEdgePopup();
        });

        // ── Edge click → show action popup (preserve node selection) ──
        graph.on("edge:click", (evt) => {
            edgeClickGuard = true;
            setTimeout(() => { edgeClickGuard = false; }, 200);

            let edgeId = evt.target.id;
            let edgeData = graph.getEdgeData(edgeId);
            if (!edgeData) return;

            // Check if the clicked edge is inactive
            const edgeStates = graph.getElementState(edgeId);
            if (edgeStates.includes("inactive")) {
                // Try to find if there's any active edge directly underneath the click position
                const canvasEl = document.getElementById("graphContainer");
                const rect = canvasEl.getBoundingClientRect();
                const clientX = evt.client?.x ?? (evt.canvas?.x + rect.left) ?? rect.left + rect.width / 2;
                const clientY = evt.client?.y ?? (evt.canvas?.y + rect.top) ?? rect.top + rect.height / 2;

                const canvasPos = graph.getCanvasByClient({ x: clientX, y: clientY });
                let activeEdgeId = null;

                try {
                    const canvas = graph.getCanvas();
                    if (canvas && canvas.document && typeof canvas.document.elementsFromPointSync === "function") {
                        const picked = canvas.document.elementsFromPointSync(canvasPos.x, canvasPos.y) || [];
                        for (const shape of picked) {
                            if (shape && shape.id) {
                                const isEdge = !!graph.getEdgeData(shape.id);
                                if (isEdge) {
                                    const elStates = graph.getElementState(shape.id);
                                    if (elStates.includes("active") || elStates.includes("activeOut") || elStates.includes("activeIn")) {
                                        activeEdgeId = shape.id;
                                        break;
                                    }
                                }
                            }
                        }
                    }
                } catch (err) {
                    console.warn("Fallback elements picking error:", err);
                }

                if (activeEdgeId) {
                    edgeId = activeEdgeId;
                    edgeData = graph.getEdgeData(edgeId);
                } else {
                    // No active edge under the cursor, treat it as a click on canvas (deselect)
                    clearSelection();
                    closePanel();
                    hideEdgePopup();
                    return;
                }
            }

            const relName = edgeData.data?.label || edgeId;
            const source = edgeData.source;
            const target = edgeData.target;
            const desc = edgeData.data?.description || "";
            const cardinality = edgeData.data?.cardinality || "";

            // Position popup near the click
            const canvasEl = document.getElementById("graphContainer");
            const rect = canvasEl.getBoundingClientRect();
            const clientX = evt.client?.x ?? (evt.canvas?.x + rect.left) ?? rect.left + rect.width / 2;
            const clientY = evt.client?.y ?? (evt.canvas?.y + rect.top) ?? rect.top + rect.height / 2;

            showEdgePopup(relName, source, target, desc, cardinality, clientX, clientY);
        });

        // ── Node click also hides edge popup ──
        graph.on("node:click", () => { hideEdgePopup(); });

        // ── Hover preview (only when nothing is selected) ──
        graph.on("node:mouseenter", (evt) => {
            if (selectedNodeId) return;
            highlightNeighbors(evt.target.id, false);
        });

        graph.on("node:mouseleave", () => {
            if (selectedNodeId) return;
            clearHighlight();
        });
    }

    // ══════════════════════════════════════════════════════
    //  Selection & Highlight
    // ══════════════════════════════════════════════════════
    function selectNode(nodeId) {
        selectedNodeId = nodeId;
        highlightNeighbors(nodeId, true);
        // Clear legend active states when focusing on a specific node
        document.querySelectorAll(".legend-item.active").forEach(el => el.classList.remove("active"));
    }
    // Expose for chat.js
    window._selectNode = selectNode;

    function clearSelection() {
        selectedNodeId = null;
        clearHighlight();
        // Clear legend active states
        document.querySelectorAll(".legend-item.active").forEach(el => el.classList.remove("active"));
    }

    // ── Performance: cache previous states for differential updates ──
    let _prevStates = null;

    function _applyStates(states) {
        // Differential state update: only send changes to G6
        if (_prevStates) {
            const diff = {};
            let hasDiff = false;
            for (const id in states) {
                const prev = _prevStates[id];
                const next = states[id];
                if (!prev || prev.length !== next.length || prev.join() !== next.join()) {
                    diff[id] = next;
                    hasDiff = true;
                }
            }
            // Also clear any elements in prev that are not in new states
            for (const id in _prevStates) {
                if (!(id in states)) {
                    diff[id] = [];
                    hasDiff = true;
                }
            }
            if (hasDiff) {
                graph.setElementState(diff);
            }
        } else {
            graph.setElementState(states);
        }
        _prevStates = states;
    }

    function highlightNeighbors(nodeId, isSelection) {
        if (!graph) return;
        const neighborIds = new Set();
        const outEdgeIds = new Set();
        const inEdgeIds = new Set();

        // Find connected edges and neighbor nodes
        const edgesData = graph.getEdgeData();
        for (let i = 0, len = edgesData.length; i < len; i++) {
            const edge = edgesData[i];
            if (edge.source === nodeId) {
                outEdgeIds.add(edge.id);
                neighborIds.add(edge.target);
            } else if (edge.target === nodeId) {
                inEdgeIds.add(edge.id);
                neighborIds.add(edge.source);
            }
        }

        const states = {};
        const nodesData = graph.getNodeData();
        for (let i = 0, len = nodesData.length; i < len; i++) {
            const node = nodesData[i];
            if (node.id === nodeId) {
                states[node.id] = isSelection ? ["selected"] : ["active"];
            } else if (neighborIds.has(node.id)) {
                states[node.id] = ["active"];
            } else {
                states[node.id] = ["inactive"];
            }
        }

        for (let i = 0, len = edgesData.length; i < len; i++) {
            const edge = edgesData[i];
            if (outEdgeIds.has(edge.id)) {
                states[edge.id] = ["activeOut"];
            } else if (inEdgeIds.has(edge.id)) {
                states[edge.id] = ["activeIn"];
            } else {
                states[edge.id] = ["inactive"];
            }
        }

        _applyStates(states);
    }

    function clearHighlight() {
        if (!graph) return;
        // Only send diff: reset elements that had non-empty state
        if (_prevStates) {
            const diff = {};
            let hasDiff = false;
            for (const id in _prevStates) {
                if (_prevStates[id].length > 0) {
                    diff[id] = [];
                    hasDiff = true;
                }
            }
            if (hasDiff) {
                graph.setElementState(diff);
            }
            _prevStates = null;
        }
    }

    // ══════════════════════════════════════════════════════
    //  GraphRAG Highlighting Logic
    // ══════════════════════════════════════════════════════
    function highlightGraph(highlightData) {
        if (!graph || !highlightData) return;

        const hlNodes = highlightData.nodes || [];
        const hlEdges = highlightData.edges || [];

        if (hlNodes.length === 0 && hlEdges.length === 0) {
            clearHighlight();
            return;
        }

        // Apply environment safety limit
        if (hlNodes.length > 50) {
            console.warn(`Highlight aborted: too many nodes (${hlNodes.length})`);
            return;
        }

        const states = {};
        let firstNodeId = null;

        graph.getNodeData().forEach((node) => {
            if (hlNodes.includes(node.id)) {
                states[node.id] = ["selected"];
                if (!firstNodeId) firstNodeId = node.id;
            } else {
                states[node.id] = ["inactive"];
            }
        });

        graph.getEdgeData().forEach((edge) => {
            const relName = edge.data?.label || edge.id;
            if (hlEdges.includes(relName) && hlNodes.includes(edge.source) && hlNodes.includes(edge.target)) {
                states[edge.id] = ["active"];
            } else {
                states[edge.id] = ["inactive"];
            }
        });

        // Apply graph-rag states (use differential update)
        _applyStates(states);

        // Focus camera on the subgraph
        if (firstNodeId) {
            selectedNodeId = firstNodeId; // Lock selection to prevent mouse hover from clearing highlight
            graph.focusElement(firstNodeId, true);
        }
    }

    window._highlightGraph = highlightGraph;

    // ══════════════════════════════════════════════════════
    //  Product Line State
    // ══════════════════════════════════════════════════════
    let currentProductLine = "general";
    let productLineList = [];

    function updateHeaderLinks() {
        const industryBtn = document.querySelector('a[href*="industry.html"]');
        if (industryBtn) {
            industryBtn.href = `/static/industry.html?product_line=${currentProductLine}`;
        }
    }

    async function loadProductLines() {
        try {
            const data = await fetchJSON("/api/product-lines");
            productLineList = data.product_lines || [];
            const select = document.getElementById("productLineSelect");
            select.innerHTML = "";
            for (const pl of productLineList) {
                const opt = document.createElement("option");
                opt.value = pl.id;
                opt.textContent = `${pl.icon} ${pl.name}`;
                select.appendChild(opt);
            }
            // Read from URL params or fallback to localStorage
            const urlParams = new URLSearchParams(window.location.search);
            let plParam = urlParams.get("product_line") || localStorage.getItem("selected_product_line") || "general";
            if (plParam && productLineList.some(p => p.id === plParam)) {
                currentProductLine = plParam;
                select.value = plParam;
                localStorage.setItem("selected_product_line", currentProductLine);
            } else {
                currentProductLine = "general";
                if (select) select.value = "general";
                localStorage.setItem("selected_product_line", "general");
            }
            
            // Update links initially
            updateHeaderLinks();

            // On change
            select.addEventListener("change", (e) => {
                currentProductLine = e.target.value;
                const url = new URL(window.location);
                if (currentProductLine === "general") {
                    url.searchParams.delete("product_line");
                    localStorage.setItem("selected_product_line", "general");
                } else {
                    url.searchParams.set("product_line", currentProductLine);
                    localStorage.setItem("selected_product_line", currentProductLine);
                }
                window.history.replaceState({}, "", url);
                
                // Update links on change
                updateHeaderLinks();

                hideEdgePopup();
            });
        } catch (e) {
            console.warn("Failed to load product lines:", e);
        }
    }

    function getProductLineInfo(plId) {
        return productLineList.find(p => p.id === plId) || { id: plId, name: plId, icon: "📦", color: "#999" };
    }

    // Expose for chat.js
    window._getCurrentProductLine = () => currentProductLine;

    // ══════════════════════════════════════════════════════
    //  Edge Action Popup (Wiki-First)
    // ══════════════════════════════════════════════════════
    let currentEdgeInfo = null;
    let currentWikiContent = null;  // raw markdown content for editing

    async function showEdgePopup(relName, source, target, desc, cardinality, x, y) {
        const popup = document.getElementById("edgePopup");
        const titleEl = document.getElementById("edgePopupTitle");
        const metaEl = document.getElementById("edgePopupMeta");
        const plEl = document.getElementById("edgePopupPL");
        const wikiArea = document.getElementById("edgeWikiArea");
        const wikiLoading = document.getElementById("edgeWikiLoading");
        const wikiContent = document.getElementById("edgeWikiContent");
        const wikiEmpty = document.getElementById("edgeWikiEmpty");
        const generateBtn = document.getElementById("edgePopupGenerate");
        const editBtn = document.getElementById("edgePopupEdit");

        titleEl.textContent = relName;
        const sourceNode = graph.getNodeData(source);
        const targetNode = graph.getNodeData(target);
        const sourceChinese = sourceNode?.data?.chineseName || "";
        const targetChinese = targetNode?.data?.chineseName || "";
        const sourceDisplay = sourceChinese ? `${source} (${sourceChinese})` : source;
        const targetDisplay = targetChinese ? `${target} (${targetChinese})` : target;

        let metaText = `${sourceDisplay}  →  ${targetDisplay}`;
        if (cardinality) metaText += `  ·  ${cardinality}`;
        if (desc) metaText += `\n${desc}`;
        metaEl.textContent = metaText;

        // Show product line badge
        const plInfo = getProductLineInfo(currentProductLine);
        plEl.textContent = `${plInfo.icon} ${plInfo.name}`;

        // Store for buttons
        currentEdgeInfo = { relName, source, target, desc, cardinality };
        currentWikiContent = null;

        // Reset wiki area
        wikiLoading.style.display = "none";
        wikiContent.style.display = "none";
        wikiContent.innerHTML = "";
        wikiEmpty.style.display = "flex";
        generateBtn.style.display = "inline-flex";
        generateBtn.disabled = false;
        generateBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg> 生成 Wiki`;
        editBtn.style.display = "none";

        // Position popup near click, but keep within viewport
        const popupW = 380;
        const popupH = 400;
        let left = Math.min(x + 12, window.innerWidth - popupW - 16);
        let top = Math.min(y - 60, window.innerHeight - popupH - 16);
        top = Math.max(60, top);

        popup.style.left = left + "px";
        popup.style.top = top + "px";
        popup.classList.remove("edge-popup-hidden");

        // ── Auto-load wiki if exists (fast filesystem read, matches product line) ──
        try {
            const wikiUrl = `/api/wiki/relationship?source=${encodeURIComponent(source)}&rel=${encodeURIComponent(relName)}&target=${encodeURIComponent(target)}&product_line=${encodeURIComponent(currentProductLine)}`;
            const wikiData = await fetchJSON(wikiUrl);

            if (wikiData.found && wikiData.content) {
                currentWikiContent = wikiData.content;
                wikiEmpty.style.display = "none";
                wikiContent.innerHTML = marked.parse(wikiData.content);
                wikiContent.style.display = "block";
                generateBtn.style.display = "none";
                editBtn.style.display = "inline-flex";
            }
        } catch (e) {
            // Wiki read failed — keep showing empty state, user can still click generate
            console.warn("Wiki read error:", e);
        }
    }

    function hideEdgePopup() {
        document.getElementById("edgePopup").classList.add("edge-popup-hidden");
        currentEdgeInfo = null;
        currentWikiContent = null;
    }

    // Wire the "Ask AI" button
    document.getElementById("edgePopupAsk").addEventListener("click", () => {
        if (!currentEdgeInfo) return;
        const { relName, source, target, desc, cardinality } = currentEdgeInfo;

        // Build a natural-language question about this relationship
        let question = `请详细解释 [[${source}]] 与 [[${target}]] 之间的 ${relName} 关系。\n`;
        question += `> 当前关系定义：${source} → ${target} · ${cardinality || 'UNKNOWN'}${desc ? ' ' + desc : ''}\n\n`;
        question += `在实际 Opcenter 建模中，什么时候需要配置这个关系？请举例说明其业务场景。`;

        hideEdgePopup();

        // Send to chat via exposed function
        if (typeof window._askQuestion === "function") {
            window._askQuestion(question);
        }
    });

    // Wire the "Generate Wiki" button — first try read, then generate
    document.getElementById("edgePopupGenerate").addEventListener("click", async () => {
        if (!currentEdgeInfo) return;
        const { relName, source, target, desc, cardinality } = currentEdgeInfo;
        const generateBtn = document.getElementById("edgePopupGenerate");
        const wikiLoading = document.getElementById("edgeWikiLoading");
        const wikiContent = document.getElementById("edgeWikiContent");
        const wikiEmpty = document.getElementById("edgeWikiEmpty");
        const editBtn = document.getElementById("edgePopupEdit");

        generateBtn.disabled = true;
        generateBtn.textContent = "⏳ 加载中...";
        wikiEmpty.style.display = "none";
        wikiLoading.style.display = "flex";

        try {
            // Step 1: Try reading existing wiki first
            const wikiUrl = `/api/wiki/relationship?source=${encodeURIComponent(source)}&rel=${encodeURIComponent(relName)}&target=${encodeURIComponent(target)}&product_line=${encodeURIComponent(currentProductLine)}`;
            const wikiData = await fetchJSON(wikiUrl);

            if (wikiData.found && wikiData.content) {
                // Wiki exists — display it
                currentWikiContent = wikiData.content;
                wikiLoading.style.display = "none";
                wikiContent.innerHTML = marked.parse(wikiData.content);
                wikiContent.style.display = "block";
                generateBtn.style.display = "none";
                editBtn.style.display = "inline-flex";
                return;
            }

            // Step 2: Wiki doesn't exist, generate via LLM
            generateBtn.textContent = "🤖 AI 生成中...";
            const res = await fetch("/api/wiki/generate-one", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    source, rel: relName, target,
                    product_line: currentProductLine,
                    cardinality: cardinality || "",
                    description: desc || "",
                    overwrite: false,
                }),
            });

            wikiLoading.style.display = "none";
            wikiContent.style.display = "block";
            wikiContent.innerHTML = `<div style="color:var(--si-green);display:flex;align-items:center;gap:8px;"><div class="wiki-spinner"></div> 🤖 AI 正在规划撰写知识库...</div>`;

            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let fullText = "";
            let buffer = "";
            let lastRenderTime = 0;
            const RENDER_THROTTLE_MS = 150; // Render at most once every 150ms to prevent browser thread freeze

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split("\n");
                buffer = lines.pop() || "";

                for (const line of lines) {
                    if (!line.startsWith("data: ")) continue;
                    try {
                        const payload = JSON.parse(line.slice(6));
                        if (payload.type === "chunk") {
                            fullText += payload.content;
                            const now = Date.now();
                            if (now - lastRenderTime > RENDER_THROTTLE_MS) {
                                wikiContent.innerHTML = marked.parse(fullText);
                                lastRenderTime = now;
                            }
                        } else if (payload.type === "done") {
                            currentWikiContent = payload.content;
                        } else if (payload.type === "error") {
                            wikiContent.innerHTML = `<span style="color:#FF6666">❌ 生成失败: ${payload.content}</span>`;
                        }
                    } catch (_) {}
                }
            }

            if (fullText) {
                wikiContent.innerHTML = marked.parse(currentWikiContent || fullText);
                generateBtn.style.display = "none";
                editBtn.style.display = "inline-flex";
            } else {
                wikiContent.style.display = "none";
                wikiEmpty.style.display = "flex";
                generateBtn.disabled = false;
                generateBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg> 重试`;
            }
        } catch (e) {
            wikiLoading.style.display = "none";
            wikiEmpty.style.display = "flex";
            generateBtn.disabled = false;
            generateBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg> 重试`;
            console.error("Wiki load error:", e);
        }
    });

    // Wire the "Edit Wiki" button
    document.getElementById("edgePopupEdit").addEventListener("click", () => {
        if (!currentEdgeInfo) return;
        openWikiEditor();
    });

    // Wire the close button
    document.getElementById("edgePopupClose").addEventListener("click", () => {
        hideEdgePopup();
    });

    // ── Make the popup draggable (Edge compat + user repositioning) ──
    (function setupPopupDrag() {
        const popup = document.getElementById("edgePopup");
        let dragging = false;
        let startX, startY, startLeft, startTop;

        function onStart(e) {
            // Only start drag from title/meta area, not from buttons or wiki area
            const target = e.target;
            if (target.closest("button") || target.closest("textarea") || target.closest(".edge-popup-actions") || target.closest(".edge-wiki-area")) return;

            dragging = true;
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            startX = clientX;
            startY = clientY;
            startLeft = parseFloat(popup.style.left) || popup.getBoundingClientRect().left;
            startTop = parseFloat(popup.style.top) || popup.getBoundingClientRect().top;
            popup.style.transition = "none";
            popup.style.cursor = "grabbing";
            e.stopPropagation();
            e.preventDefault();
        }

        function onMove(e) {
            if (!dragging) return;
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            const dx = clientX - startX;
            const dy = clientY - startY;
            popup.style.left = (startLeft + dx) + "px";
            popup.style.top = (startTop + dy) + "px";
        }

        function onEnd() {
            if (!dragging) return;
            dragging = false;
            popup.style.transition = "";
            popup.style.cursor = "";
        }

        popup.addEventListener("mousedown", onStart);
        popup.addEventListener("touchstart", onStart, { passive: false });
        document.addEventListener("mousemove", onMove);
        document.addEventListener("touchmove", onMove, { passive: false });
        document.addEventListener("mouseup", onEnd);
        document.addEventListener("touchend", onEnd);
    })();

    // ══════════════════════════════════════════════════════
    //  Wiki Editor Modal
    // ══════════════════════════════════════════════════════
    function openWikiEditor() {
        const modal = document.getElementById("wikiEditorModal");
        const titleEl = document.getElementById("wikiEditorTitle");
        const textarea = document.getElementById("wikiEditorTextarea");

        if (!currentEdgeInfo) return;
        const { relName, source, target } = currentEdgeInfo;
        const plInfo = getProductLineInfo(currentProductLine);

        titleEl.textContent = `编辑 Wiki: ${source} → ${relName} → ${target}  (${plInfo.icon} ${plInfo.name})`;
        textarea.value = currentWikiContent || "";
        modal.classList.remove("wiki-editor-hidden");
        textarea.focus();
    }

    function closeWikiEditor() {
        document.getElementById("wikiEditorModal").classList.add("wiki-editor-hidden");
    }

    document.getElementById("wikiEditorClose").addEventListener("click", closeWikiEditor);
    document.getElementById("wikiEditorCancel").addEventListener("click", closeWikiEditor);

    document.getElementById("wikiEditorSave").addEventListener("click", async () => {
        if (!currentEdgeInfo) return;
        const { relName, source, target } = currentEdgeInfo;
        const textarea = document.getElementById("wikiEditorTextarea");
        const content = textarea.value.trim();
        const saveBtn = document.getElementById("wikiEditorSave");

        if (!content) return;

        saveBtn.disabled = true;
        saveBtn.textContent = "⏳ 保存中...";

        try {
            const res = await fetch("/api/wiki/save", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    source, rel: relName, target,
                    product_line: currentProductLine,
                    content,
                    editor: "user",
                }),
            });
            const data = await res.json();

            if (data.saved) {
                // Update the popup content
                currentWikiContent = content;
                const wikiContentEl = document.getElementById("edgeWikiContent");
                wikiContentEl.innerHTML = marked.parse(content);
                wikiContentEl.style.display = "block";
                document.getElementById("edgeWikiEmpty").style.display = "none";
                document.getElementById("edgePopupGenerate").style.display = "none";
                document.getElementById("edgePopupEdit").style.display = "inline-flex";

                closeWikiEditor();
            } else {
                alert("保存失败: " + JSON.stringify(data));
            }
        } catch (e) {
            console.error("Wiki save error:", e);
            alert("保存失败: " + e.message);
        } finally {
            saveBtn.disabled = false;
            saveBtn.textContent = "💾 保存";
        }
    });

    // ══════════════════════════════════════════════════════
    //  Detail Panel (Layered Loading – Level 1)
    // ══════════════════════════════════════════════════════
    async function showClassDetail(className) {
        // Expose for chat.js
        window._showClassDetail = showClassDetail;
        const panel = document.getElementById("detailPanel");
        const panelTitle = document.getElementById("panelTitle");
        const sectionMeta = document.getElementById("sectionMeta");
        const propTable = document.getElementById("propTable");
        const relList = document.getElementById("relList");
        const sectionProperties = document.getElementById("sectionProperties");

        panelTitle.textContent = className;

        let detail;
        if (classDetailCache.has(className)) {
            detail = classDetailCache.get(className);
            sectionProperties.style.display = "";
            panel.classList.remove("panel-hidden");
        } else {
            // Show loading state for network fetch
            sectionMeta.innerHTML = `<div class="meta-row"><span class="meta-value" style="color:var(--text-muted)">加载中...</span></div>`;
            propTable.innerHTML = "";
            relList.innerHTML = "";
            sectionProperties.style.display = "";
            panel.classList.remove("panel-hidden");

            try {
                detail = await fetchJSON(`/api/graph/class/${className}`);
                classDetailCache.set(className, detail);
            } catch (err) {
                sectionMeta.innerHTML = `<div class="meta-row"><span class="meta-value" style="color:#FF6666">加载失败: ${err.message}</span></div>`;
                return;
            }
        }

        try {

            // ── Meta ──
            // find node in rawData for extra info
            const nodeInfo = rawData?.nodes?.find((n) => n.id === className);
            const module = nodeInfo?.data?.module || "other";
            const chName = nodeInfo?.data?.chineseName || "";
            const desc = nodeInfo?.data?.description || "";

            sectionMeta.innerHTML = `
                <div class="meta-row"><span class="meta-label">中文名</span><span class="meta-value">${chName || "—"}</span></div>
                <div class="meta-row"><span class="meta-label">模块</span><span class="meta-value" style="color:${(COLORS[module] || COLORS.other).fill}">${module.toUpperCase()}</span></div>
                <div class="meta-row"><span class="meta-label">描述</span><span class="meta-value">${desc || "—"}</span></div>
            `;

            // ── Properties ──
            if (detail.properties && detail.properties.length > 0) {
                let html = `<table class="prop-table"><thead><tr><th>属性名</th><th>类型</th><th>描述</th></tr></thead><tbody>`;
                for (const p of detail.properties) {
                    html += `<tr>
                        <td style="color:var(--text-primary);font-weight:500;max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${p.name}">${p.name}</td>
                        <td><span class="type-badge">${p.dataType || "String"}</span></td>
                        <td>${p.description || "—"}</td>
                    </tr>`;
                }
                html += `</tbody></table>`;
                propTable.innerHTML = html;
            } else {
                propTable.innerHTML = `<div style="color:var(--text-muted);font-size:12px;">暂无属性</div>`;
            }

            // ── Relations ──
            let relHtml = "";
            if (detail.outgoing && detail.outgoing.length > 0) {
                relHtml += `<div class="rel-section-label">它引用的对象 →</div>`;
                for (const r of detail.outgoing) {
                    relHtml += `<div class="rel-item rel-item-out" data-target="${r.targetClass}">
                        <span class="rel-arrow">→</span>
                        <span class="rel-name">${r.relName}</span>
                        <span class="rel-target">${r.targetClass}</span>
                        <span class="rel-card">${r.cardinality || ""}</span>
                    </div>`;
                }
            }
            if (detail.incoming && detail.incoming.length > 0) {
                relHtml += `<div class="rel-section-label rel-section-label-in" style="margin-top:12px">被何处引用 ←</div>`;
                for (const r of detail.incoming) {
                    relHtml += `<div class="rel-item rel-item-in" data-target="${r.sourceClass}">
                        <span class="rel-arrow">←</span>
                        <span class="rel-name">${r.relName}</span>
                        <span class="rel-target">${r.sourceClass}</span>
                        <span class="rel-card">${r.cardinality || ""}</span>
                    </div>`;
                }
            }
            relList.innerHTML = relHtml || `<div style="color:var(--text-muted);font-size:12px;">暂无关系</div>`;

            // ── Click relation chip → navigate ──
            relList.querySelectorAll(".rel-item").forEach((el) => {
                el.addEventListener("click", () => {
                    const target = el.dataset.target;
                    if (target) showClassDetail(target);
                });
            });
        } catch (err) {
            sectionMeta.innerHTML = `<div class="meta-row"><span class="meta-value" style="color:#FF6666">加载失败: ${err.message}</span></div>`;
        }
    }

    function closePanel() {
        document.getElementById("detailPanel").classList.add("panel-hidden");
    }

    // ══════════════════════════════════════════════════════
    // ══════════════════════════════════════════════════════
    //  Search
    // ══════════════════════════════════════════════════════
    function setupSearch() {
        const input = document.getElementById("searchInput");
        let debounceTimer;
        let isComposing = false;

        // 阻断拼音输入法输入期间的频繁检索重绘
        input.addEventListener("compositionstart", () => {
            isComposing = true;
        });

        input.addEventListener("compositionend", () => {
            isComposing = false;
            // 汉字选词上屏后立即执行检索
            triggerSearch(input.value.trim());
        });

        input.addEventListener("input", () => {
            if (isComposing) return; // 拼音打字过程中不触发检索

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                triggerSearch(input.value.trim());
            }, 350); // 适度增加防抖时间至 350ms 减缓冲击
        });

        function triggerSearch(text) {
            const query = text.toLowerCase();
            if (!graph || !rawData) return;

            if (!query) {
                // 清空全部高亮状态
                clearHighlight();
                return;
            }

            // 高性能 for 循环和 indexOf 匹配，避免频繁 callback 堆栈开销
            const states = {};
            const nodes = rawData.nodes;
            const len = nodes.length;

            for (let i = 0; i < len; i++) {
                const n = nodes[i];
                const label = (n.data?.label || n.id).toLowerCase();
                const cn = (n.data?.chineseName || "").toLowerCase();
                const match = label.indexOf(query) !== -1 || cn.indexOf(query) !== -1;
                states[n.id] = match ? ["active"] : ["inactive"];
            }

            _applyStates(states);
        }
    }

    // ══════════════════════════════════════════════════════
    //  Stats
    // ══════════════════════════════════════════════════════
    async function loadStats() {
        try {
            const s = await fetchJSON("/api/stats");
            document.querySelector("#statClasses .stat-num").textContent = s.classCount;
            document.querySelector("#statProps .stat-num").textContent = s.propertyCount;
            document.querySelector("#statRels .stat-num").textContent = s.relationCount;
        } catch (_) { /* silent */ }
    }

    // ══════════════════════════════════════════════════════
    //  Relationship Focus Mode
    // ══════════════════════════════════════════════════════
    function toggleRelMode() {
        relMode = !relMode;
        const btn = document.getElementById("btnRelMode");
        const body = document.body;

        if (relMode) {
            btn.classList.add("icon-btn-active");
            body.classList.add("rel-mode");
            closePanel();
            // Switch to dagre-LR for clean relationship view
            switchLayout("dagre-lr", true);
        } else {
            btn.classList.remove("icon-btn-active");
            body.classList.remove("rel-mode");
            // Restore to dagre-TB
            switchLayout("dagre-tb", true);
        }
    }

    // ── Rel-only panel (no properties, just relationships) ──
    async function showRelOnly(className) {
        const panel = document.getElementById("detailPanel");
        const panelTitle = document.getElementById("panelTitle");
        const sectionMeta = document.getElementById("sectionMeta");
        const propTable = document.getElementById("propTable");
        const relList = document.getElementById("relList");
        const sectionProperties = document.getElementById("sectionProperties");

        panelTitle.textContent = className + " — 关系视图";

        let detail;
        if (classDetailCache.has(className)) {
            detail = classDetailCache.get(className);
            sectionProperties.style.display = "none";
            panel.classList.remove("panel-hidden");
        } else {
            // Show loading state for network fetch
            sectionMeta.innerHTML = `<div class="meta-row"><span class="meta-value" style="color:var(--text-muted)">加载中...</span></div>`;
            propTable.innerHTML = "";
            relList.innerHTML = "";
            sectionProperties.style.display = "none";
            panel.classList.remove("panel-hidden");

            try {
                detail = await fetchJSON(`/api/graph/class/${className}`);
                classDetailCache.set(className, detail);
            } catch (err) {
                sectionMeta.innerHTML = `<div class="meta-row"><span class="meta-value" style="color:#FF6666">加载失败: ${err.message}</span></div>`;
                return;
            }
        }

        try {
            const nodeInfo = rawData?.nodes?.find(n => n.id === className);
            const module = nodeInfo?.data?.module || "other";
            const chName = nodeInfo?.data?.chineseName || "";

            sectionMeta.innerHTML = `
                <div class="meta-row"><span class="meta-label">类名</span><span class="meta-value" style="font-weight:600;color:var(--si-green)">${className}</span></div>
                <div class="meta-row"><span class="meta-label">中文名</span><span class="meta-value">${chName || "—"}</span></div>
                <div class="meta-row"><span class="meta-label">模块</span><span class="meta-value" style="color:${(COLORS[module] || COLORS.other).fill}">${module.toUpperCase()}</span></div>
                <div class="meta-row"><span class="meta-label">引用了</span><span class="meta-value" style="color:var(--si-green);font-weight:700">${(detail.outgoing || []).length}</span></div>
                <div class="meta-row"><span class="meta-label">被引用</span><span class="meta-value" style="color:#FF4081;font-weight:700">${(detail.incoming || []).length}</span></div>
            `;

            // Relationships only
            let relHtml = "";
            if (detail.outgoing && detail.outgoing.length > 0) {
                relHtml += `<div class="rel-section-label">它引用的对象 →</div>`;
                for (const r of detail.outgoing) {
                    relHtml += `<div class="rel-item rel-item-out" data-target="${r.targetClass}">
                        <span class="rel-arrow">→</span>
                        <span class="rel-name">${r.relName}</span>
                        <span class="rel-target">${r.targetClass}</span>
                        <span class="rel-card">${r.cardinality || ""}</span>
                    </div>`;
                }
            }
            if (detail.incoming && detail.incoming.length > 0) {
                relHtml += `<div class="rel-section-label rel-section-label-in" style="margin-top:12px">被何处引用 ←</div>`;
                for (const r of detail.incoming) {
                    relHtml += `<div class="rel-item rel-item-in" data-target="${r.sourceClass}">
                        <span class="rel-arrow">←</span>
                        <span class="rel-name">${r.relName}</span>
                        <span class="rel-target">${r.sourceClass}</span>
                        <span class="rel-card">${r.cardinality || ""}</span>
                    </div>`;
                }
            }
            relList.innerHTML = relHtml || `<div style="color:var(--text-muted);font-size:12px;">暂无关系</div>`;

            // Click to navigate
            relList.querySelectorAll(".rel-item").forEach(el => {
                el.addEventListener("click", () => {
                    const target = el.dataset.target;
                    if (target) showRelOnly(target);
                });
            });
        } catch (err) {
            sectionMeta.innerHTML = `<div class="meta-row"><span class="meta-value" style="color:#FF6666">加载失败: ${err.message}</span></div>`;
        }
    }

    // ══════════════════════════════════════════════════════
    //  Toolbar Buttons & Export
    // ══════════════════════════════════════════════════════
    function setupToolbar() {
        document.getElementById("btnFitView").addEventListener("click", () => {
            if (graph) graph.fitView();
        });

        document.getElementById("btnToggleCombo").addEventListener("click", () => {
            comboEnabled = !comboEnabled;
            if (rawData && graph) {
                const data = buildGraphData(rawData, comboEnabled);
                graph.setData(data);
                graph.render();
            }
        });

        document.getElementById("btnRelMode").addEventListener("click", toggleRelMode);

        // Layout cycling button
        document.getElementById("btnLayout").addEventListener("click", () => {
            const idx = LAYOUT_KEYS.indexOf(layoutMode);
            const nextIdx = (idx + 1) % LAYOUT_KEYS.length;
            switchLayout(LAYOUT_KEYS[nextIdx]);
        });

        document.getElementById("btnClosePanel").addEventListener("click", () => {
            closePanel();
            // Restore properties section visibility
            document.getElementById("sectionProperties").style.display = "";
        });

        // ── Export Listeners ──


        document.getElementById("btnExportHTML").addEventListener("click", exportOfflineHTML);
    }

    /**
     * Generates a standalone HTML file with embedded data and viewer
     */
    async function exportOfflineHTML() {
        if (!rawData || !graph) return;

        let cssContent = "";
        try {
            const res = await fetch("/static/style.css");
            cssContent = await res.text();
        } catch (e) { console.warn(e); }

        let g6Script = "";
        try {
            const res = await fetch("/static/lib/g6.js");
            g6Script = await res.text();
        } catch (e) { console.warn(e); }

        // Capture current data and positions
        const currentData = graph.getData();

        // Flatten the data: remove combos and ensure x,y are at the root
        // Keep only clean JSON data properties to prevent G6 v5 circular structures
        const flattenedNodes = currentData.nodes.map(n => {
            const pos = graph.getElementPosition(n.id) || [0, 0];
            const x = pos[0];
            const y = pos[1];
            const { comboId, ...cleanData } = n.data || {};

            return {
                id: n.id,
                style: {
                    x: x,
                    y: y
                },
                data: {
                    label: cleanData.label,
                    chineseName: cleanData.chineseName,
                    description: cleanData.description,
                    module: cleanData.module,
                    layer: cleanData.layer
                }
            };
        });

        // Clean edges to strip G6 internal runtime styles/references
        const cleanEdges = currentData.edges.map(e => ({
            id: e.id,
            source: e.source,
            target: e.target,
            data: {
                label: e.data?.label || "",
                cardinality: e.data?.cardinality || "",
                description: e.data?.description || ""
            }
        }));

        // Capture all current states
        const currentStates = {};
        currentData.nodes.forEach(n => {
            currentStates[n.id] = graph.getElementState(n.id);
        });
        currentData.edges.forEach(e => {
            currentStates[e.id] = graph.getElementState(e.id);
        });

        const g6ImportBlock = g6Script 
            ? `<script>${g6Script}</script>` 
            : `<script src="https://unpkg.com/@antv/g6@5.0.24/dist/g6.min.js"></script>`;

        const htmlContent = `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Opcenter Ontology Snapshot</title>
    <style>
        ${cssContent}
        body { background: #000D1A; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
        #app { height: 100vh !important; margin-top: 0 !important; display: flex; overflow: hidden; }
        #graphContainer { flex: 1; height: 100%; position: relative; background: radial-gradient(circle at center, #001A33 0%, #000D1A 100%); }
        .dropdown, #chatToggleBtn, .icon-btn-chat, .topbar-divider { display: none !important; }
        #detailPanel { position: absolute; right: 0; top: 0; bottom: 0; width: 320px; transition: transform 0.3s ease; }
    </style>
    ${g6ImportBlock}
</head>
<body>
    <main id="app">
        <div id="graphContainer">
            <div style="position:absolute; top:20px; left:20px; z-index:10; color:rgba(255,255,255,0.5); font-size:12px; pointer-events:none;">
                Opcenter Ontology Explorer - 离线快照<br/>导出时间: ${new Date().toLocaleString()}
            </div>
        </div>
        <aside id="detailPanel" class="panel-hidden">
            <div class="panel-header">
                <h2 id="panelTitle">详情</h2>
                <button onclick="document.getElementById('detailPanel').classList.add('panel-hidden')" style="color:#fff;background:none;border:none;cursor:pointer;font-size:20px;">×</button>
            </div>
            <div class="panel-body">
                <div id="sectionMeta" class="panel-section"></div>
                <div id="sectionProperties" class="panel-section"></div>
                <div id="sectionRelations" class="panel-section"></div>
            </div>
        </aside>
    </main>
    <div id="legend" class="legend-collapsed">
        <div class="legend-header" onclick="document.getElementById('legend').classList.toggle('legend-collapsed')">
            <div class="legend-title">模块图例</div>
        </div>
        <div class="legend-list" id="legendList"></div>
    </div>

    <script>
        const graphData = {
            nodes: ${JSON.stringify(flattenedNodes)},
            edges: ${JSON.stringify(cleanEdges)}
        };
        const graphStates = ${JSON.stringify(currentStates)};
        const COLORS = ${JSON.stringify(COLORS)};
        const COMBO_LABELS = ${JSON.stringify(COMBO_LABELS)};
        
        window.addEventListener("load", () => {
            const container = document.getElementById('graphContainer');
            const width = container.clientWidth || window.innerWidth || 800;
            const height = container.clientHeight || window.innerHeight || 600;
            const graph = new G6.Graph({
                container: 'graphContainer',
                width: width,
                height: height,
                autoFit: 'view',
                node: {
                    type: 'circle',
                    style: {
                        size: 48,
                        fill: (d) => (COLORS[d.data?.module] || COLORS.other).fill,
                        stroke: (d) => (COLORS[d.data?.module] || COLORS.other).stroke,
                        lineWidth: 2,
                        labelText: (d) => d.data?.chineseName ? (d.data.label || d.id) + '\\n(' + d.data.chineseName + ')' : (d.data?.label || d.id),
                        labelFill: "#E8F0F2",
                        labelFontSize: 12,
                        labelPlacement: "bottom",
                        labelOffsetY: 5,
                        iconText: (d) => (d.data?.label || d.id).substring(0, 2),
                        iconFill: "#fff",
                        iconFontSize: 14,
                        iconFontWeight: 700,
                        cursor: "pointer",
                    },
                    state: {
                        highlighted: { lineWidth: 4, stroke: "#00FFB9", shadowBlur: 20, shadowColor: "#00FFB9", zIndex: 20 },
                        inactive: { opacity: 0.45, labelOpacity: 0.45, iconOpacity: 0.45, zIndex: 2 }
                    }
                },
                edge: {
                    type: 'quadratic',
                    style: {
                        stroke: "rgba(0,255,185,0.2)",
                        lineWidth: 1.0,
                        shadowBlur: 0,
                        halo: true,
                        haloLineWidth: 6,
                        haloStroke: "rgba(0,255,185,0.0)",
                        haloPointerEvents: "auto",
                        endArrowSize: 6,
                        endArrow: true,
                        labelText: (d) => d.data?.label || "",
                        labelFill: "rgba(0,255,185,0.75)",
                        labelFontSize: 10.5,
                        labelFontFamily: "Inter, sans-serif",
                        labelFontWeight: 500,
                        labelBackgroundFill: "rgba(0,0,40,0.88)",
                        labelBackgroundOpacity: 1,
                        labelPadding: [3, 6],
                        labelBackgroundRadius: 10,
                        curveOffset: 20,
                        cursor: "pointer",
                    },
                    state: {
                        active: {
                            stroke: "#00FFB9",
                            lineWidth: 1.7,
                            labelFill: "#00FFB9",
                            labelFontWeight: 600,
                            opacity: 1,
                            haloLineWidth: 45,
                            pointerEvents: "auto",
                            interactive: true,
                            zIndex: 12,
                        },
                        activeOut: {
                            stroke: "#00FFB9",
                            lineWidth: 2.0,
                            labelFill: "#00FFB9",
                            endArrowSize: 8,
                            labelFontWeight: 600,
                            opacity: 1,
                            haloLineWidth: 45,
                            pointerEvents: "auto",
                            interactive: true,
                            zIndex: 12,
                        },
                        activeIn: {
                            stroke: "#FF4081",
                            lineWidth: 2.0,
                            labelFill: "#FF4081",
                            endArrowSize: 8,
                            labelFontWeight: 600,
                            opacity: 1,
                            haloLineWidth: 45,
                            pointerEvents: "auto",
                            interactive: true,
                            zIndex: 12,
                        },
                        inactive: {
                            opacity: 0.4,
                            labelFill: "rgba(0,255,185,0.15)",
                            labelBackgroundFill: "rgba(0,0,40,0.2)",
                            pointerEvents: "none",
                            haloLineWidth: 0,
                            interactive: false,
                            zIndex: -2,
                        },
                    }
                },
                behaviors: [
                    'drag-canvas',
                    'zoom-canvas',
                    {
                        type: 'drag-element',
                        enableTransient: true,
                    },
                    'optimize-viewport-transform',
                    'click-select'
                ],
            });

            graph.setData(graphData);
            graph.render().then(() => {
                graph.setElementState(graphStates);
            });

            // Legend Rendering
            const list = document.getElementById('legendList');
            Object.keys(COMBO_LABELS).forEach(k => {
                const item = document.createElement('div');
                item.className = 'legend-item';
                item.innerHTML = '<span class="legend-dot" style="background:'+COLORS[k].fill+'"></span>' + COMBO_LABELS[k];
                list.appendChild(item);
            });

            graph.on('node:click', (evt) => {
                const nodeId = evt.target.id;
                const nodeData = graph.getNodeData(nodeId);
                const d = nodeData?.data || {};
                const panel = document.getElementById('detailPanel');
                document.getElementById('panelTitle').innerText = d.label || nodeId;
                
                // Meta info
                document.getElementById('sectionMeta').innerHTML = \`
                    <div class="meta-row"><span class="meta-label">中文名</span><span class="meta-value">\${d.chineseName || '—'}</span></div>
                    <div class="meta-row"><span class="meta-label">模块</span><span class="meta-value" style="color:\${(COLORS[d.module] || COLORS.other).fill}">\${(d.module || 'other').toUpperCase()}</span></div>
                    <div class="meta-row"><span class="meta-label">描述</span><span class="meta-value">\${d.description || '—'}</span></div>
                \`;

                // Properties message
                document.getElementById('sectionProperties').innerHTML = \`
                    <h3>属性列表</h3>
                    <div style="color:rgba(255,255,255,0.4);font-size:12px;padding:8px 0;">离线快照暂不含详细属性字段</div>
                \`;

                // Relations traversal
                const outgoing = graphData.edges.filter(e => e.source === nodeId);
                const incoming = graphData.edges.filter(e => e.target === nodeId);
                
                let relHtml = "<h3>关系</h3>";
                if (outgoing.length > 0) {
                    relHtml += '<div class="rel-section-label">它引用的对象 →</div>';
                    outgoing.forEach(r => {
                        relHtml += \`<div class="rel-item rel-item-out" style="display:flex;align-items:center;gap:8px;padding:6px 8px;margin-bottom:4px;background:rgba(0,255,185,0.03);border:1px solid rgba(0,255,185,0.08);border-radius:4px;font-size:12px;">
                            <span class="rel-arrow" style="color:#00FFB9;">→</span>
                            <span class="rel-name" style="color:rgba(255,255,255,0.85);font-weight:500;">\${r.data?.label || ''}</span>
                            <span class="rel-target" style="color:#00FFB9;margin-left:auto;font-family:monospace;">\${r.target}</span>
                            <span class="rel-card" style="color:rgba(255,255,255,0.4);font-size:10px;">\${r.data?.cardinality || ''}</span>
                        </div>\`;
                    });
                }
                if (incoming.length > 0) {
                    relHtml += '<div class="rel-section-label" style="margin-top:12px;">被何处引用 ←</div>';
                    incoming.forEach(r => {
                        relHtml += \`<div class="rel-item rel-item-in" style="display:flex;align-items:center;gap:8px;padding:6px 8px;margin-bottom:4px;background:rgba(255,64,129,0.03);border:1px solid rgba(255,64,129,0.08);border-radius:4px;font-size:12px;">
                            <span class="rel-arrow" style="color:#FF4081;">←</span>
                            <span class="rel-name" style="color:rgba(255,255,255,0.85);font-weight:500;">\${r.data?.label || ''}</span>
                            <span class="rel-target" style="color:#FF4081;margin-left:auto;font-family:monospace;">\${r.source}</span>
                            <span class="rel-card" style="color:rgba(255,255,255,0.4);font-size:10px;">\${r.data?.cardinality || ''}</span>
                        </div>\`;
                    });
                }
                if (outgoing.length === 0 && incoming.length === 0) {
                    relHtml += '<div style="color:rgba(255,255,255,0.4);font-size:12px;padding:8px 0;">暂无关联关系</div>';
                }
                
                document.getElementById('sectionRelations').innerHTML = relHtml;
                panel.classList.remove('panel-hidden');
            });
        });
    </script>
</body>
</html>`;

        const blob = new Blob([htmlContent], { type: 'text/html' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `Opcenter_Ontology_Snapshot_${new Date().getTime()}.html`;
        link.click();
    }

    // ── Switch layout and re-render ──
    function switchLayout(key, skipLabelUpdate) {
        if (!LAYOUTS[key]) return;
        layoutMode = key;
        const data = buildGraphData(rawData, comboEnabled);

        // Adjust node size based on mode
        const nodeSize = relMode ? 36 : (key.startsWith("dagre") ? 44 : 56);
        const labelSize = relMode ? 10 : (key.startsWith("dagre") ? 10 : 11);

        data.nodes = data.nodes.map(n => ({
            ...n,
            style: { ...n.style, size: nodeSize, labelFontSize: labelSize },
        }));

        graph.setLayout({ ...LAYOUTS[key] });
        graph.setData(data);
        graph.render();

        // Update layout label indicator
        if (!skipLabelUpdate) {
            updateLayoutLabel();
        }
    }

    function updateLayoutLabel() {
        const el = document.getElementById("layoutLabel");
        if (el) el.textContent = LAYOUT_LABELS[layoutMode] || layoutMode;
    }

    // ══════════════════════════════════════════════════════
    //  Legend Interaction
    // ══════════════════════════════════════════════════════
    function setupLegend() {
        const legend = document.getElementById("legend");
        const legendHeader = legend.querySelector(".legend-header");
        const legendSearch = document.getElementById("legendSearchInput");
        const legendList = document.getElementById("legendList");
        const legendCount = document.getElementById("legendCount");

        // Clear existing items
        legendList.innerHTML = "";

        // Keep track of active module filter
        let activeModuleKey = null;

        // Helper to save current order to localStorage
        function saveLegendOrder() {
            const currentKeys = [...legendList.querySelectorAll(".legend-item")].map(el => el.dataset.key);
            try {
                localStorage.setItem("camstar_ontology_legend_order", JSON.stringify(currentKeys));
            } catch (e) {
                console.error("Failed to save legend order:", e);
            }
        }

        // Determine sorted keys from localStorage or default
        let sortedKeys = Object.keys(COMBO_LABELS);
        try {
            const stored = localStorage.getItem("camstar_ontology_legend_order");
            if (stored) {
                const parsed = JSON.parse(stored);
                if (Array.isArray(parsed)) {
                    const validParsed = parsed.filter(k => sortedKeys.includes(k));
                    const missing = sortedKeys.filter(k => !validParsed.includes(k));
                    sortedKeys = [...validParsed, ...missing];
                }
            }
        } catch (e) {
            console.error("Failed to load legend order:", e);
        }

        // Generate items dynamically in sorted order
        sortedKeys.forEach((key) => {
            const label = COMBO_LABELS[key];
            const color = (COLORS[key] || COLORS.other).fill;

            const item = document.createElement("div");
            item.className = "legend-item";
            item.setAttribute("draggable", "true");
            item.dataset.module = label;
            item.dataset.key = key;
            item.innerHTML = `<span class="legend-dot" style="background:${color};"></span>${label}`;

            let wasDragged = false;

            // ── Drag & Drop Event Listeners ──
            item.addEventListener("dragstart", () => {
                item.classList.add("dragging");
                wasDragged = true;
            });

            item.addEventListener("dragend", () => {
                item.classList.remove("dragging");
                saveLegendOrder();
                // Small timeout to let any click event bubble and get ignored
                setTimeout(() => { wasDragged = false; }, 50);
            });

            // ── Click to Highlight Module ──
            item.addEventListener("click", (e) => {
                e.stopPropagation();
                if (wasDragged) return;

                // Toggle logic
                if (activeModuleKey === key) {
                    activeModuleKey = null;
                    item.classList.remove("active");
                    clearHighlight();
                } else {
                    // Deactivate previous
                    legendList.querySelectorAll(".legend-item.active").forEach(el => el.classList.remove("active"));

                    activeModuleKey = key;
                    item.classList.add("active");
                    highlightModule(key);
                }
            });

            legendList.appendChild(item);
        });

        // ── Dragover listener on list for vertical reordering ──
        legendList.addEventListener("dragover", (e) => {
            e.preventDefault();
            const draggingItem = legendList.querySelector(".dragging");
            if (!draggingItem) return;

            const siblings = [...legendList.querySelectorAll(".legend-item:not(.dragging)")];

            const nextSibling = siblings.find(sibling => {
                const rect = sibling.getBoundingClientRect();
                const offset = e.clientY - rect.top - rect.height / 2;
                return offset < 0;
            });

            legendList.insertBefore(draggingItem, nextSibling);
        });

        const legendItems = legendList.querySelectorAll(".legend-item");

        // Set initial count
        legendCount.textContent = `(${legendItems.length})`;

        // Toggle legend
        legendHeader.addEventListener("click", () => {
            legend.classList.toggle("legend-collapsed");
        });

        // Search legend
        legendSearch.addEventListener("input", (e) => {
            const query = e.target.value.trim().toLowerCase();
            let visibleCount = 0;

            legendItems.forEach((item) => {
                const moduleName = item.dataset.module.toLowerCase();
                const match = moduleName.includes(query);
                item.classList.toggle("hidden", !match);
                if (match) visibleCount++;
            });

            legendCount.textContent = `(${visibleCount}/${legendItems.length})`;
        });

        // Prevent click bubbling on search input
        legendSearch.addEventListener("click", (e) => e.stopPropagation());
    }

    /**
     * Highlights all nodes belonging to a specific module and its external connections.
     * Disconnected module nodes (no internal edges to other module nodes) are excluded
     * from highlighting to avoid showing orphan fragments.
     */
    function highlightModule(moduleKey) {
        if (!graph || !rawData) return;

        const targetModule = String(moduleKey).trim().toLowerCase();
        selectedNodeId = null;

        const states = {};
        const moduleNodeIds = new Set();
        const connectedNodeIds = new Set();

        // 1. Identify module nodes (case-insensitive)
        const allNodes = graph.getNodeData();
        const allCombos = graph.getComboData() || [];

        allNodes.forEach((node) => {
            const nodeMod = String(node.data?.module || "other").trim().toLowerCase();
            if (nodeMod === targetModule) {
                moduleNodeIds.add(String(node.id).trim());
            }
        });

        if (moduleNodeIds.size === 0) return;

        // 1.5 Build internal adjacency and find connected components within the module.
        // Only module nodes that are internally connected (directly or transitively)
        // should be highlighted. Isolated nodes (e.g. Site in the factory module)
        // are excluded so they don't appear as disconnected glowing fragments.
        const allEdges = graph.getEdgeData();
        const internalAdj = new Map();
        moduleNodeIds.forEach(id => internalAdj.set(id, new Set()));

        allEdges.forEach((edge) => {
            const sourceId = String(edge.source?.id || edge.source).trim();
            const targetId = String(edge.target?.id || edge.target).trim();
            if (!sourceId || !targetId || sourceId === "undefined" || targetId === "undefined") return;
            if (moduleNodeIds.has(sourceId) && moduleNodeIds.has(targetId)) {
                internalAdj.get(sourceId).add(targetId);
                internalAdj.get(targetId).add(sourceId);
            }
        });

        // BFS to find all module nodes reachable via internal edges
        const connectedModuleIds = new Set();
        const visited = new Set();
        for (const [id, neighbors] of internalAdj) {
            if (neighbors.size > 0 && !visited.has(id)) {
                const queue = [id];
                visited.add(id);
                connectedModuleIds.add(id);
                while (queue.length > 0) {
                    const cur = queue.shift();
                    for (const neighbor of internalAdj.get(cur)) {
                        if (!visited.has(neighbor)) {
                            visited.add(neighbor);
                            connectedModuleIds.add(neighbor);
                            queue.push(neighbor);
                        }
                    }
                }
            }
        }

        // If internal graph has no edges at all (single-node module or fully isolated),
        // fall back to all module nodes so single-node modules still get highlighted.
        const highlightNodeIds = connectedModuleIds.size > 0 ? connectedModuleIds : moduleNodeIds;

        // 2. Identify connected nodes, combos and edges (use highlightNodeIds)
        allEdges.forEach((edge) => {
            const sourceId = String(edge.source?.id || edge.source).trim();
            const targetId = String(edge.target?.id || edge.target).trim();

            // Robustness: Ignore malformed or missing IDs
            if (!sourceId || !targetId || sourceId === "undefined" || targetId === "undefined") return;

            const isSourceIn = highlightNodeIds.has(sourceId);
            const isTargetIn = highlightNodeIds.has(targetId);

            if (isSourceIn && isTargetIn) {
                states[edge.id] = ["active"];
            } else if (isSourceIn) {
                states[edge.id] = ["activeOut"];
                connectedNodeIds.add(targetId);
            } else if (isTargetIn) {
                states[edge.id] = ["activeIn"];
                connectedNodeIds.add(sourceId);
            } else {
                states[edge.id] = ["inactive"];
            }
        });

        // 3. Apply states to nodes
        allNodes.forEach((node) => {
            const nid = String(node.id).trim();
            if (highlightNodeIds.has(nid)) {
                states[node.id] = ["highlighted"];
            } else if (connectedNodeIds.has(nid)) {
                states[node.id] = ["active"];
            } else {
                states[node.id] = ["inactive"];
            }
        });

        // 4. Apply states to combos
        allCombos.forEach((combo) => {
            const cid = String(combo.id).trim();
            if (connectedNodeIds.has(cid)) {
                states[combo.id] = ["active"];
            } else {
                states[combo.id] = ["inactive"];
            }
        });

        // 5. Apply states using differential update
        _applyStates(states);

        // 6. Focus on the first connected module node
        graph.focusElement(Array.from(highlightNodeIds)[0], true);
        showModuleDetail(moduleKey);
    }

    /**
     * Shows a summary of the module in the detail panel
     */
    async function showModuleDetail(moduleKey) {
        const panel = document.getElementById("detailPanel");
        const panelTitle = document.getElementById("panelTitle");
        const sectionMeta = document.getElementById("sectionMeta");
        const propTable = document.getElementById("propTable");
        const relList = document.getElementById("relList");
        const sectionProperties = document.getElementById("sectionProperties");

        const label = COMBO_LABELS[moduleKey] || moduleKey;
        const color = (COLORS[moduleKey] || COLORS.other).fill;

        panelTitle.innerHTML = `<span style="color:${color}">■</span> ${label} 概览`;
        sectionProperties.style.display = "none"; // Hide properties for module view
        panel.classList.remove("panel-hidden");

        // Calculate stats
        const modNodes = rawData.nodes.filter(n => (n.data?.module || "other") === moduleKey);
        const nodeIds = new Set(modNodes.map(n => n.id));

        const outgoingRels = [];
        const incomingRels = [];

        rawData.edges.forEach(e => {
            const sourceIn = nodeIds.has(e.source);
            const targetIn = nodeIds.has(e.target);

            if (sourceIn && !targetIn) {
                outgoingRels.push({ source: e.source, target: e.target, label: e.data?.label });
            } else if (!sourceIn && targetIn) {
                incomingRels.push({ source: e.source, target: e.target, label: e.data?.label });
            }
        });

        sectionMeta.innerHTML = `
            <div class="meta-row"><span class="meta-label">模块标识</span><span class="meta-value">${moduleKey}</span></div>
            <div class="meta-row"><span class="meta-label">包含类数</span><span class="meta-value" style="font-weight:700;color:var(--si-green)">${modNodes.length}</span></div>
            <div class="meta-row"><span class="meta-label">对外引用</span><span class="meta-value" style="color:var(--si-green)">${outgoingRels.length} 个关系</span></div>
            <div class="meta-row"><span class="meta-label">外部被引</span><span class="meta-value" style="color:#FF4081">${incomingRels.length} 个关系</span></div>
        `;

        // Build relations list
        let html = "";

        // Group by target class for outgoing
        if (outgoingRels.length > 0) {
            html += `<div class="rel-section-label">模块对外引用 (Outgoing)</div>`;
            // Take unique target classes or top N
            const targets = [...new Set(outgoingRels.map(r => r.target))].slice(0, 20);
            targets.forEach(t => {
                const rels = outgoingRels.filter(r => r.target === t);
                html += `<div class="rel-item rel-item-out" data-target="${t}">
                    <span class="rel-arrow">→</span>
                    <span class="rel-name">${rels[0].label}${rels.length > 1 ? '等' : ''}</span>
                    <span class="rel-target">${t}</span>
                </div>`;
            });
        }

        if (incomingRels.length > 0) {
            html += `<div class="rel-section-label rel-section-label-in" style="margin-top:12px">模块被外部引用 (Incoming)</div>`;
            const sources = [...new Set(incomingRels.map(r => r.source))].slice(0, 20);
            sources.forEach(s => {
                const rels = incomingRels.filter(r => r.source === s);
                html += `<div class="rel-item rel-item-in" data-target="${s}">
                    <span class="rel-arrow">←</span>
                    <span class="rel-name">${rels[0].label}${rels.length > 1 ? '等' : ''}</span>
                    <span class="rel-target">${s}</span>
                </div>`;
            });
        }

        relList.innerHTML = html || `<div style="color:var(--text-muted);font-size:12px;">无跨模块关系</div>`;

        // Click to navigate
        relList.querySelectorAll(".rel-item").forEach(el => {
            el.addEventListener("click", () => {
                const target = el.dataset.target;
                if (target) showClassDetail(target);
            });
        });
    }

    // ══════════════════════════════════════════════════════
    //  Window resize
    // ══════════════════════════════════════════════════════
    function setupResize() {
        let resizeTimer;
        window.addEventListener("resize", () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                if (graph) {
                    const container = document.getElementById("graphContainer");
                    graph.resize(container.clientWidth, container.clientHeight);
                }
            }, 200);
        });
    }

    // ══════════════════════════════════════════════════════
    //  Bootstrap
    // ══════════════════════════════════════════════════════
    async function main() {
        const overlay = document.getElementById("loadingOverlay");
        const container = document.getElementById("graphContainer");

        try {
            // Fetch overview data (Level 0)
            rawData = await fetchJSON("/api/graph/overview");
            window.rawData = rawData; // Expose for chat.js
            const data = buildGraphData(rawData, comboEnabled);

            // Init G6
            initGraph(container, data);

            // Load stats
            await loadStats();

            // Load UI config
            try {
                const cfg = await fetchJSON("/api/config");
                if (cfg.show_layout_switch) {
                    document.getElementById("btnLayout").style.display = "inline-flex";
                    document.getElementById("layoutLabel").style.display = "inline-block";
                }
            } catch (e) {
                console.warn("Failed to load config", e);
            }

            // Setup UI
            setupSearch();
            setupToolbar();
            setupLegend();
            setupResize();
            await loadProductLines();
        } catch (err) {
            console.error("Failed to initialise graph:", err);
            container.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#FF6666;font-size:14px;">
                加载失败: ${err.message}<br/>请确认后端服务已启动 (http://localhost:5050)
            </div>`;
        } finally {
            overlay.classList.add("hidden");
        }
    }

    // Go
    document.addEventListener("DOMContentLoaded", main);
})();
