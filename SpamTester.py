'''
Created on Nov 8, 2014

@author: Rasel
'''

import os
import re
import unicodedata
import math
from stemming.porter2 import stem

'database' 
dbase={}

'class for storing the records'
class record:
    hProb = 0.0
    sProb = 0.0
    
    def setHProb(self,prob):
        self.hProb = prob
        
    def gethProb(self):
        return self.hProb
        
    def setsProb(self,prob):
        self.sProb = prob
    
    def getsProb(self):
        return self.sProb

'Gets all the files in a specific directory'
def getFilePaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  
    return file_paths

'reads a file'    
def readFile(FilePath):
    return open(FilePath, "rb").read()
   
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

'Removes useless characters from an input file'
def removeLetters(line):
    return re.sub(r'\ba\b|\bb\b|\bc\b|\bd\b|\be\b|\bf\b|\bg\b|\bh\b|\bi\b|\bj\b|\bk\b|\bl\b|\bm\b|\bn\b|\bo\b|\bp\b|\bq\b|\br\b|\bs\b|\bt\b|\bu\b|\bv\b|\bw\b|\bx\b|\by\b|\bz\b|','',line)

'Removes all non Ascii characters from an input file'
def removeNonAscii(line):
    return str(unicodedata.normalize('NFKD', line).encode('ascii','ignore'))

'Cleans a text for training'

def cleanText(text):
    s = removeNonAscii(text)
    s = str.lower(s)
    s = removeEmail(s)
    s = removeLink(s)
    s = removeNumbers(s)
    s = removeSpecialChars(s)
    s = removeLetters(s)
    return s   
   
 

'Loads the model into the database'
def loadModel():
    dPath = input("Enter Model Path\n")
    dic = open(dPath)
    line = dic.read().splitlines()
    for l in line:
        words = l.split()
        word = words[1]
        hprob = float(words[3])
        sprob = float(words[5])
        #print(word+" "+str(hprob)+" "+str(sprob))
        if word not in dbase:
            rec = record()
            rec.setHProb(hprob)
            rec.setsProb(sprob)
            dbase[word] = rec

'tests the data and stores in the output file'
def testData():
    dir = input("Enter test Directory\n")
    disList = getFilePaths(dir)
    output = open("result.txt","a")
    i=1
    for temp in disList :
        spam = 0
        ham = 0
        text = cleanText( str(readFile(temp)))
        #print(temp)
        for word in text.split():
            word = word.strip()
            #word = stem(word)
            if word in dbase :
                ham += math.log10(dbase[word].gethProb())
                spam += math.log10(dbase[word].getsProb())
        if ham > spam:
            output.write(str(i)+"   "+temp.split('\\')[-1]+"   "+"Ham   "+str(ham)+"   "+str(spam)+"\n")
            
        else:
            output.write(str(i)+"   "+temp.split('\\')[-1]+"   "+"Spam   "+str(ham)+"   "+str(spam)+"\n")
        i +=1      
    output.close()

'Generates the sorted results in a text file'    

#F:\WorkSpace\SpamFilter\test\model.txt
#F:\WorkSpace\SpamFilter\test\testCase_ham
#F:\WorkSpace\SpamFilter\test\testCase_spam
'main sequence of the operation'        
def main():
    loadModel()
    print("Model Loaded...")
    testData()
    print("Result stored")
 
   

'Entry point of the program' 
if __name__ == '__main__':
    main()
