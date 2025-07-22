from enum import Enum
import pathlib
from typing import Any, List

import numpy as np
import pandas as pd


ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()
ArrayLike = List[Any] | np.ndarray | pd.Series


class ResponseMode(Enum):
    """
    Represents response modes available in an authentication protocol.

    Class Attributes:
    - full: Indicates a complete response mode.
    - default: Indicates the default response mode.

    Methods:
    - values
    - from_str

    The attributes specify the available response modes. The methods provide utilities for listing available modes and constructing a ResponseMode from a string.
    """

    full = "full"
    default = "default"
