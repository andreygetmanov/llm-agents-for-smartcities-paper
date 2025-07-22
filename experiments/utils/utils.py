from typing import Any


class LLAMAHandler:
    """Class for interaction with llama models."""

    def __init__(self, model, tokenizer, *args, **kwargs) -> None:
        """
        Sets up the handler by assigning the specified model and tokenizer, and prepares the prompt placeholder for future use.

        Args:
            model: The model to be used and stored in the instance.
            tokenizer: The tokenizer to be used and stored in the instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            None: This method does not return a value.
        """

        self.model = model  # Initialized model
        self.tokenizer = tokenizer
        self._prompt = None  # Set up default prompt

    def set_prompt(self):
        """
        Method for prompt configuration.
        """

        pass

    def generate(self, generation_config: Any, *args, **kwargs):
        """
        Generate an answer given prompt and generation config.
        """

        pass
