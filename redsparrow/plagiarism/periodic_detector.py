import logging
import tornado
from tornado.ioloop import PeriodicCallback
from queue import Queue
from pony.orm import db_session
import concurrent
from concurrent.futures import ThreadPoolExecutor


from redsparrow.plagiarism.detector import PlagiarismDetector
from redsparrow.utils import Singleton


class ThesesQueue(Singleton):
    def __init__(self):
        self.queue = Queue(maxsixe=20)


    def __getattr__(self, name):
        return getattr(self.queue, name)




class PeriodicDetector(PeriodicCallback):

    def __init__(self, callback_time=1000):
       super(PeriodicDetector, self).__init__(callback=self.run, callback_time=callback_time)
       self.queue = Queue(maxsize=20)
       self.executor = ThreadPoolExecutor(max_workers=4)
       self.start()

    @tornado.gen.coroutine
    def run(self):
        if self.queue.empty():
            logging.debug("Empty queue!")
            return

        thesis_id = self.queue.get_nowait()
        logging.info("Processing thesis with id {}".format(thesis_id))
        detector = PlagiarismDetector()
        def __run():
            detector.process(thesis_id)
        self.executor.submit(__run)








