from http import HTTPStatus
import json
import traceback
from  config.settings import settings
from  schemas.email import LLmEmailResponse
from fastapi import HTTPException
from google.genai import Client, types
from  config.logs import logger
from  utils.prompt_formatter import prompt_formatter_util


class AIService:
  def generate_response(self, text: str) -> LLmEmailResponse:
    try:
      client = Client(api_key=settings.GOOGLE_API_KEY)
      
      config = types.GenerateContentConfig(
        temperature=0.4,
        response_mime_type="application/json",
        response_schema=LLmEmailResponse
      )
      
      contents = [
        types.Content(parts=[types.Part(text=text)], role="user")
      ]
      
      response = client.models.generate_content(
        model=settings.GOOGLE_API_MODEL,
        contents=contents,
        config=config
      )
      
      return response.text
    except Exception as e:
      logger.error(f"Error generating response: {str(e)}")
      logger.error(traceback.format_exc())
      
      raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        detail=f"Error generating response: {str(e)}",
      )
    
  def get_email_analysis(self, content: str) -> LLmEmailResponse:
    logger.info(f"Getting email analysis")
    
    try:
      input_text = prompt_formatter_util(content)
      
      response = self.generate_response(input_text)
      logger.info(f"Response received: {response}")
      
      return json.loads(response)
      
    except json.JSONDecodeError as e:
      logger.error(f"Error decoding JSON: {str(e)}")
      logger.error(traceback.format_exc())
      raise HTTPException(
          status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
          detail=f"Error processing API response: {str(e)}",
      )
    except Exception as e:
      logger.error(f"Error get email analysis: {str(e)}")
      logger.error(traceback.format_exc())
      raise HTTPException(
          status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
          detail=f"Error get email analysis: {str(e)}",
      )