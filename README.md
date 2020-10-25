# MorseCodeDecoder

This is a Morse code translator which can be used for several utilities about Morse code such as translation between Latin and Morse,  translation from Latin to its Morse code sound, and translation from Morse code where words are seperate but letters are indistincive in which script finds all meaningful words among all possible combinations where the definition of "meaningful" is provided by  a list of words in English. Words list is taken from dwyl/english-words as you may find in the following link https://github.com/dwyl/english-words

# How to use?


## translateSentence()

This is the master method which makes the translation between Latin and Morse.

### Parameters
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
        form where words are seperated with "/" but letters must be joint.
### Returns
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
## createMorseCodeSound()
        
   This method creates a .wav file of Morse from a Latin word.
### Parameters

    sentence : str
        Regular English sentence which is seperated with spaces.
    filepath : str
        File path where the .wav will be saved.
            See examples.py for furthermore.
