## Feature: File Management

### Scenario: Upload a single file
```gherkin
Given I am logged in and on the "Files" page
When I click the "Upload File" button
And I select a file "document.pdf" from my computer
And I click "Upload"
Then I should see "The file was uploaded successfully" message
And "document.pdf" should appear in the files list
```

### Scenario: Upload multiple files
```gherkin
Given I am on the "Files" page
When I click the "Upload Files" button
And I select multiple files "image1.jpg", "image2.jpg", "data.csv"
And I click "Upload"
Then I should see "Files were uploaded successfully" message
And all three files should appear in the files list
```

### Scenario: Upload invalid file type
```gherkin
Given I am on the "Files" page
When I attempt to upload a file "malware.exe"
Then I should see an error message "No file uploaded or invalid file type"
And the file should not be uploaded
```

### Scenario: Prevent uploading a file with an existing filename
```gherkin
Given I am on the "Files" page and I click the "Upload" button
And I click on "Upload Files"
And I select a file from my local device
And a file with the same name already exists in the system
When I click the "Upload" button to upload the file
Then the file should not be uploaded
And I should see an error message stating "A file with this name already exists"
```

### Scenario: View list of files with pagination
```gherkin
Given I am on the "Files" page
And the limit per page is set to 25
And there are more than 25 files in the system
Then I should see 25 files per page
And I should see pagination controls
When I click "Next Page"
Then I should see the next 25 files
```

### Scenario: Search for files by name
```gherkin
Given I am on the "Files" page
And I click on the "Search" box
When I enter "report" in the search field
Then I should see only files with "report" in the filename
```

### Scenario: Delete multiple files
```gherkin
Given I am on the "Files" page
When I select checkboxes for files "1", "2", and "3"
And I click the "Delete" button
And I confirm the deletion in the dialog
Then I should see a success message showing deleted files
And the files should be removed from the list
```

### Scenario: Attempt to delete file attached to dataset
```gherkin
Given I am on the "Files" page
And file "important.pdf" is attached to a dataset
When I select the checkbox for "important.pdf"
And I click the "Delete" button
Then I should see an error "File is attached to a dataset. Please detach it before deleting."
And the file should remain in the list
```
### Scenario: Add single file to a dataset
```gherkin
Given I am on the "Files" page
And I have at least one file in the list
When I select the checkbox for file "document.pdf"
And I click the "Add to Dataset" button
And I select "Training Dataset 2024" from the list
And I click "Add to Dataset"
Then I should see "Successfully added 1 file(s)" message
And the file should be associated with "Training Dataset 2024"
```

### Scenario: Add multiple files to a single dataset
```gherkin
Given I am on the "Files" page
When I select checkboxes for files "report1.pdf", "report2.pdf", and "report3.pdf"
And I click the "Add to Dataset" button
And I select "Training Dataset 2024" from the list
And I click "Add to Dataset"
Then I should see "Successfully added 3 file(s)" message
And all three files should be associated with "Training Dataset 2024"
```

### Scenario: Add files to dataset with some already existing
```gherkin
Given I am on the "Files" page
And file "existing.pdf" is already in "Training Dataset 2024"
When I select checkboxes for files "existing.pdf", "new1.pdf", and "new2.pdf"
And I click "Add to Dataset"
And I attempt to add them to "Training Dataset 2024"
Then I should see "Successfully added 2 file(s). 1 file(s) were already in the dataset." message
And only the new files should be added to the dataset
```

### Scenario: Cancel file to dataset addition
```gherkin
Given I am on the "Files" page
And I have selected files to add to a dataset
When I click "Add to Dataset"
And the dataset selection modal opens
And I click "Cancel"
Then the modal should close
And no files should be added to any dataset
And my file selection should be preserved
```

### Scenario: Remove file from dataset via files page
```gherkin
Given I am viewing file "document.pdf" details
And the file belongs to datasets "Dataset A" and "Dataset B"
When I click the remove icon next to "Dataset A"
And I confirm the removal
Then I should see "File removed from dataset" message
And "Dataset A" should no longer appear in the file's datasets list
And the file should still belong to "Dataset B"
```
---