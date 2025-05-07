from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.config import settings

class GroqClient:
    def __init__(self):
        self.llm = ChatGroq(
            model_name=settings.MODEL_NAME,
            groq_api_key=settings.GROQ_API_KEY,
            temperature=0.7,
            max_tokens=1024,
        )
        self.conversation_history = []

    async def get_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        reset_conversation: bool = False
    ) -> Dict[str, str]:
        """
        Get a response from the LLM
        
        Args:
            prompt: User's input message
            system_prompt: Optional system message to set the behavior of the assistant
            reset_conversation: Whether to clear conversation history
            
        Returns:
            Dict[str, str]: Generated response from the LLM and conversation ID
        """
        try:
            if reset_conversation:
                self.conversation_history = []

            # Prepare messages list for this request
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            # Add current user message
            messages.append(HumanMessage(content=prompt))

            # Get response from the model
            response = await self.llm.agenerate([messages])

            # Extract the response text
            response_text = response.generations[0][0].text

            # Add user message and assistant's response to conversation history
            self.conversation_history.extend([
                HumanMessage(content=prompt),
                AIMessage(content=response_text)
            ])

            return {
                "response": response_text,
                "conversation_id": "temp_id",  # Implement conversation ID logic if needed
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting response from Groq: {str(e)}",
            )
    
    def clear_history(self) -> None:
        """Clear the conversation history"""
        self.conversation_history = []
