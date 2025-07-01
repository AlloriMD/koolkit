import sys
import time
import threading
import signal

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


class SpinnerProgressBar:
    def __init__(
        self,
        msg: str | None = "Working",
        exit_msg: str | None = "Done!",
        speed: str | float = "medium",
        move_to_end: bool | None = False,
    ):
        """
        Context manager for displaying a progress indicator message with animated spinner.

        Args:
            msg (str): Progress indicator message.
            exit_msg (str): Message to print when the process is completed.
            speed (str): Animation speed; 'fast', 'medium', or 'slow'
            move_to_end (bool): If True, spinner appears after the text; otherwise before.
        """

        self.msg = msg
        self.exit_msg = exit_msg
        self.speed = {"fast": 0.1, "medium": 0.25, "slow": 0.5}.get(speed.lower(), 0.25)

        self.position_at_end = move_to_end
        self._stop = threading.Event()
        self._thread = None

        self.frames = ["│", "╱", "─", "╲"]
        self._frame_index = 0

    def _animate(self):
        num_frames = len(self.frames)
        max_len = len(self.msg) + 2  # for spinner + space

        while not self._stop.is_set():
            spinner = self.frames[self._frame_index]
            if self.position_at_end:
                display = f"{self.msg} {spinner}"
            else:
                display = f"{spinner} {self.msg}"

            # Pad to clear leftover chars
            padded_display = display.ljust(max_len)

            sys.stderr.write(f"\r{padded_display}")
            sys.stderr.flush()

            self._frame_index = (self._frame_index + 1) % num_frames
            time.sleep(self.speed)

    def __enter__(self):
        sys.stderr.write(HIDE_CURSOR)
        sys.stderr.flush()
        signal.signal(signal.SIGINT, lambda *_: self.__exit__(None, None, None))
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop.set()
        self._thread.join()
        clear_line = "\r" + " " * (len(self.msg) + 2) + "\r"
        sys.stderr.write(clear_line)
        sys.stderr.write(SHOW_CURSOR)
        sys.stderr.flush()
        print(self.exit_msg)
