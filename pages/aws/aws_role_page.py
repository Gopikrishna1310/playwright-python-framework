import logging

from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)


class AWSRolePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # =========================================================================
    # OPEN ROLES PAGE
    # =========================================================================

    def open_roles_page(self) -> None:
        self.page.goto(
            "https://us-east-1.console.aws.amazon.com/iam/home#/roles",
            wait_until="domcontentloaded",
            timeout=LOAD,
        )
        self.wait.for_url_contains("/roles", timeout=LONG)
        logger.info("[AWSRolePage] Roles page opened")

    # =========================================================================
    # CLICK CREATE ROLE
    # =========================================================================

    def click_create_role(self) -> None:
        create_role_button = self.page.get_by_role("button", name="Create role")
        self.wait.for_visible(create_role_button, timeout=LONG)
        self.safe_click(create_role_button)
        logger.info("[AWSRolePage] Create Role wizard opened")

    # =========================================================================
    # SELECT AWS ACCOUNT
    # =========================================================================

    def select_aws_account(self) -> None:
        self.safe_click(self.page.get_by_text("AWS account", exact=True).first)
        logger.info("[AWSRolePage] AWS Account selected")

    # =========================================================================
    # SELECT ANOTHER AWS ACCOUNT
    # =========================================================================

    def select_another_aws_account(self) -> None:
        self.safe_click(self.page.get_by_text("Another AWS account", exact=True).first)
        logger.info("[AWSRolePage] Another AWS Account selected")

    # =========================================================================
    # ENTER ACCOUNT ID
    # =========================================================================

    def enter_account_id(self, account_id: str) -> None:
        account_input = self.page.get_by_role("textbox", name="Account ID")
        self.wait.for_visible(account_input, timeout=LONG)
        self.safe_type(account_input, account_id)
        expect(account_input).to_have_value(account_id, timeout=DEFAULT)
        logger.info("[AWSRolePage] Account ID entered")

    # =========================================================================
    # ENABLE EXTERNAL ID
    # =========================================================================

    def enable_external_id(self) -> None:
        self.safe_check(self.page.get_by_role("checkbox", name="Require external ID"))
        logger.info("[AWSRolePage] External ID checkbox enabled")

    # =========================================================================
    # ENTER EXTERNAL ID
    # =========================================================================

    def enter_external_id(self, external_id: str) -> None:
        external_id_input = self.page.get_by_role("textbox", name="External ID")
        self.wait.for_visible(external_id_input, timeout=LONG)
        self.safe_type(external_id_input, external_id)
        expect(external_id_input).to_have_value(external_id, timeout=DEFAULT)
        logger.info("[AWSRolePage] External ID entered")

    # =========================================================================
    # GO TO PERMISSIONS PAGE
    # =========================================================================

    def go_to_permissions_page(self) -> None:
        next_button = self.page.get_by_role("button", name="Next").last
        self.wait.for_visible(next_button, timeout=LONG)
        self.safe_click(next_button)
        logger.info("[AWSRolePage] Moved to permissions page")

    # =========================================================================
    # ATTACH POLICY
    # =========================================================================

    def attach_policy(self, policy_name: str) -> None:
        search_input = self.page.get_by_role("searchbox")
        self.wait.for_visible(search_input, timeout=LONG)
        self.safe_fill(search_input, policy_name)

        policy_checkbox = self.page.get_by_role("checkbox", name=policy_name)
        self.wait.for_visible(policy_checkbox, timeout=LONG)
        self.safe_check(policy_checkbox)
        logger.info(f"[AWSRolePage] Policy attached: {policy_name}")

        self.safe_click(self.page.get_by_role("button", name="Next", exact=True))
        logger.info("[AWSRolePage] Moved to review page")

    # =========================================================================
    # ENTER ROLE NAME
    # =========================================================================

    def enter_role_name(self, role_name: str) -> None:
        role_name_input = self.page.get_by_role("textbox", name="Role name")
        self.wait.for_visible(role_name_input, timeout=LONG)
        self.safe_type(role_name_input, role_name)
        expect(role_name_input).to_have_value(role_name, timeout=DEFAULT)
        logger.info(f"[AWSRolePage] Role name entered: {role_name}")

    # =========================================================================
    # CREATE ROLE
    # =========================================================================

    def create_role(self) -> None:
        self.page.bring_to_front()

        create_role_button = (
            self.page.locator("[class*='awsui_actions-section'] button")
            .filter(has_text="Create role")
            .last
        )
        self.wait.for_visible(create_role_button, timeout=LONG)

        create_role_button.dispatch_event("click")
        result = self._wait_create_result(timeout=8_000)

        if result != "success" and "/roles/create" in self.page.url:
            logger.warning("[AWSRolePage] dispatch_event didn't submit — trying element click")
            try:
                create_role_button.click(timeout=SHORT)
            except (PlaywrightTimeoutError, AssertionError):
                pass
            result = self._wait_create_result(timeout=8_000)

        if result != "success" and "/roles/create" in self.page.url:
            logger.warning("[AWSRolePage] Trying dispatch on label span")
            try:
                self.page.get_by_text("Create role", exact=True).last.dispatch_event("click")
            except (PlaywrightTimeoutError, AssertionError):
                pass
            result = self._wait_create_result(timeout=LONG)

        if result == "success":
            logger.info("[AWSRolePage] Role creation completed")
            return

        self._raise_create_failure()

    # =========================================================================
    # PRIVATE
    # =========================================================================

    def _wait_create_result(self, timeout: int) -> str:
        try:
            self.wait.for_url_not_contains("/roles/create", timeout=timeout)
            return "success"
        except PlaywrightTimeoutError:
            errors = self._collect_aws_errors()
            if errors:
                logger.warning(f"[AWSRolePage] AWS errors detected: {errors}")
                return "error"
            return "pending"

    def _collect_aws_errors(self) -> list:
        found = []
        try:
            alerts = self.page.get_by_role("alert")
            for i in range(min(alerts.count(), 5)):
                node = alerts.nth(i)
                if not node.is_visible():
                    continue
                txt = node.inner_text().strip()
                if txt and any(
                    k in txt.lower()
                    for k in ("required", "already exists", "error", "failed")
                ):
                    if txt not in found:
                        found.append(txt)
        except Exception:
            pass
        try:
            dup = self.page.get_by_text("already exists")
            if dup.count() > 0 and dup.first.is_visible():
                t = dup.first.inner_text().strip()
                if t and t not in found:
                    found.append(t)
        except Exception:
            pass
        return found

    def _raise_create_failure(self) -> None:
        try:
            self.page.screenshot(path="screenshots/create_role_failure.png", full_page=True)
            shot = " (screenshot: screenshots/create_role_failure.png)"
        except Exception:
            shot = ""

        errors = self._collect_aws_errors()

        if any("already exists" in e.lower() for e in errors):
            raise RuntimeError(
                f"Role creation failed: role already exists. Delete it in IAM → Roles and re-run.{shot}"
            )
        if errors:
            raise RuntimeError(
                f"Role creation blocked: {' | '.join(errors)}{shot}"
            )
        raise RuntimeError(
            f"Role creation did not leave the create page. Check screenshot for details.{shot}"
        )

    # =========================================================================
    # OPEN CREATED ROLE
    # =========================================================================

    def open_created_role(self, role_name: str) -> None:
        view_role_button = self.page.get_by_role("button", name=f"View role {role_name}")
        try:
            self.wait.for_visible(view_role_button, timeout=15_000)
            self.safe_click(view_role_button)
            logger.info(f"[AWSRolePage] Opened via success banner: {role_name}")
        except (PlaywrightTimeoutError, AssertionError):
            logger.info(f"[AWSRolePage] No success banner — finding role in list: {role_name}")
            search = self.page.get_by_role("searchbox")
            if search.count() > 0 and search.first.is_visible():
                self.safe_fill(search.first, role_name)
            role_link = self.page.get_by_role("link", name=role_name).first
            self.wait.for_visible(role_link, timeout=LONG)
            self.safe_click(role_link)
        logger.info(f"[AWSRolePage] Role detail page opened: {role_name}")

    # =========================================================================
    # COPY ROLE ARN
    # =========================================================================

    def copy_role_arn(self) -> str:
        self.page.bring_to_front()
        copy_arn_button = self.page.get_by_role("button", name="Copy ARN")
        self.wait.for_visible(copy_arn_button, timeout=LONG)
        self.safe_click(copy_arn_button)
        arn = self.read_clipboard(expected_prefix="arn:aws:iam")
        logger.info(f"[AWSRolePage] Role ARN copied: {arn}")
        return arn