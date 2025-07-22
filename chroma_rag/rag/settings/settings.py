from os.path import dirname
from pathlib import Path

from pydantic_settings import BaseSettings


class ChromaSettings(BaseSettings):
    """
    ChromaSettings manages configuration settings for connecting to and interacting with a Chroma database instance.

    Class Attributes:
    - chroma_host: The host address for the Chroma server.
    - chroma_port: The port number to connect to the Chroma server.
    - allow_reset: Indicates whether the database can be reset.
    - collection_name: Name of the document collection in Chroma.
    - embedding_name: Name of the embedding model to use.
    - embedding_host: Host address of the embedding provider.
    - distance_fn: Function used to calculate distance between embeddings.
    - docs_processing_config: Configuration related to document processing.
    - docs_collection_path: Local path where the Chroma collection is stored.

    Methods:
    - Provides functionality to load and manage Chroma database configurations, as well as to control connection parameters and processing settings.
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
