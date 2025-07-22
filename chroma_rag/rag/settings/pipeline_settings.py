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
    Implements the Singleton design pattern to ensure only one instance of the class exists.

    Class Methods:
    - __new__:
    """

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the class exists by returning a shared object upon each instantiation.

        If the class instance does not already exist, this method creates and stores a singleton instance; otherwise, it returns the existing instance.

        Args:
            cls: The class to create an instance of.
            *args: Variable length argument list passed to the constructor.
            **kwargs: Arbitrary keyword arguments passed to the constructor.

        Returns:
            The singleton instance of the specified class.
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
        Sets up internal attributes to manage configuration data and document transformation components within the class.

        Initializes the internal configuration dictionary and a list of document transformers as None.

        Returns:
            None: This method does not return a value.
        """

        self._config_dict: ConfigFile | None = None
        self._transformers: list[BaseDocumentTransformer] | None = None

    def make_config_structure(self, config_file: str | TextIO):
        """
        Parses a configuration from a YAML file or stream, checks its validity, and prepares the required transformation components as specified by the configuration.

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
        Provides a deep copy of the internal configuration dictionary to prevent accidental modifications.

        This property retrieves a deep copy of the internal configuration dictionary, ensuring the original configuration remains unaltered by external modifications.

        Returns:
            ConfigFile: A deep copy of the current configuration structure.
        """

        return deepcopy(self._config_dict)

    @property
    def transformers(self) -> list[BaseDocumentTransformer]:
        """
        Provides a duplicate list of transformation components currently configured for use.

        This property provides access to the current set of document transformers associated with the instance, ensuring that the returned list cannot be modified to affect the original.

        Returns:
            list: A deep copy of the list containing the document transformers.
        """

        return deepcopy(self._transformers)
