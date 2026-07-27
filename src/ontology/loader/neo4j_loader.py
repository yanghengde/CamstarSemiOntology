import os
import sys
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

# Ensure scripts dir is in path for rebuild_indexes import
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))


def load_ontology_to_neo4j(json_filepath: str):
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    if not all([uri, user, password]):
        print("Neo4j configuration is missing in .env")
        return

    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            ontology = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON file: {e}")
        return

    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        # 0. Ensure indexes via canonical registry (rebuild_indexes.py)
        try:
            from rebuild_indexes import ensure_indexes
            ensure_indexes(session, verbose=False)
        except ImportError:
            print("  Warning: rebuild_indexes not found, creating basic constraints inline")
            session.run("CREATE CONSTRAINT unique_ontology_class_name IF NOT EXISTS FOR (c:OntologyClass) REQUIRE c.name IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_ontology_property IF NOT EXISTS FOR (p:OntologyProperty) REQUIRE (p.className, p.name) IS UNIQUE")

        # ── Collect batch data from JSON ──
        class_batch = []
        property_batch = []
        relationship_batch = []

        for cls in ontology.get("classes", []):
            class_name = cls.get("className")
            class_batch.append({
                "name": class_name,
                "chineseName": cls.get("chineseName", ""),
                "description": cls.get("description", ""),
            })
            for prop in cls.get("properties", []):
                property_batch.append({
                    "className": class_name,
                    "propName": prop.get("name"),
                    "dataType": prop.get("type", "String"),
                    "description": prop.get("description", ""),
                })

        for rel in ontology.get("relationships", []):
            relationship_batch.append({
                "fromClass": rel.get("fromClass"),
                "toClass": rel.get("toClass"),
                "relName": rel.get("relationName"),
                "cardinality": rel.get("cardinality", "UNKNOWN"),
                "description": rel.get("description", ""),
                "lineStyle": rel.get("lineStyle", ""),
            })

        # ── 1. Batch MERGE Classes ──
        if class_batch:
            session.run("""
                UNWIND $batch AS cls
                MERGE (c:OntologyClass {name: cls.name})
                SET c.chineseName = cls.chineseName,
                    c.description = cls.description,
                    c.layer = 'Config'
            """, batch=class_batch)
            print(f"  Batch loaded {len(class_batch)} classes")

        # ── 2. Batch MERGE Properties + HAS_PROPERTY edges ──
        if property_batch:
            session.run("""
                UNWIND $batch AS prop
                MATCH (c:OntologyClass {name: prop.className})
                MERGE (p:OntologyProperty {name: prop.propName, className: prop.className})
                SET p.dataType = prop.dataType,
                    p.description = prop.description
                MERGE (c)-[:HAS_PROPERTY]->(p)
            """, batch=property_batch)
            print(f"  Batch loaded {len(property_batch)} properties")

        # ── 3. Batch MERGE Relationships ──
        if relationship_batch:
            session.run("""
                UNWIND $batch AS rel
                MATCH (from:OntologyClass {name: rel.fromClass})
                MATCH (to:OntologyClass {name: rel.toClass})
                MERGE (from)-[r:ONTOLOGY_RELATION {name: rel.relName}]->(to)
                SET r.cardinality = rel.cardinality,
                    r.description = rel.description,
                    r.lineStyle = rel.lineStyle
            """, batch=relationship_batch)
            print(f"  Batch loaded {len(relationship_batch)} relationships")
                 
    driver.close()
    print(f"Successfully loaded {os.path.basename(json_filepath)} into Neo4j!")

