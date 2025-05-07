from typing import Optional, Dict, Any
from fastapi import HTTPException
from app.llm.groq_client import GroqClient

class LLMService:
    def __init__(self):
        self.groq_client = GroqClient()

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        reset_conversation: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a response from the LLM
        
        Args:
            prompt: The user's input prompt
            system_prompt: Optional system prompt to guide the LLM
            reset_conversation: Whether to reset the conversation history
            
        Returns:
            dict: Response containing the generated text and conversation ID
        """
        try:
            response = await self.groq_client.get_response(
                prompt=prompt,
                system_prompt=system_prompt,
                reset_conversation=reset_conversation
            )
            
            return {
                "response": response["response"],
                "conversation_id": response.get("conversation_id", "temp_id"),
                "success": True
            }
            
        except HTTPException as he:
            raise he
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Failed to generate response",
                    "details": str(e),
                    "success": False
                }
            )
    
    def clear_conversation(self) -> None:
        """Clear the conversation history"""
        self.groq_client.clear_history()
