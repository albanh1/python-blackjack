
###
###   Blackjack
###   ----------
###   A simplified text-based blackjack game
###
###   How to run the code
###   -------------------
###   1. Copy all code in this file.
###   2. Open https://www.programiz.com/python-programming/online-compiler/
###      (or any other web-based python compiler)
###   3. Paste the code in the main.py tab
###   4. Click "Run" and follow the text prompts
###
###   How-To / Rules:
###   ---------------
###   The aim is to have a hand with a total value higher than the dealer’s without 
###   going over 21. Kings, Queens, Jacks and Tens are worth a value of 10. An Ace has 
###   the value of 1 or 11. The remaining cards are counted at face value.
###
###   Place a bet using the input provided. You are dealt two cards whilst the dealer 
###   is dealt one face up. If your first 2 cards add up to 21 (an Ace and a card valued 10), 
###   that’s Blackjack! If you have any other total, decide whether you wish to ‘hit’ or 
###   ‘stand’. You can continue to draw cards until you are happy with your hand.
###
###   You may "Double Down” your original stake on any two-card combination, however, 
###   you will only receive one more card. 
###
###   You can also “Split” any pair (including 
###   any two cards with a value of 10) by placing an additional bet equal to your original. 
###   You will then be dealt an additional card to each of your split cards to create two 
###   new hands.
###
###   For those of you familiar with the game, there is no "Insurance" feature yet.
###

import random
import time
from enum import Enum

### constants to define a deck of cards

values_ace_high = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11,
}

values_ace_low = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 1,
}

suits = (
    'Hearts',
    'Diamonds',
    'Spades',
    'Clubs',
)

ranks = (
    'Two',
    'Three',
    'Four',
    'Five',
    'Six',
    'Seven',
    'Eight',
    'Nine',
    'Ten',
    'Jack',
    'Queen',
    'King',
    'Ace',
)


#################################################################
###
###   Card class
###

class Card():
    def __init__(self, suit, rank, face_up):
        self.face_up = face_up
        self.suit = suit
        self.rank = rank
        self.value_ace_high = values_ace_high[rank.title()]
        self.value_ace_low = values_ace_low[rank.title()]

    def reveal(self):
        self.face_up = True
        return self
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

#################################################################
###
###   Deck class
###

class Deck():
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank,False))
    
    def shuffle_deck(self):
        random.shuffle(self.all_cards)
        
    def deal_one(self, reveal=True):
        if reveal:
            return self.all_cards.pop().reveal()
        else:
            return self.all_cards.pop()


#################################################################
###
###   utility enums, maps and functions for the Hand class
###

class HandStatus(Enum):
    active = 1
    standing = 2
    won_standard = 3
    won_blackjack = 4
    loss = 5
    tie = 6
    
settle_map = {
    HandStatus.won_standard: 1,
    HandStatus.won_blackjack: 1.5,
    HandStatus.loss: -1,
    HandStatus.tie: 0,
}

def settle_message(hand):
    if hand.status == HandStatus.won_standard:
        return f'Lucky! Hand {hand.name}, you won £{abs(hand.settle())}'
    elif hand.status == HandStatus.won_blackjack:
        f'Blackjack! Hand {hand.name}, you won £{abs(hand.settle())}'
    elif hand.status == HandStatus.loss:
        return f'Unlucky... hand {hand.name}, you lost £{abs(hand.settle())}'
    elif hand.status == HandStatus.tie:
        return f'It\'s a tie... Hand {hand.name}, bets are repaid.'
    else:
        return 'Something went wrong... in settle_message function'

class Actions(Enum):
    hit = 1,
    stand = 2,
    dd = 3,
    split = 4,
    insurance = 5
    
def actions_string_to_map(text):
    text = text.upper()
    if text == 'HIT': 
        return Actions.hit
    elif text == 'STAND': 
        return Actions.stand
    elif text == 'DD':
        return Actions.dd
    elif text == 'DOUBLE DOWN':
        return Actions.dd
    elif text == 'DOUBLEDOWN': 
        return Actions.dd
    elif text == 'SPLIT':
        return Actions.split
    elif text == 'INSURANCE': 
        return Actions.insurance
    else:
        return ''

actions_map_to_string = {
    Actions.hit: 'Hit',
    Actions.stand: 'Stand',
    Actions.dd: 'Double Down',
    Actions.split: 'Split',
    Actions.insurance: 'Insurance'
}

#################################################################
###
###   Hand class
###

