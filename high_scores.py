# the high scores module
# we should limit the players name to 5 uppercase characters

def get_high_scores() -> ([str], [int]):
    """
    get_high_scores - returns a tuple consisting of a sorted list of the all time 5 high scorers and a list of their scores (sorted)
    """
    names = []
    scores = []
    with open("high_scores.txt", "r") as file:
        for line in file:
            data = line.split(",")
            if data[0] != "":
                names.append(data[0])
                scores.append(int(data[1].strip()))

    return (names, scores)

def get_score_index(score, scores):
    """
    get_score_index - returns the index that a new score should be added at. If its greater than 4, then the score is smaller than anyone else on the board
    """
    insert_location = 0
    for i in range(len(scores)):
        if scores[i] < score:
            break
        insert_location += 1
    return insert_location

def add_high_score(name, score) -> ([str], [int]):
    """
    add_high_score - adds a new name and score to the high scores if the new name and score scored higher than the previous top 5
    returns the new list
    """
    names, scores = get_high_scores()

    insert_location = get_score_index(score, scores)

    if insert_location < 5:
        names.insert(insert_location, name)
        scores.insert(insert_location,score)
        if len(names) > 5:
            names.pop()
            scores.pop()
        with open("high_scores.txt", "w") as file:
            for i in range(len(names)):
                file.write(names[i] + ", " + str(int(scores[i])))
                if i < len(names)-1:
                    file.write("\n")
    return (names, scores)

def reset_high_scores():
    """
    reset_high_scores - removes all previous high scores.
    """
    open("high_scores.txt","w").close()
    return

if __name__ == '__main__':
    # testing code
    passed = True

    reset_high_scores()
    add_high_score("Bot A", 2)
    add_high_score("Bot B", 5)
    add_high_score("Bot C", 3)
    add_high_score("Bot D", 1)
    add_high_score("Bot E", 4)

    names, scores = get_high_scores()
    if names[0] != "Bot B" or scores[0] != 5:
        print("Bot B is not in the right place.")
        passed = False
    if names[1] != "Bot E" or scores[1] != 4:
        print("Bot E is not in the right place.")
        passed = False
    if names[2] != "Bot C" or scores[2] != 3:
        print("Bot C is not in the right place.")
        passed = False
    if names[3] != "Bot A" or scores[3] != 2:
        print("Bot A is not in the right place.")
        passed = False

    if names[4] != "Bot D" or scores[4] != 1:
        print("Bot D is not in the right place.")
        passed = False

    add_high_score("Player 1", 6)
    names, scores = get_high_scores()
    if names[0] != "Player 1" or scores[0] != 6:
        print("Player 1 has not been added to the list properly")
        passed = False

    if passed:
        print("Congratulations, the high score code passed all the tests.")
    else:
        print("Unforunately, it seems that one or more test cases have failed, please try again")
