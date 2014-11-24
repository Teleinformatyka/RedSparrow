def calculate(text, pattern):
    """Naive algorythm implementation"""
    if text == None or pattern == None:
        return -1
    if text == "" or pattern == "":
        return -2
    if len(pattern) > len(text):
        return -3
    result = []

    for i in range(len(text)-len(pattern)+1):   # all possible positions in text
        match = 1
        for j in range(len(pattern)):           # all positions in pattern
            if (text[i+j] != pattern[j]):
                match = 0                       # mis-match
        if (match == 1):
            result = result + [i]
	    i = i+len(pattern)            

    return result

