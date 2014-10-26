from redsparrow.queue import PubQueue, QueueMessage
from redsparrow.config import Config

import time


conf = Config()
conf.load('../config/config.yml')



pub = PubQueue(conf['subqueue'])

message = QueueMessage()
message.id = 1
message.method = 'gettext'
message.params = dict()
message.params['file_path'] = '/tmp/pdf.pdf'

for i in range(0, 1):
    time.sleep(2)
    pub.send_string(str(message))
    time.sleep(2)



