from typing import Optional, Dict, Any

try:
    import openai
except ImportError:
    openai = None


class Generator:
    """Text generator for RAG pipeline."""

    def __init__(self, api_key: str, model: str = 'gpt-4', temperature: float = 0.7):
        """
        Initialize generator.

        Args:
            api_key: LLM API key
            model: Model name
            temperature: Generation temperature
        """
        if openai is None:
            raise ImportError("openai is not installed. Install it with: pip install openai")

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def generate(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate response using query and context.

        Args:
            query: User query
            context: Retrieved context
            system_prompt: Optional system prompt

        Returns:
            Dictionary with generated response and metadata
        """
        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant that answers questions based on the provided context. "
                "If the context doesn't contain relevant information, say so. "
                "Always cite which document(s) you used to answer."
            )

        user_message = f"""Context:
{context}

Question: {query}

Please answer the question based on the context provided above."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=self.temperature
            )

            return {
                'answer': response.choices[0].message.content,
                'model': self.model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }

        except Exception as e:
            return {
                'answer': None,
                'error': str(e)
            }
