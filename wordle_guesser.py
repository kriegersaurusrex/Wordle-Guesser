import itertools

# Creates decreasing frequency dictionary from existing letter mapping
def remap_letter_frequency(dict_to_rev):
    dict_inv = {}
    for key, value in dict_to_rev.items():
        if value in dict_inv:
            dict_inv[value].append(key)
        else:
            dict_inv[value] = [key]
    return dict_inv

# Creates set of yellow letters outside of current position
def other_yellow(yellow_letters, curr_index):
    all_other_yellow = set()
    for i in range(0, len(yellow_letters)):
        if(i == curr_index):
            continue
        if(len(yellow_letters[i]) > 0):
            for j in range(0, len(yellow_letters[i])):
                all_other_yellow.add(yellow_letters[i][j])
    return all_other_yellow
            

# Builds set of possible words if there are yellow letter(s) at the current position
def add_yellow_set(five_letter_words, yellow_letters, curr_index, grey_letters, other_yellow_set):
    yellow_set = set()
    for i in range(0, len(five_letter_words)):
        if five_letter_words[i][curr_index] not in yellow_letters and five_letter_words[i][curr_index] not in grey_letters:
            num_match = 0
            for j in range(0, len(five_letter_words[i])):
                if five_letter_words[i][j] in other_yellow_set:
                    num_match += 1
            if(num_match == len(other_yellow_set)):
                yellow_set.add(five_letter_words[i])
    return yellow_set

# Builds set of possible words if there is a green letter at the current position
def add_green_set(five_letter_words, green_letter, curr_index, grey_letters):
    green_set = set()
    for i in range(0, len(five_letter_words)):
        if(five_letter_words[i][curr_index] == green_letter):
            for j in range(0, len(five_letter_words[i])):
                if five_letter_words[i][j] in grey_letters:
                    break
                if(j == 4):
                    green_set.add(five_letter_words[i])
    return green_set

lines = []
five_letter_words = []
with open('wordle-answers-alphabetical.txt') as f:
    lines = f.readlines()
for line in lines:
    five_letter_words.append(line[0:5])
f.close()

# Enter existing letters here
grey_letters = ['c','a','y']
yellow_letters = [[],[],[],['z'],[]]
green_letters = ['','','','','']

current_guesses = []
for i in range(0, len(yellow_letters)):
    to_add = set()
    if(len(green_letters[i]) == 1):
        to_add = add_green_set(five_letter_words, green_letters[i], i, grey_letters)
    elif(len(yellow_letters[i]) > 0):
        other_yellow_set = other_yellow(yellow_letters, i)
        to_add = add_yellow_set(five_letter_words, yellow_letters[i], i, grey_letters, other_yellow_set)
    else:
        to_add = set(five_letter_words)
    current_guesses.append(to_add)

# Puts intersecting values from all lists into a single set
valid_guesses = sorted(set.intersection(*current_guesses))

remaining_letter_freq = []
for i in range(0, 5):
    if(len(green_letters[i]) == 1):
        remaining_letter_freq.append(green_letters[i])
        continue
    temp_freq = {}
    for word in valid_guesses:        
        if word[i] not in temp_freq and word[i] not in grey_letters:
            temp_freq[word[i]] = 1
        elif word[i] in temp_freq and word[i] not in grey_letters:
            temp_freq[word[i]] += 1
    temp_freq = sorted(remap_letter_frequency(temp_freq).items(), key=lambda x: x[0], reverse=True)
    remaining_letter_freq.append(temp_freq)
print("Remaining Letter frequency", remaining_letter_freq)

all_yellow_letters = {}
for i in range(0, len(yellow_letters)):
    if(len(yellow_letters) > 0):
        for j in range(0, len(yellow_letters[i])):
            all_yellow_letters[yellow_letters[i][j]] = 0

to_guess = [[],[],[],[],[]]
for i in range(0, len(green_letters)):
    if(len(green_letters[i]) != 0):
        to_guess[i] = green_letters[i]

num_pass = 0
constructed_words = []
final_words = []
while(len(constructed_words) == 0):
    final_words = []
    for i in range(0, 5):
        if len(green_letters[i]) == 1 or (num_pass >= len(remaining_letter_freq[i])):
            continue        
        to_guess[i] += remaining_letter_freq[i][num_pass][1]
    print("After", num_pass, "passes", to_guess)
    # Looks for words based on all possible 5-letter permutations in 
    possible_combos = list(itertools.product(to_guess[0],to_guess[1],to_guess[2],to_guess[3],to_guess[4]))
    for i in range(0, len(possible_combos)):
        check_if_valid_word = ''.join(possible_combos[i])
        if check_if_valid_word in five_letter_words:
            constructed_words.append(check_if_valid_word)
    num_pass += 1
    # Checks that a given constructed word contains the yellow letters, tosses triple repeating letters for better guessing
    if(len(all_yellow_letters) > 0):
        for i in range(0, len(constructed_words)):
            yellow_temp = all_yellow_letters.copy()
            for j in range(0, len(constructed_words[i])):
                if constructed_words[i][j] in all_yellow_letters:
                    yellow_temp[constructed_words[i][j]] += 1
            if(min(yellow_temp.items(), key=lambda x: x[1])[1] > 0 and max(yellow_temp.items(), key=lambda x: x[1])[1] < 3):
                final_words.append(constructed_words[i])
        #If this is empty, then must do more passes to satisfy yellow letter constraints
        if(len(final_words) == 0):
            constructed_words = []
    else:
        final_words = constructed_words
# Outputs a list of words which satisfy the given constraints: may want to find a way to narrow down the best single guess
print(final_words)

