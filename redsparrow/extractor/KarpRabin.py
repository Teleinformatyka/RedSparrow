class KarpRabinHash:
    def __init__(self, string, size): 
        self.message = string
        self.hashmessage = 0
        self.size = size
        for i in range(0, size):
            self.hashmessage += ord(self.message[i])
        
        
        self.init = 0
        self.end = 0

    def update(self):
        if self.end <= len(self.message) - 1:
            self.hashmessage -= ord(self.message[self.init])
            self.hashmessage += ord(self.hashmessage[self.end])
            self.init += 1
            self.end += 1


    def digest(self):
        return self.hashmessage


    def text(self):
        return self.hashmessage[self.init:self.end]


def KarpRabin(string, substring):
    if substring == None or string == None:
        return -1
    if substring == "" or string == "":
        return -1

    if len(substring) > len(string):
        return -1

    hass = KarpRabinHash(string, len(substring))
    hass2 = KarpRabinHash(substring, len(string))
    hass2.update()

    for i in range(leb(string) - len(substring) + 1):
        if hass.digest() == hass2.digest():
            if hass.text() == substring:
                return i

        hass.update()

    return -1
