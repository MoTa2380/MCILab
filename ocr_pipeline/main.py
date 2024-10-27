import json
from ocr_utils import process_inputs, extract_text_from_images
from post_process import refine_extracted_text_LLM, system_prompt
import os
from ceph_handlers import download_file, client
from settings import settings
from minio.error import S3Error

def save_to_json(data, output_file):
    """Save extracted data to a JSON file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_filename_without_extension(file_name):
    return os.path.splitext(file_name)[0]

def file_exists(file_path):
    """Check if a file already exists."""
    return os.path.exists(file_path)

def ensure_directory_exists(directory_path):
    """Ensure that a directory exists, create it if it doesn't."""
    os.makedirs(directory_path, exist_ok=True)

def apply_ocr(inputs, output_file, config):
    """
    Main function to process both PDFs and images, and save OCR output to JSON.
    :param inputs: List of input file paths (both PDFs and images).
    :param output_file: Path to the output JSON file.
    """
    images = process_inputs(inputs, dpi=300)  # Convert inputs to images

    # Extract text from the images using OCR
    ocr_data = extract_text_from_images(images, config=config)

    # Save the OCR data to a JSON file
    save_to_json(ocr_data, output_file)
    # print(f"original text:\n{ocr_data[1]}")
    # print(f"refined: {refine_extracted_text_LLM(ocr_data[1], system_prompt=system_prompt)}")

    print(f"Output saved to {output_file}")

def remove_file_extension(file_name):
    return os.path.splitext(file_name)[0]

def process_ceph_directory(bucket_name, prefix, output_directory):
    try:
        objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)
        for obj in objects:
            if obj.object_name.lower().endswith(".pdf"):
                relative_path = os.path.relpath(obj.object_name, prefix)
                relative_path_no_ext = remove_file_extension(relative_path)
                print(relative_path_no_ext)
                output_file_path = os.path.join(output_directory, f"{relative_path_no_ext}.json")
                download_path = os.path.join("ocr_pipeline/input_pdf", relative_path)

                # Skip already processed files
                if file_exists(output_file_path):
                    continue

                # Ensure the directory for download_path exists
                ensure_directory_exists(os.path.dirname(download_path))

                # Download file from Ceph if it doesn't exist locally
                if not file_exists(download_path):
                    download_file(bucket_name, obj.object_name, download_path)

                input_pdf = [download_path]

                # Ensure the output directory exists
                ensure_directory_exists(os.path.dirname(output_file_path))

                apply_ocr(input_pdf, output_file_path, config=settings.get_environment_variable("CONFIG_TESSERACT"))

    except S3Error as err:
        print(f"S3 Error: {err}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    
    bucket_name = "llm-dataset-backup"
    prefix = "datasets/llm-training/non-text/irandoc"
    output_directory = "ocr_pipeline/output_json"

    process_ceph_directory(bucket_name, prefix, output_directory)