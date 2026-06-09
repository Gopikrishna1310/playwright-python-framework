import pytest

from pages.common.login_page import LoginPage

from pages.datasets.datasets_page import DatasetsPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.datasets
def test_dataset_actions(page):

    # ============================================
    # LOGIN
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    print(
        "\nLogin successful"
    )

    # ============================================
    # OPEN DATASETS PAGE
    # ============================================

    datasets_page = DatasetsPage(page)

    datasets_page.open_datasets_page()

    datasets_page.validate_datasets_page_opened()

    print(
        "\nTC_04_01 Open Datasets page completed"
    )

    # ============================================
    # TC_04_02
    # CREATE MULTIPLE DATASETS
    # ============================================

    datasets = [

        ("Test 1", "Text", ""),

        ("Test 2", "Image", ""),

        ("Test 3", "Audio", "Description"),

        ("Test 4", "Video", ""),

        ("Test 5", "PDF", ""),

        ("Test 6", "Scanned (OCR)", ""),

        ("Test 7", "CSV", ""),

        ("Test audio 2", "Audio", "")
    ]

    for (
            dataset_name,
            dataset_type,
            description
    ) in datasets:

        datasets_page.create_dataset(
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            description=description
        )

        print(
            f"\nDataset creation completed:\n{dataset_name}"
        )

    print(
        "\nTC_04_02 Create Dataset completed"
    )

    # ============================================
    # TC_04_03
    # ADD FILES TO TEST 3 DATASET
    # ============================================

    datasets_page.open_dataset(
        "Test 3"
    )

    datasets_page.open_add_files_popup()

    dataset_files = [

        "Copy - Copy.mp3",

        "Copy - Copy.wav",

        "audio 4.wav",

        "audio 1.aac"
    ]

    for file_name in dataset_files:

        datasets_page.select_dataset_file(
            file_name
        )

    datasets_page.click_add_files_button()

    for file_name in dataset_files:

        datasets_page.validate_dataset_file(
            file_name
        )

    print(
        "\nTC_04_03 Add files to Test 3 dataset completed"
    )

    # ============================================
    # RETURN TO DATASETS PAGE
    # ============================================

    datasets_page.open_datasets_page()

    # ============================================
    # TC_04_03
    # ADD FILES TO TEST AUDIO 2 DATASET
    # ============================================

    datasets_page.open_dataset(
        "Test audio 2"
    )

    datasets_page.open_add_files_popup()

    audio_2_files = [

        "audio 4.wav",

        "Copy - Copy.wav"
    ]

    for file_name in audio_2_files:

        datasets_page.select_dataset_file(
            file_name
        )

    datasets_page.click_add_files_button()

    for file_name in audio_2_files:

        datasets_page.validate_dataset_file(
            file_name
        )

    print(
        "\nTC_04_03 Test audio 2 files added completed"
    )

    # ============================================
    # RETURN TO DATASETS PAGE
    # ============================================

    datasets_page.open_datasets_page()

    # ============================================
    # OPEN TEST 3 DATASET AGAIN
    # ============================================

    datasets_page.open_dataset(
        "Test 3"
    )

    # ============================================
    # TC_04_04
    # REMOVE FILES FROM DATASET
    # ============================================

    delete_files = [

        "audio 1.aac",

        "Copy - Copy.mp3"
    ]

    for file_name in delete_files:

        datasets_page.select_dataset_file_checkbox(
            file_name
        )

    datasets_page.click_delete_dataset_file_button()

    datasets_page.enter_dataset_delete_confirmation()

    datasets_page.confirm_dataset_file_delete()

    datasets_page.close_delete_summary_popup()

    print(
        "\nTC_04_04 Remove files from dataset completed"
    )

    # ============================================
    # RETURN TO DATASETS PAGE
    # ============================================

    datasets_page.open_datasets_page()

    # ============================================
    # TC_04_05
    # DELETE DATASETS
    # ============================================

    delete_datasets = [

        "Test 1",

        "Test 2"
    ]

    for dataset_name in delete_datasets:

        datasets_page.select_dataset_checkbox(
            dataset_name
        )

    datasets_page.click_delete_dataset_button()

    datasets_page.enter_dataset_confirmation()

    datasets_page.confirm_dataset_delete()

    print(
        "\nTC_04_05 Delete Dataset completed"
    )