"""Module for handling user input and background listeners."""

import sys
import threading
import time

if sys.platform == "win32":
  import msvcrt

  def get_keypress() -> bool:
    """Returns True if a key has been pressed on Windows."""
    return msvcrt.kbhit()
else:
  import select

  def get_keypress() -> bool:
    """Returns True if a key has been pressed on Unix-like systems."""
    return select.select([sys.stdin], [], [], 0)[0]


def listener_thread(stop_event: threading.Event):
  """Background thread that watches for a keypress to stop the program."""
  while not stop_event.is_set():
    if get_keypress():
      stop_event.set()
      break
    time.sleep(0.1)
