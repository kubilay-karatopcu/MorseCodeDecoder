from itertools import combinations
import json


class MorseDecoder:

    def __init__(self):
        self.MORSE_CODE_DICT_LATIN = { 'A':'.-', 'B':'-...',
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


        self.MORSE_CODE_DICT = {v: k for k, v in self.MORSE_CODE_DICT_LATIN.items()}
        with open("wordlistEnglish.txt","r") as f:
            self.wordlist = f.read().splitlines()

            self.WORDLIST = [word.upper() for word in self.wordlist]

    def morsCodeCombs(self, word):
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

    def possibleTranslations(self, word):
        morsDict = self.morsCodeCombs(word)
        allTranslations = []
        for index, word_list in morsDict.items():
            for word in word_list:
                curWordListed = word.split("/")
                curWordTranslated = ""
                flag = 0
                for elm in curWordListed:
                    try:
                        latinLetter = self.MORSE_CODE_DICT[elm]
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

    def meaningfulTranslations(self, word):
        print(word)
        allTranslations = self.possibleTranslations(word)
        meaningfulTranslationList = []
        for trans in allTranslations:
            if trans in self.WORDLIST:
                meaningfulTranslationList.append(trans)
        return meaningfulTranslationList

    def translateSentence(self, sentence, type = "LatinToMorse", words = "Distinctive"):
        if type == "LatinToMorse":
            words = sentence.split(" ")
            translation = ""
            for word in words:
                cur_translation = ""
                for letter in word:
                    cur_translation += self.MORSE_CODE_DICT[letter]
                translation += cur_translation
                translation += " "
            return translation[:-1]
        elif type == "MorseToLatin":
            if words == "Distinctive":
                words = sentence.split(" ")
                translation = ""
                for word in words:
                    cur_translation = ""
                    letters = word.split("/")
                    for letter in letters:
                        cur_translation += self.MORSE_CODE_DICT[letter]
                    translation += cur_translation
                    translation += " "
                return(translation[:-1])
            elif words == "Indistinctive":
                print(sentence)
                words = sentence.split(" ")
                translations = {i: self.meaningfulTranslations(i) for i in words}
                return(json.dumps(translations,indent = 2))
            else:
                raise Exception("You have to indicate words' situation ['Distinctive','Indistinctive']")
        else:
            raise Exception("You have to indicate translation type ['LatinToMorse','MorseToLatin']")


morseDecoder = MorseDecoder()
#sentence = ".. -...-...--- -.-----..- ....-..-.-.-- -...--.....- --........ -.-----..-.-. ...---..-.-.."
sentence = ".. -..-.."
morseDecoder.translateSentence(sentence,type = "MorseToLatin",words = "Indistinctive")
