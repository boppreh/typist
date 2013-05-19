import os
from collections import Counter

def all_typed():
    """
    Returns a list of all keys presses.
    """
    lines = []
    all_dates = os.listdir('data/')
    for i, date in enumerate(all_dates):
        print 'Reading {} ({}/{})'.format(date, i + 1, len(all_dates))
        with open('data/' + date) as date_file:
            lines.extend(date_file.read().split('\n'))

    down_lines = (line for line in lines if 'key down' in line)
    key_codes = [int(line.split(' - ')[2]) for line in down_lines if line]

    return key_codes

def groups(key_codes):
    """
    Converts `key_codes` to characters and groups them based on spacing.
    """
    text = ''.join(map(chr, key_codes)).lower()
    return filter(lambda c: 1 < len(c) < 20, text.split())

def words(key_codes):
    """
    Return all fully typed words from `key_codes`.
    """
    letter_codes = (code if 31 < code < 127 else 32 for code in key_codes)
    return filter(str.isalpha, groups(letter_codes))

def mistakes(key_codes):
    """
    Return all typed words from `key_codes` that contain backspaces.
    """
    typing_codes = (code for code in key_codes if 31 < code < 127 or code == 8)
    typed_words = groups(typing_codes)
    has_mistakes = lambda w: 1 <= w.count(chr(8)) < w.index(chr(8))
    return filter(has_mistakes, typed_words)


if __name__ == '__main__':
    key_codes = all_typed()

    print '---\n'

    print 'Most common words:\n'
    for word, count in Counter(words(key_codes)).most_common(20):
        print word, count

    print '---\n'

    print 'Most common mistakes:\n'
    for word, count in Counter(mistakes(key_codes)).most_common(20):
        print '{} ({}) {}'.format(word, word.replace(chr(8), '!'), count)

    raw_input()