if __name__ == "__main__":
    files_to_load = [
        "workflow_ontology.json",
        "operation_ontology.json",
        "spec_ontology.json",
        "workcenter_ontology.json",
        "factory_ontology.json",
        "mfgline_ontology.json",
        "mfgcalendar_ontology.json",
        "product_ontology.json",
        "bom_ontology.json",
        "erpbom_ontology.json",
        "carrier_ontology.json",
        "businessrule_ontology.json",
        "container_ontology.json",
        "datacollection_ontology.json",
        "quality_ontology.json",
        "electronic_procedure_ontology.json",
        "resource_ontology.json",
        "material_ontology.json",
        "employee_ontology.json",
        "role_ontology.json",
        "mfgorder_ontology.json",
        "maintenance_ontology.json",
        "salesorder_ontology.json",
        "sampling_ontology.json",
        "document_ontology.json",
        "label_ontology.json",
        "tool_ontology.json",
        "change_management_ontology.json",
        "recipe_ontology.json",
        "inventory_ontology.json",
        "rework_ontology.json",
        "timer_ontology.json",
        "setup_ontology.json",
        "packaging_ontology.json",
        "part_ontology.json",
        "organization_ontology.json",
        "owner_ontology.json",
        "package_creation_template_ontology.json",
        "package_type_ontology.json",
        "param_ontology.json",
        "pause_reason_ontology.json",
        "pause_reason_group_ontology.json",
        "phase_template_ontology.json",
        "phase_template_disposition_ontology.json",
        "physical_position_ontology.json",
        "physical_location_ontology.json",
        "plan_template_ontology.json",
        "plan_template_disposition_ontology.json",
        "print_queue_ontology.json",
        "printer_label_definition_ontology.json",
        "priority_level_ontology.json",
        "priority_code_ontology.json",
        "process_timer_type_ontology.json",
        "process_timer_ontology.json",
        "process_list_ontology.json",
        "process_object_template_ontology.json",
        "process_model_template_ontology.json",
        "product_family_ontology.json",
        "product_type_ontology.json",
        "production_process_ontology.json",
        "product_conversion_plan_ontology.json",
        "qty_adjust_reason_ontology.json",
        "qty_adjust_reason_group_ontology.json",
        "quality_resolution_code_ontology.json",
        "recipe_list_ontology.json",
        "recurring_date_req_ontology.json",
        "regulatory_report_type_ontology.json",
        "regulatory_agency_ontology.json",
        "replace_reason_ontology.json",
        "remove_difference_reason_ontology.json",
        "removal_reason_ontology.json",
        "release_reason_ontology.json",
        "resource_type_ontology.json",
        "resource_status_code_ontology.json",
        "resource_status_reason_ontology.json",
        "resource_family_ontology.json",
        "resource_group_ontology.json",
        "resource_status_model_ontology.json",
        "resource_layout_ontology.json",
        "resource_bom_ontology.json",
        "resource_material_part_ontology.json",
        "response_set_ontology.json",
        "res_status_reason_group_ontology.json",
        "res_status_code_group_ontology.json",
        "returned_equipment_action_ontology.json",
        "rework_reason_ontology.json",
        "rework_reason_group_ontology.json",
        "role_permissions_ontology.json",
        "rollup_reason_ontology.json",
        "rollup_reason_group_ontology.json",
        "scale_ontology.json",
        "scale_group_ontology.json",
        "scale_status_code_ontology.json",
        "scale_status_reason_ontology.json",
        "scheduling_route_ontology.json",
        "scheduled_business_rule_ontology.json",
        "scrap_reason_ontology.json",
        "sell_reason_ontology.json",
        "sell_reason_group_ontology.json",
        "setup_maint_ontology.json",
        "setup_access_ontology.json",
        "shift_ontology.json",
        "shipment_destination_ontology.json",
        "shipment_destination_group_ontology.json",
        "shipping_reason_ontology.json",
        "shipping_reason_group_ontology.json",
        "substitution_reason_ontology.json",
        "task_list_ontology.json",
        "mfg_order_task_list_ontology.json",
        "mfg_order_task_status_ontology.json",
        "tda_ontology.json",
        "tda_reason_ontology.json",
        "tda_maint_ontology.json",
        "thruput_req_ontology.json",
        "tool_ontology.json",
        "tool_family_ontology.json",
        "tool_group_ontology.json",
        "tool_plan_ontology.json",
        "triage_spec_ontology.json",
        "billofprocess_ontology.json",
        "team_ontology.json",
        "terminal_ontology.json",
        "supplier_ontology.json",
        "esignature_ontology.json",
        "alarm_ontology.json",
        "scrap_ontology.json",
        "uoms_ontology.json",
        "training_plan_ontology.json",
        "history_ontology.json",
        "environment_ontology.json",
        "aql_levels_ontology.json",
        "switching_rules_ontology.json",
        "start_reasons_ontology.json",
        "bonus_reasons_ontology.json",
        "buy_reasons_ontology.json",
        "business_process_ontology.json",
        "checklist_ontology.json",
        "component_defect_ontology.json",
        "computation_ontology.json",
        "computer_ontology.json",
        "customer_ontology.json",
        "data_transport_ontology.json",
        "dictionary_ontology.json",
        "delegation_ontology.json",
        "dispatch_ontology.json",
        "disposition_ontology.json",
        "enterprise_ontology.json",
        "erp_route_ontology.json",
        "failure_ontology.json",
        "issue_ontology.json",
        "local_rework_ontology.json",
        "loss_reason_ontology.json",
        "master_data_catalog_ontology.json",
        "master_recipe_ontology.json",
        "mfg_order_procedure_ontology.json",
        "ncr_ontology.json",
        "notification_target_ontology.json",
        "occupation_ontology.json",
        "numbering_ontology.json",
        "spc_ontology.json",
        "cross_module_ontology.json"
    ]
    
    for filename in files_to_load:
        json_path = os.path.join(os.path.dirname(__file__), "..", "wiki_kb", filename)
        if os.path.exists(json_path):
            print(f"Loading {filename} into Neo4j...")
            load_ontology_to_neo4j(json_path)
        else:
            print(f"File not found: {json_path}")
