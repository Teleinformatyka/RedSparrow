
from pony.orm import db_session

from redsparrow.orm import Thesis
from redsparrow.plagiarism.levenshtein import  Levenshtein
from redsparrow.plagiarism.rabinkarb import  RabinKarb




class PlagiarismDetector(object):

    def preprocess(self, thesis_id):
        pass
        # get data from db
        # get keyword
        # start processing in by neares keyword
    @db_session
    def process(self, toCheck):
        thesis = Thesis.select()[:]
        result = {'thesis_id': toCheck['id']}
        thesisToAnalyze = []
        for thesi in thesis:
            thesi = thesi.to_dict(with_collections=True, related_objects=True)
            if RabbinKarb.calculate(thesi['keywords'], toCheck['keywords']):
                thesisToAnalyze.append(thesis)

        result['Levenshtein'] = {}
        for thesi in thesisToAnalyze:
            result['Levenshtein'][thesi['id']] = Levenshtein.distance(toCheck['text'],  thesi['text'])

        return result



