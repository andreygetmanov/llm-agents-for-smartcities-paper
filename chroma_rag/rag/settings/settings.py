from os.path import dirname
from pathlib import Path

from pydantic_settings import BaseSettings


class ChromaSettings(BaseSettings):
    """
    Manages configuration settings for connecting and interacting with a Chroma server and document collections.

    Class Attributes:
    - chroma_host: The hostname of the Chroma server.
    - chroma_port: The port on which the Chroma server is running.
    - allow_reset: Whether resetting of indexes or collections is allowed.
    - collection_name: The name of the document collection in Chroma.
    - embedding_name: Identifier for the embedding to use.
    - embedding_host: The host for the embedding service.
    - distance_fn: The distance function used for similarity calculations.
    - docs_processing_config: Configuration parameters for document processing.
    - docs_collection_path: Filesystem path to the document collection.

    Methods:
    - Provides class-level configuration management for Chroma database connections and behavior.
    """

    # Chroma DB settings
    chroma_host: str = "10.32.1.34"
    chroma_port: int = 9941
    allow_reset: bool = False

    # Documents collection's settings
    collection_name: str = "strategy-spb"
    embedding_name: str = "intfloat/multilingual-e5-large"
    embedding_host: str = "http://10.32.1.34:9942/embed"
    distance_fn: str = "cosine"

    # Documents' processing settings
    docs_processing_config: str = str(
        Path(dirname(dirname(__file__)) + "/configs/" + "docs_processing_config.yaml")
    )
    # docs_collection_path: str = str(Path(Path(__file__).parent.parent.parent, 'docs', 'strategy.pdf'))
    docs_collection_path: str = str(
        Path(dirname(dirname(dirname(__file__))) + "/docs/" + "example.docx")
    )

    # TODO: decide if we need a chroma.env local config
    # model_config = SettingsConfigDict(
    #     env_file=Path(dirname(dirname(__file__)) + '/configs/' + 'chroma.env'),
    #     env_file_encoding='utf-8',
    #     extra='ignore',
    # )


settings = ChromaSettings()
