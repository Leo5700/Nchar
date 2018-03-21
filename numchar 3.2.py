# Python: 3.5

import os
import itertools
import re


key = ['р', 'бп', 'вф', 'гк', 'дт', 'жшщхцч', 'зс', 'л', 'м', 'н']


# Читаем словарь

dictName = 'dictionary.txt'  # Unicode

dictionary = []
dictPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), dictName)
with open(dictPath, 'r', encoding='utf') as file:
    for word in file.readlines():
        dictionary.append(''.join(word.split()))


def selectWordsByKey(number, key, dictionary):
    '''
    Выбираем слова в соответствии с кодом
    '''
    chars = []
    for n in number:
        chars.append(key[int(n)])

    charCombs = set(itertools.product(*chars))

    selectedWords = []
    for word in dictionary:
        wordSogl = re.sub('[оиаыюяэёуе]', '', word.lower())

        for charComb in charCombs:
            stringCharComb = ''.join(charComb)
            if wordSogl[:len(stringCharComb)] == stringCharComb:
                selectedWords.append(word)

    return selectedWords


# Выводим диалог

for i in range(len(key)):
    print(i, key[i])

while True:

    print('-' * 80)
    print('Введите числа')
    numbers = re.findall('[0-9]+', input())
    numbers = list(filter(lambda x: x != '', numbers))

    for number in numbers:
        print()
        print(number)
        selectedWords = selectWordsByKey(number, key, dictionary)
        print(', '.join(selectedWords))

    print()
