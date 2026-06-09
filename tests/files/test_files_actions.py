import pytest

from pages.common.login_page import LoginPage
from pages.files.files_page import FilesPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.files
def test_files_actions(page):

    # ============================================
    # LOGIN
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    print("\nLogin successful")

    # ============================================
    # OPEN FILES PAGE
    # ============================================

    files_page = FilesPage(page)

    files_page.open_files_page()

    files_page.validate_files_page_opened()

    # ============================================
    # TC_03_02
    # SINGLE FILE UPLOAD
    # ============================================

    files_page.open_upload_files_popup()

    single_file = (
        "test_data/files/audio/audio 1.aac"
    )

    files_page.upload_single_file(
        single_file
    )

    files_page.click_upload_button()

    files_page.validate_uploaded_file(
        "audio 1.aac"
    )

    print(
        "\nTC_03_02 Single file upload completed"
    )

    # ============================================
    # TC_03_03
    # MULTIPLE FILE UPLOAD
    # ============================================

    files_page.open_upload_files_popup()

    multiple_files = [

        "test_data/files/audio/audio 2.flac",

        "test_data/files/audio/audio 3.mp3",

        "test_data/files/audio/audio 4.wav"
    ]

    files_page.upload_multiple_files(
        multiple_files
    )

    files_page.click_upload_button()

    uploaded_files = [

        "audio 2.flac",

        "audio 3.mp3",

        "audio 4.wav"
    ]

    for file_name in uploaded_files:

        files_page.validate_uploaded_file(
            file_name
        )

    print(
        "\nTC_03_03 Multiple file upload completed"
    )

    # ============================================
    # TC_03_04
    # INVALID FILE UPLOAD
    # ============================================

    files_page.open_upload_files_popup()

    invalid_file = (
        "test_data/files/Invalid/Sample-BAT-File-calculator.bat"
    )

    files_page.upload_invalid_file(
        invalid_file
    )

    files_page.click_upload_button()

    files_page.validate_invalid_file_error()

    print(
        "\nTC_03_04 Invalid file upload validation completed"
    )

    # ============================================
    # CLOSE INVALID FILE POPUP
    # ============================================

    files_page.close_upload_popup()

    # ============================================
    # TC_03_06
    # IMPORT FILES FROM S3
    # ============================================

    files_page.open_upload_files_popup()

    files_page.open_import_from_s3()

    files_page.select_s3_integration()

    files_page.open_s3_file_picker()

    files_page.select_s3_files()

    files_page.click_s3_upload_button()

    print(
        "\nTC_03_06 Import files from S3 completed"
    )

    # ============================================
    # WAIT FOR FILE TABLE REFRESH
    # ============================================

    page.wait_for_timeout(5000)

    # ============================================
    # TC_03_05
    # DELETE MULTIPLE FILES
    # ============================================

    files_to_delete = [

        "Copy - Copy.aac",

        "Copy - Copy.flac",

        "audio 2.flac",

        "audio 3.mp3"
    ]

    for file_name in files_to_delete:

        files_page.select_file_checkbox(
            file_name
        )

    print(
        "\nImported + uploaded files selected for delete"
    )

    files_page.click_delete_button()

    files_page.enter_delete_confirmation()

    files_page.confirm_delete()

    print(
        "\nTC_03_05 Delete multiple files completed"
    )