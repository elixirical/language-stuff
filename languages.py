import PAN as PAN

def LangSorter(language, PoS, word, detail):
    if language == "Proto-North-Anfean":
        if PoS == 1: # noun
            return(PAN.nounPrettifier(word, detail))
        elif PoS == 2: # verb
            return(PAN.verbPrettifier(word, detail))
    else: return("Invalid entry")
