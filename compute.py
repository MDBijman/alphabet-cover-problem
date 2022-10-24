import cProfile
import sys
import time

def current_milli_time():
        return round(time.time() * 1000)

begin = current_milli_time()

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

alphabet = word_to_number("abcdefghijklmnopqrstuvwxyz")

# dict of letter to first index of word beginning with next letter
next_chapter = {}
words = []
original_words = []
first_letters = []
first_letters_num = []

prev_chapter = None
cur_chapter = None
for i, line in enumerate(in_file.readlines()[9300:]):
    elems = line.split(" ")
    words.append(elems[0])
    original_words.append(elems[1][:-1])

    first_letters.append(elems[0][0])
    first_letters_num.append(letter_to_number(elems[0][0]))

    if cur_chapter is None:
        cur_chapter = first_letters[-1]
    elif ord(first_letters[-1]) > ord(cur_chapter):
        prev_chapter = cur_chapter
        cur_chapter = first_letters[-1]
        next_chapter[letter_to_number(prev_chapter)] = i
    
bin_words = [word_to_number(w) for w in words]

do_trace = False
def trace(s):
    if do_trace:
        print(s)

def solve():
    i = 0
    iter = 0
    stack = []
    last = current_milli_time()
    print_every = 500000
    cur_alphabet = alphabet

    while True:
        iter += 1
        if iter % print_every == 0 and len(stack) > 0:
            now = current_milli_time()
            iterps = round((1000.0 / (now - last)) * print_every)
            print("Iter", iter, "-", "iter/s", iterps)
            last = now

        # word found
        if len(stack) == 5:
            t = stack[-1]
            stack.pop()
            cur_alphabet = (cur_alphabet + t[0])
            # move previous idx up
            if t[1] == len(bin_words):
                t = stack[-1]
                stack.pop()
                i = t[1]
                cur_alphabet = (cur_alphabet + t[0])
            # move current idx up
            else:
                i = t[1]
            continue
        elif i + 1 > len(bin_words) and stack == []:
            break
        elif i == len(bin_words):
            t = stack[-1]
            stack.pop()
            i = t[1]
            cur_alphabet = (cur_alphabet + t[0])
            continue

        cur_word = bin_words[i]

        # otherwise check all letters
        if letters_available(cur_alphabet, cur_word):
            cur_alphabet = (cur_alphabet - cur_word)
            stack.append((cur_word, i + 1))
            i = i + 1
        else:
            # check first letter first - if fail we skip to next chapter
            first_letter_num = first_letters_num[i]
            if not letters_available(cur_alphabet, first_letter_num):
                # end of book
                if first_letters_num[i] not in next_chapter:
                    t = stack[-1]
                    stack.pop()
                    i = t[1]
                    cur_alphabet = (cur_alphabet + t[0])
                else:
                    i = next_chapter[first_letters_num[i]]
            # if letters unavailable increment by one
            else:
                i += 1

    print("done")
    running_time = (current_milli_time() - begin) / 1000.0
    print("took", str(running_time) + "s")
    print(iter, "iterations")
    print(iter / running_time, "iter/s")

solve()
