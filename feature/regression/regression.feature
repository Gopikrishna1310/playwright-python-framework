Company Admin :\
Login feature :

TC\_01\_01 : Scenario: Login to the tool as admin

Given I am on the login page

And I enter a valid username in the "Username" field

And I enter a valid password in the "Password" field

When I click the "Sign In" button

Then the organization selection screen should be displayed

When I click on the "Organization" dropdown field

And I select an organization from the list

Then the role selection field should be displayed

When I select the role "Company Admin "

And I click the "Continue" button

Then the admin home page should be displayed



Integration feature\
TC\_02\_01 \:Scenario: Open Integrations list page

Given I am logged in

When I click on the "Integrations" option from the left-hand side menu

Then the Integrations list page should open

TC\_02\_01 : Scenario: Create a new S3 integration



Given I am on the "Integrations" page

When I click the "New Integration" button

Then the "Add S3 Integration" popup should be displayed


When I select an option from Dropdown 1

And enter the Integration Title and S3 Bucket Name

Then Dropdown 2 should be enabled automatically

When I click Dropdown 2

Then the generated JSON configuration should be displayed

When I click the "Copy" button below Dropdown 2

Then the JSON configuration should be copied successfully

Given I am logged into my AWS account

And I open the IAM Policies page

When I search for the S3 bucket policy associated with the provided bucket name

And open the policy

And click the "Edit" button

And replace the existing JSON with the copied JSON from the tool

And click the "Save" button

Then I should be navigated to the save confirmation page

When I click the "Save Changes" button

Then the IAM policy should be updated successfully

When I open Dropdown 3 in the tool

Then I should see the Account ID and External ID fields

Given I am on the IAM Roles page in AWS

When I click the "Create Role" button

Then the Create Role page should be displayed

When I select the "AWS Account" option

And choose "Another AWS Account"

And enter the copied Account ID from Dropdown 3 into the AWS Account ID field

And enable the "Require External ID" option

And enter the copied External ID from Dropdown 3 into the External ID field

And click the "Next" button

Then the Add Permissions page should be displayed

When I select the required S3 policy using the checkbox

And proceed to the role creation page

And enter the role name "FMN-S3-test" in AWS

And enter the same role name in the third field of Dropdown 3 in the tool

And click the "Create Role" button

Then the IAM Role should be created successfully

When I open the created IAM Role

And copy the ARN ID using the copy icon

And paste the ARN ID into the fourth field of Dropdown 3 in the tool

Then Dropdown 4 should display the CORS JSON configuration

When I click the "Copy" button in Dropdown 4

Then the CORS JSON configuration should be copied successfully

Given I open the selected S3 bucket in AWS

When I navigate to the "Permissions" tab

And open the CORS configuration section

And click the "Edit" button

And replace the existing JSON with the copied CORS JSON

And save the changes

Then the CORS configuration should be updated successfully

When I click the "Create" button in the tool

Then the S3 integration should be created successfully



TC\_02\_03 : Scenario: Run a test to verify the S3 integration



Given I am on the "Integrations" page

When I click the "Run a Test" button

Then the "Test Integration" popup should be displayed

Given I open the integrated S3 bucket in AWS

And navigate to the "Objects" section

When I open a file from the bucket

Then the Object Overview page should be displayed

When I copy the S3 URL of the file

And paste the S3 URL into the "Test Integration" popup in the tool

And click the "Check" button

Then the integration test should pass successfully



Files page :

TC\_03\_01 \:Scenario: Open Files list page

Given I am logged in

When I click on the "Files" option from the left-hand side menu

Then the Files list page should open



TC\_03\_02 : Scenario: Upload a single file

Given I am logged in and on the "Files" page

When I click the "Upload File" button\
And I select a file "document.pdf" from my computer

And I click "Upload"

Then I should see "The file was uploaded successfully" message

And "document.pdf" should appear in the files list



TC\_03\_03 :  Scenario: Upload multiple files

Given I am on the "Files" page

When I click the "Upload Files" button

And I select multiple files "image1.jpg", "image2.jpg", "data.csv"

And I click "Upload" T

hen I should see "Files were uploaded successfully" message

And all three files should appear in the files list

TC\_03\_04 : Scenario: Upload invalid file type

Given I am on the "Files" page

When I attempt to upload a file "malware.exe"

Then I should see an error message "No file uploaded or invalid file type"

And the file should not be uploaded



TC\_03\_05 : Scenario: Delete multiple files

