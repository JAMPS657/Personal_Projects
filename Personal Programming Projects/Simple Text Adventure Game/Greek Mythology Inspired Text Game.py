# The function play_again() asks if user wants play again or not
def play_again():
    print("\nDo you want to play again? (y or n)")

    # convert the user's input to lower_case to account for variance in capitalization
    answer = input(">").lower()

    # if user enters anything with the letter 'y', the program will restart
    if "y" in answer:
        start()
    else:
        # if user types anything without the letter 'y' the program will end
        exit()


# The function game_over() accepts an argument labeled 'reason' and calls on the function play_again
def game_over(reason):
    # print the 'reason' for game over in a new line using "\n"
    print("\n" + reason)
    print("Game Over!")
    # ask user to play again or not by running the play_again() function
    play_again()


# game_of_chance() Function allows for the game of chance to run
def game_of_chance():
    import random

    # producing a list consisting of a random integer with a domain of (0, 1] for two elements
    # the domain allows for simpler user winning conditions in the playing_goc() function
    samples = [random.randint(1, 2) for i in range(1)]

    # the two elements are labeled 'heads' and 'tails'.
    heads = samples.count(1)
    tails = samples.count(2)

    for s in samples:
        msg = 'Heads' if s==1 else 'Tails'
        print(msg)

    # Results of the game_of_chance() function are displayed to user
    print("Heads count=%d, Tails count=%d" % (heads, tails))
    return heads, tails

# The function playing_goc() is called from the final_room() function and provides prompts related
# to the game_of_chance() function
def playing_goc():
    print("The stranger accepts")
    print("\n Call, Heads or Tails?.")
    print("1). Heads")
    print("2). Tails")

    # take input()
    answer = int(input(">"))

    # calling game_of_chance() function
    heads, tails = game_of_chance()

    # setting conditions for user winning the coin toss
    # if user chooses option 1 AND the function game_of_chance() results in a heads count of 1:0 OR
    # if user chooses option 2 AND game_of_chance() results in a tails count of 0:1;
    # then a variant of the winning message is displayed
    if answer == 1 and heads == 1 or answer == 2 and tails == 1:
        print("\nYou've won the game of chance and slip past the stranger! The minotaur is still alive, but who cares?")

    # other inputs, aside from the ones asked for will result in the game_over() function running
    # (i.e. the user losing the coin toss)
    else:
        game_over("You've lost the game of chance, your fate is sealed")


# The function give_ring() is called from the function final_room(). # The function is available
# to be called upon, if prompt 3 from the final_room() function is available to the user
def give_ring():
    if "shiny ring" in player_inventory:
        # print a winning message variant
        print("\nDistracted by the ring, you slip past the stranger and escape! The minotaur is still alive, "
              "but who cares?")
    else:
        game_over("Sorry, but you don't have the ring and this angers the stranger, your fate is sealed")


# The function final_room() is the final stage of the program
def final_room():
    # some prompts and dialogue
    # '\n' is to print the prompts and dialogue in a new line
    print("\nYou come across an area where a previous victim stands in your way.")
    print("\nBehind the stranger, there is the exit! What will you do?")
    print("1). Fight the stranger.")
    print("2). Offer a game of chance")

    # Prompt 3 is only present if user has "shiny ring" in the list labeled player_inventory
    if "shiny ring" in player_inventory:
        print("3). Give the ring and get the heck outta here!")

    print("4). Bargain with the stranger!")

    # take input()
    answer = int(input(">"))

    # if user enters integer 1 the function game_over() runs
    if answer == 1:
        game_over("Weak from your trials you are overpowered, your fate is sealed.")
    # if user enters integer 2 the function playing_goc() runs
    elif answer == 2:
        playing_goc()
    # if user enters integer 3 the function playing_goc() runs
    elif answer == 3:
        give_ring()
    # if user enters integer 4 the function game_over() runs
    elif answer == 4:
        game_over("\nHaving nothing to bargain with, the stranger feels deceived and attacks, your fate is sealed")
    # any other user input will result in the function game_over() to run
    # (i.e.) accounting for user inputs not listed as part of the function's prompts
    else:
        game_over("The stranger has noticed your hesitation and ended you, your fate is sealed.")


