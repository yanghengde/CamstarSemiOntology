import io

from starlette.datastructures import UploadFile

from web.routers import ontology_import


TABLES = """CDODefId,CDOName,Workspace,
1,Product,csi,
2,NewBusinessObject,csi,
3,AuditHistoryDetail,csi,
"""

FIELDS = """CDODefId,CDOName,FieldID,FieldName,IsList,IsPrimaryKey,IsCandidateKey,IsForeignKey,FKCDODefId,FKTableName,FKFieldName,DataType,Precision,Scale,
1,Product,11,ProductName,False,True,False,False,0,,,12,255,0,
2,NewBusinessObject,21,ProductId,False,False,False,True,1,Product,ProductId,1,16,0,
3,AuditHistoryDetail,31,Description,False,False,False,False,0,,,12,255,0,
"""


def upload(name: str, value: str) -> UploadFile:
    return UploadFile(filename=name, file=io.BytesIO(value.encode("utf-8")))


def test_csv_analysis_never_auto_selects_new_cdos(monkeypatch):
    monkeypatch.setattr(ontology_import, "_reviewed_class_names", lambda: {"Product"})
    monkeypatch.setattr("web.designer_metadata.load_cdo_description_catalog", lambda database: {
        "product": {"description": "A product."},
        "newbusinessobject": {"description": "A new business object."},
    })
    monkeypatch.setattr(ontology_import, "_translate_candidate_descriptions", lambda values: (
        {value: f"中文：{value}" for value in values if value}, "",
    ))
    ontology_import._sessions.clear()

    result = ontology_import.analyze_import(upload("tables.csv", TABLES), upload("fields.csv", FIELDS), "sqlserver")
    candidates = {item["className"]: item for item in result["candidates"]}

    assert candidates["Product"]["status"] == "approved"
    assert candidates["Product"]["selected"] is True
    assert candidates["NewBusinessObject"]["status"] == "review"
    assert candidates["NewBusinessObject"]["selected"] is False
    assert candidates["AuditHistoryDetail"]["status"] == "excluded"
    assert candidates["AuditHistoryDetail"]["selected"] is False
    assert candidates["Product"]["descriptionEn"] == "A product."
    assert candidates["Product"]["descriptionZh"] == "中文：A product."
    assert result["database"] == "sqlserver"
    assert result["summary"] == {
        "tables": 3,
        "fields": 3,
        "approved": 1,
        "review": 1,
        "excluded": 1,
        "defaultSelected": 1,
        "described": 2,
        "translated": 2,
    }


def test_apply_import_writes_only_explicitly_selected_objects(monkeypatch):
    monkeypatch.setattr(ontology_import, "_reviewed_class_names", lambda: {"Product"})
    monkeypatch.setattr("web.designer_metadata.load_cdo_description_catalog", lambda database: {})
    ontology_import._sessions.clear()
    analysis = ontology_import.analyze_import(upload("tables.csv", TABLES), upload("fields.csv", FIELDS), "sqlserver")
    calls = []

    class Result:
        def consume(self):
            return self

    class Session:
        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

        def run(self, query, **parameters):
            calls.append(parameters.get("batch", []))
            return Result()

    class Driver:
        def session(self):
            return Session()

    monkeypatch.setattr(ontology_import, "driver", Driver())
    monkeypatch.setattr(ontology_import, "_write_imported_ontology", lambda classes, relationships: None)
    monkeypatch.setattr(ontology_import, "_write_manifest", lambda selected, source_count: None)

    result = ontology_import.apply_import(ontology_import.ImportApplyRequest(
        importId=analysis["importId"], selected=["NewBusinessObject"],
    ))

    assert result == {"success": True, "classes": 1, "newClasses": 1, "properties": 1, "relationships": 1}
    assert [item["name"] for item in calls[0]] == ["NewBusinessObject"]
    assert calls[2][0]["toClass"] == "Product"


def test_description_translation_falls_back_to_english_without_llm(monkeypatch, tmp_path):
    monkeypatch.setattr(ontology_import, "DESCRIPTION_TRANSLATION_CACHE", tmp_path / "cache.json")
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    translations, warning = ontology_import._translate_candidate_descriptions(["English CDO description."])

    assert translations == {}
    assert "英文原文" in warning


def test_a_prefix_uses_designer_base_description():
    catalog = {"joborder": {"description": "Designer description."}}
    assert ontology_import._designer_description_for("A_JobOrder", catalog) == "Designer description."


def test_database_description_failure_does_not_block_csv_review(monkeypatch):
    monkeypatch.setattr(ontology_import, "_reviewed_class_names", lambda: {"Product"})
    monkeypatch.setattr("web.designer_metadata.load_cdo_description_catalog", lambda database: (_ for _ in ()).throw(RuntimeError("offline")))

    result = ontology_import.analyze_import(upload("tables.csv", TABLES), upload("fields.csv", FIELDS), "oracle")

    assert result["database"] == "oracle"
    assert result["summary"]["tables"] == 3
    assert "Oracle" in result["descriptionWarning"]
    assert all(not item["descriptionEn"] for item in result["candidates"])
