# Python: 3.5

import os
import itertools
import re


key = ['р', 'бп', 'вф', 'гк', 'дт', 'жшщхцч', 'зс', 'л', 'м', 'н']
key = ['нм', 'гж', 'дт', 'кх', 'чщ', 'пб', 'шл', 'сз', 'вф', 'рц']
key = ['нл', 'рц', 'дг', 'тз', 'чкх', 'пб', 'шжщ', 'с', 'вф', 'м']
key = ['нл', 'ф', 'д', 'тр', 'чк', 'п', 'шщ', 'с', 'в', 'бм']
key = ['н', 'кх', 'лмр', 'т', 'чг', 'п', 'шж', 'с', 'вб', 'дз']
key = ['л', 'н', 'вф', 'р', 'ч', 'пб', 'шжщ', 'сз', 'м', 'дт']

# Читаем словарь

dictName = 'dictionary.txt'  # Unicode only

dictionary = []
dictPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), dictName)
with open(dictPath, 'r', encoding='utf') as file:
    for word in file.readlines():
        dictionary.append(''.join(word.split()))


def selectWordsByKey(number, key, dictionary):
    '''
    Выбираем слова в соответствии с кодом
    '''
    if len(str(number)) > 4:
        print('Это может быть долго, если что, грохните терминал')
    chars = []
    for n in str(number):
        chars.append(key[int(n)])
    charCombs = set(itertools.product(*chars))
    selectedWords = []
    for word in dictionary:
        wordSogl = re.sub('[оиаыюяэёуе]', '', word.lower())

        for charComb in charCombs:
            stringCharComb = ''.join(charComb)
            if wordSogl[:len(stringCharComb)] == stringCharComb:
                selectedWords.append(word)
    return selectedWords, chars


# Выводим диалог

for i in range(len(key)):
    print(i, key[i])

while True:
    print('-' * 80)
    print('Введите числа')
    inputstr = input()

    # Тестовый режим

    if inputstr == 'test':

        freqs = {
        'б': 0.15,
        'в': 0.41,
        'г': 0.15,
        'д': 0.27,
        'ж': 0.09,
        'з': 0.15,
        'к': 0.32,
        'л': 0.4,
        'м': 0.29,
        'н': 0.61,
        'п': 0.26,
        'р': 0.43,
        'с': 0.5,
        'т': 0.57,
        'ф': 0.02,
        'х': 0.09,
        'ц': 0.04,
        'ч': 0.13,
        'ш': 0.07,
        'щ': 0.03
        }

        keyfreqs = {}
        for keychar in key:
            keyfreqs.update({keychar: 0})
            for char in tuple(keychar):
                keyfreqs[keychar] += freqs[char]

        for c in key:
            print(c + '\t', '#' * round((keyfreqs[c]) * 10))

        testnumbers = range(0, 1000)
        emptycombs = []
        for i in testnumbers:
            wordscount = len(selectWordsByKey(i, key, dictionary)[0])
            if wordscount == 0:
                emptycombs.append((i, selectWordsByKey(i, key, dictionary)[1]))
                print(emptycombs[-1])
        print('Код не покрывает', len(emptycombs), 'из', len(testnumbers),
              'чисел от 0 до 1000')
        break


    # Собственно, кодирование

    numbers = re.findall('[0-9]+', inputstr)
    numbers = list(filter(lambda x: x != '', numbers))

    for number in numbers:
        print()
        selectedWords = selectWordsByKey(number, key, dictionary)[0]
        if not selectedWords:
            print('Похоже, у меня нет подходящих слов')
        else:
            print(number)
            print(', '.join(selectedWords))

    print()
