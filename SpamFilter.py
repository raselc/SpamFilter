'''
Created on Oct 20, 2014

@author: Rasel
'''
import os
import re
import collections
import unicodedata
import math
from decimal import Decimal
from decimal import ROUND_DOWN
#from stemming.porter2 import stem

'Global Declaration'

englishDictionary ={}
dbase={}
totalHam = 0
totalSpam =0

'Class holds the word, ham count and spam count'
class record:
    word = ''
    hCount = 0
    sCount = 0
    
    def setWord(self,word):
        self.word = word
        
    def getWord(self):
        return self.word
       
    def sethCount(self):
        self.hCount += 1
        
    def gethCount(self):
        return self.hCount
        
    def setsCount(self):
        self.sCount += 1
    
    def getsCount(self):
        return self.sCount
    
    def reset(self):
        self.hCount = 0
        self.sCount =0
        self.word = ''

'Stores english words list for filtering useless words from the texts'
def installDictionary():
    dPath = input("Enter Dictionary Path\n")
    dic = readFile(dPath)
    for word in dic.split():
        if word not in englishDictionary:
            englishDictionary[word.strip()] =" "

'Gets all the files in a specific directory'
def getFilePaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  
    return file_paths  

'Reads the contents of a file'
def readFile(FilePath):
    return open(FilePath, 'r').read()

'Removes email address from an input file using regular expression'
def removeEmail(line):
    return re.sub(r'[\w\.-]+@[\w\.-]+',' ', line)

'Removes web links from an input file'
def removeLink(line):
    return re.sub(r'https?://[^\s<>"]+|www\.[^\s<>"]+',' ', line)

'Removes punctuations and other special characters from an input file'
def removeSpecialChars(line):
    return re.sub("[`\~\!\@\#\$\%\^\&\*\(\)\'\_\-\+\=\[\]\\\{\}\|\;\:\"\,\.\/\<\>\?]",' ',line)  
           
'Removes numbers from an input file'
def removeNumbers(line):
    return re.sub("[0123456789]",' ', line)

'Removes some stop words from an input file'
def removeStopWords(line):
    return re.sub(r'\bam\b|\bis\b|\bare\b|\bwere\b|\bi\b|\bof\b|\bthe\b|\bto\b|\bfrom\b|\band\b', ' ', line)

'Removes useless characters from an input file'
def removeLetters(line):
    return re.sub(r'\ba\b|\bb\b|\bc\b|\bd\b|\be\b|\bf\b|\bg\b|\bh\b|\bi\b|\bj\b|\bk\b|\bl\b|\bm\b|\bn\b|\bo\b|\bp\b|\bq\b|\br\b|\bs\b|\bt\b|\bu\b|\bv\b|\bw\b|\bx\b|\by\b|\bz\b|','',line)

'Removes all non Ascii characters from an input file'
def removeNonAscii(line):
    return str(unicodedata.normalize('NFKD', line).encode('ascii','ignore'))

'Cleans a text for training'
def cleanText(text):
    s = str.lower(text)
    s = removeEmail(s)
    s = removeLink(s)
    s = removeNonAscii(s)
    s = removeNumbers(s)
    s = removeSpecialChars(s)
    s = removeLetters(s)
    s = removeStopWords(s)
    return s

'Calculates the probability of ham words'
def calHam(inp):
    return Decimal(str(math.log10((inp + 0.5)/(totalHam + (0.5 * len(dbase)))))).quantize(Decimal('.0000001'), rounding=ROUND_DOWN)

'Calculates the probability of spam words'
def calSpam(inp):
    return Decimal(str(math.log10((inp + 0.5)/(totalSpam+(0.5 * len(dbase)))))).quantize(Decimal('.0000001'), rounding=ROUND_DOWN)

'Counts the number of spam words, if the word not in the dbase inserts it'
def spamCounter(text):
    global totalSpam
    for word in text.split():
        rec = record()
        if word not in dbase:
            rec.setWord(word)
            rec.setsCount()
            dbase[word] = rec
            totalSpam +=1
        else:
            dbase[word].setsCount()
        totalSpam +=1
'''        if word.strip() in englishDictionary :
            if word not in dbase:
                rec.setWord(word)
                rec.setsCount()
                dbase[word] = rec
                totalSpam +=1
            else:
                dbase[word].setsCount()
            totalSpam +=1 '''
        

'Counts the number of ham words, if the word not in the dbase inserts it'
def hamCounter(text):
    global totalHam
    for word in text.split():
        rec = record()
        if word.strip() in englishDictionary :
            if word.strip() not in dbase:
                rec.setWord(word.strip())
                rec.sethCount()
                dbase[word] = rec
                totalHam +=1
            else:
                dbase[word].sethCount()
            totalHam +=1

'Reads the directory path, and does readfile, cleanText and spam counter for spam dataset'
def spamTrainer():
    spamPath = input("Enter spam directory:\n")
    fileList = getFilePaths(spamPath)
    for i in range(0,1000):
        text = readFile(fileList[i])
        text = cleanText(text)
        spamCounter(text)   

'Reads the directory path, and does readfile, cleanText and ham counter for ham dataset'
def hamTrainer():
    hamPath = input("Enter ham directory:\n")
    fileList = getFilePaths(hamPath)
    for i in range(0,1000):
        text = readFile(fileList[i])
        text = cleanText(text)
        hamCounter(text)

'Generates the sorted results in a text file'    
def printResult():
    sortedValue = collections.OrderedDict(sorted(dbase.items()))
    f = open('model.txt', 'w')
    #f = open('F:/WorkSpace/SpamFilter/test/workfile2.txt', 'r+')
    f.write("Total unique Word:"+str(len(dbase))+"\n")
    f.write("Total Ham:"+str(totalHam)+"\n")
    f.write("Total Spam:"+str(totalSpam)+"\n")
    i=1
    for k,v in sortedValue.items():
        f.write(str(i)+"   "+v.getWord()+"   "+str(v.gethCount())+"   "+str(calHam(v.gethCount()))+"   "+str(v.getsCount())+"   "+str(calSpam(v.getsCount()))+"\n")
        i+=1
    f.close

#F:\WorkSpace\SpamFilter\easy_ham_2
#F:\WorkSpace\SpamFilter\spam_2
#F:\WorkSpace\SpamFilter\test\dictionary.txt

'main sequence of the operation'        
def main():
    installDictionary()
    print("Dictionary Loaded...")
    print(len(englishDictionary))
    hamTrainer()
    print("Ham training Done")
    spamTrainer()
    print("Spam training Done")
    printResult()
    print("Result stored")

'Entry point of the program' 
if __name__ == '__main__':
    main()

