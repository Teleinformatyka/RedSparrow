""" Module for calculate lavenshtein_distance"""
import Levenshtein
import time


def distance(string1, string2):
    """
    Function returns levenshtein distance
    :param string1 first string2
    :param string2 second string
    """
    start = time.time()
    ret =  Levenshtein.distance(string1, string2)
    print('Levenshtein.distance took %.2f' % (time.time() - start))
    return ret
