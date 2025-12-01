"""
LLM Client - Unified interface for LLM calls.
Supports OpenAI, Azure OpenAI, and other providers.
"""

import os
import json
from typing import List, Dict, Any, Optional, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass
from openai import OpenAI, AzureOpenAI
from src.financial_research_agent.config import Config


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    content: str
    model: str
    usage: Dict[str, int]
    raw_response: Any = None


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def chat(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> LLMResponse:
        """Send chat completion request."""
        pass
    
    @abstractmethod
    def complete(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """Send completion request (wraps as chat)."""
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI API client."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY env var or pass api_key.")
        
        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
            
        self.client = OpenAI(**client_kwargs)
        self.default_model = "gpt-4o"
    
    def chat(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> LLMResponse:
        """Send chat completion request."""
        kwargs = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
            
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**kwargs)
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            raw_response=response
        )
    
    def complete(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """Send completion request (wraps as chat)."""
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, model, temperature, max_tokens)


class AzureOpenAIClient(BaseLLMClient):
    """Azure OpenAI API client."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        api_version: str = "2024-02-15-preview"
    ):
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = api_version
        
        if not self.api_key or not self.endpoint:
            raise ValueError("Azure OpenAI credentials not provided.")
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
        self.default_model = "gpt-4o"
    
    def chat(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> LLMResponse:
        """Send chat completion request."""
        kwargs = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
            
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**kwargs)
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            raw_response=response
        )
    
    def complete(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """Send completion request (wraps as chat)."""
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, model, temperature, max_tokens)


class LLMRouter:
    """
    RouteLLM - Adaptive model routing for cost/quality optimization.
    Routes requests to appropriate models based on task complexity.
    Section 2.6.
    """
    
    def __init__(self, client: BaseLLMClient):
        self.client = client
        
        # Model tiers
        self.strong_models = ["gpt-4o", "gpt-4-turbo", "gpt-4"]
        self.weak_models = ["gpt-4o-mini", "gpt-3.5-turbo"]
        
        # Task type to model mapping
        self.task_model_map = {
            "planning": "gpt-4o",       # High complexity
            "arbitration": "gpt-4o",    # High complexity
            "review": "gpt-4o",         # High complexity
            "research": "gpt-4o-mini",  # Medium complexity, high volume
            "writing": "gpt-4o-mini",   # Medium complexity
            "summarize": "gpt-4o-mini", # Low complexity, high volume
            "default": "gpt-4o-mini"
        }
    
    def route(
        self, 
        task_type: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> LLMResponse:
        """Route request to appropriate model based on task type."""
        model = self.task_model_map.get(task_type, self.task_model_map["default"])
        return self.client.chat(messages, model, temperature, max_tokens, json_mode)
    
    def estimate_complexity(self, prompt: str) -> str:
        """
        Estimate task complexity to determine model tier.
        Returns: 'high', 'medium', or 'low'
        """
        # Simple heuristic based on prompt length and keywords
        high_complexity_keywords = [
            "analyze", "evaluate", "compare", "synthesize", 
            "recommend", "predict", "assess risk", "arbitrate"
        ]
        
        prompt_lower = prompt.lower()
        
        # Check for high complexity keywords
        if any(kw in prompt_lower for kw in high_complexity_keywords):
            return "high"
        
        # Length-based heuristic
        if len(prompt) > 2000:
            return "medium"
        
        return "low"
    
    def auto_route(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> LLMResponse:
        """Automatically route based on prompt complexity."""
        # Get the user message for complexity estimation
        user_messages = [m for m in messages if m["role"] == "user"]
        if user_messages:
            complexity = self.estimate_complexity(user_messages[-1]["content"])
        else:
            complexity = "low"
        
        if complexity == "high":
            model = self.strong_models[0]
        elif complexity == "medium":
            model = self.weak_models[0]  # gpt-4o-mini
        else:
            model = self.weak_models[0]
        
        return self.client.chat(messages, model, temperature, max_tokens, json_mode)


def get_llm_client(provider: str = "openai") -> BaseLLMClient:
    """Factory function to get LLM client."""
    if provider == "openai":
        return OpenAIClient()
    elif provider == "azure":
        return AzureOpenAIClient()
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_llm_router(provider: str = "openai") -> LLMRouter:
    """Factory function to get LLM router."""
    client = get_llm_client(provider)
    return LLMRouter(client)


# Convenience functions
def chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    json_mode: bool = False
) -> str:
    """Simple chat completion function."""
    client = get_llm_client()
    response = client.chat(messages, model, temperature, max_tokens, json_mode)
    return response.content


def simple_completion(prompt: str, model: Optional[str] = None) -> str:
    """Simple completion function."""
    client = get_llm_client()
    response = client.complete(prompt, model)
    return response.content
