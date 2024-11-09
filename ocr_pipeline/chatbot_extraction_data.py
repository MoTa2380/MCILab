import os
import subprocess
from post_process import post_process, save_pages_txt
import time

def extract_text_from_pdf(pdf_path):
    try:
        result = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True, check=True)
        return result.stdout 
    except subprocess.CalledProcessError as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def process_pdfs(input_directory, output_directory):
    pdf_counter = 0
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, _, files in os.walk(input_directory):
        print(f"root:\n{root}")
        for file in files:
            
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                text = extract_text_from_pdf(pdf_path)
                if text is not None:
                    pdf_counter += 1
                    pages = post_process(text, first_time=True, toc_thres=0, repeatable_sentence="")
                    
                    relative_path = os.path.relpath(root, input_directory)
                    output_subdir = os.path.join(output_directory, relative_path)
                    if not os.path.exists(output_subdir):
                        os.makedirs(output_subdir)

                    output_file = os.path.join(output_subdir, f"{os.path.splitext(file)[0]}.txt")
                    
                    save_pages_txt(file_path=output_file, pages=pages)

    return pdf_counter
if __name__ == "__main__":
    start = time.time()
    input_dir = "ocr_pipeline/مستندات چت بات"
    output_dir = "ocr_pipeline/مستندات چت بات"
    pdf_counter = process_pdfs(input_dir, output_dir)
    end = time.time()
    print(f"{(end - start)} s took to process {pdf_counter} pdf files.")


