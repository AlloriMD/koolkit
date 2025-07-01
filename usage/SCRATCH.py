# Example for using the progress bars...

import time

from koolkit.progress_bars import RippleProgressBar, SpinnerProgressBar, EllipsisProgressBar

# Using the ripple effect as a context manager...
with RippleProgressBar("••• Working •••",
                       rainbow=True,
                       inverse=True,
                       colors=["cyan", "blue", "magenta"]
                       ):
    # Your wrapped code goes here...
    # Do some stuff...
    time.sleep(5)
    # Do other stuff.
print("Out of the context block. Doing something else now...\n")


with SpinnerProgressBar(speed='fast', move_to_end=False):
    time.sleep(5)
print("Out of the context block. Doing something else now...\n")

with EllipsisProgressBar():
    time.sleep(5)
print("Out of the context block. Doing something else now...\n")

