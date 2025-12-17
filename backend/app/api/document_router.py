from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from app.api.dtos.document import DocumentUploadResponse
from app.api.dtos.medical_record_dto import MedicalRecordDTO
from app.domain.document_service import DocumentService
from app.core.dependencies import get_document_service

router = APIRouter()

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "docx", "txt"}


@router.post("/document", response_model=DocumentUploadResponse)
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
    if len(file_content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty. Please upload a file with content",
        )
    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 50MB",
        )

    document = await run_in_threadpool(
        document_service.create_document, file.filename, file_type, file_content
    )
    return DocumentUploadResponse.from_domain(document)


@router.put("/document/{document_id}", response_model=DocumentUploadResponse)
async def update_document_medical_record(
    document_id: str,
    medical_record_dto: MedicalRecordDTO,
    document_service: DocumentService = Depends(get_document_service),
):
    domain_medical_record = medical_record_dto.to_domain()

    updated_document = await run_in_threadpool(
        document_service.update_medical_record, document_id, domain_medical_record
    )

    if not updated_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    return DocumentUploadResponse.from_domain(updated_document)


def extension_allowed(file_type: str) -> bool:
    return file_type in ALLOWED_EXTENSIONS
