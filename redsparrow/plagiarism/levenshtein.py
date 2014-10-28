""" Module for calculate lavenshtein_distance"""
import Levenshtein

def distance(string1, string2):
    """
    Function returns levenshtein distance
    :param string1 first string2
    :param string2 second string
    """
    return Levenshtein.distance(string1, string2)
