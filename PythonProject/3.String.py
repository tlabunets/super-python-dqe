import re
# text into variable
text = '''tHis iz your homeWork, copy these Text to variable.\n\n
You NEED TO normalize it fROM letter CASEs point oF View. also, 
create one MORE senTENCE witH LAST WoRDS of each existING SENtence 
and add it to the END OF this Paragraph.\n\n
it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.\n\n
last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, 
not only Spaces, but ALL whitespaces. I got 87.'''

# 1. Normalize text
text = text.lower()

# 2. Replace "iz" to "is", if "iz" is not in quotes
text = re.sub(r'(?<![“"])iz(?![”"])', 'is', text)

#split text to sentences
sentences = re.split(r'([.!?])', text)

words = []
for i in range(len(sentences)):
    sentences[i] = sentences[i].strip().capitalize() #capitalize every sentence
    word = sentences[i].split() #split every sentence to words
   # print(word[-1])
    if not word:
        continue
    if word[-1] != '.':
       words.append(word[-1]) #take last word from every sentence and add into separate sentence
text = ' '.join(sentences)
print(text)
print(' '.join(words).capitalize())

whitespace_count = len(re.findall(r'\s', text))
print('Number of whitespaces is ', whitespace_count)