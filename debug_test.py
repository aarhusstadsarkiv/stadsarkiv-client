import logging

print("Hello from debug_test.py")

log = logging.getLogger(__name__)

log.debug("This is a debug message")

log.setLevel(logging.DEBUG)

log.debug("This is a debug message after debug level is set")
