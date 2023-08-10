from datetime import datetime
import os
import tamb.mbplot as mbp
import time

def get_file_change_date(file, path):
    try:
        change_timestamp = os.path.getmtime(f'{path}{file}') #./PDF_output/
        change_date = time.strftime('%Y-%m-%d', time.localtime(change_timestamp))
        return change_date
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {e}"


# # download list of all files in a directory
# path = './PDF_output/'

class PDFMerger():
    def __init__(self, path, file_name_pdf, output_folder) -> None:
        self.path = path
        self.file_name_pdf = file_name_pdf
        self.output_folder = output_folder
        self.create_pdf_list()
        
    def create_pdf_list(self):
        
        # InputPDFs = os.listdir(path)
        self.InputPDFs = [x for x in os.listdir(self.path) 
                    if get_file_change_date(x, self.path) == datetime.today().strftime('%Y-%m-%d')]
        print(self.InputPDFs)
        return self.InputPDFs
    
    def merge_pdf_list(self):
        
        mbp.merge_pdfs(self.InputPDFs, self.file_name_pdf, self.output_folder)