# A navigation function for the user while travelling in the labyrinth
def direction3():
    print("\nThe halls are narrowing.")
    print("Quick, which way will you go right, or straight?")

    # accounting for capitalization variance in user input by converting it to lower case
    # this will be helpful with control flow in the following if statement
    answer = input(">").lower()

    if "r" in answer:
        # if user enters anything with the letter 'r' the function game_over() runs
        game_over("You walked directly into the clutches of the minotaur, your fate is sealed.")
    elif "s" in answer:
        # if user enters anything with the letter 's' the function final_room() runs
        final_room()
    # if user enters anything with the letter 's' or 'r' the function game_over() runs
    else:
        game_over("The walls have crushed you, your fate is sealed")

# Note for future navigation functions, they all work exactly the same way, the difference being what
# prompt variance is present and what respective function is called (dependent on user input). However,
# comments will be added if something not yet discussed has been implemented.

# The function ring_room() is where the player is able to add an item labeled "shiny ring"
# to the list labeled player_inventory.
def ring_room():
    # some dialogue and prompts
    print("\nYou are now in a room filled with treasure!")
    print("However, a ring seems to gleam brightest")
    print("What will you do?")
    print("1). Take the ring and and continue forward.")
    print("2). Take the ring and follow the source of light.")
    print("3). Take the ring and go right.")
    print("4). Just move forward.")
    print("5). Just follow the source of light.")
    print("6). Just go right.")

    # take input()
    answer = input(">")

    # if user enters 1, "shiny ring" is added to the list labeled player_inventory. Works the same way for
    # any other expected user input in relation to picking up the ring
    if answer == "1":
        player_inventory.append("shiny ring")
        # the function direction(3) allows the user to continue the game after picking up the ring
        direction3()
    elif answer == "2":
        player_inventory.append("shiny ring")
        game_over("The other worldly light has blinded you, you can no longer navigate the labyrinth and "
                  "your fate is sealed")
    elif answer == "3":
        player_inventory.append("shiny ring")
        game_over("You walked directly into the clutches of the minotaur, your fate is sealed.")
    elif answer == "4":
        # this prompt is the same as "1" with the exception of the "shiny ring" not being added to the
        # list labeled player_inventory
        direction3()
    elif answer == "5":
        game_over("The other worldly light has blinded you, you can no longer navigate the labyrinth and your "
                  "fate is sealed")
    elif answer == "6":
        game_over("You walked directly into the clutches of the minotaur, your fate is sealed.")
    else:
        game_over("The treasure drives you so mad you can no longer continue, your fate is sealed")

# Global variable is a list labeled 'player_inventory' that awaits a potential item labeled "shiny ring"
# to be added depending on user input for ring_room() function
player_inventory = []

# Another navigation function for the user while travelling in the labyrinth
def direction2():
    print("\nProceeding through, you see a pile of skeletons")
    print("Have to keep moving, which way will you go left, right, or straight?")

    answer = input(">").lower()

    # similar to the conditions for the letter "s" or"r" being present, if the letter "l" is present in user input
    # the function direction() is ran
    if "l" in answer:
        direction()
    elif "s" in answer:
        ring_room()
    elif "r" in answer:
        game_over("You walked directly into the clutches of the minotaur, your fate is sealed.")
    else:
        game_over("You've stood idle for too long, and you hear the clinking of bones behind you, your fate is sealed")

# Another navigation function for the user while travelling in the labyrinth
def direction():
    print("\nProceeding through, you hear the stomps of the minotaur")
    print("Those steps sounded close...., which way will you go left, right, or straight?")

    answer = input(">").lower()

    if "l" in answer:
        game_over("You walked directly into the clutches of the minotaur, your fate is sealed.")
    elif "r" in answer:
        direction2()
    elif "s" in answer:
        ring_room()
    else:
        game_over("You've walked into a wall and passed out, your fate is sealed")

# The function start() begins the game for the user and is also called upon from play_again() function
# when a losing condition is met
def start():
    # intro dialogue and prompts
    print("\nWelcome to the Labyrinth. Apparently you're the poor lad or lass they've sent in before Theseus.")
    print("Better get a move on, which way will you go left, right, or straight?")

    answer = input(">").lower()

    if "l" in answer:
        game_over("You walked directly into the clutches of the minotaur, your fate is sealed.")
    elif "r" in answer:
        direction2()
    elif "s" in answer:
        direction()
    else:
        game_over("You've walked directly into a wall and passed out, your fate is sealed")


# Run the function start() to begin the game
start()

#-----------------------------------Scratch paper for Final Project-------------------------------------#