class Hand():
    def __init__(self, name, initial_bet, is_split = False):
        self.name = name
        self.total_bet = initial_bet
        self.status = HandStatus.active
        self.cards = []
        self.is_split = is_split
    
    def double_down(self, new_card):
        self.total_bet *= 2
        self.hit(new_card)
        self.status = HandStatus.standing
    
    def hit(self, new_card):
        self.cards.append(new_card)
        
    def stand(self):
        self.status = HandStatus.standing
        
    def split_pop(self):
        self.name = self.name + 'a'
        self.is_split = True
        return self.cards.pop()
            
    def get_total_ace_high(self):
        total = 0
        for card in self.cards:
            if card.face_up:
                total += card.value_ace_high 
        return total
    
    def get_total_ace_low(self):
        total = 0
        for card in self.cards:
            if card.face_up:
                total += card.value_ace_low 
        return total
    
    def get_total(self):
        if self.get_total_ace_high() > 21:
            return self.get_total_ace_low()
        else:
            return self.get_total_ace_high()
        
    def check_is_bust(self):
        is_bust = self.get_total() > 21
        if is_bust:
            self.status = HandStatus.loss
        return is_bust
    
    def check_is_blackjack(self):
        is_blackjack = len(self.cards) == 2 and self.get_total() == 21
        if is_blackjack:
            self.status = HandStatus.standing
        return is_blackjack
    
    def settle(self):
        return round(settle_map[self.status] * self.total_bet)
    
    def settle_amount(self):
        return round((settle_map[self.status] * self.total_bet) + self.total_bet)
    
    def get_is_blackjack(self):
        return len(self.cards) == 2 and self.get_total() == 21
    
    def get_visible_cards(self):
        return list(filter(lambda card: card.face_up, self.cards))
    
    def __str__(self):
        visible_cards = self.get_visible_cards()
        msg = ''
        for i,card in enumerate(visible_cards):
            msg = msg + f'{card.rank}'
            if i != len(self.get_visible_cards())-1:
                msg = msg + ', '
                
        if 'Ace' in map(lambda card: card.rank, visible_cards):
            if self.get_total_ace_high() > 21:
                msg = msg + f': total {self.get_total_ace_low()}'
            elif self.get_total_ace_high() == 21:
                msg = msg + f': total {self.get_total_ace_high()}'
            else:
                msg = msg + f': total {self.get_total_ace_high()} -or- {self.get_total_ace_low()}'
        else:
            msg = msg + f': total {self.get_total()}'
        
        return msg

    
#################################################################
###
###   Player class
###

class Player():
    def __init__(self, name):
        self.name = name
        self.total_money = 500
        self.hands = []
    
    def init_new_hand(self, index):
        isValid = False
        message = f'Hand {len(self.hands)+1} - place your bet, minimum £50, you have £{self.total_money}: £'
        while not isValid:
            bet_str = input(message)
            try:
                bet_int = int(bet_str)
                if bet_int < 50:
                    message = 'Minimum bet is £50: '
                elif bet_int > self.total_money:
                    message = 'You dont have enough money for that... '
                else:  
                    new_hand = Hand(name=f'{index}', initial_bet=bet_int)
                    self.hands.append(new_hand)
                    self.update_money(-bet_int)
                    isValid = True
                    return new_hand
            except:
                message = 'Invalid input, enter a whole number: '
        
    def split_hand(self, index, orig_hand):
        new_hand = Hand(name=f'{index}b', initial_bet=orig_hand.total_bet, is_split=True)
        new_hand.hit(orig_hand.split_pop())
        self.hands.insert(index, new_hand)
        self.update_money(-orig_hand.total_bet)
        return (orig_hand, new_hand)
    
    def get_available_actions(self, hand):
        if hand.status == HandStatus.standing:
            return []
        else:
            # double down and split only available on first 2 cards
            if len(hand.cards) == 2:
                actions = [Actions.hit, Actions.stand, Actions.dd]
                # prevent split if is_split flag True or if not enough money to match original bet
                if not hand.is_split or (self.total_money > hand.total_bet):
                    # allow split if pair
                    if hand.cards[0].rank == hand.cards[1].rank:
                        actions.append(Actions.split)
                    # allow split if two 10 value cards 
                    elif hand.cards[0].value_ace_high == hand.cards[1].value_ace_high:
                        actions.append(Actions.split)
                return actions
            # if more than 2 cards you can only hit or stand
            else:
                return [Actions.hit, Actions.stand]
        
    def update_money(self, amount):
        self.total_money += amount
        
    def get_active_hands(self):
        return list(filter(lambda hand: hand.status == HandStatus.active, self.hands))

    def get_standing_hands(self):
        return list(filter(lambda hand: hand.status == HandStatus.standing, self.hands))
        
#################################################################
###
###   Main function
###

