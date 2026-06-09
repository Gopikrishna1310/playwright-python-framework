import pytest

from pages.common.login_page import LoginPage
from pages.files.files_page import FilesPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.files
def test_open_files_page(page):

    # ============================================
    # LOGIN TO TOOL
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    print("\nLogin successful")

    # ============================================
    # FILES PAGE
    # ============================================

    files_page = FilesPage(page)

    files_page.open_files_page()

    # ============================================
    # VALIDATE FILES PAGE
    # ============================================

    files_page.validate_files_page_opened()