Given I am on the "Files" page

When I select checkboxes for files "1", "2", and "3"

And I click the "Delete" button

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click “DELETE” button

Then I should see a success message showing deleted files

And the files should be removed from the list




TC\_03\_06 : Scenario: Import files from S3



Given I am on the "Files" page

When I click the "Upload Files" button

Then the "Upload Files" popup should be displayed

When I click the "Import from S3" option

Then the "Select Integration" dropdown should be displayed

When I click the integration dropdown

Then the available integrations should be displayed

When I select an integration

And click the upload field

Then the file selection popup should be displayed

When I select one or more files using the checkboxes

And click the "Upload" button

Then the selected files from the S3 bucket should be uploaded successfully

And the uploaded files should be displayed in the files list



Datasets Page :

TC\_04\_01 : Scenario: Open Datasets list page

Given I am logged in

When I click on the "Datasets" option from the left-hand side menu

Then the Datasets list page should open



TC\_04\_02 : Scenario: Create a new dataset

Given I am logged in and on the "Datasets" page

When I click the "New Dataset" button

And I fill in "Training Dataset 2024" in the "Name" field

And I fill in "Dataset for training ML models" in the "Description" field

And I select "PDF" from the "Dataset Type" dropdown

And I click the "Save" button

Then I should see "Dataset created successfully" message

And "Training Dataset 2024" should appear in the datasets list

TC\_04\_03 : Scenario: Add files to a dataset

Given I am viewing dataset "Training Dataset 2024"

When I click the "Add Files" button

And I select files with IDs "101", "102", "103" from the available files list

And I click "Add to Dataset"

Then I should see "Files successfully added to dataset" message

And the dataset should show 3 new files

TC\_04\_04 : Scenario: Remove files in the dataset

Given I am viewing dataset "Training Dataset 2024"

When I select checkboxes for files "1", "2", and "3"

And I click the "Delete" button

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click “DELETE” button

Then I should see a success message showing deleted files

And the files should be removed from the list



TC\_04\_05 : Scenario: Delete dataset

Given I am on the "Datasets" page

And that dataset is not being used by any active project

When I select checkbox for dataset "1"

And I click the "Delete" button

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click “DELETE” button

Then I should see a success message showing deleted dataset

And the Dataset should be removed from the list



Templates page :

TC\_05\_01 : Scenario: Open Templates list page

Given I am logged in

When I click on the "Templates" option from the left-hand side menu

Then the Templates list page should open

TC\_05\_02 : Scenario : Upload new template

Given I am on the Templates list page

When I click on "Upload New Template"

And the Upload Template popup appears

And I enter "Invoice NER" in the "Template Name" field

And I optionally enter "Template for invoice entity extraction" in the "Description" field

And I click "Choose file" to select a template file from my local file system

And the file follows the defined template schema

And after filling up all the mandatory sections the "Upload" button is activated

And I click "Upload"

And after upload completes, a success message "Template uploaded successfully" appears



TC\_05\_03 : Scenario: Delete Templates



Given I am on the "Templates" page

And that Template is not being used by any active project

When I select checkbox for Template "1"

And I click the "Delete" button

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click “DELETE” button

Then I should see a success message showing deleted Template

And the Template should be removed from the list



Workflow page

TC\_06\_01 : Scenario: Open Workflow list page

Given I am logged in

When I click on the "Workflow" option from the left-hand side menu

Then the Workflow list page should open



TC\_06\_02 : Scenario: Create a new workflow

Given I am logged in and on the "Workflows" page

When I click the "Create Workflow" button

And I fill in "NER Annotation Workflow" in the "Name" field

And I fill in "Workflow for NER annotation" in the "Description" field

And I click a "START" node onto the canvas

And I click an "ANNOTATION" node onto the canvas

And I configure the "ANNOTATION" node (Explained in detail below)

And I click an "Review" node onto the canvas

And I click "COMPLETE" node onto the canvas

And I connect the node points based on the expectation of flow of project

And I click "Save Workflow"

Then I should see "Workflow created successfully" message

And "NER Annotation Workflow" should appear in the workflows list

TC\_06\_03 : Scenario: Configure annotation node in workflow

Given I am creating a workflow

And I have added an "ANNOTATION" node

When I click on the “+” option of "ANNOTATION" node

And the available template options are displayed

And I click on "Template 1" option

And I set "Annotation Type" to "Template 1"

Then the node configuration should be saved

