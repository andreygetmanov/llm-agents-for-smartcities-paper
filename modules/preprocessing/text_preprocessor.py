from abc import ABCMeta
from abc import abstractmethod
import json
from string import Template
from typing import Callable, Dict, List

from requests import Response


StrTemplateType = str | Dict[str, str] | List[str]


class TextProcessorInterface(metaclass=ABCMeta):
    """Preprocessor intended for text preparation for using with LLMs."""

    @abstractmethod
    def preprocess_input(self, *args, **kwargs) -> StrTemplateType:
        """Preprocess input."""
        raise NotImplementedError

    @abstractmethod
    def preprocess_output(self, *args, **kwargs) -> str:
        """Extract actual answer from recieved response and process it to str form."""
        raise NotImplementedError


class BaseTextProcessor(TextProcessorInterface):
    """Default text preprocessor.

    Transforms given prompt to required format.
    Transforms LLM response to str type.
    """

    def __init__(self, input_format: StrTemplateType, out_format: Callable) -> None:
        """
        Set up the processor with the necessary input pattern and a function to convert the output data.

        Args:
            input_format (StrTemplateType): Required format of input data for LLM usage.
            out_format (Callable): Function which describes how to transform LLM's response
            to str.

        """

        self.input_format = input_format
        self.out_format = out_format

    def preprocess_input(self, **kwargs) -> StrTemplateType:
        """
        Transforms the input prompt and supplied parameters into a specified structured format, substituting template values and handling both string and dictionary formats as required.

                Raises:
                    ValueError: _description_

                Returns:
                    StrTemplateType: _description_

        """

        match self.input_format:
            case str():
                return json.loads(
                    Template(self.input_format)
                    .safe_substitute(**kwargs)
                    .replace("\n", "\\n")
                )
            case Dict():
                messages_key = kwargs.pop("template_messages")
                processed = self.input_format
                processed[messages_key] = Template(
                    self.input_format[messages_key]
                ).safe_substitute(**kwargs)
                return processed
            case _:
                raise ValueError(f"{type(self.input_format)} is not supported.")

    def preprocess_output(self, text: Response) -> str:
        """
        Converts the model's response object to a formatted text string using the specified output transformation function.

        Process response from the model to string format using given
        transformation function.

        Args:
            text (Response): Response received from the model.

        Returns:
            str: LLM's response in text format.

        """

        return self.out_format(text)
