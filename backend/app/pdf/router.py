from fastapi import APIRouter, UploadFile, File

from app.pdf.service import extract_pdf_text
from app.verification.pipeline import verify_pipeline

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Verification"]
)


@router.post("/verify")
def verify_pdf(file: UploadFile = File(...)):

    text = extract_pdf_text(file)

    result = verify_pipeline(text)

    return result