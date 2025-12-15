from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.api.dtos.document import DocumentUploadResponse
from app.domain.services.document_service import DocumentService
from app.core.dependencies import get_document_service

router = APIRouter()

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "docx", "txt"}


@router.post("/documents", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
):
    file_type = file.filename.split(".")[-1].lower()
    if not extension_allowed(file_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type"
        )

    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 50MB",
        )
    document = document_service.create_document(file.filename, file_type, file_content)
    return DocumentUploadResponse.from_domain(document)


def extension_allowed(file_type: str) -> bool:
    return file_type in ALLOWED_EXTENSIONS
