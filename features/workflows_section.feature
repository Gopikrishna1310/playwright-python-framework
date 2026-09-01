## Feature: Workflows Management

# TC_01_Workflow_Start_Annotate_Review_Complete.py

### Scenario: Create workflow Start -> Annotate 1 -> Review -> Complete
```gherkin
Given I am logged in and on the "Templates" page
When I create a template "AUT_WF_Template_01"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_01_Start_Annotate_Review_Complete"
And I add nodes ["Start", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Template_01" to Annotate node 1
And I connect Review 1 to Annotate 1 node
And I click "Save"
Then the workflow "AUT_WF_01_Start_Annotate_Review_Complete" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_02_Workflow_Start_Annotate1_Annotate2_Review_Complete_Same_Template.py

### Scenario: Create workflow Start -> Annotate 1 -> Annotate 2 -> Review -> Complete (Same Template)
```gherkin
Given I am logged in and on the "Templates" page
When I create a template "AUT_WF_Template_02"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_02_Start_Ann1_Ann2_Rev_Complete_Same"
And I add nodes ["Start", "Annotate", "Annotate", "Review", "Complete"]
And I apply the same template "AUT_WF_Template_02" to both Annotate node 1 and Annotate node 2
And I connect Review 1 to Annotate 2 node
And I click "Save"
Then the workflow "AUT_WF_02_Start_Ann1_Ann2_Rev_Complete_Same" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_03_Workflow_Start_Annotate1_Annotate2_Review_Complete_Diff_Template.py

### Scenario: Create workflow Start -> Annotate 1 -> Annotate 2 -> Review -> Complete (Different Templates)
```gherkin
Given I am logged in and on the "Templates" page
When I create template "AUT_WF_Template_03A" and template "AUT_WF_Template_03B"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_03_Start_Ann1_Ann2_Rev_Complete_Diff"
And I add nodes ["Start", "Annotate", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Template_03A" to Annotate 1 and template "AUT_WF_Template_03B" to Annotate 2
And I connect Review 1 to Annotate 2 node
And I click "Save"
Then the workflow "AUT_WF_03_Start_Ann1_Ann2_Rev_Complete_Diff" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_04_Workflow_Start_Annotate_Review1_Review2_Complete.py

### Scenario: Create workflow Start -> Annotate 1 -> Review 1 -> Review 2 -> Complete
```gherkin
Given I am logged in and on the "Templates" page
When I create a template "AUT_WF_Template_04"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_04_Start_Ann_Rev1_Rev2_Complete"
And I add nodes ["Start", "Annotate", "Review", "Review", "Complete"]
And I apply template "AUT_WF_Template_04" to Annotate node 1
And I connect Review 1 to Annotate 1 and Review 2 to Review 1
And I click "Save"
Then the workflow "AUT_WF_04_Start_Ann_Rev1_Rev2_Complete" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_05_Workflow_Start_Annotate1_Annotate2_Complete_Same_Template.py

### Scenario: Create workflow Start -> Annotate 1 -> Annotate 2 -> Complete (Same Template)
```gherkin
Given I am logged in and on the "Templates" page
When I create a template "AUT_WF_Template_05"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_05_Start_Ann1_Ann2_Complete_Same"
And I add nodes ["Start", "Annotate", "Annotate", "Complete"]
And I apply the same template "AUT_WF_Template_05" to both Annotate node 1 and Annotate node 2
And I click "Save"
Then the workflow "AUT_WF_05_Start_Ann1_Ann2_Complete_Same" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_06_Workflow_Start_Annotate1_Annotate2_Complete_Diff_Template.py

### Scenario: Create workflow Start -> Annotate 1 -> Annotate 2 -> Complete (Different Templates)
```gherkin
Given I am logged in and on the "Templates" page
When I create template "AUT_WF_Template_06A" and template "AUT_WF_Template_06B"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_06_Start_Ann1_Ann2_Complete_Diff"
And I add nodes ["Start", "Annotate", "Annotate", "Complete"]
And I apply template "AUT_WF_Template_06A" to Annotate 1 and template "AUT_WF_Template_06B" to Annotate 2
And I click "Save"
Then the workflow "AUT_WF_06_Start_Ann1_Ann2_Complete_Diff" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_07_Workflow_Start_Annotate1_Review1_Annotate2_Review2_Complete_Same_Template.py

