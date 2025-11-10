"""
Script to discover and run all unit tests in the project.

This script:
  - Ensures the project root is discoverable by Python
  - Automatically finds all `test_*.py` files recursively
  - Executes them using unittest runner
  - Exits with proper exit code (0 = success, 1 = failures/errors)
"""
import sys
import unittest
from pathlib import Path


def add_project_root_to_sys_path():
    """
    Ensure project root is added to sys.path so imports work correctly.
    """
    root_path = Path(__file__).resolve().parent.parent

    if str(root_path) not in sys.path:
        sys.path.insert(0, str(root_path))
        print(f"[INFO] Using project root: {root_path}")


def run_all_tests() -> int:
    """
    Discover and run all unit tests in the project.

    Returns:
        int: 0 if all tests pass, otherwise 1
    """
    add_project_root_to_sys_path()

    loader = unittest.TestLoader()
    tests_directory = Path(__file__).resolve().parent

    print(f"[INFO] Searching tests under: {tests_directory}")

    test_suite = loader.discover(start_dir=str(tests_directory), pattern="test_*.py")

    # Higher verbosity gives more detailed output
    runner = unittest.TextTestRunner(verbosity=2)

    result = runner.run(test_suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    # Exit process using return code based on test execution
    sys.exit(run_all_tests())
