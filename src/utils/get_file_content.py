from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
import io
import re
from typing import List, Tuple
import PyPDF2
from fastapi import File, HTTPException
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes


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
    
    if not content.strip():
      content = await get_file_content_from_img_util(file_content)
    
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

def process_image(
    img_tuple: Tuple[int, Image.Image],
    max_dimension: int = 2000,
    tesseract_config: str = r'--oem 1 --psm 6',
    lang: str = 'por'
) -> Tuple[int, str]:
  idx, image = img_tuple
  
  if image.width > max_dimension or image.height > max_dimension:
    ratio = min(max_dimension / image.width, max_dimension / image.height)
    new_size = (
      int(image.width * ratio),
      int(image.height * ratio)
    )
    image = image.resize(new_size, Image.Resampling.LANCZOS)
  
  text = pytesseract.image_to_string(
    image,
    lang=lang,
    config=tesseract_config
  )
  
  return (idx, text.strip())


async def get_file_content_from_img_util(
  file_content: bytes,
  max_workers: int = 4,
  dpi: int = 200,
  max_dimension: int = 2000,
  lang: str = 'por'
) -> str:
  try:
      images: List[Image.Image] = convert_from_bytes(
        file_content,
        dpi=dpi
      )
      
      tesseract_config: str = r'--oem 1 --psm 6'
      
      with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results: List[Tuple[int, str]] = list(
          executor.map(
            lambda img_tuple: process_image(
              img_tuple,
              max_dimension=max_dimension,
              tesseract_config=tesseract_config,
              lang=lang
            ),
            enumerate(images)
          )
        )
      
      results.sort(key=lambda x: x[0])
      
      text_parts: List[str] = [text for _, text in results if text]
      full_text: str = "\n".join(text_parts)
      
      if not full_text.strip():
        raise HTTPException(
          status_code=HTTPStatus.BAD_REQUEST,
          detail="No text could be extracted from the PDF images"
        )
      
      return full_text
      
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(
      status_code=HTTPStatus.BAD_REQUEST,
      detail=f"Error extracting text from PDF images: {str(e)}"
    )