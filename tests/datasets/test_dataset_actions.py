import pytest
import logging

from pages.common.login_page import LoginPage
from pages.datasets.datasets_page import DatasetsPage
from config.credentials import TOOL_EMAIL, TOOL_PASSWORD

logger = logging.getLogger(__name__)


@pytest.mark.datasets
def test_dataset_actions(page):

    # =========================================================================
    # LOGIN
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)

    # =========================================================================
    # TC_04_01: Open Datasets page
    # =========================================================================

    datasets_page = DatasetsPage(page)

    # When: Click Datasets from sidebar
    datasets_page.open_datasets_page()

    # Then: Datasets list page should open
    datasets_page.verify_datasets_page_opened()
    logger.info("TC_04_01 Datasets page opened and verified")

    # =========================================================================
    # TC_04_02: Create multiple datasets
    # =========================================================================

    datasets = [
        ("Test 1", "Text",         ""),
        ("Test 2", "Image",        ""),
        ("Test 3", "Audio",        "Description"),
        ("Test 4", "Video",        ""),
        ("Test 5", "PDF",          ""),
        ("Test 6", "Scanned (OCR)", ""),
        ("Test 7", "CSV",          ""),
        ("Test audio 2", "Audio",  ""),
    ]

    for dataset_name, dataset_type, description in datasets:

        # When: Fill in details and click Create
        datasets_page.create_dataset(
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            description=description
        )

        # Then: Dataset should appear in the list
        datasets_page.verify_dataset_visible(dataset_name)
        logger.info(f"TC_04_02 Dataset created and verified: {dataset_name}")

    logger.info("TC_04_02 All datasets created successfully")

    # =========================================================================
    # TC_04_03: Add files to Test 3 dataset
    # =========================================================================

    datasets_page.open_dataset("Test 3")
    datasets_page.open_add_files_popup()

    test3_files = [
        "Copy - Copy.mp3",
        "Copy - Copy.wav",
        "audio 4.wav",
        "audio 1.aac",
    ]

    for file_name in test3_files:
        datasets_page.select_dataset_file(file_name)

    datasets_page.click_add_files_button()

    # Then: All files should appear in the dataset
    for file_name in test3_files:
        datasets_page.verify_file_in_dataset(file_name)

    logger.info("TC_04_03 Files added and verified in Test 3")

    # =========================================================================
    # TC_04_03: Add files to Test audio 2 dataset
    # =========================================================================

    datasets_page.open_datasets_page()
    datasets_page.open_dataset("Test audio 2")
    datasets_page.open_add_files_popup()

    audio2_files = [
        "audio 4.wav",
        "Copy - Copy.wav",
    ]

    for file_name in audio2_files:
        datasets_page.select_dataset_file(file_name)

    datasets_page.click_add_files_button()

    # Then: All files should appear in the dataset
    for file_name in audio2_files:
        datasets_page.verify_file_in_dataset(file_name)

    logger.info("TC_04_03 Files added and verified in Test audio 2")

    # =========================================================================
    # TC_04_04: Remove files from Test 3 dataset
    # =========================================================================

    datasets_page.open_datasets_page()
    datasets_page.open_dataset("Test 3")

    delete_files = [
        "audio 1.aac",
        "Copy - Copy.mp3",
    ]

    for file_name in delete_files:
        # When: Select files for deletion
        datasets_page.select_dataset_file_checkbox(file_name)

    datasets_page.click_delete_dataset_file_button()
    datasets_page.enter_dataset_delete_confirmation()

    # When: Confirm deletion
    datasets_page.confirm_dataset_file_delete()
    datasets_page.close_delete_summary_popup()

    # Then: Removed files should not be visible in the dataset
    for file_name in delete_files:
        datasets_page.verify_file_not_in_dataset(file_name)

    logger.info("TC_04_04 Files removed and verified as not visible")

    # =========================================================================
    # TC_04_05: Delete datasets
    # =========================================================================

    datasets_page.open_datasets_page()

    delete_datasets = [
        "Test 1",
        "Test 2",
    ]

    for dataset_name in delete_datasets:
        # When: Select datasets for deletion
        datasets_page.select_dataset_checkbox(dataset_name)

    datasets_page.click_delete_dataset_button()
    datasets_page.enter_dataset_confirmation()

    # When: Confirm deletion
    datasets_page.confirm_dataset_delete()

    # Then: Deleted datasets should not be visible in the list
    for dataset_name in delete_datasets:
        datasets_page.verify_dataset_not_visible(dataset_name)

    logger.info("TC_04_05 Datasets deleted and verified as not visible")