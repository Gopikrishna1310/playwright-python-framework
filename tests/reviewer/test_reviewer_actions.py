import pytest

from config.credentials import (
    REVIEWER_EMAIL,
    REVIEWER_PASSWORD,
    ANNOTATOR_EMAIL,
    ANNOTATOR_PASSWORD
)

from pages.reviewer.reviewer_page import (
    ReviewerPage
)

from pages.annotator.annotator_page import (
    AnnotatorPage
)


@pytest.mark.reviewer
def test_reviewer_actions(page):

    reviewer = ReviewerPage(page)
    annotator = AnnotatorPage(page)

    # =====================================================
    # TC_01_01
    # REVIEWER LOGIN
    # =====================================================

    reviewer.open_login_page()

    reviewer.login(
        REVIEWER_EMAIL,
        REVIEWER_PASSWORD
    )

    reviewer.select_organization_and_role()

    reviewer.validate_reviewer_login()

    print(
        "\nTC_01_01 Reviewer login completed"
    )

    # =====================================================
    # TC_01_02
    # CLAIM TASK
    # =====================================================

    reviewer.open_task(
        "Test project"
    )

    reviewer.claim_task()

    print(
        "\nTC_01_02 Claim task completed"
    )

    # =====================================================
    # TC_01_04
    # REJECT TASK
    # =====================================================

    reviewer.reject_task(
        "Need correction in annotation"
    )

    print(
        "\nTC_01_04 Reject task completed"
    )

    # =====================================================
    # TC_01_05
    # REVIEWER LOGOUT
    # =====================================================

    reviewer.open_profile_menu()

    reviewer.logout()

    print(
        "\nTC_01_05 Reviewer logout completed"
    )

    # =====================================================
    # TC_01_06
    # ANNOTATOR RESUBMIT
    # =====================================================

    annotator.login(
        ANNOTATOR_EMAIL,
        ANNOTATOR_PASSWORD
    )

    annotator.select_organization_and_role()

    annotator.open_task(
        "Test project"
    )

    # CLAIM REJECTED TASK AGAIN

    annotator.claim_task()

    print(
        "\nRejected task claimed again"
    )

    # CLOSE REJECTION POPUP

    page.get_by_role(
        "button",
        name="Close"
    ).click()

    print(
        "\nRejection popup closed"
    )

    # WAIT FOR TEMPLATE LOAD

    annotator.wait_for_template_load()

    # RESUBMIT TASK

    annotator.submit_annotation()

    print(
        "\nTC_01_06 Annotator resubmitted task"
    )

    # =====================================================
    # LOGOUT ANNOTATOR
    # =====================================================

    annotator.logout()

    print(
        "\nAnnotator logout completed"
    )

    # =====================================================
    # TC_01_07
    # REVIEWER APPROVE TASK
    # =====================================================

    reviewer.login(
        REVIEWER_EMAIL,
        REVIEWER_PASSWORD
    )

    reviewer.select_organization_and_role()

    reviewer.open_task(
        "Test project"
    )

    # CLICK APPROVE BUTTON

    reviewer.approve_task()

    print(
        "\nApprove button clicked"
    )



    print(
        "\nTC_01_07 Reviewer approved task"
    )

    # =====================================================
    # FINAL LOGOUT
    # =====================================================

    reviewer.open_profile_menu()

    reviewer.logout()

    print(
        "\nReviewer final logout completed"
    )

    print(
        "\nReviewer regression completed successfully"
    )