from redsparrow.queue import PubQueue, SubQueue
import sys


pub = PubQueue('tcp://127.0.0.1:5600')
try:
    for i in range(0, 10000000000000):
        pub.send_string('test')
except KeyboardInterrupt:
    sys.exit(0)
