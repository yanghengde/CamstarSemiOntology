import unittest

from src.qa.sql_query_builder import build_query_builder_plan


class SqlQueryBuilderTests(unittest.TestCase):
    def test_empty_plan(self):
        plan = build_query_builder_plan([])
        self.assertEqual(plan["nodes"], [])
        self.assertEqual(plan["sql"], "")

    def test_single_table_plan_uses_primary_key(self):
        plan = build_query_builder_plan(["Container"])
        self.assertEqual(plan["root_table"], "Container")
        self.assertIn("ContainerId", plan["sql"])
        self.assertIn("FROM Container c", plan["sql"])
        self.assertEqual(plan["unconnected"], [])

    def test_join_plan_only_renders_verified_physical_join(self):
        plan = build_query_builder_plan(["Container", "CurrentStatus"])
        self.assertTrue(plan["joins"])
        self.assertIn("JOIN CurrentStatus", plan["sql"])
        self.assertIn("CurrentStatusId", plan["sql"])
        self.assertTrue(all(edge["from_field"] for edge in plan["joins"]))
        self.assertTrue(all(edge["to_field"] for edge in plan["joins"]))

    def test_sqlserver_identifiers_and_aliases(self):
        plan = build_query_builder_plan(
            ["Container", "CurrentStatus"],
            dialect="sqlserver",
        )
        self.assertIn("FROM [Container] AS c", plan["sql"])
        self.assertIn("JOIN [CurrentStatus] AS cs", plan["sql"])

    def test_ambiguous_physical_fk_is_disclosed(self):
        plan = build_query_builder_plan(["Container", "Spec"])
        self.assertTrue(any("物理外键候选" in item for item in plan["warnings"]))

    def test_unknown_table_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "未知物理对象"):
            build_query_builder_plan(["DefinitelyNotATable"])


if __name__ == "__main__":
    unittest.main()
