import json
from pathlib import Path
from typing import Any, Callable, Iterator

from langchain_community.document_loaders import JSONLoader
from langchain_core.documents import Document

from chroma_rag.rag.loaders.utilities import get_text


class CustomJSONLoader(JSONLoader):
    """
    Loads and processes JSON or JSON Lines files, extracting content and metadata for further use.

    Attributes:
        file_path: Path to the JSON or JSON Lines file.
        content_key: Key or schema for extracting content from JSON objects.
        metadata_func: Function to generate or update metadata dictionaries.
        text_content: Flag indicating if content is expected as a string.
        json_lines: Flag indicating if input data uses JSON Lines format.

    Methods:
        __init__
        _parse
        _get_text
        _get_metadata
        _validate_content_key
        _validate_metadata_func

    The class reads JSON or JSON Lines files, extracts content based on a specified key or jq-compatible schema, and can use a custom function to construct or enrich metadata. It includes methods for parsing input, verifying keys and metadata functions, and converting JSON samples to text suitable for downstream processing.
    """

    def __init__(
        self,
        file_path: str | Path,
        content_key: str | None = None,
        metadata_func: Callable[[dict, dict], dict] | None = None,
        text_content: bool = True,
        json_lines: bool = False,
    ):
        """
        Initializes the JSONLoader
        Args:
            file_path (Union[str, Path]): The path to the JSON or JSON Lines file.
            content_key (str): The key to use to extract the content from
                the JSON if the jq_schema results to a list of objects (dict).
                If is_content_key_jq_parsable is True, this has to be a jq compatible
                schema. If is_content_key_jq_parsable is False, this should be a simple
                string key.
            metadata_func (Callable[dict, dict]): A function that takes in the JSON
                object and the default metadata and returns a dict of the updated metadata.
            text_content (bool): Boolean flag to indicate whether the content is in
                string format, default to True.
            json_lines (bool): Boolean flag to indicate whether the input is in
                JSON Lines format.

        """

        self.file_path = Path(file_path).resolve()
        self._content_key = content_key
        self._metadata_func = metadata_func
        self._text_content = text_content
        self._json_lines = json_lines

    def _parse(self, content: str, index: int) -> Iterator[Document]:
        """
        Convert given content to documents.
        """

        data = json.loads(content)

        if self._content_key is not None:
            self._validate_content_key(data)
        if self._metadata_func is not None:
            self._validate_metadata_func(data)

        for i, sample in enumerate(data, index + 1):
            text = self._get_text(sample=sample)
            metadata = self._get_metadata(
                sample=sample, source=str(self.file_path), seq_num=i
            )
            yield Document(page_content=text, metadata=metadata)

    def _get_text(self, sample: Any) -> str:
        """
        Convert sample to string format
        """

        if self._content_key is not None:
            content = sample.get(self._content_key)
        else:
            content = sample

        if self._text_content and not isinstance(content, str):
            raise ValueError(
                f"Expected page_content is string, got {type(content)} instead. \
                    Set `text_content=False` if the desired input for \
                    `page_content` is not a string"
            )

        return get_text(content)

    def _get_metadata(
        self, sample: dict[str, Any], **additional_fields: Any
    ) -> dict[str, Any]:
        """
        Generate a metadata dictionary for a document using either a custom processing function or the provided additional fields.

        Args:
            sample (dict[str, Any]): The data payload used for generating metadata.
            **additional_fields (Any): Key-value pairs to be included in the metadata.

        Returns:
            dict[str, Any]: The resulting metadata dictionary for the document.

        """

        if self._metadata_func is not None:
            return self._metadata_func(sample, additional_fields)
        else:
            return additional_fields

    def _validate_content_key(self, data: list) -> None:
        """
        Check if a content key is valid
        """

        sample = data[0]
        if not isinstance(sample, dict):
            raise ValueError(
                f"Expected the json schema to result in a list of objects (dict), \
                    so sample must be a dict but got `{type(sample)}`"
            )

        if sample.get(self._content_key) is None:
            raise ValueError(
                f"Expected the json schema to result in a list of objects (dict) \
                    with the key `{self._content_key}` with the not-none value"
            )

    def _validate_metadata_func(self, data: list) -> None:
        """
        Check if the metadata_func output is valid
        """

        sample = data[0]
        if self._metadata_func is not None:
            sample_metadata = self._metadata_func(sample, {})
            if not isinstance(sample_metadata, dict):
                raise ValueError(
                    f"Expected the metadata_func to return a dict but got \
                        `{type(sample_metadata)}`"
                )
