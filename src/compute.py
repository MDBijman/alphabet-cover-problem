import pprint
import ast
import cProfile
import sys
import time

def current_milli_time():
        return round(time.time() * 1000)

in_path = sys.argv[1]
in_file = open(in_path, "r")

def letters_available(letters, word):
    return letters & word == word

def letter_to_number(ch):
    return 2**(ord(ch) - ord('a'))

def word_to_number(word):
    nums = [letter_to_number(c) for c in word]
    sum = 0
    for n in nums:
        sum += n
    return sum

def number_to_letters(n):
    letters = []
    i = 0
    while i < 32:
        if n & 1 == 1:
            letters.append(chr(ord('a') + i))
        i += 1
        n = n >> 1
    return letters

def count_letters(alphabet):
    return alphabet.bit_count()

alphabet = word_to_number("abcdefghijklmnopqrstuvwxyz")

# dict of letter to first index of word beginning with next letter
next_chapter = {}
words = []
wordsets = []
first_letters = []
first_letters_num = []

prev_chapter = None
cur_chapter = None
for i, line in enumerate(in_file.readlines()):
    word = line.split(" ")[0]
    words.append(word)
    wordset = line[len(word) + 1:]
    wordsets.append(ast.literal_eval(wordset))

    first_letters.append(word[0])
    first_letters_num.append(letter_to_number(word[0]))

    if cur_chapter is None:
        cur_chapter = first_letters[-1]
    elif ord(first_letters[-1]) > ord(cur_chapter):
        prev_chapter = cur_chapter
        cur_chapter = first_letters[-1]
        next_chapter[letter_to_number(prev_chapter)] = i

words_len = len(words)
    
print(len(words), "words")
bin_words = [word_to_number(w) for w in words]

do_trace = False
def trace(s):
    if do_trace:
        print(s)


#pprint.PrettyPrinter().pprint(next_chapter)

# quickly compute set of words that fit in given alphabet
memoize = {}
memoized = 0
computed = 0
calls = 0
# alphabet -> sets containing words of len 5
def solve_dynamic(alphabet):
    global memoized, computed, calls
    calls += 1
    if alphabet in memoize:
        memoized += 1
        return memoize[alphabet]
    computed += 1
    
    if count_letters(alphabet) == 6:
        out = [bw for bw in bin_words if letters_available(alphabet, bw)]
        memoize[alphabet] = out
        return out

    out = []

    i = 0
    while i < words_len:
        # Goto next chapter
        fln = first_letters_num[i]
        if alphabet & fln == 0:
            if fln in next_chapter:
                i = next_chapter[fln]
                continue
            else:
                i = words_len
                continue

        bw = bin_words[i]
        if letters_available(alphabet, bw):
            new_alphabet = alphabet - bw
            sub = solve_dynamic(new_alphabet)
            for s in sub:
                s.append(bw)
            out += sub

        i += 1

    memoize[alphabet] = out
    return out

begin_deep = current_milli_time()
solutions = solve_dynamic(alphabet)
#cProfile.run('solve_dynamic(alphabet)')
print(calls, memoized, computed)
#print(solutions)
running_time = (current_milli_time() - begin_deep) / 1000.0
print("took", str(running_time) + "s")

