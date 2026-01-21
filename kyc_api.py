from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid
import base64
from deepface import DeepFace
import pytesseract
from PIL import Image
import io

app = FastAPI()

kyc_records = {}

class KYCRequest(BaseModel):
    full_name: str
    dob: str
    document_type: str
    document_number: Optional[str] = None
    selfie_image: str
    id_image: str

class KYCResponse(BaseModel):
    status: str
    match_score: float
    document_valid: bool

def decode_image(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))

@app.post("/kyc/submit")
def submit(data: KYCRequest):
    ref = str(uuid.uuid4())

    id_img = decode_image(data.id_image)
    selfie = decode_image(data.selfie_image)

    # OCR
    extracted = pytesseract.image_to_string(id_img)

    # Face match
    result = DeepFace.verify(selfie, id_img)
    score = 100 if result["verified"] else 40

    status = "verified" if score > 70 else "manual_review"

    kyc_records[ref] = {
        "status": status,
        "match_score": score,
        "document_valid": len(extracted) > 3
    }

    return {"reference_id": ref, "status": status}
