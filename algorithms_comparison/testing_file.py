import redsparrow.plagiarism.levenshtein as Levenshtein
import redsparrow.plagiarism.rabinkarb as RabinKarb
import redsparrow.plagiarism.naive as Naive


with open("data.txt", "r") as myfile:
        data = myfile.read().replace('\n', '')
myfile.closed
with open("data1.txt", "r") as myfile2:
        data1 = myfile2.read().replace('\n', '')
myfile2.closed
# print Naive.calculate(data, data1)
# print Naive.calculate(data, "aplikacji miejsca")
# print Naive.calculate("ada ma kota, kot ma ade a ada ma kota, ktorego ada ma kota", "ada kota")
# print RabinKarb.calculate("ada ma kota, kot ma ade a ada ma kota, ktorego ada ma kota", "ada kota", 257, 13)
# print RabinKarb.calculate(data, "aplikacji miejsca", 257, 13)
# print Levenshtein.distance("ada ma kota", "ada ma kota, kot ma ade a ada ma kota, ktorego ada kota")
# print Levenshtein.distance("ada ma kota, kot ma ade a ada ma kota, ktorego ada ma kota", "ada kota")
# print Levenshtein.distance(data, "aplikacji miejsca")
# print RabinKarb.calculate(data, data1, 257, 13)
# print Levenshtein.distance(data, data1)
print Levenshtein.distance("aaa aaa bb aaa aaa bc aaa aaa bb aaa aa","bb aaa aaa")
print Naive.calculate("aaa aaa bb aaa aaa bc aaa aaa bb aaa aa", "bb aaa aaa")
print RabinKarb.calculate("aaa aaa bb aaa aaa bc aaa aaa bb aaa aa", "bb aaa aaa", 257, 13)
