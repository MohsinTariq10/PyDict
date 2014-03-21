from textblob import TextBlob
import urllib,argparse

def argparsing(parser):
    parser.add_argument("--verbose","-v",action="store_true",help="increase output verbosity", default="false")
    parser.add_argument("source",help = "source file",type = str)
    parser.add_argument("dest",help = "destination file", type = str)

def main():
    #parsing arguments
    parser = argparse.ArgumentParser(description="A simple script that make some changes to the text of a file and add some zinger words in it.")
    argparsing(parser)
    arg = parser.parse_args()

    #lists of parts of speech
    tagAd = ("RB","RBR","RBS")
    tagVB = ("VBD","VB","VBG","VBN")
    tagAD = ("JJ","JJR","JJS")
    tagignore = ("CC","NN","NNS","CD","DT","EX","FW","VBZ","MD","NNP","NNPS","LS","IN","POS","PRP","PRP$","RP","SYM","TO","UH","WDT","WP","WP$","WRB","VBP","VBZ")
    newline = []

    filename = open(arg.source, 'r')
    dest = open(arg.dest, 'w')

    for line in filename:
        blob = TextBlob(line)
        words = blob.tags
        for word in words:
            flag = False
            newword = word[0]
            try:
                if word[1] not in tagignore:
                    webpage = urllib.urlopen("http://words.bighugelabs.com/api/2/614c64e055d7bb781e843d8a6f58b51d/{}/".format(word[0]))
                    for content in webpage:
                        if content != "":
                            pos = content.split("|")
                        if word[1] in tagAd:
                            if pos[0] == "adverb":
                                flag = True
                                break
                        elif word[1] in tagVB:
                            if pos[0] == "verb":
                                flag = True
                                break
                        elif word[1] in tagAd:
                            if pos[0] == "adjective":
                                flag = True
                                break
                    webpage.close()
                    if flag:
                        newword = pos[2].strip()
                        if arg.verbose:
                            print("\"{}\" replaced with \"{}\"".format(word[0],newword))
            except IndexError:
                pass
            newline.append(newword)
    dest.write(" ".join(newline))
if __name__ == "__main__":
    main()
