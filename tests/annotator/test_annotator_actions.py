import pytest

from config.credentials import (
    ANNOTATOR_EMAIL,
    ANNOTATOR_PASSWORD
)

from pages.annotator.annotator_page import (
    AnnotatorPage
)


@pytest.mark.annotator
def test_annotator_actions(page):

    annotator = AnnotatorPage(page)

    # =====================================================
    # TC_01_01 LOGIN
    # =====================================================

    annotator.open_login_page()

    annotator.login(
        ANNOTATOR_EMAIL,
        ANNOTATOR_PASSWORD
    )

    annotator.select_organization_and_role()

    annotator.validate_annotator_login()

    print(
        "\nTC_01_01 Annotator login completed"
    )

    # =====================================================
    # TC_01_02 CLAIM TASK
    # =====================================================

    annotator.open_task(
        "Test project"
    )

    annotator.claim_task()

    print(
        "\nTC_01_02 Claim task completed"
    )

    # =====================================================
    # TC_01_04 AUDIO ANNOTATION
    # =====================================================

    annotator.create_audio_annotation(
        "This is for the testing purposes"
    )

    print(
        "\nTC_01_04 Audio annotation completed"
    )

    # =====================================================
    # TC_01_05 SUBMIT TASK
    # =====================================================

    annotator.submit_annotation()

    print(
        "\nTC_01_05 Submit annotation completed"
    )

    # =====================================================
    # TC_01_06 RELEASE TASK
    # =====================================================

    annotator.open_task(
        "Test project"
    )

    annotator.claim_task()

    annotator.release_task()

    print(
        "\nTC_01_06 Release task completed"
    )

    # =====================================================
    # TC_01_07 LOGOUT
    # =====================================================

    annotator.logout()

    print(
        "\nTC_01_07 Logout completed"
    )

    print(
        "\nAnnotator regression completed successfully"
    )