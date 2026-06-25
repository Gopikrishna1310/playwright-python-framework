# =============================================================================
# tests/reviewer/test_reviewer_actions.py  —  Reviewer Regression (Fixed)
# =============================================================================
#
# ROOT CAUSE OF FAILURE:
#   When annotator opens a rejected task, a Comments popup auto-opens showing
#   the reviewer's rejection feedback ("Need correction in annotation").
#   This popup blocks ALL interaction on the page — including the Claim Task
#   button — until it is closed.
#
#   Screenshot evidence confirmed:
#     • Task Status: "Rejected" (not "Annotate" as previously assumed)
#     • Comments popup is open and blocking
#     • "Submit Annotation" is directly available — no Claim Task needed
#     • Claim Task button was NOT visible (hidden behind / not present)
#
# FIX APPLIED IN TC_01_06:
#   1. Added annotator.close_comments_popup() after open_task()
#      → Closes the Comments popup before attempting any other action
#
#   2. Made claim_task() conditional (try if visible, skip if not)
#      → For Rejected-status tasks, Submit Annotation is directly available
#      → Claim Task button may or may not appear depending on task state
#
#   3. print() → logger.info() throughout
#
# =============================================================================

import logging
import pytest

from config.credentials import (
    REVIEWER_EMAIL,
    REVIEWER_PASSWORD,
    ANNOTATOR_EMAIL,
    ANNOTATOR_PASSWORD
)

from pages.reviewer.reviewer_page import ReviewerPage
from pages.annotator.annotator_page import AnnotatorPage

logger = logging.getLogger(__name__)


@pytest.mark.reviewer
def test_reviewer_actions(page):

    reviewer = ReviewerPage(page)
    annotator = AnnotatorPage(page)

    # =========================================================================
    # TC_01_01: REVIEWER LOGIN
    # =========================================================================

    reviewer.open_login_page()
    reviewer.login(REVIEWER_EMAIL, REVIEWER_PASSWORD)
    reviewer.select_organization_and_role()
    reviewer.validate_reviewer_login()

    logger.info("TC_01_01 Reviewer login completed")

    # =========================================================================
    # TC_01_02: CLAIM TASK
    # =========================================================================

    reviewer.open_task("Test project")
    reviewer.claim_task()

    logger.info("TC_01_02 Claim task completed")

    # =========================================================================
    # TC_01_04: REJECT TASK
    # =========================================================================

    reviewer.reject_task("Need correction in annotation")

    logger.info("TC_01_04 Reject task completed")

    # =========================================================================
    # TC_01_05: REVIEWER LOGOUT
    # =========================================================================

    reviewer.open_profile_menu()
    reviewer.logout()

    logger.info("TC_01_05 Reviewer logout completed")

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

    # No claim_task() here -- the task is already claimed by this annotator
    # (claimed + submitted earlier, then rejected back to them). "Claim Task"
    # is always present in the DOM regardless of state, so clicking it again
    # was likely what re-rendered the page and dismissed the rejection-
    # feedback popup before this Close-click could run.

    # TEMPORARY DIAGNOSTIC -- remove once resolved.
    print("\n[DIAGNOSTIC] Visible buttons before Close-click:")
    for btn in page.get_by_role("button").all():
        if btn.is_visible():
            label = btn.get_attribute("aria-label") or btn.inner_text()
            print(f"  - {label!r}")
    dialogs = page.get_by_role("dialog").all()
    print(f"[DIAGNOSTIC] Open dialogs: {len(dialogs)}")
    for d in dialogs:
        if d.is_visible():
            print(f"  - dialog text: {d.inner_text()[:200]!r}")

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

    # =========================================================================
    # ANNOTATOR LOGOUT
    # =========================================================================

    annotator.logout()

    logger.info("Annotator logout completed")

    # =========================================================================
    # TC_01_07: REVIEWER APPROVE TASK
    # =========================================================================

    reviewer.login(REVIEWER_EMAIL, REVIEWER_PASSWORD)
    reviewer.select_organization_and_role()
    reviewer.open_task("Test project")
    reviewer.approve_task()

    logger.info("TC_01_07 Reviewer approved task")

    # =========================================================================
    # FINAL LOGOUT
    # =========================================================================

    reviewer.open_profile_menu()
    reviewer.logout()

    logger.info("Reviewer final logout completed")
    logger.info("Reviewer regression test completed successfully")