class test_data_inputs:

    # Testcase Inputs ::
    Dataset_Name_Valid = "AUT_Dataset_Valid"
    Dataset_Type_CSV = "CSV"
    Dataset_File_Valid = ["csv/CSV Test data.csv","mixed/converted_data.csv"]
    Dataset_Name_Invalid = "AUT_Dataset_Invalid"
    Dataset_Type_PDF = "PDF"
    Dataset_File_Invalid = ["csv/CSV Test data.csv","mixed/converted_data.csv"]
    Invalid_Dataset_Name = "AUT_123_#$%^&_hello"
    Pagination_Datset_Name = "AUT_Pagination_Check"
    Search_Dataset_Name = "AUT_Search_Datset"
    Text_Files = ["text/ascii-art.txt", "text/long-doc.txt", "text/sample-1.doc", "text/sample1.docx"]
    Extra_Text_Files = ["text/config conftest.py.txt"]
    Dataset_Type_Text = "TEXT"
    Dataset_Name_Text = "AUT_Dataset_Text_1"
    Dataset_Delete_Files = "AUT_Delete_Files"
    Prevent_dataset_name = "AUT_Prevent_Dataset"
    Prevent_template_name = "AUT_Prevent_Template"
    Prevent_workflow_name = "AUT_Prevent_WorkFlow"
    Prevent_project_name = "AUT_Prevent_Project"
    Dataset_Type_Audio = "Audio"
    Audio_Files = ["audio/audio 2.flac"]
    Template_files_upload = ["template/Updated Audio template.zip"]
    Prevent_node_list = ["Start", "Annotate", "Review", "Complete"]
    datasets_to_test = [
            {"name": "AUT_Dataset_Text_1", "type": "TEXT", "file": "text/ascii-art.txt"},
            {"name": "AUT_Dataset_Image", "type": "Image", "file": "image/web_optimized_1200x800_97kb.jpg"},
            {"name": "AUT_Dataset_Video", "type": "Video", "file": "video/sample_960x540.mkv"},
            {"name": "AUT_Dataset_PDF", "type": "PDF", "file": "pdf/PDF Test data.pdf"},
            {"name": "AUT_Dataset_OCR", "type": "Scanned (OCR)", "file": "pdf/Resume for Testing.pdf"},
            {"name": "AUT_Dataset_CSV", "type": "CSV", "file": "csv/CSV Test data.csv"}
        ]
    expected_dataset_types = ['Text', 'Image', 'Audio', 'Video', 'PDF', 'Scanned (OCR)', 'CSV']
    search_popup_dataset_name = "AUT_Search_Popup_Dataset"
    popup_text_file = ["text/ascii-art.txt"]
    description = "Add Item to Dataset"
    Dataset_Name_Image = "AUT_Dataset_Image"
    Dataset_Type_Image = "Image"
    Image_Single_File = ["image/web_optimized_1200x800_97kb.jpg"]
    Project_Integrate_Name = "AUT_Project_Integrate"
    Project_Workflow_Name = "AUT_Project_Workflow"
    Project_Template_Name = "AUT_Project_Template"
    switch_role_dataset_name = "AUT_Switch_Role_Dataset"

