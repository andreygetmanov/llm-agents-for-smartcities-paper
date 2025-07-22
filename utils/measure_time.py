import datetime
import time


def measure_execution_time(func):
    """
    No valid docstring found.
    """

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        return result, elapsed

    return wrapper


class Timer:
    """
    A context manager for timing execution intervals using datetime.

    Class Methods:
    - __init__:
    """

    def __init__(self):
        """
        Sets the initial state for tracking whether a process has been terminated.

        Returns:
            None: This method does not return a value.
        """

        self.process_terminated = False

    def __enter__(self):
        """
        Initializes timing by capturing the current timestamp when entering the context, allowing measurement of elapsed time within the context block.

        Records the current datetime as the start time when entering the context manager.

        Returns:
            The current instance of the object with the start time set.
        """

        self.start = datetime.datetime.now()
        return self

    @property
    def start_time(self):
        """
        Retrieves the initial time value recorded by the timer instance.

        Returns:
            The start time associated with this object.
        """

        return self.start

    @property
    def spent_time(self) -> datetime.timedelta:
        """
        Returns the duration that has passed since the timer was initiated.

        Returns:
            datetime.timedelta: The duration of time that has passed since the start time.
        """

        return datetime.datetime.now() - self.start_time

    @property
    def seconds_from_start(self) -> float:
        """
        Returns the elapsed duration in seconds since initialization.

        Returns:
            float: The total seconds spent from the start, as calculated from the spent_time attribute.
        """

        return self.spent_time.total_seconds()

    def __exit__(self, *args):
        """
        Finalizes timing operations and returns the timer's termination status when exiting the context.

        Args:
            args: Variable length argument list for exit information.

        Returns:
            bool: Indicates whether the process has been terminated.
        """

        return self.process_terminated
