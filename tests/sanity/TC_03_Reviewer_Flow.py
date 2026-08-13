import allure
import pytest
from actions.action_factory import ActionFactory

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("reviewer_Username")
    password = action_factory.helpers.fetch_dotenv("reviewer_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv(
        "different_email_for_otp_password"
    )
    # Login
    action_factory.login_actions.perform_login(
        url=url,
        email=email,
        password=password
    )
    action_factory.login_actions.use_different_email_OTP(
        diff_email,
        diff_email_password
    )
    action_factory.login_actions.select_organization(company_Name, "Reviewer")
    return action_factory

@allure.feature("DataSet")
@allure.story("Data Set Flow")
@allure.title("Data Set Flow Validation")
def test_Reviewer_Flow_test(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each

        project_name = action_factory.helpers.fetch_dotenv("sanity_Projects_Name")
        Dataset_files_upload = ["audio 2.flac"]
        input_text = "Update From Reviewer Side"
        
        # Reviewer Functionality 
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.tasks_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.current_task_heading)
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.reviewer_page.project_name_list)
        if project_name in project_list:
            status = "Pass"
            message = f"Project '{project_name}' found in the list."
            action_factory.helpers.attach_screenshot(name="ProjectFound")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' not found in the list."
            action_factory.helpers.attach_screenshot(name="ProjectNotFound")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert False, message
        
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.click_project_name(project_name))
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.reviewer_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files = [file.split("/")[-1] for file in Dataset_files_upload]
        if all(file in files_name_list for file in expected_files):
            status = "Pass"
            message = f"All files uploaded successfully for dataset '{Dataset_files_upload}'."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload all files for dataset '{Dataset_files_upload}'."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.click_project_name(Dataset_files_upload[0]))
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.claim_button, timeout = 10000)
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.claim_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.begin_recording, timeout = 10000)
        is_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.reviewer_page.begin_recording)
        if is_visible:
            status = "Pass"
            message = f"Begin Recording button is visible."
            action_factory.helpers.attach_screenshot(name="Begin Recording button")
            action_factory.helpers.attach_allure(name="Begin Recording button", text="egin Recording button is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Begin Recording button is not visible."
            action_factory.helpers.attach_screenshot(name="Begin RecordingButtonNotVisible")
            action_factory.helpers.attach_allure(name="Begin Recording button", text="Begin Recording button is not visible")
            assert False, message
        
        action_factory.annotator_actions.annontate_files(input_text)
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.approve_button)
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.approve_task_btn)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.tasks_menu,timeout=10000)
        files_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.reviewer_page.files_name_list)
        if Dataset_files_upload[0] not in files_list:
            status = "Pass"
            message = f"Reviewer completed the file"
            action_factory.helpers.attach_screenshot(name="ReviewerCompleted")
            action_factory.helpers.attach_allure(name="Reviewer Task", text="Reviewer Task")
            assert True, message
        else:
            status = "Fail"
            message = f"Reviewer does not completed the file"
            action_factory.helpers.attach_screenshot(name="ReviewerNotCompleted")
            action_factory.helpers.attach_allure(name="Reviewer Task", text="Reviewe Task")
            assert False, message

    except Exception as e:
        status = "Fail"
        message = str(e)
        action_factory.helpers.handle_failure(message=message)
        raise

    finally:
        action_factory.helpers.write_test_results(
            status=status,
            message=message
        ) 