def play_blackjack():        
    
    # instantiate players
    p1_name = input('Please enter your name: ')
    p1 = Player(p1_name)
        
    # While loop to allow user to exit game
    game_on = True
    while game_on: 
        
        # instantiate deck and shuffle it
        new_deck = Deck()
        new_deck.shuffle_deck()
        
        # reset player hands
        p1.hands = []
        
        # init first hand
        p1.init_new_hand(1)

        # add another hand?
        # maximum of 3 hands at at ime, if no more money left shouldnt ask for another hand
        message = 'Do you want to add another hand? Enter Y or N: '
        idx = 2
        while len(p1.hands) < 3 and p1.total_money >= 50:
            result = input(message).upper()
            if result == 'Y':
                new_hand = p1.init_new_hand(idx)
                idx += 1
            elif result == 'N': 
                break
            else: 
                message = 'Invalid input, enter Y or N: '
        
        # deal initial cards
        for hand in p1.hands:
            hand.hit(new_deck.deal_one())
            hand.hit(new_deck.deal_one())
            print(f'Hand {hand.name} - {hand}')

        # instantiate dealer hand and deal initial cards
        dealer_hand = Hand(0, 0)
        dealer_hand.hit(new_deck.deal_one())
        dealer_hand.hit(new_deck.deal_one(reveal=False))
        print(f'Dealer hand - {dealer_hand}')

        # check player blackjack
        for hand in p1.hands:
            hand.check_is_blackjack()

        # Player turns
        i = 0
        while len(p1.get_active_hands()) > 0:
            hand = p1.get_active_hands()[0]
            message = f'Hand {hand.name} -'
            while hand.status == HandStatus.active:
                
                actions = p1.get_available_actions(hand)
                actions_text = ''
                
                for action_ind,action in enumerate(actions):
                    action = actions_map_to_string[action]
                    actions_text += action
                    if action_ind != len(actions) - 1:
                        actions_text += ', '
                actions_text += ': '
                
                result = actions_string_to_map(input(f'{message} {actions_text}'))
                
                # validate input result is in the available actions:
                if result not in actions:
                    message = 'Invalid input, enter'
                
                else:
                    # hit
                    if result == Actions.hit:
                        hand.hit(new_deck.deal_one())
                        if hand.check_is_bust():
                            print(f'Bust... Final hand {hand.name} - {hand}')
                        else:
                            print(f'Hand {hand.name} - {hand}')
                    # stand
                    elif result == Actions.stand:
                        hand.stand()
                        print(f'Final hand {hand.name} - {hand}')
                    # double down
                    elif result == Actions.dd:
                        hand.double_down(new_deck.deal_one())
                        print(f'Double down! Bet increased to £{hand.total_bet}. Final hand {hand.name} - {hand}')
                        hand.check_is_bust()
                    # split
                    else:
                        # check enough money to match original bet
                        if p1.total_money >= hand.total_bet:
                            print(f'You split hand {hand.name}...')
                            split_hands = p1.split_hand(i+1, hand)
                            print(f'Hand {split_hands[0].name} - {split_hands[0]}')
                            print(f'Hand {split_hands[1].name} - {split_hands[1]}')
                            break
                        else:
                            print('You dont have enough money to match your original bet.')
            i += 1
        
        # small delay
        delay = 0.5
        time.sleep(delay)

        # If hands remain, dealer draws their cards
        if len(p1.get_standing_hands()) != 0:
            dealer_hand.cards[1].reveal()
            print(f'Dealer hand - {dealer_hand}')
            time.sleep(delay)
            
            # Dealer always draws cards if their total is below 16
            while dealer_hand.get_total() <= 16:
                dealer_hand.hit(new_deck.deal_one())
                print(f'Dealer hand - {dealer_hand}')
                time.sleep(delay)

        # Assign win/loss status to each hand:
        # If a hand goes bust, they always lose their bet, regardless of the dealers hand.
        # If the dealer and the player had the same score, its a tie and the bets are repaid.
        # Otherwise the highest hand wins.
        # A blackjack win by the player is paid 3:2, all other wins are paid 1:1.
        for i,hand in enumerate(p1.hands):

            # player bust = loss
            if hand.get_total() > 21:
                hand.status = HandStatus.loss

            # otheriwse dealer bust = win
            # but need to differentiate a blackjack win due to different odds/winnings
            elif dealer_hand.get_total() > 21:
                    # blackjack win
                    if (len(hand.cards) == 2 and hand.get_total()) == 21:
                        hand.status = HandStatus.won_blackjack
                    # regular win
                    else:
                        hand.status = HandStatus.won_standard

            # neither player or dealer are bust (i.e. both score < 21)
            else:
                # if their score is equal its a tie
                # except for when one has blackjack and the other doesnt
                if hand.get_total() == dealer_hand.get_total():
                    # blackjack only possible with 2 cards
                    if len(hand.cards) == 2 and len(dealer_hand.cards) != 2:
                        hand.status = HandStatus.won_blackjack
                    elif len(hand.cards) != 2 and len(dealer_hand.cards) == 2:
                        hand.status = HandStatus.loss
                    else:
                        hand.status = HandStatus.tie

                # otherwise, highest score wins
                elif hand.get_total() > dealer_hand.get_total():
                    hand.status = HandStatus.won_standard
                else:
                    hand.status = HandStatus.loss

            # update player money
            p1.update_money(hand.settle_amount())

            print(settle_message(hand))
        
        # if no money left then end the game
        if p1.total_money < 50:
            print('Game over... you ran out of money.')
            print('Thanks for playing')
            game_on = False
            break
        else:
            # play again?
            play_again_message = f'{p1.name}, you have £{p1.total_money}. Do you want to play again? Enter Y or N: '
            while True:
                play_again = input(play_again_message)
                if play_again.upper() == 'Y':
                    break
                elif play_again.upper() == 'N':
                    print('Thanks for playing.')
                    game_on = False
                    break
                else:
                    play_again_message = 'Invalid input, enter Y or N: '

play_blackjack()
