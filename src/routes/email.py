from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from http import HTTPStatus

from  schemas.email import EmailRequest, EmailResponse
from  services.ai_service import AIService
from  utils.get_file_content import get_file_content_util

router = APIRouter(prefix="/email", tags=["Email"])

def get_ai_service() -> AIService:
  return AIService()

@router.post("/analysis")
async def get_email_analysis(
  request: EmailRequest, ai_service = Depends(get_ai_service)
) -> EmailResponse:
  try:
    analysis = ai_service.get_email_analysis(request.content)
    return analysis
  
  except Exception as e:
    raise HTTPException(
      status_code=HTTPStatus.BAD_REQUEST, 
      detail=f"Error get email analysis {e}"
    )
    
@router.post("/analysis/file")
async def get_email_analysis_from_file(
  file: UploadFile = File(...),
  ai_service = Depends(get_ai_service)
):
  try:
    text = await get_file_content_util(file)
  
    analysis = ai_service.get_email_analysis(text)
    return analysis
    
  except Exception as e:
    raise HTTPException(
      status_code=HTTPStatus.BAD_REQUEST,
      detail=f"Error get email analysis {e}"
    )
  