
from pony.orm import db_session, commit, flush

from redsparrow.orm import Thesis, Similarity, LinesWords
import redsparrow.plagiarism.levenshtein as Levenshtein
import redsparrow.plagiarism.rabinkarb as   RabinKarb
from redsparrow.extractor.winnowing import winnow
from redsparrow.keywords import calculate_keywords_similarity


class PlagiarismDetector(object):
    LINE_LENGHT = 80

    def preprocess(self, thesis_id):
        pass
        # get data from db
        # get keyword
        # start processing in by neares keyword
    def winnowing(self, thesis1, thesis2, window=15):
        """ Function that return by characters similarity in text
            :param thesis1 - text
            :param thesis2  - text
            :returns list of touple (index1, index2)
        """

        winnows1 = winnow(thesis1, window)
        winnows2 = winnow(thesis2, window)
        result = []
        for index in winnows1.keys():
            if winnows1[index] in winnows2.values():
                second_index = list(winnows2.keys())[list(winnows2.values()).index(dict(winnows1)[index])]
                result.append((index, second_index))
        return result

    def calculate_percentageSimilarity(self, winnowing_result, text_len):
        if len(winnowing_result) == 1:
            return 0
        winnowing_result = sorted(winnowing_result, key=lambda x: x[1], reverse=True)
        result = 0
        for i in range(0, len(winnowing_result) - 1, 1):
            result += winnowing_result[i][1] -  winnowing_result[i + 1][1]

        result = result /text_len
        return int(result * 100)
    def __calculate_keywords_similarity(self, kerwords1, kerwords2):
        list_key1 = [ key.keyword for key in kerwords1]
        list_key2 = [ key.keyword for key in kerwords2]
        return int(calculate_keywords_similarity(list_key1, list_key2) * 100)

    @db_session
    def process(self, id_toCheck):
        toCheck = Thesis.select(lambda ti: ti.id != id_toCheck)[:][0]
        thesis = Thesis.select(lambda ti: ti.id != toCheck.id)[:]
        result = {'thesis_id': toCheck.id, 'similarity': []}
        thesisToAnalyze = []
        # for thesi in thesis:
        #     thesi = thesi.to_dict(with_collections=True, related_objects=True)
        #     # if calculate_keywords_similarity(thesi['keywords'], toCheck['keywords']) > 0.3:
        #     thesisToAnalyze.append(thesi)

        for thesi in thesis:
            # with db_session:
            winnowing_result = self.winnowing(toCheck.text, thesi.text)
            lines = []
            percentageSimilarity = self.calculate_percentageSimilarity(winnowing_result, len(thesi.text))
            print(percentageSimilarity)
            similarity = Similarity(thesis1=toCheck.id,
                                    thesis2=thesi.id,
                                    keywordSimilarity=self.__calculate_keywords_similarity(toCheck.keywords, thesi.keywords),
                                    percentageSimilarity=percentageSimilarity)
            commit()
            # with db_session:
            if percentageSimilarity > 90:
                winnowing_result = [(0, 0), (int(0.9 *  len(toCheck.text)), int(0.9 * len(thesi.text)))]
            for i in range(0, len(winnowing_result) - 1, 1):
                index1Start = winnowing_result[i][0]
                if index1Start > winnowing_result[i + 1][0]:
                    index1Start = winnowing_result[i + 1][0]
                    index1End = winnowing_result[i][0]
                else:
                    index1End = winnowing_result[i + 1][0]


                index2Start = winnowing_result[i][1]
                if index2Start > winnowing_result[i + 1][1]:
                    index2Start = winnowing_result[i + 1][1]
                    index2End = winnowing_result[i][1]
                else:
                    index2End = winnowing_result[i + 1][1]

                linesWord = LinesWords(thesis1CharStart=index1Start,
                                        thesis1CharEnd=index1End,
                                        thesis2CharStart=index2Start,
                                        thesis2CharEnd=index2End,
                                        similarity = similarity)
                similarity.linesWords.add(linesWord)
                lines.append(linesWord.to_dict())
                commit()
            result['similarity'].append({
                'thesis': similarity.thesis1.id,
                'thesis2': similarity.thesis2.id,
                'linesword': lines,
                'keywordSimilarity': similarity.keywordSimilarity,
                'percentageSimilarity': similarity.percentageSimilarity,
                            })


        return result



