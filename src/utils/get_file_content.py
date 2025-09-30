from http import HTTPStatus
import io
import re
import PyPDF2
from fastapi import File, HTTPException


async def get_file_content_util(file: File) -> str:
  try:
    filename = (file.filename or "").lower()
    if not filename.endswith((".txt", ".pdf")):
      raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Invalid file type. Please upload .txt or .pdf file"
      )
  
    content = ""
  
    if filename.endswith('.txt'):
      file_content = await file.read()
      content = file_content.decode("utf-8", errors="replace")
      
    elif filename.endswith(".pdf"):
      file_content = await file.read()
      pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
      parts = []
      
      for page in pdf_reader.pages:
        parts.append(page.extract_text() or "")
        
      content = "\n".join(parts)
    
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'\s+([,.;:!?%])', r'\1', content)
    
    if not content.strip():
      raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="File is empty or could not be read."
      )
      
    return content
  except Exception as e:
    raise HTTPException(
      status_code=HTTPStatus.BAD_REQUEST, 
      detail=f"Error read file {e}"
    )
  