TC\_06\_04 : Scenario: Delete multiple workflows

Given I am on the "Workflows" page

When I select checkboxes for workflows "1", "2", and "3"

And I click the "Delete" button

And I confirm the deletion

Then I should see a notification of which workflows were deleted successfully

And the workflows should be removed from the list




Users Page :

TC\_07\_01 : Scenario: Open Users list page

Given I am logged in

When I click on the "Users" option from the left-hand side menu

Then the Users list page should open



TC\_07\_02 : Scenario: Create User


Given I am on users page

When I click on the "Create User" button

And a Create User popup should open

And the form is displayed

And I fill the  following mandatory fields "Full Name", "Email", "Password", "Confirm Password"\

And I open the other mandatory field “Roles” dropdown\

And I should be able to select single/multiple roles at once

And I click “Create User”

Then the Create User popup should close

And a toast message "New user added successfully" should be displayed

And the new user should be added at the top of the users list




TC\_07\_03 : Scenario: Activate or deactivate a single user



Given the users list displays users with Active and Inactive statuses

And the "Change Status" button is disabled by default

When I select a single user using the checkbox

And the "Change Status" button become enabled

Then I click on the "Change Status" button

And the dropdown should display an option based on the selected user's current status

And "Deactivate" should be shown if the selected user is Active

And "Activate" should be shown if the selected user is Inactive

And selecting "Activate" should make the user Active, or selecting "Deactivate" should make the user Inactive

And the status column should reflect the updated state




TC\_07\_04 : Scenario: Activate or deactivate multiple users in bulk



Given the users list displays multiple users with mixed Active and Inactive statuses

And the "Change Status" button is disabled by default

When I select multiple users using the checkboxes

And the "Change Status" button becomes enabled

Then I choose an action from the "Change Status" dropdown

And the dropdown should display both "Activate" and "Deactivate" options

And selecting "Activate" should make all selected users Active, or selecting "Deactivate" should make all selected users Inactive

And the status column should reflect the updated statuses of all the selected users



Project Page :

TC\_08\_01 : Scenario: Open Projects list page



Given I am logged in

When I click on the "Projects" option from the left-hand side menu

Then the Projects list page should open





TC\_08\_02 : Scenario: Create a new project

Given I am logged in and on the "Projects" page

And datasets "1" and "2" already exist

When I click the "Create Project" button

And I fill in "Vehicle Classification" in the "Name" field

And I fill in "Project for vehicle classification" in the "Description" field

And I select datasets "1" and "2"

And I select taxonomies "1" and "2" (optional)

And I select workflow "NER Annotation Workflow"

And I click "Create Project"

Then I should see "Project created successfully" message

And "Vehicle Classification" should appear in the projects list





TC\_08\_03 : Scenario: Project deletion with cascade

Given a project named "Test Project" exists

And I have the required permissions to delete projects

When I initiate deletion for project "Test Project"

And I confirm the deletion action in the confirmation dialog

Then the system should delete the project and all its associated data (tasks, annotations, and NER tags)

And I should see the message "Project deleted successfully"

And "Test Project" should no longer appear in the projects list





TC\_08\_04 : Scenario: Tasks page view



Given I am on the Project page

When I click on Test Project

And I see “Tasks” by default

And I should see an "Export" button for exporting tasks as a JSON file

And I should see a “Search box” beside “Export button” & “Reset button” for searching tasks

And below these controls I should see a detailed tasks list with columns: File Name, Annotator, Reviewer, Updated, Task Status





TC\_08\_05 : Scenario : Export project data

Given I am on tasks tab of the project

When I click the “Export” button

Then the project data should be exported



TC\_08\_06 : Scenario: Reset tasks in the project

Given I am on the "Tasks" tab of the project

And I select one or more tasks using the checkboxes

When I click the "Reset" button

Then the reset confirmation popup should be displayed

When I enter "RESET" in the text field

And I click the "Reset" button

Then the selected tasks should be moved to the reset state

And the status of the selected tasks should be updated accordingly



TC\_08\_07 : Scenario: Add new datasets from the Datasets tab of the project



Given I am on the "Test Project" page

When I click the "Datasets" tab

Then the Datasets page of the project should be displayed

When I click the "Add" button

Then the "Add/Sync Datasets" popup should be displayed

And the "New Datasets" tab should be selected by default

When I select one or more datasets using the checkbox

And I click the "Add/Sync" button

Then the selected datasets should be added to the project




