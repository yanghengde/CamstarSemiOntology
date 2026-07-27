import os
import re
import json

PROJECT_ROOT = "D:\\Deepseek\\camstar\\CamstarOntology"
catalog_path = os.path.join(PROJECT_ROOT, "scenarios_catalog.md")
scenarios_dir = os.path.join(PROJECT_ROOT, "src", "ontology", "scenarios", "general")

with open(catalog_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to parse each scenario block
pattern = r"### 📌 (SC_00[6-9]|SC_01[0-9]): ([^\n]+)\n\n-\s+\*\*本体模型映射\*\*:\s+`([^`]+)`\n-\s+\*\*业务痛点 \(Pain Point\)\*\*:\s+([^\n]+)\n-\s+\*\*数字化映射方案 \(Digital Solution\)\*\*:\s+([^\n]+)\n-\s+\*\*客户易懂价值 \(Value to Client\)\*\*:\s+([^\n]+)"

matches = re.findall(pattern, content)
print(f"Matched {len(matches)} target scenarios (SC_006 to SC_019) from catalog.")

# Helper to clean text
def clean(text):
    return text.strip().replace("“", "「").replace("”", "」")

for sid, title, twins_str, pain, solution, value in matches:
    sid = clean(sid)
    title = clean(title)
    pain = clean(pain)
    solution = clean(solution)
    value = clean(value)
    
    # Parse twins
    twins = [t.strip() for t in twins_str.split(",") if t.strip()]
    
    # Formulate description
    description = f"{solution} 核心解决痛点：{pain} 数字化价值：{value}"
    
    has_mfg = "MfgOrder" in twins
    has_container = "Container" in twins or "Carrier" in twins
    has_spec = "Spec" in twins
    has_resource = "Resource" in twins or "WorkCenter" in twins
    has_rule = "BusinessRule" in twins or "SPC" in twins
    has_quality = "Quality" in twins or "Alarm" in twins
    has_bom = "BOM" in twins or "Material" in twins

    # Base steps
    steps = []
    
    # Step 1: Initialization
    step1_twins = []
    if has_mfg: step1_twins.append("MfgOrder")
    if has_bom: step1_twins.append("BOM")
    step1_twins.append("Container")
    if "Product" in twins: step1_twins.append("Product")
    step1_twins = list(dict.fromkeys(step1_twins))
    
    step1_rels = []
    if "MfgOrder" in step1_twins:
        step1_rels.append("MfgOrder -[GENERATES_CONTAINER]-> Container")
    if "BOM" in step1_twins:
        step1_rels.append("MfgOrder -[USES_BOM]-> BOM")
    if "Product" in step1_twins:
        step1_rels.append("Container -[IS_PRODUCT]-> Product")
        
    steps.append({
        "step": "Step 1: 业务前置校验与容器初始化",
        "desc": f"系统根据【{title}】的业务要求启动。校对生产工单与所需主数据，将生产批次实例化激活为 Container 本体进行数字化防错校验。",
        "twins": step1_twins,
        "rels": step1_rels,
        "code": f"INSERT INTO Container (ContainerName, MfgOrderId, Status) VALUES ('C-{sid}-BATCH-01', 'MO-2026-{sid}', 'Active');"
    })
    
    # Step 2: Processing
    step2_twins = ["Container"]
    if has_spec: step2_twins.append("Spec")
    else: step2_twins.append("Spec") # fallback
    if has_resource: 
        step2_twins.append("Resource" if "Resource" in twins else "WorkCenter")
    else:
        step2_twins.append("Resource") # fallback
    if "Recipe" in twins: step2_twins.append("Recipe")
    if "DataCollection" in twins: step2_twins.append("DataCollection")
    step2_twins = list(dict.fromkeys(step2_twins))
    
    step2_rels = ["Container -[UNDERGOES_SPEC]-> Spec", "Spec -[REQUIRES_RESOURCE]-> Resource"]
    if "Recipe" in step2_twins:
        step2_rels.append("Spec -[USES_RECIPE]-> Recipe")
    if "DataCollection" in step2_twins:
        step2_rels.append("Spec -[COLLECTS_DATA]-> DataCollection")
        
    steps.append({
        "step": "Step 2: 制造工步 Spec 执行与控制",
        "desc": f"物理批次 Container 进入 【{title}】 关键过站工序 Spec 并锁定对应设备。设备开始执行工艺控制、配方参数下发或进行现场数据采集。",
        "twins": step2_twins,
        "rels": step2_rels,
        "code": f"UPDATE Container SET Status = 'InProcess', LastSpec = 'S-{sid}-OP', LastResource = 'R-{sid}-MC' WHERE ContainerName = 'C-{sid}-BATCH-01';"
    })
    
    # Step 3: Analysis & Quality
    step3_twins = ["Container"]
    if has_rule: step3_twins.append("BusinessRule" if "BusinessRule" in twins else "SPC")
    if has_quality: step3_twins.append("Quality" if "Quality" in twins else "Alarm")
    step3_twins.append("History")
    step3_twins = list(dict.fromkeys(step3_twins))
    
    step3_rels = ["Container -[HAS_HISTORY_LOG]-> History"]
    if "BusinessRule" in step3_twins or "SPC" in step3_twins:
        step3_rels.append("Container -[USES_RULE]-> BusinessRule" if "BusinessRule" in twins else "Container -[USES_SPC]-> SPC")
    if "Quality" in step3_twins or "Alarm" in step3_twins:
        step3_rels.append("Container -[HAS_QUALITY_RECORD]-> Quality" if "Quality" in twins else "Container -[TRIGGERS_ALARM]-> Alarm")
        
    steps.append({
        "step": "Step 3: 异常判异与生命周期完工归档",
        "desc": f"批次加工结束，系统自动校验质量限度规则并沉淀效率指标。若触发【{title}】偏离逻辑自动报警并拦截锁定，最后对过站生命周期数据进行历史归档。",
        "twins": step3_twins,
        "rels": step3_rels,
        "code": f"INSERT INTO WIPHistory (ContainerId, SpecId, ResourceId, CompletionTime) VALUES ('C-{sid}-BATCH-01', 'S-{sid}-OP', 'R-{sid}-MC', GETDATE());"
    })
    
    # Assemble complete scenario data
    scenario_data = {
        "scenario_id": sid,
        "industry": "general",
        "name": f"{sid}. {title}",
        "description": description,
        "steps": steps
    }
    
    # Write JSON file
    file_name = f"scenario_{sid}.json"
    file_path = os.path.join(scenarios_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f_out:
        json.dump(scenario_data, f_out, ensure_ascii=False, indent=4)
    print(f"Successfully generated scenario {sid}: {title}")

print("Target scenarios regeneration complete!")
