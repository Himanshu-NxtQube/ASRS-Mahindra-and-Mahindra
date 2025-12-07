from backend.utils.google_ocr import OCRClient
from backend.utils.annotations_parser import AnnotationsParser
from backend.utils.data_manager import get_record
from backend.utils.json_result import build_result
from backend.utils.data_manager import upload_result
from backend.utils.s3_operator import upload_images
from backend.utils.detection import detect_vehicle
import os

ocr_client = OCRClient()
parser = AnnotationsParser()

def process_single_image(image_path):
    annotations = ocr_client.get_annotations(image_path)
    unique_ids = parser.get_unique_ids(annotations)
    records = [get_record(unique_id[0]) for unique_id in unique_ids]
    detection = detect_vehicle(image_path, records)
    image_name = os.path.basename(image_path)
    return build_result(image_name, records, detection)
    

def get_inferences(report_dir, report_id):
    for image_name in os.listdir(report_dir):
        if image_name.lower().endswith(".jpg") or image_name.lower().endswith(".png"):
            image_path = os.path.join(report_dir, image_name)
            result = process_single_image(image_path)
            s3_key, s3_url = upload_images(image_path)
            upload_result(result, report_id, s3_url)

if __name__ == "__main__":
    get_inferences("./uploaded_reports/test", 1)
            
            