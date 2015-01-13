import zmq
from zmq.eventloop import ioloop
ioloop.install()

import tornado

import time
from redsparrow.queue import RequestQueue, QueueReqMessage

def callback(tmp):
    print(tmp)

def add_thesis(send):
    # msg = QueueReqMessage(id='1', params={'login': 'test', 'password': 'test'}, method='login')
    msg = QueueReqMessage()
    msg.id = 1
    msg.method = 'thesismethods-add_thesis'
    # msg.params = {'thesis_name': 'test', 'user_id': 1, 'supervisor_id': 2, 'fos_id': 1,'filepath': '/home/aldor/workspace/RedSparrow/lecturer_database/Mariusz_Starzak-praca_magisterska.odt'}
    msg.params = {'thesis_name': 'test', 'user_id': 1, 'supervisor_id': 2, 'fos_id': 1,'filepath': '/home/aldor/workspace/RedSparrow/lecturer_database/webrtc - praca magisterska.docx'}
    send.on_recv(callback)
    send.send_string(str(msg))
    time.sleep(4)
def run_analysis(send):
    # msg = QueueReqMessage(id='1', params={'login': 'test', 'password': 'test'}, method='login')
    msg = QueueReqMessage()
    msg.id = 1
    msg.method = 'thesismethods-run_analysis'
    msg.params = {'thesis_id': 7}
    send.on_recv(callback)
    send.send_string(str(msg))
    time.sleep(4)

def main():
    send = RequestQueue("tcp://localhost:5555")
    run_analysis(send)
    # add_thesis(send)



if __name__ == '__main__':
    ioloop.IOLoop.instance().run_sync(main)
