import os
from pathlib import Path

from deepeval.models.base_model import DeepEvalBaseLLM
from dotenv import load_dotenv
from openai import OpenAI
from openai._types import NOT_GIVEN

from modules.variables import ROOT


path_to_config = Path(ROOT, "config.env")


class VseGPTConnector(DeepEvalBaseLLM):
    """Implementation of Evaluation agent based on large language model for Assistant's answers evaluation."""

    def __init__(
        self,
        model: str,
        sys_prompt: str = "",
        base_url="https://api.vsegpt.ru/v1",
    ):
        """
        Set up the connector by loading environment settings and initializing model configuration, system prompt, and API endpoint before preparing the model for use

        Args:
            model: Evaluation model's name
            sys_prompt: predefined rules for model
            base_url: URL where models are available

        """

        load_dotenv(path_to_config)
        self._sys_prompt = sys_prompt
        self._model_name = model
        self.base_url = base_url
        self.model = self.load_model()

    def load_model(self) -> OpenAI:
        """
        Load model's instance.
        """

        # TODO extend pull of possible LLMs (Not only just OpenAI's models)
        return OpenAI(api_key=os.environ.get("VSE_GPT_KEY"), base_url=self.base_url)

    def generate(
        self,
        prompt: str,
        context: str = None,
        temperature: float = 0.015,
        *args,
        **kwargs,
    ) -> str:
        """
        Generate a text-based reply based on the provided input and optional supporting context, controlling output variability through temperature settings.

        Args:
            prompt (str): User's question, the model must answer.
            context (str, optional): Supplementary information, may be used for answer.
            temperature (float, optional): Determines randomness and diversity of generated answers.
            The higher the temperature, the more diverse the answer is. Defaults to .015.

        Returns:
            str: Model's response for user's question.

        """

        usr_msg_template = (
            prompt if context is None else f"Вопрос:{prompt} Контекст:{context}"
        )
        formatted_message = [
            {"role": "system", "content": self._sys_prompt},
            {"role": "user", "content": usr_msg_template},
        ]
        response_format = kwargs.get("schema", NOT_GIVEN)
        response = self.model.chat.completions.create(
            model=self._model_name,
            messages=formatted_message,
            temperature=temperature,
            n=1,
            max_tokens=8182,
            response_format=response_format,
        )
        return response.choices[0].message.content

    async def a_generate(
        self,
        prompt: str,
        context: str = None,
        temperature: float = 0.015,
        *args,
        **kwargs,
    ) -> str:
        """
        Produces a text output by leveraging a prompt and optional context, adjusting randomness with the provided temperature parameter.

        Args:
            prompt: The input text to generate a response for.
            context: Optional supplementary context to guide the generation process.
            temperature: Controls the randomness or creativity of the output. Lower values result in more deterministic output.
            *args: Additional positional arguments passed to the underlying generate method.
            **kwargs: Additional keyword arguments passed to the underlying generate method.

        Returns:
            str: The generated response as a string.
        """

        return self.generate(prompt, context, temperature, *args, **kwargs)

    def get_model_name(self, *args, **kwargs) -> str:
        """
        Retrieves a descriptive identifier for the custom language model implementation.

        Args:
            self: The instance of the class.

        Returns:
            str: A string representing the custom LLM name.
        """

        return "Implementation of custom LLM for evaluation."
