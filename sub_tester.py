from redsparrow.queue import PubQueue, SubQueue
import sys
import time

def on_data(stream, data='nic'):
      sys.stdout.write(data + '\n')
      for txt in stream:
          print(txt)
      sys.stdout.flush()
sub = SubQueue('tcp://127.0.0.1:5600', on_data)
data = sub.socket.recv()
print('------------{}'.format(data))
try:
    while True:
        sub.stream.flush()
except KeyboardInterrupt:
    sys.exit(0)

