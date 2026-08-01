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
    ontology_import._sessions.clear()

    result = ontology_import.analyze_import(upload("tables.csv", TABLES), upload("fields.csv", FIELDS))
    candidates = {item["className"]: item for item in result["candidates"]}

    assert candidates["Product"]["status"] == "approved"
    assert candidates["Product"]["selected"] is True
    assert candidates["NewBusinessObject"]["status"] == "review"
    assert candidates["NewBusinessObject"]["selected"] is False
    assert candidates["AuditHistoryDetail"]["status"] == "excluded"
    assert candidates["AuditHistoryDetail"]["selected"] is False
    assert result["summary"] == {
        "tables": 3,
        "fields": 3,
        "approved": 1,
        "review": 1,
        "excluded": 1,
        "defaultSelected": 1,
    }


def test_apply_import_writes_only_explicitly_selected_objects(monkeypatch):
    monkeypatch.setattr(ontology_import, "_reviewed_class_names", lambda: {"Product"})
    ontology_import._sessions.clear()
    analysis = ontology_import.analyze_import(upload("tables.csv", TABLES), upload("fields.csv", FIELDS))
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
