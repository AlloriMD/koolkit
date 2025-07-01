import sys
import time
import threading
import signal

try:
    from rich.console import Console
    from rich.text import Text
    _rich_installed = True
except ImportError:
    _rich_installed = False

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

ANSI_COLOR_CODES = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "bright_black": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97,
}

class RippleProgressBar:
    def __init__(
        self,
        msg: str | None = "Working...",
        exit_msg: str | None = "Done!",
        speed: str|None = "medium",
        rainbow: bool|None = False,
        colors: list[str] | None = None,
        inverse: bool|None = False,
        use_rich: bool|None = None,
    ):
        """
        Context manager for displaying a progress indicator message with animated "rippling" colors.

        Inspired by Brett Terpstra:
        https://brettterpstra.com/2025/06/30/ripple-an-indeterminate-progress-indicator/
        Thanks for the idea!

        Args:
            msg (str): Progress indicator message that will be animated.
            exit_msg (str): Message to print when the process is completed.
            speed (str): 'fast', 'medium', or 'slow'.
            rainbow (bool): Enable rainbow coloring.
            colors (list of str): List of color names to use for rainbow effect.
            inverse (bool): Enable inverse coloring mode.
            use_rich (bool or None): If True, force use of Rich (if installed); if False, disable Rich;
                if None, auto-detect Rich support.

        """


        self.msg = msg
        self.exit_msg = exit_msg
        self.speed = {"fast": 0.05, "medium": 0.1, "slow": 0.2}.get(speed.lower(), 0.1)
        self.rainbow = rainbow
        self.inverse = inverse
        if use_rich is None:
            self.use_rich = _rich_installed
        else:
            self.use_rich = bool(use_rich) and _rich_installed

        self._index = 0
        self._direction = 1
        self._stop = threading.Event()
        self._thread = None
        self.console = Console() if self.use_rich else None

        if not colors:
            colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        if len(colors) < 6:
            needed = 6 - len(colors)
            extension = colors[-needed:][::-1]
            colors += extension
        self.colors = colors

    def _rich_frame(self):
        t = Text()
        length = len(self.msg)
        for i, char in enumerate(self.msg):
            # Highlight chars at self._index and self._index + 1
            if i == self._index or i == self._index + 1:
                if self.inverse:
                    # current chars dim
                    t.append(char, style="dim")
                else:
                    if self.rainbow:
                        color_index = (i + self._index) % len(self.colors)
                        t.append(char, style=self.colors[color_index])
                    else:
                        t.append(char, style="bold")
            else:
                if self.inverse:
                    if self.rainbow:
                        color_index = (i + self._index) % len(self.colors)
                        t.append(char, style=self.colors[color_index])
                    else:
                        t.append(char, style="bold")
                else:
                    t.append(char, style="dim")
        return t

    def _ansi_frame(self):
        RESET = "\033[0m"
        DIM = "\033[2m"
        BOLD = "\033[1m"

        output = ""
        length = len(self.msg)
        for i, ch in enumerate(self.msg):
            is_current = i == self._index or i == self._index + 1

            if is_current:
                if self.inverse:
                    output += f"{DIM}{ch}{RESET}"
                else:
                    if self.rainbow:
                        color_name = self.colors[(i + self._index) % len(self.colors)]
                        color_code = ANSI_COLOR_CODES.get(color_name.lower(), 37)
                        output += f"\033[{color_code}m{ch}{RESET}"
                    else:
                        output += f"{BOLD}{ch}{RESET}"
            else:
                if self.inverse:
                    if self.rainbow:
                        color_name = self.colors[(i + self._index) % len(self.colors)]
                        color_code = ANSI_COLOR_CODES.get(color_name.lower(), 37)
                        output += f"\033[{color_code}m{ch}{RESET}"
                    else:
                        output += f"{BOLD}{ch}{RESET}"
                else:
                    output += f"{DIM}{ch}{RESET}"
        return output

    def _animate(self):
        length = len(self.msg)
        while not self._stop.is_set():
            # Move index back and forth between 0 and len(text)-2
            if self._index >= length - 2:
                self._direction = -1
            elif self._index <= 0:
                self._direction = 1
            self._index += self._direction

            if self.use_rich:
                frame = self._rich_frame()
                # Print frame without newline or automatic carriage return
                self.console.print(frame, end="")
                # Move cursor back to start to overwrite in next iteration
                self.console.file.write("\r")
                self.console.file.flush()
            else:
                frame = self._ansi_frame()
                sys.stderr.write(f"\r{frame}")
                sys.stderr.flush()

            time.sleep(self.speed)

    def __enter__(self):
        # Hide cursor and start animation thread
        sys.stderr.write(HIDE_CURSOR)
        sys.stderr.flush()
        signal.signal(signal.SIGINT, lambda *_: self.__exit__(None, None, None))
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Stop animation and clean up
        self._stop.set()
        self._thread.join()
        clear_line = "\r" + " " * (len(self.msg) + 10) + "\r"
        sys.stderr.write(clear_line)
        sys.stderr.write(SHOW_CURSOR)
        sys.stderr.flush()
        print(self.exit_msg)


