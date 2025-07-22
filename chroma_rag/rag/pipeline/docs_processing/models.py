from typing import Any

from pydantic import BaseModel


class ConfigLoader(BaseModel):
    """
    Loads, parses, and manages configuration files for various sources.

    Class Attributes:
    - doc_path
    - save_path
    - loader_name
    - parsing_params

    Methods:
    - __init__
    - load
    - parse
    - save
    - validate

    The class provides mechanisms to load configuration documents from the specified path, parse them according to the loader's logic and parameters, validate their contents, and save results to a target path. Attributes store relevant file paths, loader identity, and parsing configuration.
    """

    doc_path: str = ""
    save_path: str = ""
    loader_name: str
    parsing_params: dict[str, Any] = dict()


class ConfigSplitter(BaseModel):
    """
    Splits configuration objects into separate parts based on specified rules.

    Class Attributes:
    - splitter_name: Name or identifier for the splitter instance.
    - splitter_params: Parameters used to control splitter behavior.

    Methods:
    - split()
    - validate()
    - update_params()

    The methods allow for splitting the configuration, validating configurations, and updating the splitter's parameters. The attributes store the splitter's name and its operational parameters.
    """

    splitter_name: str | None = None
    splitter_params: dict[str, Any] = dict()


class ConfigFile(BaseModel):
    """
    Represents a configuration file handler for loading, splitting, and tokenizing text files.

    Class Methods:
    - load_config()
    - save_config()
    - process_file()

    Class Attributes:
    - loader: Responsible for loading the configuration file from disk.
    - splitter: Handles splitting the loaded text into sections or components.
    - tokenizer: Tokenizes the text data for further processing.

    The methods allow for configuration files to be loaded, saved, and processed, while the attributes manage the functional components for handling file operations and text processing.
    """

    loader: ConfigLoader
    splitter: ConfigSplitter = ConfigSplitter()
    tokenizer: str | None = None