TC\_08\_08 : Scenario: Add annotator users to the project



Given I am on the "Test Project" page

When I click the "Teams" tab

Then the Teams page should be displayed

When I click the "Add Users" button

Then the "Add Users to Project" popup should be displayed

And the user role dropdown should be available

And the "Annotator" role should be selected by default

And only annotator users should be displayed for selection

When I select one or more annotator users

And I click the "Add" button

Then the selected annotator users should be added to the project

And the added annotator users should be displayed in the Teams tab




TC\_08\_09 : Scenario: Add reviewer users to the project



Given I am on the "Test Project" page

When I click the "Teams" tab

Then the Teams page should be displayed

When I click the "Add Users" button

Then the "Add Users to Project" popup should be displayed

And the user role dropdown should be available

And the "Annotator" role should be selected by default

When I change the user role from "Annotator" to "Reviewer"

Then only reviewer users should be displayed for selection

When I select one or more reviewer users

And I click the "Add" button

Then the selected reviewer users should be added to the project

And the added reviewer users should be displayed in the Teams tab



Restriction to delete  the feature that attached to the Project

TC\_09\_01 : Scenario: Attempt to delete workflow attached to project

Given I am on the "Workflows" page

When I select the checkbox for "Workflow 1"

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click the "Delete" button

Then I should see an error "Workflow 1 is attached to a dataset. Please detach it before deleting."\
And the Workflow should remain in the list



TC\_09\_02 :  Scenario: Prevent deleting a Template that is used in a project, Workflow

Given I am on the "Templates" page

When I select the checkbox for "Template 1"

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click the "Delete" button

Then I should see an error "Template 1 is attached to a dataset. Please detach it before deleting."\
And the Template should remain in the list



TC\_09\_03 :  Scenario: Prevent deleting a dataset that is used in a project

Given I am on the "Datasets" page

When I select the checkbox for "Audio dataset"

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click the "Delete" button Then I should see an error "Dataset is attached to a project. Please detach it before deleting."

And the Dataset should remain in the list



TC\_09\_04 :   Scenario : Remove files in the dataset that attached to the project

Given I am viewing the dataset ”Dataset 1”

When I select checkboxes for files “1”, “2”, “3”

And I click the "Delete" button

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click “DELETE” button

Then I should see an error "File is attached to a dataset that attached to the project. Please detach it before deleting."

And the Dataset should remain in the list



TC\_09\_05 :   Scenario: Attempt to delete file attached to dataset from files page

Given I am on the "Files" page And file "important.mp3" is attached to a dataset

When I select the checkbox for "important.mp3"

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click the "Delete" button

Then I should see an error "File is attached to a dataset. Please detach it before deleting."

And the file should remain in the list



TC\_09\_06 :  Scenario: Prevent deleting a integration that is used in files page\
Given I am on the "Integrations" page

When I select the checkbox for "Test"\
And I click the “Delete” button

And I should see Delete confirmation popup

And I type “DELETE” on the text field of that popup

When I click the "Delete" button Then I should see an error "Integration is attached to the dataset. Please detach it before deleting."

And the Integration should remain in the list





TC\_10\_01 : Scenario: Logout from the tool

Given I am on the Admin page

When I click the profile icon located at the bottom-left corner

Then the "Switch Roles" and "Logout" options should be displayed

When I click the "Logout" option

Then I should be logged out successfully

And the Login/Signup page should be displayed





Annotator

TC\_01\_01 : Scenario: Login to the tool as an annotator

Given I am on the login page

And I enter a valid username in the "Username" field

And I enter a valid password in the "Password" field

When I click the "Sign In" button

Then the organization selection screen should be displayed

When I click on the "Organization" dropdown field

And I select an organization from the list

Then the role selection field should be displayed

When I select the role "Annotator "

And I click the "Continue" button

Then the user successfully logs into the tool

And the tool should open with a left sidebar showing only "Home" and "Tasks"

And the annotator should be automatically redirected to the "Tasks" page as the default page





TC\_01\_02 :  Scenario: Pick and claim a task from the assigned project by annotator

Given the annotator is logged into the tool

And the annotator is redirected to the "Tasks" page by default after login

When the annotator clicks anywhere on the row of an assigned project

Then the annotator should be navigated to the selected task page

When the annotator clicks the "Claim Task" button

Then the task should be claimed successfully by the annotator

And the same task should not be available for claiming by another annotator




TC\_01\_03 : Scenario: Change the "Claim Task" button to "Release" after claiming a task

