import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from web.routers import i18n


def test_catalog_exposes_all_ontology_display_names(monkeypatch):
    catalog = i18n._ontology_catalog()

    assert len(catalog["node"]) >= 500
    assert len(catalog["property"]) >= 8_000
    assert "relationship" not in catalog
    assert any(item["key"] == "Workflow" and item["descriptionZh"] for item in catalog["node"])
    assert any(item["key"] == "Workflow.revision" for item in catalog["property"])
    assert any(item["key"] == "Workflow.revision" for item in catalog["propertiesByNode"]["Workflow"])
    graph_nodes = [
        {"key": "OtherWorkflow", "original": "OtherWorkflow", "owner": "test", "chineseName": "", "descriptionZh": "", "descriptionEn": "", "propertyCount": 0},
        {"key": "Workflow", "original": "Workflow", "owner": "test", "chineseName": "工作流", "descriptionZh": "", "descriptionEn": "", "propertyCount": 1},
    ]
    monkeypatch.setattr(i18n, "_graph_catalog_snapshot", lambda: (graph_nodes, {}))
    search_result = i18n.get_translation_catalog(search="Workflow", offset=0, limit=5)
    assert search_result["items"][0]["key"] == "Workflow"


def test_translation_override_is_persisted_atomically(tmp_path, monkeypatch):
    translation_file = tmp_path / "display_translations.json"
    monkeypatch.setattr(i18n, "I18N_DIR", str(tmp_path))
    monkeypatch.setattr(i18n, "TRANSLATIONS_FILE", str(translation_file))

    result = i18n.update_translation(i18n.TranslationUpdate(
        kind="property_description",
        key="Workflow.revision",
        zh="修订版本字段说明",
        en="Revision field description",
    ))

    assert result["success"] is True
    assert result["revision"] == 1
    saved = json.loads(translation_file.read_text(encoding="utf-8"))
    assert saved["translations"]["propertyDescriptions"]["Workflow.revision"] == {
        "zh": "修订版本字段说明",
        "en": "Revision field description",
    }

    description_result = i18n.update_translation(i18n.TranslationUpdate(
        kind="node_description",
        key="Workflow",
        zh="用于定义制造流程。",
        en="Defines the manufacturing process.",
    ))
    assert description_result["revision"] == 2
    saved = json.loads(translation_file.read_text(encoding="utf-8"))
    assert saved["translations"]["nodeDescriptions"]["Workflow"]["en"] == "Defines the manufacturing process."


def test_identifier_defaults_are_readable():
    assert i18n._default_zh("changeHistory") == "变更历史"
    assert i18n._default_zh("HAS_ACTION_CATEGORY") == "包含操作类别"
    assert i18n._default_en("HAS_ACTION_CATEGORY") == "Has Action Category"
    assert i18n._default_en("changeHistoryId") == "Change History ID"


def test_node_editor_uses_exact_graph_detail_properties(tmp_path, monkeypatch):
    monkeypatch.setattr(i18n, "I18N_DIR", str(tmp_path))
    monkeypatch.setattr(i18n, "TRANSLATIONS_FILE", str(tmp_path / "display_translations.json"))
    graph_node = {
        "key": "MfgOrder", "original": "MfgOrder", "owner": "mfgorder",
        "chineseName": "制造工单", "descriptionZh": "制造工单描述", "descriptionEn": "", "propertyCount": 2,
    }
    graph_details = {
        "MfgOrder": {
            "properties": [
                {"name": "beginProduct", "dataType": "Navigation", "description": "初始产品"},
                {"name": "consumingOrder", "dataType": "String", "description": "父级消耗工单"},
            ]
        }
    }
    monkeypatch.setattr(i18n, "_graph_catalog_snapshot", lambda: ([graph_node], graph_details))

    editor = i18n.get_node_translation_editor("MfgOrder")

    assert [item["original"] for item in editor["properties"]] == ["beginProduct", "consumingOrder"]
    assert editor["properties"][0]["dataType"] == "Navigation"
    assert editor["properties"][0]["sourceDescription"] == "初始产品"
    assert editor["properties"][0]["descriptionZh"] == "初始产品"
    assert editor["properties"][0]["descriptionEn"] == ""
