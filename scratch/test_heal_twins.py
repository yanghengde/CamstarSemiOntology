import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from web.routers.scenarios import heal_twins

def test_heal_bom_workflow():
    print("\n--- Test: heal_twins(BOM, Workflow) ---")
    result = heal_twins(["BOM", "Workflow"])
    print("Healed twins:", result)
    assert "SetupAccess" not in result, "Error: SetupAccess was included in healed twins!"
    assert "BOM" in result
    assert "Workflow" in result
    assert "MfgOrder" in result or "Product" in result, "Error: Failed to connect BOM and Workflow via MfgOrder/Product!"
    print("SUCCESS: BOM and Workflow healed successfully without SetupAccess!")

def test_heal_spec_employee():
    print("\n--- Test: heal_twins(Spec, Employee) ---")
    result = heal_twins(["Spec", "Employee"])
    print("Healed twins:", result)
    assert "ES_DisplayOptions" not in result, "Error: ES_DisplayOptions was included in healed twins!"
    assert "ChangeStatus" not in result, "Error: ChangeStatus was included in healed twins!"
    assert "Spec" in result
    assert "Employee" in result
    print("SUCCESS: Spec and Employee healed successfully without metadata hubs!")

if __name__ == "__main__":
    try:
        test_heal_bom_workflow()
        test_heal_spec_employee()
        print("\nALL HEAL_TWINS TEST CASES PASSED SUCCESSFULLY!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\nTEST FAILURE: {e}")
        sys.exit(1)
