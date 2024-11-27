from openai import OpenAI
import os
from typing import Optional, List
from enum import Enum, auto
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class Role(Enum):
    """Enum for different expert roles"""
    COIN_EXPERT = auto()
    PLANT_EXPERT = auto()


class Task(Enum):
    """Enum for different tasks"""
    TRANSLATE = auto()
    EXPLAIN = auto()
    ANALYZE = auto()
    SUMMARIZE = auto()
    FETCH_KEYWORDS_FROM_DIANDIAN = auto()


def get_system_context(role: Role) -> str:
    """
    Get the system context for OpenAI API calls based on the role.
    
    Args:
        role: Role enum value
        
    Returns:
        String containing the system context
    """
    contexts = {
        
        Role.COIN_EXPERT: """You are a numismatic expert with deep knowledge of coins, their history, 
and collecting. You provide detailed, accurate information about coins, their value, historical significance, 
and collecting practices. Your responses should be informative and precise.""",
        
        Role.PLANT_EXPERT: """You are a botanical expert with comprehensive knowledge of plants, 
gardening, and horticulture. You provide detailed advice about plant care, identification, growing conditions, 
and botanical science. Your responses should be practical and scientifically accurate.""",
    }
    
    return contexts.get(role, contexts[Role.PLANT_EXPERT])


def get_task_instruction(task: Task, **kwargs) -> str:
    """
    Get the task-specific instruction.
    
    Args:
        task: Task enum value
        **kwargs: Additional parameters needed for the task
    
    Returns:
        Task-specific instruction string
    """
    instructions = {
        Task.TRANSLATE: f"Translate the following text to {kwargs.get('target_language', 'English')}. Only respond with the translation, nothing else. If you think it does not have a proper translation, respond with the original text.",
        Task.EXPLAIN: "Explain the following concept in detail, providing clear examples where appropriate.",
        Task.ANALYZE: "Analyze the following information and provide insights and observations.",
        Task.SUMMARIZE: "Provide a concise summary of the following text, highlighting key points.",
        Task.FETCH_KEYWORDS_FROM_DIANDIAN: """Extract and clean ASA keywords from the following text. 
Return only the keywords, one per line. 
Remove any duplicates and invalid keywords.
Do not include any explanations or additional text."""
    }
    
    return instructions.get(task, "Please process the following input.")


def process_with_ai(text: str, role: Role, task: Task, **kwargs) -> Optional[str]:
    """
    Process text using OpenAI API with specified role and task.
    
    Args:
        text: The input text to process
        role: Role enum specifying the expert role
        task: Task enum specifying the operation to perform
        **kwargs: Additional parameters needed for specific tasks
    
    Returns:
        Processed text or None if processing fails
    """
    try:
        system_context = get_system_context(role)
        task_instruction = get_task_instruction(task, **kwargs)
        
        response = client.chat.completions.create(
            model="gpt-4",  # or your specific model name
            messages=[
                {
                    "role": "system",
                    "content": f"Your role:{system_context}\n\nYour task:{task_instruction}"
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Processing error: {str(e)}")
        return None


def translate_text(text: str, target_language: str) -> Optional[str]:
    """
    Convenience function for translation tasks.
    
    Args:
        text: The text to translate
        target_language: The language to translate to
    
    Returns:
        Translated text or None if translation fails
    """
    return process_with_ai(
        text=text,
        role=Role.COIN_EXPERT,
        task=Task.TRANSLATE,
        target_language=target_language
    )


def extract_keywords_from_diandian(text: str) -> List[str]:
    """
    Extract and clean keywords from diandian text content.
    Returns a list of cleaned keywords.
    """
    result = process_with_ai(
        text=text,
        role=Role.COIN_EXPERT,
        task=Task.FETCH_KEYWORDS_FROM_DIANDIAN
    )
    
    if result:
        # Split by newline and clean each keyword
        keywords = [kw.strip() for kw in result.split('\n') if kw.strip()]
        return keywords
    
    return []
