#!/usr/bin/python3

##################################################
#
# pydict - a unix command line tool.
# written by Mohsin Tariq (mohsin.tariq10@gmail.com)
#
##################################################


from textblob import TextBlob
import urllib,urllib2,argparse
import StringIO

SEARCH_URL = "http://words.bighugelabs.com/api/2/614c64e055d7bb781e843d8a6f58b51d/{}/"

#lists of parts of speech
tagadverb = ("RB","RBR","RBS")
tagverb = ("VBD","VB","VBG","VBN")
tagadjective = ("JJR","JJS")
tagignore = ("JJ","CC","NN","NNS","CD","DT","EX","FW","VBZ","MD","NNP","NNPS","LS","IN","POS","PRP","PRP$","RP","SYM","TO","UH","WDT","WP","WP$","WRB","VBP","VBZ")

def argparsing(parser):
    parser.add_argument("--verbose","-v",action="store_true",help="increase output verbosity", default="false")
    parser.add_argument("source",help = "source file",type = str)
    parser.add_argument("dest",help = "destination file", type = str)

def getresult(url):
    print url
    result = urllib.urlopen(url)
    return StringIO.StringIO(result.read())

def alternativeword(word , webpage):
    newword = ""
    for content in webpage:
        if content != "":
            pos = content.split("|")
        if word in tagadverb:
            if pos[0] == "adverb":
                newword = pos[2]
                break
        elif word in tagverb:
            if pos[0] == "verb":
                newword = pos[2]
                break
        elif word in tagadjective:
            if pos[0] == "adjective":
                newword = pos[2]
                break
    return newword.strip()


def main():
    #parsing arguments
    parser = argparse.ArgumentParser(description="A simple script that make some changes to the text of a file and add some zinger words in it.")
    argparsing(parser)
    arg = parser.parse_args()

    newline = []

    sourcefile = open(arg.source, 'r')
    destfile = open(arg.dest, 'w')

    for line in sourcefile:
        blob = TextBlob(line)
        words = blob.tags
        for word in words:
            newword = word[0]
            try:
                if word[1] not in tagignore:
                    url = SEARCH_URL.format(urllib.quote(word[0]))
                    webpage = getresult(url)
                    result = alternativeword(word[1],webpage)
                    if result != "":
                        newword = result
                    if arg.verbose:
                        print("\"{}\" replaced with \"{}\"".format(word[0],newword))
            except IndexError:
                pass
            newline.append(newword)
    destfile.write(" ".join(newline))

if __name__ == "__main__":
    main()
