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

#while True:



print('-' * 80)
print('Введите числа')
inputstr = input()

if inputstr == 'test':
    testnumbers = range(0, 1000)
    emptycombs = []
    for i in testnumbers:
        wordscount = len(selectWordsByKey(i, key, dictionary)[0])
        if wordscount == 0:
            emptycombs.append((i, selectWordsByKey(i, key, dictionary)[1]))
            print(emptycombs[-1])
    print('Код не покрывает', len(emptycombs), 'из', len(testnumbers), 'чисел от 0 до 1000test')
    raise Exception('Закончено')



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
