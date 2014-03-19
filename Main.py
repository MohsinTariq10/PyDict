from textblob import TextBlob
import urllib
import xpath
def main():
    toReplace = ("\n"," ",",",".","'","(",")")
    tagAd = ("RB","RBR","RBS")
    tagVB = ("VBD","VB","VBG","VBN")
    tagAD = ("JJ","JJR","JJS")
    newline = []
    tagignore = ("CC","NN","NNS","CD","DT","EX","FW","VBZ","MD","NNP","NNPS","LS","IN","POS","PRP","PRP$","RP","SYM","TO","UH","WDT","WP","WP$","WRB","VBP","VBZ")
    filename = open("/home/mohsin/Desktop/test.txt", 'r')
    dest = open("/home/mohsin/Desktop/result.txt", 'w')
    for line in filename:
        words = line.split(" ")
        for word in words:
            for one in toReplace:
                word = word.replace(one,"")
                newword = word
            tag = TextBlob(word)
            try:
                if tag.tags[0][1] not in tagignore:
                    #print(tag.tags[0][0])
                    webpage = urllib.urlopen("http://words.bighugelabs.com/api/2/614c64e055d7bb781e843d8a6f58b51d/{}/".format(word))
                    for content in webpage:
                        if content != "":
                            pos = content.split("|")
                        if tag.tags[0][1] in tagAd:
                            if pos[0] == "adverb":
                                newword = pos[2]
                                print(newword)
                                break
                        elif tag.tags[0][1] in tagVB:
                            if pos[0] == "verb":
                                newword = pos[2]
                                print(newword)
                                break
                        elif tag.tags[0][1] in tagAd:
                            if pos[0] == "adjective":
                                newword = pos[2]
                                print(newword)
                                break
                    #print(newword) 
                    webpage.close()            
            except IndexError:
                pass
            newline.append(newword)
    dest.write(" ".join(newline))
if __name__ == "__main__":
    main()