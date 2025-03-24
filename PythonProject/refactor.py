import re

def normalize_text(text):
# Text into variable
    text = text.lower()
# Replace "iz" to "is", if "iz" is not in quotes
    text = re.sub(r'(?<![“"])iz(?![”"])', 'is', text)
# Split text to sentences
    sentences = re.split(r'([.!?])', text)
    return sentences

def create_last_sentence(sentences):
    words = []
    for i in range(len(sentences)):
        sentences[i] = sentences[i].strip().capitalize() #capitalize every sentence
        word = sentences[i].split() # Split every sentence to words
    # print(word[-1])
        if not word:
            continue
        if word[-1] != '.':
            words.append(word[-1]) # Take last word from every sentence and add into separate sentence
    text = ' '.join(sentences)
    return text + (' '.join(words).capitalize())

def calc_space(text):
    whitespace_count = len(re.findall(r'\s', text))
    return whitespace_count

txt = '''tHis iz your homeWork, copy these Text to variable.\n\n
    You NEED TO normalize it fROM letter CASEs point oF View. also, 
    create one MORE senTENCE witH LAST WoRDS of each existING SENtence 
    and add it to the END OF this Paragraph.\n\n
    it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.\n\n
    last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, 
    not only Spaces, but ALL whitespaces. I got 87.'''

res1 = normalize_text(txt)
res2 = create_last_sentence(res1)
res3 =  calc_space(res2)
print ('Number of whitespaces is ', res2)
