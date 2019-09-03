from random import randint
class Deck(): #will hold cards for game
    def __init__(self):
        self.cards = []
        for index in range(1,14):
            for _ in range(1,5):
                self.cards.append(index) #adds one number for each card in game. This game has 1 deck of 52 cards, with the index representing the card number
        for index,card in enumerate(self.cards): #certain cards are assigned to be face cards
            if card == 1:
                self.cards[index] = 'Ace'
            elif card == 11:
                self.cards[index] = 'Jack'
            elif card == 12:
                self.cards[index] = 'Queen'
            elif card == 13:
                self.cards[index] = 'King'
    def remove_card(self):
        while True:
            card_num = randint(1,13)
            if card_num == 1:
                if 'Ace' in self.cards: #this statement makes sure the numb generated is still available in the deck
                    self.cards.remove('Ace')
                    return 'Ace'
                    break
            elif card_num == 11:
                if 'Jack' in self.cards:
                    self.cards.remove('Jack')
                    return 'Jack'
                    break
            elif card_num == 12:
                if 'Queen' in self.cards:
                    self.cards.remove('Queen')
                    return 'Queen'
                    break
            elif card_num == 13:
                if 'King' in self.cards:
                    self.cards.remove('King')
                    return 'King'
                    break
            else:
                if card_num in self.cards:
                    self.cards.remove(card_num)
                    return card_num
                    break
class Bankroll(): #keeps track of the player's money
    def __init__(self):
        self.money = 100
    def get_bet(self):
        print(f'You have ${self.money} available')
        while True:
            bet = int(input('Input your bet: '))
            if bet <= self.money:
                self.money -= bet
                print('Bet accepted')
                return bet
            else: #Special case where the player tries to bet more money than they have
                print("You don't have that kind of money")
    def add_prize(self, prize):
        self.money += prize
    def get_money(self):
        return self.money
class PlayerHand():
    def __init__(self):
        self.player_cards = []
        self.player_value = 0
    def add_card(self,card):
        self.player_cards.append(card)
        if type(card) == int: #number card case
            self.player_value += card
        #Jack queen and king case
	elif card != 'Ace':
            self.player_value += 10
        else: #Ace case allows player to choose if ace is 1 or 11 points
            print('You got an Ace!')
            while True:
                ace_value = int(input('Would you like your ace to be worth 1 or 11 points? '))
                if ace_value == 1 or ace_value == 11:
                    self.player_value += ace_value
                    self.player_cards[-1] = 'Ace (' + str(ace_value) + ')' #For easy reference, the card is relabeled to have the point value right next to it
                    break
                else:
                    print('Not accepted value') #In case the player types a nonaccepted value
    def check_win(self): #Checks if the player has 21 points
        if self.player_value == 21:
            return True
        else:
            return False
    def check_lose(self):
        if self.player_value > 21:
            return True
        else:
            return False
    def get_player_value(self):
        return self.player_value
    def print_player_cards(self):
        print(f'Player cards: {self.player_cards}')
class DealerHand():
    def __init__(self):
        self.dealer_cards = []
        self.dealer_value = 0
    def add_card(self,card):
        self.dealer_cards.append(card)
        if card == 'Hidden': #At the beginning, the dealer traditionally gets a facedown card, which Hidden represents
            self.dealer_value += 0 #The point value isn't counted since we don't know what the card is
        elif type(card) == int:
            self.dealer_value += card
        elif card != 'Ace':
            self.dealer_value += 10
        else: #Ace case, algorithm only counts it as 11 if the dealer won't bust in doing so
            if self.dealer_value <= 10:
                self.dealer_value += 11
            else:
                self.dealer_value += 1
    def check_win(self):
        if self.dealer_value == 21:
            return True
        else:
            return False
    def check_lose(self):
        if self.dealer_value > 21:
            return True
        else:
            return False
    def get_dealer_value(self):
        return self.dealer_value
    def print_dealer_cards(self):
        print(f'Dealer cards: {self.dealer_cards}')
    def remove_hidden(self): #Removes Hidden and replaces it with an actual card
        for card in self.dealer_cards:
            if card == 'Hidden':
                self.dealer_cards.remove('Hidden')
player_bank = Bankroll()
print('Welcome to Blackjack!')
while True:
    if player_bank.get_money() == 0:
        print('You ran out of money!')
        break
    if input('Would you like to play Blackjack? (Y or N) ') == 'N':
        break
    my_deck = Deck()
    player_hand = PlayerHand()
    dealer_hand = DealerHand()
    current_bet = player_bank.get_bet()
    def player_won():
	#these variables are global so they can be used and edited outside the method
        global player_hand
        global dealer_hand
        global current_bet
        global player_bank
        print('The player has won!')
        player_hand.print_player_cards()
        dealer_hand.print_dealer_cards()
        player_bank.add_prize(2 * current_bet)
    def dealer_won():
        global player_hand
        global dealer_hand
        global current_bet
        global player_bank
        print('The dealer has won!')
        dealer_hand.print_dealer_cards()
        player_hand.print_player_cards()
    player_hand.add_card(my_deck.remove_card())
    player_hand.add_card(my_deck.remove_card())
    if player_hand.check_win(): #in the case that the player got Ace and a face card
        player_won()
        continue
    dealer_hand.add_card(my_deck.remove_card())
    dealer_hand.add_card('Hidden') #Note that Hidden is a placeholder for a card
    dealer_hand.print_dealer_cards()
    player_hand.print_player_cards()
    choice = 0
    while choice != 2:
        choice = int(input('Press 1 to hit or 2 to stay: '))
        if choice == 1:
            player_hand.add_card(my_deck.remove_card())
            if player_hand.check_win():
                player_won()
                break
            elif player_hand.check_lose():
                dealer_won()
                break
            else:
                player_hand.print_player_cards()
    #this line of code is to skip to the beginning of the game, which we couldn't do in a decision construct
    if player_hand.check_win() or player_hand.check_lose():
        continue
    dealer_hand.remove_hidden()
    dealer_hand.add_card(my_deck.remove_card()) #Hidden replacement is added
    if dealer_hand.check_win():
        dealer_won()
        continue
    while dealer_hand.get_dealer_value() < 17:
        dealer_hand.add_card(my_deck.remove_card())
        print('The dealer hit!')
    if dealer_hand.check_win():
        dealer_won()
        continue
    elif dealer_hand.check_lose():
        player_won()
        continue
    #at this point neither person has busted nor has 21, so their point values are compared
    elif player_hand.get_player_value() > dealer_hand.get_dealer_value():
        player_won()
        continue
    elif player_hand.get_player_value() < dealer_hand.get_dealer_value():
        dealer_won()
        continue
    else: #Tie case
        print('Tie!')
        player_hand.print_player_cards()
        dealer_hand.print_dealer_cards()
        player_bank.add_prize(current_bet)

