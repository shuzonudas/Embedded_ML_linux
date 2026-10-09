"""Unit test to verify the exit-on-keypress logic."""

import unittest
import threading
import time
from unittest.mock import patch
import input_handler

class TestExitLogic(unittest.TestCase):

  def test_listener_sets_event_on_keypress(self):
    """Verify that listener_thread sets the stop_event when a key is pressed."""
    stop_event = threading.Event()
    
    # We mock get_keypress to return False for 2 calls, then True
    with patch('input_handler.get_keypress') as mock_keypress:
      mock_keypress.side_effect = [False, False, True]
      
      # Start the listener in a thread
      t = threading.Thread(target=input_handler.listener_thread, args=(stop_event,))
      t.start()
      
      # Wait for the thread to process the side_effects
      # (0.1s sleep in listener * 3 calls = ~0.3s)
      t.join(timeout=2)
      
      self.assertTrue(stop_event.is_set(), "Stop event should be set after keypress simulation.")
      self.assertFalse(t.is_alive(), "Listener thread should have terminated.")

if __name__ == '__main__':
  unittest.main()
