from copy import deepcopy
from typing import TextIO

from langchain_core.documents import BaseDocumentTransformer
from transformers import AutoTokenizer
import yaml

from chroma_rag.rag.pipeline.docs_processing.entities import transformer_object_dict
from chroma_rag.rag.pipeline.docs_processing.exceptions import TransformerNameError
from chroma_rag.rag.pipeline.docs_processing.models import ConfigFile


class Singleton:
    """
    Implements the Singleton design pattern, ensuring only one instance of the class exists throughout the program.

    Class Methods:
    - __new__:
    """

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one object of this class exists by always returning the same instance when the class is instantiated.

        Args:
            cls: The class for which the instance is being created.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The single instance of the class.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class PipelineSettings(Singleton):
    """Singleton class that manages configuration settings and initializes document transformers
    for a document processing pipeline.

    This class loads configuration from a file, validates it, and sets up the necessary document
    transformers based on the configuration.
    """

    def __init__(self):
        """
        Constructs an instance with placeholders for configuration data and document transformation components.

        Returns:
            None: This method does not return a value.
        """

        self._config_dict: ConfigFile | None = None
        self._transformers: list[BaseDocumentTransformer] | None = None

    def make_config_structure(self, config_file: str | TextIO):
        """
        Reads a configuration from a YAML file or text stream, verifies its structure, and sets up the necessary components based on the specified settings.

        Args:
            config_file (str | TextIO): Path to the YAML configuration file or a text stream containing the configuration.

        Raises:
            TransformerNameError: If the specified transformer name in the configuration is not recognized.

        """

        if isinstance(config_file, str):
            with open(config_file) as f:
                yaml_config = yaml.safe_load(f)
        else:
            yaml_config = config_file
        self._config_dict = ConfigFile.model_validate(yaml_config)

        splitter_params = self._config_dict.splitter.splitter_params

        if self._config_dict.splitter.splitter_name not in transformer_object_dict:
            raise TransformerNameError(
                f'There is no DocumentTransformer related to the name: "{self._config_dict.splitter}"'
            )
        else:
            transformer_names = ["recursive_character"]
            if self._config_dict.splitter.splitter_name != "recursive_character":
                transformer_names.append(self._config_dict.splitter.splitter_name)
            self._transformers = []
            transformer_params = []
            for transformer_name in transformer_names:
                transformer_class = transformer_object_dict[transformer_name]
                transformer_obj = transformer_class()
                transformer_params.append(
                    {
                        key: value
                        for key, value in splitter_params.items()
                        if f"_{key}" in transformer_obj.__dict__
                        or key in transformer_obj.__dict__
                    }
                )

                self._transformers.append(transformer_class(**transformer_params[-1]))

        if self._config_dict.tokenizer is not None:
            tokenizer = AutoTokenizer.from_pretrained(self._config_dict.tokenizer)

            for i in range(len(self._transformers)):
                transformer = self._transformers[i]
                self._transformers[i] = transformer.from_huggingface_tokenizer(
                    tokenizer, **transformer_params[i]
                )

    @property
    def config_structure(self) -> ConfigFile:
        """
        Returns a deep-copied representation of the internal configuration dictionary, enabling safe access and manipulation without affecting the original data.

        Returns:
            ConfigFile: A deep copy of the internal configuration dictionary.
        """

        return deepcopy(self._config_dict)

    @property
    def transformers(self) -> list[BaseDocumentTransformer]:
        """
        Returns a deep copy of the transformer objects managed by this settings instance.

        Returns:
            list: A deep copy of the list containing BaseDocumentTransformer objects.
        """

        return deepcopy(self._transformers)
