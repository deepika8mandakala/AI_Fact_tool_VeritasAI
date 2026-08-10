from fastapi import APIRouter, UploadFile, File

from app.image.service import extract_text_from_image
from app.verification.pipeline import verify_pipeline

router = APIRouter(
    prefix="/image",
    tags=["Image Verification"]
)


@router.post("/verify")
def verify_image(file: UploadFile = File(...)):

    text = extract_text_from_image(file)

    print("=" * 80)
    print("OCR TEXT")
    print(text)
    print("=" * 80)

    result = verify_pipeline(text)

    result["ocr_text"] = text

    return result