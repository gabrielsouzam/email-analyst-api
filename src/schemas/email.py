from pydantic import BaseModel, Field
from enum import Enum
  
class EnumCategory(Enum):
  PRODUCTIVE = "productive"
  UNPRODUCTIVE = "unproductive"

class EmailRequest(BaseModel):
    content: str = Field(
      description="Email text content to be analyzed"
    )
    
class EmailResponse(BaseModel):
  category: EnumCategory = Field(
    description= "Email classification: productive or unproductive",
    examples=["productive", "unproductive"]
  )
  response: str = Field(
    description="Suggested response in Portuguese",
    examples=["I also wish you a great end of the year and happy holidays!"]
  )
  
class LLmEmailResponse(BaseModel):
  category: str
  response: str