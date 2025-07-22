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
    A utility class for measuring the elapsed time of code execution, typically within a context manager.

    Class Methods:
    - __init__
    - __enter__
    - start_time
    - spent_time
    - seconds_from_start
    - __exit__

    Attributes:
    - start: Stores the timestamp when timing begins.
    - process_terminated: A flag indicating if the process running the timer was terminated.

    This class allows users to measure elapsed time using a context manager. The start attribute records the starting time, while process_terminated notes whether the associated process was terminated. Methods are provided to obtain the start time, compute elapsed time as a timedelta, retrieve the number of seconds elapsed, and manage cleanup upon exiting the context.
    """

    def __init__(self):
        """
        Creates a new timer instance and initializes its state to indicate that the associated process is active.

        Args:
            self: The instance of the class.

        Returns:
            None: This method does not return a value.
        """

        self.process_terminated = False

    def __enter__(self):
        """
        Records the current timestamp when entering the context and provides access to timing information via the context manager instance.

        Returns:
            The context manager instance with the start time initialized.
        """

        self.start = datetime.datetime.now()
        return self

    @property
    def start_time(self):
        """
        Retrieves the initial recorded time value.

        Returns:
            The start time associated with the object.
        """

        return self.start

    @property
    def spent_time(self) -> datetime.timedelta:
        """
        Computes the time duration from when the timer started to the present moment

        Returns:
            datetime.timedelta: The duration of time that has passed since the start time.
        """

        return datetime.datetime.now() - self.start_time

    @property
    def seconds_from_start(self) -> float:
        """
        Returns the total elapsed time in seconds since the timer was initiated.

        Returns:
            float: The total number of seconds elapsed, as calculated from spent_time.
        """

        return self.spent_time.total_seconds()

    def __exit__(self, *args):
        """
        Determines the outcome when exiting the context by returning the recorded process termination status.

        Args:
            *args: Arbitrary positional arguments passed by the context manager protocol.

        Returns:
            Boolean. Indicates whether the process has been terminated.
        """

        return self.process_terminated