### Scenario: Create workflow Start -> Annotate 1 -> Review 1 -> Annotate 2 -> Review 2 -> Complete (Same Template)
```gherkin
Given I am logged in and on the "Templates" page
When I create a template "AUT_WF_Template_07"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_07_Start_Ann1_Rev1_Ann2_Rev2_Complete_Same"
And I add nodes ["Start", "Annotate", "Review", "Annotate", "Review", "Complete"]
And I apply the same template "AUT_WF_Template_07" to Annotate 1 and Annotate 2
And I connect Review 1 to Annotate 1 and Review 2 to Annotate 2
And I click "Save"
Then the workflow "AUT_WF_07_Start_Ann1_Rev1_Ann2_Rev2_Complete_Same" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_08_Workflow_Start_Annotate1_Review1_Annotate2_Review2_Complete_Diff_Template.py

### Scenario: Create workflow Start -> Annotate 1 -> Review 1 -> Annotate 2 -> Review 2 -> Complete (Different Templates)
```gherkin
Given I am logged in and on the "Templates" page
When I create template "AUT_WF_Template_08A" and template "AUT_WF_Template_08B"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_08_Start_Ann1_Rev1_Ann2_Rev2_Complete_Diff"
And I add nodes ["Start", "Annotate", "Review", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Template_08A" to Annotate 1 and template "AUT_WF_Template_08B" to Annotate 2
And I connect Review 1 to Annotate 1 and Review 2 to Annotate 2
And I click "Save"
Then the workflow "AUT_WF_08_Start_Ann1_Rev1_Ann2_Rev2_Complete_Diff" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_09_Workflow_Start_Annotate_Consensus_Review_Complete.py

### Scenario: Create workflow Start -> Annotate 1 (2 Annotators Consensus) -> Review 1 -> Complete
```gherkin
Given I am logged in and on the "Templates" page
When I create a template "AUT_WF_Template_09"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_WF_09_Start_Ann_Consensus_Rev_Complete"
And I add nodes ["Start", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Template_09" to Annotate node 1
And I set required annotators to "2" (Consensus)
And I connect Review 1 to Annotate 1
And I click "Save"
Then the consensus workflow "AUT_WF_09_Start_Ann_Consensus_Rev_Complete" should be saved and created successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_10_Workflow_Save_Disabled_Without_Template.py

### Scenario: Save button disabled when template is not configured on annotate node
```gherkin
Given I am logged in and on the "Workflows" page
When I click "Create workflow" and enter name "AUT_WF_10_Unconfigured_Template_Save_Disabled"
And I add nodes ["Start", "Annotate", "Review", "Complete"]
And I connect the nodes without configuring any template on the Annotate node
Then the "Save" button should be in disabled mode
When I cancel or navigate away from the workflow editor
Then the workflow "AUT_WF_10_Unconfigured_Template_Save_Disabled" should NOT be created in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_11_Duplicate_Invalid_Workflow_Naming.py

### Scenario: Duplicate workflow name error validation
```gherkin
Given I am logged in and on the "Workflows" page
When I have an existing workflow "AUT_Workflow_Duplicate"
And I attempt to click "Create workflow" and enter the duplicate name "AUT_Workflow_Duplicate"
Then I should see an error message "A workflow with this name already exists"
When I click "Cancel" on the workflow creation modal
Then the creation modal should close without creating a duplicate workflow
```

### Scenario: Special character workflow name error validation
```gherkin
Given I am on the "Workflows" page
When I click "Create workflow" and enter a name with special characters "AUT_@$%%$_Workflow"
Then I should see an error message "Only letters, numbers, spaces, _ and - are allowed"
When I click "Cancel" on the workflow creation modal
Then the creation modal should close without creating the invalid workflow
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_12_Search_Workflow_Names.py

### Scenario: Search workflow names and handle non-existing search
```gherkin
Given I am logged in and on the "Workflows" page
When I enter an existing workflow name "AUT_WF_Search_Workflow" into the search bar
Then "AUT_WF_Search_Workflow" should be displayed in the search results
When I enter a non-existing workflow name "Checking_Workflow_Not_There" into the search bar
Then I should see a message "No workflows found"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_13_Edit_Workflow_Functionality.py

### Scenario: Edit an existing workflow and save updates
```gherkin
Given I am logged in and on the "Workflows" page
When I have created a valid workflow "AUT_WF_13_Edit_Workflow"
And I click on the workflow "AUT_WF_13_Edit_Workflow"
Then the "Edit" button should be visible on the workflow details page
When I click the "Edit" button
And I modify the workflow by adding a node
And I click "Save"
Then I should see the workflow "AUT_WF_13_Edit_Workflow" updated successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_14_Delete_Single_And_Bulk_Unlinked_Workflows.py

### Scenario: Single unlinked workflow deletion
```gherkin
Given I am logged in and on the "Workflows" page
When I create a single unlinked workflow "AUT_WF_Single_Delete"
And I select the checkbox for "AUT_WF_Single_Delete" and click "Delete"
Then the workflow "AUT_WF_Single_Delete" should be removed from the workflows list
```

### Scenario: Bulk unlinked workflow deletion
```gherkin
Given I am logged in and on the "Workflows" page
When I create 3 unlinked workflows ["AUT_WF_Bulk_Delete_01", "AUT_WF_Bulk_Delete_02", "AUT_WF_Bulk_Delete_03"]
And I select checkboxes for all 3 workflows and click "Delete"
Then all 3 workflows should be removed from the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_15_Prevent_Delete_Workflow_Linked_To_Project.py

### Scenario: Prevent deletion of a workflow linked to an active project
```gherkin
Given I am logged in
When I create a dataset "AUT_WF_Linked_Dataset_15" and template "AUT_WF_Linked_Template_15"
And I create a workflow "AUT_WF_Linked_Workflow_15"
And I create a project "AUT_WF_Linked_Project_15" linking the dataset and workflow
And I navigate back to the "Workflows" page
And I attempt to delete the workflow "AUT_WF_Linked_Workflow_15"
Then I should see an error message "Cannot delete workflow linked to project"
And the workflow "AUT_WF_Linked_Workflow_15" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_16_Workflows_Pagination.py

### Scenario: Workflows pagination limits (5, 10, 20, 50) and persistence
```gherkin
Given I am logged in and on the "Workflows" page
When I select pagination option "5"
Then the displayed workflows count should be <= 5
When I create a new template and a new workflow "AUT_WF_Pagination_Workflow"
Then the displayed workflows count should remain <= 5
When I navigate to the "Datasets" page and return to the "Workflows" page
Then the pagination limit should persist as "5" and displayed workflows count should remain <= 5
When I select pagination option "10"
Then the displayed workflows count should be <= 10
When I select pagination option "20"
Then the displayed workflows count should be <= 20
When I select pagination option "50"
Then the displayed workflows count should be <= 50
```
