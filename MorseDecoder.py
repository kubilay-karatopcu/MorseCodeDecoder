from itertools import combinations
import json
import winsound
from MorseSoundMaker import MorseSoundMaker

class MorseDecoder:
    """
    This class is used for several utilities about Morse code such as
    translation between Latin and Morse,  translation from latin to MorseCode
    sound, and translation from MorseCode where words are seperate but letters
    are indistincive.

    """
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

        self.MORSE_CODE_DICT = {v: k for k, v in self.MORSE_CODE_DICT_LATIN.items()} #Morse to Latin dictionary
        with open("wordlistEnglish.txt","r") as f:
            self.wordlist = f.read().splitlines()

        self.WORDLIST = [word.upper() for word in self.wordlist] #Upper case English world list
        self.MorseSoundMaker = MorseSoundMaker() #Init class translating Latin to Morse Sound.

    def morsCodeCombs(self, word):
        """
        This method finds all MorseCode combinations in a word given that
        letters are not seperate and indistincive.
        Parameters
        ----------
        word : str
            The word that is needed to be translated.
        Returns
        -------
        dictionary
            a dictionary of all combinations with different word lenghts where
            indexes are the lenghts.
        """
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
        """
        This class translates the word's dictionary given by the morsCodeCombs
        into Latin.
        Parameters
        ----------
        word : str
            The word that is needed to be translated.
        Returns
        -------
        list
            All possible words which is meaningful or not in Latin.
        """
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
        """
        This class compares the words list given by the possibleTranslations
        with self.WORDLIST which contains 466k English worlds in order to query
        meaningful words.
        Parameters
        ----------
        word : str
            The word that is needed to be translated.
        Returns
        -------
        list
            All possible meaningful words in Latin.
        """
        allTranslations = self.possibleTranslations(word)
        meaningfulTranslationList = []
        for trans in allTranslations:
            if trans in self.WORDLIST:
                meaningfulTranslationList.append(trans)
        return meaningfulTranslationList

    def translateSentence(self, sentence, type = "LatinToMorse", words = "Distinctive"):
        """
        This is the master method which makes the translation between Latin and
        Morse.
        Parameters
        ----------
        sentence : str
            The sentence that is needed to be translated.
        type : str -> ['LatinToMorse','MorseToLatin']
            Translation type.
            If the translation "type" is "LatinToMorse" then the sentence must be given
            in the form of space seperated words.
            If the translation "type" is "MorseToLatin" then the sentence must be given
            in the form where letters are seperated with spaces and the words are
            seperated with "/"
        words : str -> ['Distinctive','Indistinctive']
            It shows whether letters are seperated and known or the words are
            seperated but  the letters are not known.
            It is needed to be defined if translation type is MorseToLatin.
            If "words" is "Distinctive" then the sentence must be given in the
            form where letters are seperated with spaces and the words are
            seperated with "/"
            If "words" is "Indistinctive" then the sentence must be given in the
            form where words are seperated with "/" but letters are joint.
        Returns
        -------
        type = LatinToMorse
            str
                Translation in Morse. The sentence is in the form where letters
                are seperated with spaces and the words are seperated with "/"
        type = MorseToLatin & words = Distinctive
            str
                Translation in Latin. Regular English sentence.
        type = MorseToLatin & words = Indistinctive
            dictionary
                A dictionary where keys are the words in Morse, and values are
                all possible meaningful translations in Latin.
        """
        if type == "LatinToMorse":
            sentence = sentence.upper()
            words = sentence.split(" ")
            translation = ""
            for word in words:
                cur_translation = ""
                for letter in word:
                    cur_translation += self.MORSE_CODE_DICT_LATIN[letter]
                    cur_translation += " "
                translation += cur_translation[:-1]
                translation += "/"
            return translation[:-1]
        elif type == "MorseToLatin":
            if words == "Distinctive":
                words = sentence.split("/")
                translation = ""
                for word in words:
                    cur_translation = ""
                    letters = word.split(" ")
                    for letter in letters:
                        cur_translation += self.MORSE_CODE_DICT[letter]
                    translation += cur_translation
                    translation += " "
                return(translation[:-1])
            elif words == "Indistinctive":
                print(sentence)
                words = sentence.split("/")
                translations = {i: self.meaningfulTranslations(i) for i in words}
                return(json.dumps(translations,indent = 2))
            else:
                raise Exception("You have to indicate words' situation ['Distinctive','Indistinctive']")
        else:
            raise Exception("You have to indicate translation type ['LatinToMorse','MorseToLatin']")

    def createMorseCodeSound(self, sentence, filepath = "morseCode.wav"):
        """
        This method creates a .wav file of Morse from a Latin word.
        Parameters
        ----------
        sentence : str
            Regular English sentence which is seperated with spaces.
        filepath : str
            File path where the .wav will be saved.
        Returns
        -------
        """
        morseCode = self.translateSentence(sentence, type= "LatinToMorse")

        if filepath[-4:] != ".wav":
            filepath += ".wav"
        self.MorseSoundMaker.makeSound(morseCode, filepath)


morseDecoder = MorseDecoder()
sentence = "I am Kubilay"
print(morseDecoder.translateSentence(sentence, type = "LatinToMorse"))
IamKubilay = morseDecoder.translateSentence(sentence, type = "LatinToMorse")
print(morseDecoder.translateSentence(IamKubilay, type = "MorseToLatin", words = "Distinctive"))
print(sentence.upper() == morseDecoder.translateSentence(IamKubilay, type = "MorseToLatin", words = "Distinctive"))
print(morseDecoder.translateSentence("../.---", type = "MorseToLatin",words = "Indistinctive"))
morseDecoder.createMorseCodeSound(sentence,filepath = "IamKubilay.wav")
