class PathIsNotAssigned(Exception):
    """
    Exception raised when an expected file system path has not been assigned.

    Attributes:
        message: The error message associated with the exception.

    The attribute `message` holds the details about the specific path assignment error.
    """

    def __init__(self, message):
        super.__init__(message)


class PipelineError(Exception):
    """
    Represents an error encountered during the execution of a pipeline.

    Attributes:
        message: The error message describing the pipeline issue.

    Class Methods:
    - __init__

    The 'message' attribute stores details about the pipeline error. The '__init__' method initializes the instance with a specific error message.
    """

    def __init__(self, message):
        super().__init__(message)


class FileExtensionError(Exception):
    """
    Exception raised when a file extension is not supported.

    Attributes:
        message: The error message associated with the exception.

    The class provides a custom exception for signaling invalid or unsupported file extensions.
    """

    def __init__(self, message):
        super().__init__(message)


class TransformerNameError(Exception):
    """
    Represents a custom exception for errors related to transformer naming conflicts or misconfigurations.

    Attributes:
        message: The error message describing the specific naming issue.

    Class Methods:
    - __init__
    """

    def __init__(self, message):
        super().__init__(message)


class LoaderNameError(Exception):
    """
    Exception raised when a loader name is invalid or not found.

    Attributes:
        message: The error message associated with the exception.

    Class Methods:
    - __init__:
    """

    def __init__(self, message):
        """
        Constructs the error instance with a specified message, enabling customized error reporting.

        Args:
            message: The message to be associated with this instance.

        Returns:
            None: This method does not return a value.
        """

        super().__init__(message)
