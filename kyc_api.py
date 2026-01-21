# SaloneVerID KYC API (FastAPI-based, cloud-ready)
# Uses mocks for face recognition and OCR for stable online deployment

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid
import base64
import io
from PIL import Image

app = FastAPI(title="SaloneVerID KYC API")

# In-memory database simulation
kyc_records = {}

class KYCRequest(BaseModel):
    full_name: str
    dob: str
    document_type: str
    document_number: Optional[str] = None
    selfie_image: str  # Base64
    id_image: str      # Base64

class KYCResponse(BaseModel):
    status: str
    match_score: float
    document_valid: bool

# Decode Base64 image to PIL Image
def decode_image(b64: str):
    try:
        return Image.open(io.BytesIO(base64.b64decode(b64)))
    except:
        return None

# Mock face recognition
def mock_face_match(selfie, id_img) -> float:
    # Always return a high match for demo
    return 95.0

# Mock OCR extraction
def mock_ocr_extract_id(id_img) -> str:
    # Return dummy ID
    return "EXTRACTED123456"

@app.post("/kyc/submit")
def submit_kyc(data: KYCRequest):
    reference_id = str(uuid.uuid4())

    selfie = decode_image(data.selfie_image)
    id_img = decode_image(data.id_image)

    # Use mocks for cloud-friendly deployment
    match_score = mock_face_match(selfie, id_img)
    extracted_doc_number = mock_ocr_extract_id(id_img)

    # Simple validation
    document_valid = extracted_doc_number.startswith("EXTRACTED")
    status = "verified" if match_score >= 90 and document_valid else "manual_review"

    kyc_records[reference_id] = {
        "status": status,
        "match_score": match_score,
        "document_valid": document_valid
    }

    return {"reference_id": reference_id, "status": status}

@app.get("/kyc/status/{reference_id}", response_model=KYCResponse)
def get_kyc_status(reference_id: str):
    if reference_id not in kyc_records:
        return {
            "status": "not_found",
            "match_score": 0.0,
            "document_valid": False
        }
    return kyc_records[reference_id]

# Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("kyc_api_
