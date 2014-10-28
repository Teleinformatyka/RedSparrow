import string
# sanitize

sanitizedChars = "\n\r\t\ \f!()-[]{};:'\"\,<>./?@#$%^&*_~"

def sanitize(removedChars):

    def remove(s):
        return ''.join(ch.lower() for ch in s if not ch in removedChars)
    return remove

sanitizedString = sanitize(sanitizedChars)

#-> usage
# test = "read this asdasdas,.,as;short text somethingr                 ead\"\"\"\::thisas\n././././,..,.,.'';';';';';'.,.,.,;l;';'1!!dasdasasshorttext'"
# print(sanitizedString(test))

#winnowing

# downcasing
