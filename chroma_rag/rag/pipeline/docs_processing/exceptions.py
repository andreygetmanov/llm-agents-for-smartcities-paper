class PathIsNotAssigned(Exception):
    """
    Exception raised when a required filesystem path has not been assigned.

    Attributes:
        message: The message associated with this exception, providing details about the missing path.

    Methods:
    - __init__
    """

    def __init__(self, message):
        super.__init__(message)


class PipelineError(Exception):
    """
    Represents an error that occurs within a data processing pipeline.

    Attributes:
        message: The error message describing what caused the exception.

    The class provides a structured way to handle and represent exceptions specific to pipeline operations by storing a descriptive message.
    """

    def __init__(self, message):
        super().__init__(message)


class FileExtensionError(Exception):
    """
    Exception raised for errors involving invalid or unsupported file extensions.

    Attributes:
        message: Stores the error message associated with the exception.

    The message attribute contains a descriptive explanation of the file extension error.
    """

    def __init__(self, message):
        super().__init__(message)


class TransformerNameError(Exception):
    """
    Exception raised when there is a name-related error in a transformer component.

    Class Methods:
    - __init__

    Attributes:
    - message

    __init__:
        Initializes TransformerNameError with a specific error message, which can be accessed via the 'message' attribute.
    """

    def __init__(self, message):
        super().__init__(message)


class LoaderNameError(Exception):
    """
    Exception raised when a specified loader name fails to resolve or is invalid.

    Attributes:
    - message

    The 'message' attribute stores the error message describing the loader name issue.
    Methods:
    - __init__
    """

    def __init__(self, message):
        """
        Constructs the exception with a specific error message.

        Args:
            message: The message to be passed to the superclass initializer.

        Returns:
            None. Initializes the object.
        """

        super().__init__(message)
