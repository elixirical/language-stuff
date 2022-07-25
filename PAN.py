from dataclasses import dataclass, fields
from pprint import pprint

TESTVERBS = ['omaẓi','adaha']#,'an','ace','ažik','ahi']
TESTNOUNS = [['lakac','a'],['oh','o'],['oraš','c'],['eyana','d']]

# Makes a clean string for languages.py->GUI.py
def verbPrettifier(verb,detail):
    whitespaceMax = 20
    modalities = ["indicative","imperative",
                  "prohibitive","imperative-prohibitive",
                  "hypothetical","negative-hypothetical"]
    numbers = ["singular ","dual ","plural "]
    tenses = ["present\n","past\n","future\n"]
    toReturn = ""
    verbC = conjugateVerb(verb)
    if detail == 1:
        n=0
        for field in fields(verbC):
            if str(field.name) == "inf":
                toReturn=verbC.inf+whiteSpace(whitespaceMax,verbC.inf)+"infinitive\n"
            else:
                for x in range(3):      # number
                    for y in range(3):  # tense
                        toReturn = (toReturn+
                                    getattr(verbC,field.name)[(x*3)+y]+
                                    whiteSpace(whitespaceMax,
                                               getattr(verbC,field.name)[(x*3)+y])+
                                    modalities[n]+
                                    " "+
                                    numbers[x]+
                                    tenses[y])
                n+=1
    else:
        for field in fields(verbC):
            if str(field.name) == "inf":
                toReturn=verbC.inf+"\n"
            else:
                for x in range(3):      # number
                    for y in range(3):  # tense
                        toReturn = toReturn+getattr(verbC,field.name)[(x*3)+y]+"\n"
    return(toReturn)

# Calculates the amount of webspace to add in Prettifier
def whiteSpace(maxSpace, word):
    toReturn = ""
    for x in range(len(word), maxSpace):
        toReturn = toReturn+" "
    return(toReturn)

# Generates a VerbConjugations dataclas with all modalities + the infinitive
def conjugateVerb(verb):
    splitVerb = detectVerbStem(verb)
    template = {}
    a = []
    if splitVerb[1] == 'a':
        template = ASTEM
    elif splitVerb[1] == 'o':
        template = OSTEM
    a.append(moodlessConj(template,splitVerb[0]))
    for mood in V_INCOMPATIBLE:
        a.append(modalConjGeneral(a[0], V_INCOMPATIBLE[mood]))
    return VerbConjugations(verb,a[0],a[1],a[2],a[3],a[4],a[5])

# This does default moodless, aorist in all tenses
def moodlessConj(stemTemp, root):
    z = []
    for number in stemTemp:
        for inflection in stemTemp[number]:
            z.append(inflection+root)
    return(z)

# Applies modal prefixes to indicative conjugations from moodlessConj()
def modalConjGeneral(indList, rules):
    z = []
    copy = indList
    for n in copy:
        ffs = False
        toConjugate = n
        for x in range(1,len(rules)):
            if toConjugate.startswith(rules[x][0]):
                toConjugate = rules[x][1]+toConjugate[len(rules[x][0]):]
                ffs = True
                break
        if not ffs:
            toConjugate = rules[0]+n
        z.append(toConjugate)
    return(z)

# splits verb into stem+root
def detectVerbStem(word):
    if word[0] in ['a','o']:
        return([word[1:],word[0]])   #returns the word without the stem, and the stem
    else: return(['','x'])            #returns nothing, and x for invalid

@dataclass
class VerbConjugations:
    inf: str
    indicative: list #sg du pl
    imperative: list
    prohibitive: list
    impprohib: list
    hypothetical: list
    neghypo: list

#def nounPrettifier(nounDeclensions,detail):
def nounPrettifier(nounAndClass,detail):
    noun=nounAndClass.split(" ")
    whitespaceMax = 20
    cases = [' intransitive\n', ' ergative\n',' accusative\n', ' dative\n',
             ' genitive\n', ' locative\n', ' vocative\n']
    nounD = nounDecliner(noun[0],noun[1])
    toReturn = ''
    if detail == 1:
        n = 0
        for field in fields(nounD):
            toReturn = toReturn+getattr(nounD,field.name)+whiteSpace(whitespaceMax,getattr(nounD,field.name))+cases[n]
            n += 1
    else:
        for field in fields(nounD):
            toReturn = toReturn+getattr(nounD,field.name)+"\n"
    return(toReturn)

def nounDecliner(noun,nounClass):
    if nounClass == 'a':
        return(nounClassInflector(noun,ANIMAL))
    elif nounClass == 'o':
        return(nounClassInflector(noun,OBJECT))
    elif nounClass == 'c':
        return(nounClassInflector(noun,CONCEPT))
    elif nounClass == 'd':
        return(nounClassInflector(noun,DIVINE))

# actually applies the inflections
def nounClassInflector(noun,classRules):
    temp = []
    root = noun
    print(noun[-1])
    if noun[-1] in ["a","o","i","e","é","ó","á","í"]:
        root = noun[0:-1]
    temp.append(noun)
    for x in classRules:
        temp.append(root+x)
    return(NounDeclensions(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6]))

@dataclass
class NounDeclensions:
    intransitive: str
    ergative: str
    accusative: str
    dative: str
    genitive: str
    locative: str
    vocative: str

IRREGVERB = []
IRREGNOUN = []

# Verb conjugations  present past   future
OSTEM = {"singular":['ge',   'a',   'šara'],
         "dual":    ['e',    'a',   'šara'],
         "plural":  ['θe',   'θa',  'šara']}
ASTEM = {"singular":['go',   'ga',  'šaro'],
         "dual":    ['ho',   'ha',  'šaho'],
         "plural":  ['yo',   'ya',  'šayo']}

# incompatible modality-verb phoneme pairings ... [MOD,Verb,replacement]
V_INCOMPATIBLE = { "imperative":  [ 'k', ['g','k'],['h','k'] ],           # k  + X -> Y
                   "prohibitive": [ 'n', ['θ','n'] ],                     # n  + X -> Y
                   "impprohib":   [ 't', ['h','θ'],['θ','t'] ],           # t  + X -> Y
                   "hypothetical":[ 's', ['h','s'],['š','s'] ],           # s  + X -> Y
                   "neghypo":     [ 'ẓ', ['h','ẓ'],['θ','ẓ'],['š','θ'] ]} # cc + X -> Y

# Noun declensions
#          ergative accusative dative genitive locative vocative
ANIMAL  = ['is',    'a',       'o',   'ta',    'iža',  'om']
OBJECT  = ['i',     'a',       'o',   'ata',   'až',   'ana']
CONCEPT = ['i',     'an',      'on',  'ina',   'iẓa',  'om']
DIVINE  = ['is',    'aš',      'onya','ina',   'iθa', 'aža']
