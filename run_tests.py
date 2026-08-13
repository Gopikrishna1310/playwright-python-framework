
# If you want to run testcases you can use the following command in the terminal:
# python run_tests.py
# Generate allure reports after test execution using the following command in the terminal:
# allure serve allure-results

import os
import shutil
import subprocess
import sys
from glob import glob

# Browser Configuration
HEADLESS = False
SLOW_MO = 500
VIEWPORT = {
    "width": 1250,
    "height": 700
}
DEFAULT_TIMEOUT = 3000
NAVIGATION_TIMEOUT = 30000


TEST_FILES = [
            "tests/sanity/TC_01_companyAdmin_Flow.py",
            "tests/sanity/TC_02_Annotator_Flow.py",
            # "tests/sanity/TC_03_Reviewer_Flow.py",
            # "tests/sanity/TC_04_Validate_File_Status.py"
            ]

if __name__ == "__main__":
    # Delete old reports
    for folder in ["allure-results", "allure-report", "reports"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    # Run tests
    subprocess.run(
    [sys.executable, "-m", "pytest", "-v", "--alluredir=allure-results"] + TEST_FILES
    )
    # Generate Allure report
    subprocess.run(
        "allure generate allure-results --clean -o allure-report",
        shell=True
    )