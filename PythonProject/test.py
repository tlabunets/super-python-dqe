import re

text = '''tHis iz your homeWork, copy these Text to variable.\n\n
You NEED TO normalize it fROM letter CASEs point oF View. also, 
create one MORE senTENCE witH LAST WoRDS of each existING SENtence 
and add it to the END OF this Paragraph.\n\n
it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.\n\n
last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, 
not only Spaces, but ALL whitespaces. I got 87.'''
text = text.lower()
# 2. Замінюємо "iz" на "is", якщо "iz" не знаходиться в лапках
text = re.sub(r'(?<![“"])iz(?![”"])', 'is', text)

# 3. Розбиваємо текст на параграфи
paragraphs = re.split(r'\n\s*\n', text.strip())
processed_paragraphs = []
last_words = []

for idx, paragraph in enumerate(paragraphs):
    # Виправлення регістру для кожного речення
    sentences = re.findall(r'[^.]*[^.]', paragraph)
    capitalized_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        # Капіталізація речення
        capitalized_sentence = sentence[0].upper() + sentence[1:]
        capitalized_sentences.append(capitalized_sentence)

        # Додаємо останнє слово речення
        words = sentence.rstrip('.').split()
        if words:
            last_words.append(words[-1])

    # Створення нового речення з останніх слів (тільки після першого параграфа)
    if idx == 0 and last_words:
        final_sentence = ' '.join(last_words).capitalize() + '.'
        # Вставка нового речення перед останнім реченням параграфа
        if len(capitalized_sentences) >= 2:
            capitalized_sentences.insert(-1, final_sentence)
        else:
            capitalized_sentences.append(final_sentence)

    # Об'єднання речень у параграф
    processed_paragraph = ' '.join(capitalized_sentences)
    processed_paragraphs.append(processed_paragraph)



# 5. Формування фінального тексту
final_text = '\n\n'.join(processed_paragraphs)

#print(final_text)'''