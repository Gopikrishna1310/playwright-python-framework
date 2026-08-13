import allure
import pytest
from actions.action_factory import ActionFactory

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("annotator_Username")
    password = action_factory.helpers.fetch_dotenv("annotator_Password")
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
    action_factory.login_actions.select_organization("Annotator")
    return action_factory

@allure.feature("DataSet")
@allure.story("Data Set Flow")
@allure.title("Data Set Flow Validation")
def test_Annotator_Flow_test(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        project_name = action_factory.helpers.fetch_dotenv("sanity_Projects_Name")
        annotator_email = action_factory.helpers.fetch_dotenv("annotator_Username")
        Dataset_files_upload = ["audio 2.flac","audio 3.mp3"]
        input_text = "This is an audio test file"

        # Annotator Functionality 
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.tasks_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.current_task_heading)
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.project_name_list)
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
        
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(project_name))
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
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

        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[0]))
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.claim_button, timeout = 10000)
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.claim_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.save_and_exit_button, timeout = 10000)
        is_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.annotator_page.save_and_exit_button)
        if is_visible:
            status = "Pass"
            message = f"Save and exit button is visible."
            action_factory.helpers.attach_screenshot(name="SaveAndExitButtonVisible")
            action_factory.helpers.attach_allure(name="Save and exit button", text="Save and exit button is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Save and exit button is not visible."
            action_factory.helpers.attach_screenshot(name="SaveAndExitButtonNotVisible")
            action_factory.helpers.attach_allure(name="Save and exit button", text="Save and exit button is not visible")
            assert False, message
        action_factory.ui_utils.smart_wait()
        action_factory.annotator_actions.annontate_files(input_text)
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.submit_annotation)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.claim_button, timeout=10000)
        claim_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.annotator_page.claim_button)
        if claim_visible:
            action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.back_button)
            action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=10000)
        files_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
        if Dataset_files_upload[0] not in files_list:
            status = "Pass"
            message = f"Annotator completed the file"
            action_factory.helpers.attach_screenshot(name="AnnotatorCompleted")
            action_factory.helpers.attach_allure(name="Annotator Email", text=annotator_email)
            assert True, message
        else:
            status = "Fail"
            message = f"Annotator does not completed the file"
            action_factory.helpers.attach_screenshot(name="AnnotatorNotCompleted")
            action_factory.helpers.attach_allure(name="Annotator Email", text=annotator_email)
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