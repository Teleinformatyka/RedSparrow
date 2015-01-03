import zmq
from zmq.eventloop import ioloop
ioloop.install()

import tornado

import time
from redsparrow.queue import RequestQueue, QueueReqMessage

def callback(tmp):
    print(tmp)

def main():
    send = RequestQueue("tcp://localhost:5555")
    # msg = QueueReqMessage(id='1', params={'login': 'test', 'password': 'test'}, method='login')
    msg = QueueReqMessage()
    msg.id = 1
    msg.method = 'thesismethods-add_thesis'
    msg.params = {'thesis_name': 'test', 'user_id': 1, 'supervisor_id': 2, 'fos_id': 1,'filepath': '/home/aldor/workspace/RedSparrow/lecturer_database/praca_mgr.docx'}
    send.on_recv(callback)
    send.send_string(str(msg))
    time.sleep(4)

if __name__ == '__main__':
     ioloop.IOLoop.instance().run_sync(main)
