import pytest
import logging

from pages.common.login_page import LoginPage
from pages.files.files_page import FilesPage
from config.credentials import TOOL_EMAIL, TOOL_PASSWORD

logger = logging.getLogger(__name__)


@pytest.mark.files
def test_files_actions(page):

    # =========================================================================
    # LOGIN
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)

    # =========================================================================
    # TC_03_01: Open Files page
    # =========================================================================

    files_page = FilesPage(page)

    # When: Click Files from sidebar
    files_page.open_files_page()

    # Then: Files page should open
    files_page.verify_files_page_opened()
    logger.info("TC_03_01 Files page opened and verified")

    # =========================================================================
    # TC_03_02: Single file upload
    # =========================================================================

    # When: Click Upload Files and select a file
    files_page.open_upload_files_popup()
    files_page.upload_single_file("test_data/files/audio/audio 1.aac")
    files_page.click_upload_button()

    # Then: Success message should be displayed
    files_page.verify_upload_success()

    # And: File should appear in the files list
    files_page.verify_file_visible("audio 1.aac")
    logger.info("TC_03_02 Single file upload verified")

    # =========================================================================
    # TC_03_03: Multiple file upload
    # =========================================================================

    # When: Click Upload Files and select multiple files
    files_page.open_upload_files_popup()
    files_page.upload_multiple_files([
        "test_data/files/audio/audio 2.flac",
        "test_data/files/audio/audio 3.mp3",
        "test_data/files/audio/audio 4.wav"
    ])
    files_page.click_upload_button()

    # Then: Success message should be displayed
    files_page.verify_upload_success()

    # And: All files should appear in the files list
    for file_name in ["audio 2.flac", "audio 3.mp3", "audio 4.wav"]:
        files_page.verify_file_visible(file_name)
    logger.info("TC_03_03 Multiple file upload verified")

    # =========================================================================
    # TC_03_04: Invalid file upload
    # =========================================================================

    # When: Attempt to upload an invalid file type
    files_page.open_upload_files_popup()
    files_page.upload_invalid_file(
        "test_data/files/Invalid/Sample-BAT-File-calculator.bat"
    )
    files_page.click_upload_button(expect_popup_close=False)

    # Then: Error message should be displayed
    files_page.verify_invalid_file_error()

    # And: File should not appear in the files list
    files_page.close_upload_popup()
    files_page.verify_file_not_visible("Sample-BAT-File-calculator.bat")
    logger.info("TC_03_04 Invalid file upload verified")

    # =========================================================================
    # TC_03_06: Import files from S3
    # =========================================================================

    # When: Open Upload Files popup and click Import from S3
    files_page.open_upload_files_popup()
    files_page.open_import_from_s3()

    # Then: S3 integration dropdown should be displayed
    files_page.verify_s3_integration_visible()

    # Then: Integration should be available (enabled)
    # Fails clearly here if no S3 integrations are configured in this environment
    files_page.verify_s3_integration_available()
    logger.info("TC_03_06 S3 integration dropdown verified")

    # When: Select integration and open file picker
    files_page.select_s3_integration()
    files_page.open_s3_file_picker()

    # When: Select files and click Upload
    files_page.select_s3_files()
    files_page.click_s3_upload_button()

    # Then: Selected files should appear in the files list
    imported_files = ["Copy - Copy.aac", "Copy - Copy.flac"]
    files_page.verify_s3_files_visible(imported_files)
    logger.info("TC_03_06 S3 import verified")

    # =========================================================================
    # TC_03_05: Delete multiple files
    # =========================================================================

    files_to_delete = [
        "Copy - Copy.aac",
        "Copy - Copy.flac",
        "audio 2.flac",
        "audio 3.mp3"
    ]

    # When: Select files and click Delete
    for file_name in files_to_delete:
        files_page.select_file_checkbox(file_name)

    files_page.click_delete_button()

    # And: Type DELETE in confirmation popup
    files_page.enter_delete_confirmation()
    files_page.confirm_delete(deleted_files=files_to_delete)

    # Then: Files should be removed from the list
    files_page.verify_files_deleted(files_to_delete)
    logger.info("TC_03_05 Delete multiple files verified")