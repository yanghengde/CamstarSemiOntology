from src.ontology.wiki_manager import (
    build_relationship_sql_section,
    build_wiki_prefix,
    collect_all_relationships,
    resolve_relationship_join,
)


def test_master_recipe_printer_label_join_uses_physical_fk():
    join = resolve_relationship_join(
        "MasterRecipe",
        "PrinterLabelDefinition",
        "MasterRecipe.PrinterLabelDefinitionId",
    )

    assert join["resolved"] is True
    assert join["sourceField"] == "PrinterLabelDefinitionId"
    assert join["targetField"] == "PrinterLabelDefinitionId"
    assert join["sourcePrimaryKey"] == "MasterRecipeId"

    section = build_relationship_sql_section(
        "MasterRecipe",
        "HAS_PRINTER_LABEL_DEFINITION",
        "PrinterLabelDefinition",
        "MasterRecipe.PrinterLabelDefinitionId",
    )
    assert "FROM [MasterRecipe] AS src" in section
    assert "LEFT JOIN [PrinterLabelDefinition] AS tgt" in section
    assert (
        "ON src.[PrinterLabelDefinitionId] = "
        "tgt.[PrinterLabelDefinitionId]"
    ) in section
    assert "WHERE src.[MasterRecipeId] = @SourceId" in section


def test_sql_section_is_at_top_before_relationship_body():
    prefix = build_wiki_prefix(
        "通用",
        "MasterRecipe",
        "HAS_PRINTER_LABEL_DEFINITION",
        "PrinterLabelDefinition",
        "MANY_TO_ONE",
        "MasterRecipe.PrinterLabelDefinitionId",
        "2026-07-28",
    )

    assert prefix.startswith(
        "# MasterRecipe → HAS_PRINTER_LABEL_DEFINITION → "
        "PrinterLabelDefinition"
    )
    assert prefix.index("## SQL 关联示例") < len(prefix)
    assert "## 关系说明" not in prefix


def test_every_current_relationship_resolves_to_one_physical_join():
    unresolved = []
    for relationship in collect_all_relationships():
        join = resolve_relationship_join(
            relationship["fromClass"],
            relationship["toClass"],
            relationship.get("description", ""),
        )
        if not join["resolved"]:
            unresolved.append(
                (
                    relationship["fromClass"],
                    relationship["relationName"],
                    relationship["toClass"],
                )
            )

    assert unresolved == []
