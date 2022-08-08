import random
import sys
import csv
from collections import namedtuple
from collections import defaultdict


class Hand:
    ''' The class labeled as "Hand" encapsulating the logic for a hand of blackjack.'''
    def __init__(self, cards=None):
        ''' The method initializes our "Hand" class' attributes "cards","total", and "soft_ace_count"
        '''

        # Conditions for the game having yet begun (i.e. no cards have been dealt)
        if cards == None:
            self.cards = []
            self.total = 0
            self.soft_ace_count = 0
        # Otherwise, cards have been dealt
        else:
            self.cards = cards
            self.total = self.score().total
            self.soft_ace_count = self.score().soft_ace_count

    def __str__(self):
        ''' The method returns a string that represents our blackjack hand'''
        return f'Hand: cards={self.cards}, total={self.total}, soft ace count={self.soft_ace_count}'

    def add_card(self):
        ''' The method returns a random value between 1 and 13 (where 1 = Ace & 13 = King), simulating
        an infinite deck of cards. Where we call the score function to update our hand
        '''
        get_card = random.randint(1,13)
        self.cards.append(get_card)

        self.total = self.score().total
        self.soft_ace_count = self.score().soft_ace_count

    def is_blackjack(self):
        ''' The method returns True if the conditions are such that the total of hand is equal to 21.'''
        # Code for all possible hands (w/ only 2 cards) that result in blackjack
        # (i.e. a soft ace and a 10, 11=Jack, 12=Queen, or 13=King)
        for card in self.cards:
            if card == 10 or card == 11 or card == 12 or card == 13:
                blackjack = True
            else:
                blackjack = False  # otherwise return False when total does not equal 21

        return (self.soft_ace_count == 1 and blackjack)

    def is_bust(self):
        '''The method returns True if Hand total is greater than 21.'''
        if self.total > 21:
            return True

    def score(self):
        ''' The function takes a list of numbers resulting in a namedtuple where the 1st element
        is the total value of the blackjack hand and second element is the number of soft aces present.
        '''
        # First we begin with 0 as our total, since no cards have been dealt out
        total = 0

        # Code for the event that NO aces are drawn (i.e. non of them soft)
        ace_found = False
        soft_ace_count = False

        for card in self.cards:
            if card >= 10:        # ">=" greater than or equal to
                total += 10       # "+=" add to a variable and assigns result to the same variable
            else:
                total += card
            # Code for the PRESENCE of aces
            if card == 1:         # "==" is equal to
                ace_found = True

        # Code for the event that aces are drawn and the conditions are such that the ace('s)
        # drawn can be considered "soft" (i.e. the value of the Ace can be considered to have a value=11)
        if total < 12 and ace_found:
            total += 10
            soft_ace_count = True

        # Code that creates a namedtuple called "Score"
        Score = namedtuple("Score", 'total, soft_ace_count')
        hand = Score(total, soft_ace_count)      # namedtuple "Score" w/ specific values labeled as "hand"

        return hand


class Strategy:
    ''' The class labeled as "Strategy" represents a hand of blackjack.'''
    def __init__(self, stand_on_value, stand_on_soft):
        ''' The method initializes our class "Strategy"'s attributes.'''
        self.stand_on_value = stand_on_value
        self.stand_on_soft = stand_on_soft

    def __str__(self):
        if self.stand_on_soft:
            return f'S{self.stand_on_value}'
        else:
            return f'H{self.stand_on_value}'

    def stand(self, hand):
        '''The method will return a Boolean value indicating whether the player will stand on
        a “soft” hand or just on a “hard” for the Hand-object that iss passed in via the "play" method.

        Boolean logic is as follows (independent of strategy),
            True = STAND on hand
            False = to HIT
        '''
        total, soft_ace_count = Hand.score(hand)
        # Score < stand value, we will stand no matter what
        if total < self.stand_on_value:
            return False
        # Score > stand value, we will stand no matter what
        elif total > self.stand_on_value:
            return True
        # Code for conditions related to the soft and hard strategy
        elif soft_ace_count == 0 or self.stand_on_soft:
            return True
        else:
            return False

    def play(self):
        '''The method simulates playing a single hand of blackjack by instantiating the class we created
        labeled "Hand".
        '''
        # Code for the first hand in the game
        hand = Hand()
        hand.add_card()
        hand.add_card()

        # Code for the event of hitting (i.e. adding another card to the hand)
        while self.stand(hand) == False:
            hand.add_card()

        return hand


def main():
    '''The function will return the probability of going bust based on a single command line argument, the
     number of games played between the player and the dealer.

     Additionally, the function creates a table via a csv file with the calculated percentage of games won
     by the player.
    '''

    sim_count = int(sys.argv[1])

    # Code for invalid input (i.e. we cannot have a negative amount of simulations)
    if sim_count <= 0:
        raise ValueError ('Please enter a valid argument \n'
                         'Argument is any integer value above 0 \n')

    # Code that creates a variable that
    all_strategies = [Strategy(sov, sos) for sos in (False,True) for sov in range(13,21)]

    # Create the csv and label it "blackjack3_results.csv"
    with open("blackjack3_results.csv", 'w', encoding='utf8', newline="") as file:
        writer = csv.writer(file)
        # Code for titling the column related to player strategy
        row1 = ['P-Strategy']

        for i in all_strategies:            # fill the remaining of row 1 with the prefix "D-" to represent
                                            # the dealer's strategy
            row1.append(f'D-{i.__str__()}')

        writer.writerow(row1)  # update the csv

        # Nested for loops to encapsulate all possible cases where player win count increases and a tie
        for player_strat in all_strategies:
            win_counts = defaultdict(int)
            for dealer_strat in all_strategies:
                for sim in range(sim_count):

                    player_hand = player_strat.play()     # a variable to represent the player strategy

                    # Conditions for the event the player loses (i.e. bust)
                    if player_hand.is_bust() == True:
                        continue

                    dealer_hand = dealer_strat.play()

                    # Conditions for the event player win count increases, due to dealer bust
                    if dealer_hand.is_bust() == True:
                        win_counts[dealer_strat.__str__()] += 1
                        continue

                    # Conditions for the event player win count increases, due to having Blackjack
                    if player_hand.is_blackjack() == True and dealer_hand.is_blackjack() == False:
                        win_counts[dealer_strat.__str__()] += 1
                        continue

                    # Conditions for the event of a tie and a win count is not added for either the dealer
                    # or player
                    push_count = 0
                    if player_hand.total == dealer_hand.total:
                        push_count += 1
                        continue

                    # The conditions for contender (player or dealer) with the higher total has win count
                    # increased
                    elif player_hand.total > dealer_hand.total:
                        win_counts[dealer_strat.__str__()] += 1
                        continue
                    else:          # otherwise, with respect to conditions where player win count increases
                                   # the dealer win count will increase instead
                        continue

            # Code that accounts for games where neither contender's win count increases to calculate the
            # player's correct win percentage
            total_games = sim_count - push_count


            rows = [f'P-{player_strat.__str__()}']  # fill the remainder of rows, where the first value in
                                                    #  each row has the prefix "P-" to represent player
                                                    # strategy

            # Code for the percentages of games won by the player
            for strat in all_strategies:
                player_win_percentage = round(100*win_counts[strat.__str__()]/total_games,2)
                rows.append(player_win_percentage)    # add the calculated percentages to your table

            writer.writerow(rows)  # update the csv based on the player win percentage


if __name__ == '__main__':
     main()
