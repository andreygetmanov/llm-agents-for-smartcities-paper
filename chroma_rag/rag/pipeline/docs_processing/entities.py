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
    Defines types of data loaders supported by the application.

    Class Attributes:
    - docx
    - doc
    - odt
    - rtf
    - pdf
    - directory
    - zip
    - json

    These attributes represent supported file formats and sources for loading documents into the system.
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
    Loads documents for use with LangChain in a memory-efficient, on-demand fashion.

    Attributes:
        file_path: The path to the file containing the documents to be loaded.

    Methods:
        __init__
        lazy_load

    The __init__ method sets up the loader with the target file path. The lazy_load method allows processing large document collections by loading and yielding them one at a time, reducing memory usage.
    """

    def __init__(self, file_path: str):
        """
        Sets up the document loader with the specified path to the file to be processed.

        Args:
            file_path: The path to the file to be used by the instance.

        Returns:
            None: This method does not return a value.
        """

        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """
        Efficiently reads and yields parsed elements from a specified file stream as needed.

        Opens the file specified by the instance's file_path attribute, loads its content,
        and yields each document as it is loaded. This allows processing large files without
        loading all documents into memory at once.

        Returns:
            Iterator[Document]: An iterator that yields Document objects loaded from the file.
        """

        with open(self.file_path) as f:
            for i, doc_dict in load(f).items():
                yield ln_load(doc_dict)
