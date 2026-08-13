import allure
import pytest
from actions.action_factory import ActionFactory

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
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
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("DataSet")
@allure.story("Data Set Flow")
@allure.title("Data Set Flow Validation")
def test_Validate_File_status_test(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each

        project_name = action_factory.helpers.fetch_dotenv("sanity_Projects_Name")
        Dataset_files_upload = ["audio 2.flac"]

        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        project_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        print(f"Project names list: {project_name_list}")
        if project_name in project_name_list:
            status = "Pass"
            message = f"Project '{project_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="Project Created")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' creation failed."
            action_factory.helpers.attach_screenshot(name="Project Creation Failed")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()
        for file_Name in Dataset_files_upload:
            action_factory.ui_utils.element_wait_for(action_factory.page_factory.projects_page.get_file_status(file_Name,"Complete"))
            status_of_file_completed = action_factory.ui_utils.is_element_visible(action_factory.page_factory.projects_page.get_file_status(file_Name,"Complete"))
            if status_of_file_completed:
                status = "Pass"
                message = f"File status '{Dataset_files_upload}' completed successfully."
                action_factory.helpers.attach_screenshot(name="File Status Completed")
                action_factory.helpers.attach_allure(name="File Status", text=file_Name)
                assert True, message
            else:
                status = "Fail"
                message = f"File status '{Dataset_files_upload}' completion failed."
                action_factory.helpers.attach_screenshot(name="File Status Completion Failed")
                action_factory.helpers.attach_allure(name="File Status", text=file_Name)
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