from itertools import combinations
import json
MORSE_CODE_DICT_LATIN = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}


MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT_LATIN.items()}
with open("wordlistEnglish.txt","r") as f:
    wordlist = f.read().splitlines()

WORDLIST = [word.upper() for word in wordlist]

def morsCodeCombs(word):
    # .--..--
    allMorsCombs = {i: [] for i in range(0, len(word))}
    combs = {i: list(combinations(list(range(0,len(word))),i)) for i in range(0, len(word))}
    for index, positions in combs.items():
        for position in positions:

            temp_word = list(word)
            count = 0
            for elm in position:
                temp_word.insert(int(elm + count),"/")
                count += 1

            allMorsCombs[index].append("".join(temp_word))
    return(allMorsCombs)
                                                                                                                                                                                                                                                                                                                                                                                                                               

def possibleTranslations(word):
    morsDict = morsCodeCombs(word)
    allTranslations = []
    for index, word_list in morsDict.items():
        for word in word_list:
            curWordListed = word.split("/")
            curWordTranslated = ""
            flag = 0
            for elm in curWordListed:
                try:
                    latinLetter = MORSE_CODE_DICT[elm]
                    curWordTranslated += latinLetter
                except:
                    flag = 1
                    continue
            if flag == 1:
                flag = 0
                continue
            else:
                allTranslations.append(curWordTranslated)
    return allTranslations

def meaningfulTranslations(word):
    print(word)
    allTranslations = possibleTranslations(word)
    meaningfulTranslationList = []
    for trans in allTranslations:
        if trans in WORDLIST:
            meaningfulTranslationList.append(trans)
    return meaningfulTranslationList

def translateSentence(sentence):
    print(sentence)
    words = sentence.split(" ")
    translations = {i: meaningfulTranslations(i) for i in words}
    return translations

sentence = ".. -...-...--- -.-----..- ....-..-.-.-- -...--.....- --........ -.-----..-.-. ...---..-.-.."

print(json.dumps(translateSentence(sentence),indent = 2))
