from enum import Enum
from json import load
from typing import Iterator

from docs_processing.splitting import HierarchicalMerger
from docs_processing.splitting import ListHierarchySplitter
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.load import load as ln_load
from langchain_text_splitters import RecursiveCharacterTextSplitter


transformer_object_dict = {
    "recursive_character": RecursiveCharacterTextSplitter,
    "list_hierarchy": ListHierarchySplitter,
    "hierarchical_merger": HierarchicalMerger,
}


class LoaderType(str, Enum):
    """
    Represents different types of document loaders supported by the application.

    Class Attributes:
    - docx
    - doc
    - odt
    - rtf
    - pdf
    - directory
    - zip
    - json

    Attributes represent the supported file formats and input sources that can be handled by the application.
    """

    docx = "docx"
    doc = "doc"
    odt = "odt"
    rtf = "rtf"
    pdf = "pdf"
    directory = "directory"
    zip = "zip"
    json = "json"


class LangChainDocumentLoader(BaseLoader):
    """
    Loads documents using the LangChain framework, facilitating integration with various document formats and sources.

    Methods:
    - __init__
    - lazy_load

    Attributes:
    - file_path
    - file_format

    Methods Summary:
    - __init__: Initializes the document loader with the specified file path and format.
    - lazy_load: Loads and yields documents one at a time from the file, allowing efficient document processing.

    Attributes Summary:
    - file_path: The path to the document source file.
    - file_format: The format of the document file to be processed.
    """

    def __init__(self, file_path: str):
        """
        Sets up the loader with the path to the input file for document processing.

        Args:
            file_path: The path to the file to be associated with the instance.

        Returns:
            None. This constructor does not return a value.
        """

        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """
        Efficiently retrieves and generates document objects from the specified file as needed, minimizing memory usage by processing one document at a time.

        Opens the file specified by the instance, parses its contents, and yields each document after processing.

        Returns:
            Iterator of Document: An iterator that yields Document objects loaded from the file.
        """

        with open(self.file_path) as f:
            for i, doc_dict in load(f).items():
                yield ln_load(doc_dict)
