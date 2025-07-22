from enum import Enum
import pathlib
from typing import Any, List

import numpy as np
import pandas as pd


ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()
ArrayLike = List[Any] | np.ndarray | pd.Series


class ResponseMode(Enum):
    """
    Represents different modes of responding within the system.

    Class Attributes:
    - full
    - default

    Methods:
    - __init__
    - from_str
    - __str__
    - __eq__

    The class provides constants for response modes and utility methods for initialization, string conversion, and comparison.
    """

    full = "full"
    default = "default"
