#!/usr/bin/python

import sys, re

TEXTID = re.compile(r'<text id="(.*)">')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'One argument required: a pl196x corpus to split.'
        sys.exit()

    inputFileName = sys.argv[1]

    inputFile = open(inputFileName, 'r')
    input = inputFile.read()
    inputFile.close()

    input = input.decode('utf-8').splitlines()

    header = ""

    inHeader = True
    for line in input:
        if inHeader:
            if line.find('<text lang="pl">') >= 0:
                pass
            elif line.find('<group>') >= 0:
                pass
                header = header
                inHeader = False
            else:
                header += line + '\n'
        else:
            if line.find('<text') >= 0:
                outputFileName = TEXTID.search(line).group(1)
                outputFile = open(outputFileName, 'w')
                outputFile.write(header.encode('utf-8'))
                outputFile.write('<text lang="pl" id="'+outputFileName+'">"\n')
            elif line.find('</text>') >= 0:
                outputFile.write(line[5: ].encode('utf-8')+'\n')
                outputFile.write('</TEI.2>\n')
                outputFile.close()
            elif line.find("</group>") >= 0:
                break
            elif len(line) == 0:
                pass
            else:
                outputFile.write(line[5: ].encode('utf-8')+'\n')

