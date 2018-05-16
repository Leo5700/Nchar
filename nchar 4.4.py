#!/usr/bin/env python3


import os
import itertools
import re
import random
import difflib


key = ['р', 'бп', 'вф', 'гк', 'дт', 'жшщхцч', 'зс', 'л', 'м', 'н']
# key = ['нм', 'гж', 'дт', 'кх', 'чщ', 'пб', 'шл', 'сз', 'вф', 'рц']
# key = ['нл', 'рц', 'дг', 'тз', 'чкх', 'пб', 'шжщ', 'с', 'вф', 'м']
# key = ['нл', 'ф', 'д', 'тр', 'чк', 'п', 'шщ', 'с', 'в', 'бм']
# key = ['н', 'кх', 'лмр', 'т', 'чг', 'п', 'шж', 'с', 'вб', 'дз']
# key = ['л', 'н', 'вф', 'р', 'ч', 'пб', 'шжщ', 'сз', 'м', 'дт']

if len(key) != 10:
    raise Exception('key должен содержать ровно 10 элементов')

# Читаем словарь

dictName = 'dictionary.txt'  # Unicode only

dictionarysource = []
dictPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), dictName)

def loadDictionary():
    with open(dictPath, 'r', encoding='utf') as file:
        for word in file.readlines():
            dictionarysource.append(''.join(word.split()))
    dictionary = set([x.lower() for x in dictionarysource])  # Удаляем повторы
    return dictionary

def selectWordsByKey(number, key, dictionary):
    '''
    Выбираем слова в соответствии с кодом
    '''
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

    dictionary = loadDictionary()

    print('-' * 10 + 'Введите числа или слова' + '-' * 9)
    inputstr = input()

    # Режим повтора предыдущего ввода

    if inputstr.lower() in ['r', 'rep']:
        try:
            inputstr = prewinputstr
        except NameError:
            print()
            print('Предыдущих команд не найдено')
            continue
    prewinputstr = inputstr

    # Предупреждение о длительном процессе

    if inputstr.isdigit() and len(inputstr) > 4:
        print('Что-то происходит... Для чисел > 99999 это будет долго')

    # Режим проверки ключа

    if inputstr.lower() in ['t', 'test']:

        freqs = {
        'б': 0.159,
        'в': 0.454,
        'г': 0.170,
        'д': 0.298,
        'ж': 0.094,
        'з': 0.165,
        'к': 0.349,
        'л': 0.440,
        'м': 0.321,
        'н': 0.670,
        'п': 0.281,
        'р': 0.473,
        'с': 0.547,
        'т': 0.626,
        'ф': 0.026,
        'х': 0.097,
        'ц': 0.048,
        'ч': 0.144,
        'ш': 0.073,
        'щ': 0.036
        }

        keyfreqs = {}
        for keychar in key:
            keyfreqs.update({keychar: 0})
            for char in tuple(keychar):
                keyfreqs[keychar] += freqs[char]

        print('\nОтносительная частотность ключа:')
        for c in key:
            print(c + '\t', '#' * round((keyfreqs[c]) * 10))

        print('\nПроверка покрытия:')
        testnumbers = range(0, 1000)
        emptycombs = []
        for i in testnumbers:
            wordscount = len(selectWordsByKey(i, key, dictionary)[0])
            if wordscount == 0:
                emptycombs.append((i, selectWordsByKey(i, key, dictionary)[1]))
                print(emptycombs[-1])
        print('Код не покрывает', len(emptycombs), 'из', len(testnumbers),
              'чисел от 0 до 1000')
        continue

    # Режим пополнения словаря

    if inputstr and inputstr.split()[0].lower() in ['a', 'add']:

        with open(dictPath, 'a', encoding='utf') as file:
            file.write('\n' + inputstr.split()[1])
        print()
        print('Слово добавлено в словарь')
        dictionary = loadDictionary()  # Перезагружаем словарь
        print()
        continue

    # Режим поиска похожих слов

    if inputstr and inputstr.split()[0].lower() in ['s', 'sim']:

        print()
        print('Похожие слова (до 12 шт.):')
        for word in inputstr.split()[1:]:
            print(difflib.get_close_matches(word, dictionary, 12))
        print()
        continue

    # Режим декодирования

    if inputstr and not inputstr[0].isdigit():
            print()
            numbers = []
            numbersstring = ''
            for word in inputstr.split():
                number = ''
                for character in word.lower():
                    for element in key:
                        if character in set(element):
                            number = ''.join((number, str(key.index(element))))
                numbers.append(number)
                numbersstring = ''.join((numbersstring, number, ' '))
            if not numbersstring.split():
                print('Ключ не содержит подходящих букв')
            else:
                print(numbersstring)
            print()
            continue

    # Режим кодирования

    numbers = re.findall('[0-9]+', inputstr)
    numbers = list(filter(lambda x: x != '', numbers))

    for number in numbers:
        print()
        selectedWords = selectWordsByKey(number, key, dictionary)[0]
        if not selectedWords:
            print('Похоже, у меня нет слов на буквах')
            print(selectWordsByKey(number, key, dictionary)[1])
            print('Чтобы добавить новое слово в словарь,\nиспользуйте конструкцию "add слово"')
        else:
            print(number)
            nrand = 12  # Число случайных слов
            if len(selectedWords) > nrand:
                randSelectedWords = [selectedWords.pop(random.randrange(0,
                                    len(selectedWords))) for x in range(nrand)]
                print('Выборка', nrand, '/', len(selectedWords),'случайный слов:')
            else:
                randSelectedWords = selectedWords
            randSelectedWords.sort()
            print(', '.join(randSelectedWords))

    print()
