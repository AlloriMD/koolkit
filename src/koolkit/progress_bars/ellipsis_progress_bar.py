import sys
import time
import threading
import signal

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


class EllipsisProgressBar:
    def __init__(
        self,
        msg: str | None = "Working",
        exit_msg: str | None = "Done!",
        speed: str | None = "medium",
        forward_only: bool | None = False,
    ):
        """
        Context manager for displaying a progress indicator message with animated ellipsis.

        Args:
            msg (str): Progress indicator message that will be animated.
            exit_msg (str): Message to print when the process is completed.
            speed (str): 'fast', 'medium', or 'slow'.
            forward_only (bool): If True, ellipsis grows then resets; else pulses back and forth

        """

        self.msg = msg
        self.exit_msg = exit_msg
        self.speed = {"fast": 0.1, "medium": 0.25, "slow": 0.5}.get(speed.lower(), 0.25)

        self._stop = threading.Event()
        self._thread = None
        self._frame_index = 0

        if forward_only:
            self.frames = ["", ".", "..", "..."]
        else:
            self.frames = ["", ".", "..", "...", "..", ".", ""]

    def _animate(self):
        num_frames = len(self.frames)
        max_len = len(self.msg) + 3  # max length with "..."
        while not self._stop.is_set():
            frame = self.frames[self._frame_index]
            display = f"{self.msg}{frame}"
            # Pad with spaces to clear previous longer text
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
        clear_line = "\r" + " " * (len(self.msg) + 5) + "\r"
        sys.stderr.write(clear_line)
        sys.stderr.write(SHOW_CURSOR)
        sys.stderr.flush()
        print(self.exit_msg)
