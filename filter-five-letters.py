import sys

in_path = sys.argv[1]
word_file = open(in_path, "r")
out_path = sys.argv[2]
filtered_file = open(out_path, "w")

def is_candidate(word):
    letters = set([x for x in word])
    if len(letters) == len(word):
        return True
    return False

out = []
for line in word_file:
    word = line[:-1]

    if not is_candidate(word):
        continue

    if len(word) == 5:
        out.append(word)

out.sort()
for word in out:
    filtered_file.write(word)
    filtered_file.write("\n")