Given the annotator is on the selected task page

When the annotator clicks the "Claim Task" button

Then the task should be claimed successfully by the annotator

And the "Claim Task" button should be changed to "Release"

When the annotator clicks the "Release" button

Then the task should be released successfully

And the task should be available for claiming by another annotator



TC\_01\_04 : Scenario: Create an annotation using the audio template

Given the annotator is on the selected task page

And the task is claimed by the annotator

When the annotator clicks the "Begin Recording" button

Then the audio recording should start

When the annotator clicks the "Begin Recording" button again

Then the recording should stop

And the transcription text popup should be displayed

When the annotator enters the transcription data for the recorded audio

And clicks the "Set Text" button

Then the annotation should be saved successfully



TC\_01\_05 : Scenario: Submit a task after completing annotations

Given the annotator is on the selected task page

And the annotator has completed one or more annotations

When the annotator clicks the "Submit" button

Then the task should be submitted successfully

And the task should no longer be available to the annotator

And the task should be assigned for review to the reviewer



TC\_01\_06 : Scenario : Release a task after claiming

Given the annotator is on the task page\

And the annotator selected and claimed a task\

When the annotator clicks “Release” button\

And the release confirmation popup should be opened\

When the annotator click “Release button” on that popup\

Then the task should be released\

And the task page should be displayed after releasing the task



TC\_01\_07 : Scenario: Logout from the tool

Given the annotator is on the task page

When the annotator clicks the profile icon located at the bottom-left corner

Then the "Switch Roles" and "Logout" options should be displayed

When the annotator clicks the "Logout" option

Then the annotator should be logged out successfully

And the Login/Signup page should be displayed

Reviewer :\
TC\_01\_01 : Scenario: Login to the tool as a reviewer

Given I am on the login page

And I enter a valid username in the "Username" field

And I enter a valid password in the "Password" field

When I click the "Sign In" button

Then the organization selection screen should be displayed

When I click on the "Organization" dropdown field

And I select an organization from the list

Then the role selection field should be displayed

When I select the role "Reviewer "

And I click the "Continue" button

Then the user successfully logs into the tool

And the tool should open with a left sidebar showing only "Home" and "Tasks"

And the Reviewer should be automatically redirected to the "Tasks" page as the default page



TC\_01\_02 :  Scenario: Pick and claim a task from the assigned project by reviewer

Given the reviewer is logged into the tool

And the reviewer is redirected to the "Tasks" page by default after login

When the reviewer clicks anywhere on the row of an assigned project

Then the reviewer should be navigated to the selected task page

When the reviewer clicks the "Claim Task" button

Then the task should be claimed successfully by the reviewer

And the same task should not be available for claiming by another reviewer



TC\_01\_04 : Scenario: Reject a submitted task

Given the reviewer is on the selected task page

When the reviewer clicks the "Reject" button

Then the comment popup should be displayed

When the reviewer enters a comment (optional)

And clicks the "Submit" button in the popup

Then the task should be rejected successfully

And the rejected task should be reassigned to the annotator who submitted the task



TC\_01\_05 : Scenario: Logout from the tool

Given the reviewer is on the task page

When the reviewer clicks the profile icon located at the bottom-left corner

Then the "Switch Roles" and "Logout" options should be displayed

When the reviewer clicks the "Logout" option

Then the reviewer should be logged out successfully

And the Login/Signup page should be displayed



TC\_01\_06 : Scenario: Rejected task is picked again and resubmitted by the annotator

Given the annotator is logged into the tool

And the annotator can view the task that was rejected by the reviewer

When the annotator selects the rejected task

Then the rejection comment popup should be displayed

When the annotator clicks the close icon at the top-right corner of the popup

Then the popup should be closed

When the annotator updates the annotation

And clicks the "Submit" button

Then the submission confirmation popup should be displayed

When the annotator clicks the "OK" button

Then the task should be submitted successfully to the reviewer again



TC\_01\_07 : Scenario: Reviewer approves a resubmitted task

Given the reviewer is logged into the tool

And the reviewer is on the task page of a task resubmitted by the annotator after rejection

And the rejection comment popup should be displayed

When the reviewer clicks the close icon at the top-right corner of the popup

Then the popup should be closed

When the reviewer clicks the "Approve" button

Then the confirmation popup should be displayed

When the reviewer clicks the "OK" button on the confirmation popup

Then the task should be approved successfully.



