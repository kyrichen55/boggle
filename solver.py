import json, sys, string

with open('boggle.json') as f:
    game = json.load(f)

words = game['dictionary']
letters = game['board']
coords = {} #maps coordinate to letter
for i in range(3):
    for j in range(3):
        coords[(i,j)] = letters[i][j]
letter_to_coords = {letters[i][j]: [] for i in range(3) for j in range(3)} #maps letter to all of its coordinates
for c in coords:
    letter_to_coords[coords[c]].append(c)

"""
Raises error if anything isn't a string, or isn't an alphabetical character.
Also raises error if anything in the board doesn't have upper case letters.
"""
error_message = "Something is wrong with your input. Try again!"

for word in words:
    if type(word) != str:
        print(error_message)
        exit()
    for l in word:
        if l not in string.ascii_letters:
            print(error_message)
            exit()
for list in letters:
    for l in list:
        if type(l) != str:
            print(error_message)
            exit()
        for c in l:
            if c not in string.ascii_uppercase:
                print(error_message)
                exit()

"""
Creates a dictionary with each coordinate as the key and the
adjacent letters in a set as the value.
"""
adj = {}
for i in range(3):
    for j in range(3):
        adj[(i,j)] = set()
        for a in range(max(i-1,0), i+2): #max so it doesn't index into negatives
            for b in range(max(j-1,0), j+2): #max so it doesn't index into negatives
                try: #doesn't index beyond array
                    adj[(i,j)].add(letters[a][b])
                except:
                    pass
        adj[(i,j)].remove(letters[i][j])

def solve(word, n=0):
    """
    Takes in a word, returns True if it's in the board and False if not
    """
    ans = ""
    visited = set()
    if ans == word: #empty set is always in Boggle game
        return True
    if word[n] not in letter_to_coords: #checks if first letter in board
        return False
    for n in range(len(word)): #iterates through word
        ans += word[n]
        if ans == word:
            return True
        for c in letter_to_coords[word[n]]: #current coord, loops through options
            try:
                for next_coord in letter_to_coords[word[n+1]]: #loops through options for next coord
                    if next_coord not in visited and word[n+1] in adj[c]: #checks if an available next letter is in adjacent letter
                        visited.add(c)
                        break # if letter works, add it to visited and move on to next letter
                    else:
                        return False
                break
            except: #next letter not in board
                return False
        n += 1

for w in words:
    w = w.upper() #converts all valid strings to all uppercase
    if solve(w) == True:
        print(w)
