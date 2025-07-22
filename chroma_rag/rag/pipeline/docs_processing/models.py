from typing import Any

from pydantic import BaseModel


class ConfigLoader(BaseModel):
    """
    ConfigLoader is responsible for loading, parsing, and saving configuration files for various data processing workflows.

    Class Attributes:
    - doc_path
    - save_path
    - loader_name
    - parsing_params

    Methods:
    - load
    - save
    - parse
    - validate

    The methods provide functionality for loading and parsing configuration documents, saving the processed configurations, and validating the configuration data. The attributes specify file paths, the name of the loader, and parameters used during parsing.
    """

    doc_path: str = ""
    save_path: str = ""
    loader_name: str
    parsing_params: dict[str, Any] = dict()


class ConfigSplitter(BaseModel):
    """
    Splits complex configuration files into smaller, manageable sub-configurations.

    Class Attributes:
    - splitter_name: The name identifying the specific splitting strategy used.
    - splitter_params: Parameters that control or customize the splitting behavior.

    Methods:
    - __init__
    - split
    - validate

    The methods of this class provide initialization with desired parameters, splitting logic to divide configurations, and validation to ensure correctness of the split. The attributes allow control over which splitting strategy is applied and with what parameters.
    """

    splitter_name: str | None = None
    splitter_params: dict[str, Any] = dict()


class ConfigFile(BaseModel):
    """
    Represents a configuration file handler for processing and managing configuration data.

    Class Attributes:
    - loader: Loads configuration contents from a file.
    - splitter: Splits the content into sections or segments.
    - tokenizer: Breaks down the segments into manageable tokens for parsing.

    Methods:
    - load
    - save
    - validate
    - parse
    """

    loader: ConfigLoader
    splitter: ConfigSplitter = ConfigSplitter()
    tokenizer: str | None = None
