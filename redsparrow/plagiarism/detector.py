
from pony.orm import db_session

from redsparrow.orm import Thesis, Similarity, LinesWords
from redsparrow.plagiarism.levenshtein import  Levenshtein
from redsparrow.plagiarism.rabinkarb import  RabinKarb
from redsparrow.extractor.winnowing import winnow
from redsparrow.keywords import calculate_keywords_similarity


class PlagiarismDetector(object):
    LINE_LENGHT = 80

    def preprocess(self, thesis_id):
        pass
        # get data from db
        # get keyword
        # start processing in by neares keyword
    def __winnowing(self, thesis1, thesis2):
        """ Function that return by characters similarity in text
            :param thesis1 - text
            :param thesis2  - text
            :returns list of touple (index1, index2)
        """

        winnows1 = winnow(thesis1)
        winnows2 = winnow(thesis2)
        result = []
        for index in winnows1.keys():
            if winnows1[index] in winnows2.values():
                second_index = list(winnows2.keys())[list(winnows2.values()).index(dict(winnows1)[index])]
                result.append((index, second_index))
        return result

    @db_session
    def process(self, toCheck):
        thesis = Thesis.select(lambda ti: ti.id != toCheck['id'])[:]
        result = {'thesis_id': toCheck['id']}
        thesisToAnalyze = []
        for thesi in thesis:
            thesi = thesi.to_dict(with_collections=True, related_objects=True)
            # if calculate_keywords_similarity(thesi['keywords'], toCheck['keywords']) > 0.3:
            thesisToAnalyze.append(thesis)

        for thesi in thesisTcoAnalyze:
            winnowing_result = self.__winnowing(toCheck['text', thesi['text']])
            similarity = Similarity(thesis1=toCheck['id'],
                                    thesis2=thesi['id'],
                                    keywordSimilarity=calculate_keywords_similarity(toCheck['keywords'], thesi['keywords']),
                                    percentageSimilarity = (len(winnowing_result) * 5) / len(thesis1['text']),
                                    similarWords = len(winnowing_result))
            for i in range(0, len(result) - 1, 1):
                similarity.linesWord.append(LinesWords(thesis1CharStart=winnowing_result[i][0],
                                        thesis1CharEnd=winnowing_result[i + 1][0],
                                        thesis2CharStart=winnowing_result[i][1],
                                        thesis2CharEnd=winnowing_result[i + 1][1]))


        return result



