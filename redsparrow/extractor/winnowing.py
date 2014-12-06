import string
import hashlib
# sanitize

# sanitizedChars = "\n\r\t\ \f!()-[]{};:'\"\,<>./?@#$%^&*_~"

# def sanitize(removedChars):

#     def remove(s):
#         return ''.join(ch.lower() for ch in s if not ch in removedChars)
#     return remove

# sanitizedString = sanitize(sanitizedChars)

#-> usage
# test = "read this asdasdas,.,as;short text somethingr                 ead\"\"\"\::thisas\n././././,..,.,.'';';';';';'.,.,.,;l;';'1!!dasdasasshorttext'"
# print(sanitizedString(test))

#winnowing

# downcasing

# Winnowing by suminb => https://github.com/suminb/winnowing
import unittest

def sanitize(text):
    """Removes irrelevant features such as spaces and commas.
    :param text: A string of (index, character) tuples.
    """

    import re

    # NOTE: \p{L} or \p{Letter}: any kind of letter from any language.
    # http://www.regular-expressions.info/unicode.html
    p = re.compile(r'\w', re.UNICODE)

    def f(c):
        return p.match(c[1]) != None

    return list(filter(f, map(lambda x: (x[0], x[1].lower()), text)))


def kgrams(text, k=5):
    """Derives k-grams from text."""

    n = len(set(text))

    if n < k:
        yield text
    else:
        for i in range(n - k + 1):
            yield list(text)[i:i+k]

def default_hash(text):
 
    hs = hashlib.sha1(text.encode('utf-8'))
    hs = hs.hexdigest()[-4:]
    hs = int(hs, 16)

    return hs

hash_function = default_hash

def winnowing_hash(kgram):
    """
    :param kgram: e.g., [(0, 'a'), (2, 'd'), (3, 'o'), (5, 'r'), (6, 'u')]
    """
    kgram = list(zip(*kgram))
    len_kgram = len(kgram[1])
    # FIXME: What should we do when kgram is shorter than k?
    text = ''.join(kgram[1]) if len_kgram > 1 else ''
    hs = hash_function(text)

    # FIXME: What should we do when kgram is shorter than k?
    return (kgram[0][0] if len_kgram > 1 else -1, hs)

# def hash_text(kgram):
# 	kgram = list(zip(*kgram))
# 	len_kgram = len(kgram[1])
# 	text = ''.join(kgram[1]) if len_kgram > 1 else ''
# 	hs = hash_function(text)

# 	return hs

def select_min(window):
    """In each window select the minimum hash value. If there is more than one
    hash with the minimum value, select the rightmost occurrence. Now save all
    selected hashes as the fingerprints of the document.
    :param window: A list of (index, hash) tuples.
    """

    #print window, min(window, key=lambda x: x[1])

    return min(window, key=lambda x: x[1])


def winnow(text, k=5):
    n = len(text)

    text = zip(range(n), text)
    text = sanitize(text)


    hashes = [winnowing_hash(x) for x in kgrams(text, k)]
    windows = list(kgrams(hashes, 4))
    return set(map(select_min, windows))

def hash_text(text, k=5):
    n = len(text)

    text = zip(range(n), text)
    text = sanitize(text)

    hashes = [winnowing_hash(x) for x in kgrams(text, k=5)]
    
    return list(hashes)

# Specified a hash function. You may override this.

# class DefaultTestCase(unittest.TestCase):
#     def test_fingerprinting(self):
#         actual = winnow('A do run run run, a do run run')
#         expected = set([(5, 23942), (14, 2887), (2, 1966), (9, 23942), (20, 1966)])
#         self.assertEqual(actual, expected)

#     def test_custom_hash(self):
#         def hash_md5(text):
#             import hashlib

#             hs = hashlib.md5(text.encode('utf-8'))
#             hs = hs.hexdigest()
#             hs = int(hs, 16)

#             return hs

#         import winnowing

#         # Override the hash function
#         winnowing.hash_function = hash_md5

#         actual = winnowing.winnow('The cake was a lie')
#         expected = set([(9, 65919358278261454015134408903900174701),  (6, 10871086811686999948319704115083909333),   (5, 89272493548844644660374857453353035753),    (2, 119020521100057720362335995528842780418)])

#         self.assertEqual(actual, expected)

#         # Restore the hash function
#         winnowing.hash_function = winnowing.default_hash

# if __name__ == "__main__":
#     unittest.main()

# przykladowy = "intuition behind choosing the minimum hash is"

# przykladowy_winnow = przykladowy
# win = winnow(przykladowy_winnow)

# print("\nWYNIK WINNOWINGU: \n")
# print(list(win))

# lista_text = hash_text(przykladowy)
# print("\nHashe tekstu: \n")
# print(lista_text)


