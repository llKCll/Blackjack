import tkinter as tk
from CardLabel import *
from tkinter.messagebox import showinfo, showerror, askquestion, ERROR
from Card import *
from Deck import *

app = tk.Tk()
CardLabel.load_images()
class BlackjackFrame(tk.Frame):
    '''BlackjackGame fully encapsulated'''
    
    def __init__(self, parent):
        '''defines blackjack game'''
        tk.Frame.__init__(self, parent)

        # Create deck and shuffle.
        self._cards = Deck()
        self._cards.shuffle()
        
        # The deck and the hands are lists.
        self._player_hand = self._cards.deal(2)
        self._dealer_hand = self._cards.deal(2)
        
        # Set initial display up. dc = dealer card and pc = player card.

        dealer_label = tk.Label(self, text='Dealer')
        dealer_label.grid(row=0, column=0, sticky=tk.W, padx = 20, pady = 20)

        self.dc1 = CardLabel(self)
        self.dc1.grid(row = 1, column = 0)
        self.dc1.display('back', self._dealer_hand[0].key())
        
        self.dc2 = CardLabel(self)
        self.dc2.grid(row = 1, column = 1)
        self.dc2.display('back', self._dealer_hand[1].key())
        
        self.dc3 = CardLabel(self)
        self.dc3.grid(row = 1, column = 2)
        self.dc3.display('blank')
        
        self.dc4 = CardLabel(self)
        self.dc4.grid(row = 1, column = 3)
        self.dc4.display('blank')
        
        self.dc5 = CardLabel(self)
        self.dc5.grid(row = 1, column = 4)
        self.dc5.display('blank')
        
        self.dc6 = CardLabel(self)
        self.dc6.grid(row = 1, column = 5)
        self.dc6.display('blank')

        player_label = tk.Label(self, text='You')
        player_label.grid(row=3, column=0, sticky=tk.W, padx = 20, pady = 20)

        self.pc1 = CardLabel(self)
        self.pc1.grid(row=4, column=0)
        self.pc1.display('back', self._player_hand[0].key())
        
        self.pc2 = CardLabel(self)
        self.pc2.grid(row = 4, column = 1)
        self.pc2.display('back', self._player_hand[1].key())

        self.pc3 = CardLabel(self)
        self.pc3.grid(row = 4, column = 2)
        self.pc3.display('blank')
        
        self.pc4 = CardLabel(self)
        self.pc4.grid(row = 4, column = 3)
        self.pc4.display('blank')
        
        self.pc5 = CardLabel(self)
        self.pc5.grid(row = 4, column = 4)
        self.pc5.display('blank')
        
        self.pc6 = CardLabel(self)
        self.pc6.grid(row = 4, column = 5)
        self.pc6.display('blank')
        
        # Keep score and buy in.
        self.bet = 0
        self.balance = 0
        self.pcscore = 0
        self.urscore = 0

        # Balance and bet labels.
        balance_label = tk.Label(self, text='Balance:')
        balance_label.grid(row=5, column=0, pady = 20)
        self.balance_label = tk.Label(self, text='$'+str(self.balance))
        self.balance_label.grid(row=5, column=1, padx=20, pady = 20)

        bet_label = tk.Label(self, text='Bet:')
        bet_label.grid(row=5, column=2, pady = 20)
        self.bet_label = tk.Label(self, text='$'+str(self.bet))
        self.bet_label.grid(row=5, column=3, padx=20, pady=20)

        # Dealer and player score labels
        pcscore_label = tk.Label(self, text='Dealer Score:')
        pcscore_label.grid(row=5, column=4, padx = 20, pady = 20)
        self.pcscore_label = tk.Label(self, text=self.pcscore)
        self.pcscore_label.grid(row=5, column=5, padx = 20, pady = 20)

        urscore_label = tk.Label(self, text='Your Score:')
        urscore_label.grid(row=5, column=6, padx = 20, pady = 20)
        self.urscore_label = tk.Label(self, text=self.urscore)
        self.urscore_label.grid(row=5, column=7, padx = 20, pady = 20)

        self.balance_entry = tk.Entry(self)
        self.balance_entry.grid(row=6, column=1, padx = 20)
        self.bet_entry = tk.Entry(self)
        self.bet_entry.grid(row=6, column=3, padx = 20)
        
        # Buttons.
        self.balcb = tk.Button(self, text='Buy-in', command=self.buy_in) 
        self.balcb.grid(row=6, column=0)
        self.betcb = tk.Button(self, text='Bet', command=self.bet_press) 
        self.betcb.grid(row=6, column=2)
        self.dealcb = tk.Button(self, text='Deal', command=self.deal)
        self.dealcb.grid(row=7, column=1, pady = 30, padx = 20)
        self.hitcb = tk.Button(self, text='Hit', command=self.hit, state=DISABLED) 
        self.hitcb.grid(row=7, column=2, pady = 30, padx = 20)
        self.standcb = tk.Button(self, text='Stand', command=self.stand, state=DISABLED) 
        self.standcb.grid(row=7, column=3, pady = 30, padx = 20)

    def turn_on(self):
        ''' Configure button status while game in progress'''
        self.betcb.configure(state=DISABLED)
        self.balcb.configure(state=DISABLED)
        self.dealcb.configure(state=DISABLED)
        self.hitcb.configure(state=NORMAL)
        self.standcb.configure(state=NORMAL)                  
        return

    def turn_off(self):
        ''' Configure button status while game is in break'''
        self.betcb.configure(state=NORMAL)
        self.balcb.configure(state=NORMAL)
        self.dealcb.configure(state=NORMAL)
        self.hitcb.configure(state=DISABLED)
        self.standcb.configure(state=DISABLED)
        return

    def hit(self):
        '''Request another card from the dealer to be drawn.
           If players busts, the player automatically loses.
           Displays message when a bust occurs.
        '''
        # Must have enough money in balance to bet.
        if self.balance >= self.bet and self.bet != 0:
            p_score = self.total(self._player_hand)
            d_score = self.total(self._dealer_hand)

            # Get number of cards in Player's hand. Subtract 2 to correct for the two drawn in the Computer's hand.
            crdsDrawn =  52 - len(self._cards) - 2

            if crdsDrawn <= 6:
                # Used to select which card to flip over. Use cards drawn from the deck to get the index here. 
                player_flip_list = [ self.pc3, self.pc4, self.pc5, self.pc6 ]
                
                # Draw a card from the deck and put it in the Player's hand.
                draw = self._cards.deal(1)
                self._player_hand.extend(draw)

                # To get the index subtract 2 from cards drawn in hand. Note when crdsDrawn is defined and Player draws a card afterward.
                showCard = player_flip_list[crdsDrawn-2]
                crdnHand = self._player_hand[crdsDrawn].key()
                showCard.display('front', crdnHand)
        
                # Tally up total in player's hand.
                p_score = self.total(self._player_hand)
                
            # Player went over 21. Player loses.
            if p_score > 21:
                self.turn_off()
                winner = False
                self.score(winner)
                self.calc_bal(winner)
                showinfo(title = 'Bust', message = "Bust! You've been defeated. Better luck next time.")
                
        elif self.balance < self.bet:
            showinfo(title = 'Need Money!', message = "You must add more money to balance first.")
        
    def bet_press(self):
        ''' Checks for all numbers and updates current bet.
        '''
        cur_bet = self.bet_entry.get()
        # Must be an integer.
        if cur_bet.isdigit():
            self.bet = int(cur_bet)
            self.bet_label.config(text='$'+str(self.bet))
        
    def buy_in(self):
        ''' Add money to balance to keep playing.
        '''
        add = self.balance_entry.get()
        if add.isdigit():
            self.balance += int(add)
            self.balance_label.config(text='$'+str(self.balance))
 
        
    def total(self, hand):
        '''Returns the total value of the BlackJack hand
           Args - A player's hand as a list.
        '''
        values = { 0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7,
                   6: 8, 7: 9, 8: 10, 9: 10, 10: 10,
                   11: 10, 12: 11 }
        total_hand = 0
        num_Ace = 0
        for card in hand:
            total_hand += values[card.rank()]
            if card.rank() == 12:
                num_Ace += 1
        while total_hand > 21 and num_Ace > 0:
            total_hand -= 10
            num_Ace -= 1
        return total_hand
        
    def deal(self):
        '''Resets the game.'''
        # Flip lists to keep track of next card to flip over for player and dealer.
        player_flip_list = [ self.pc3, self.pc4, self.pc5, self.pc6 ]
        dealer_flip_list = [ self.dc3, self.dc4, self.dc5, self.dc6 ]
        if self.balance >= self.bet and self.bet != 0:
            self.turn_on()
            # Flip first three cards face up. 
            self.dc2.display('front', self._dealer_hand[1].key())
            self.pc1.display('front', self._player_hand[0].key())
            self.pc2.display('front', self._player_hand[1].key())
            # Return cards to the deck from Player and Dealer's hands then shuffle.
            self._cards.restore(self._player_hand)
            self._cards.restore(self._dealer_hand)
            self._cards.shuffle()
            # Redraw from deck.
            self._player_hand = self._cards.deal(2)
            self._dealer_hand = self._cards.deal(2)
            # Set display back up with new dealt cards.
            self.dc1.display('back', self._dealer_hand[0].key())
            self.dc2.display('front', self._dealer_hand[1].key())
            self.pc1.display('front', self._player_hand[0].key())
            self.pc2.display('front', self._player_hand[1].key())
            # Display blank for unused labels            
            while len(player_flip_list) > 0:
                dealer_flip_list[0].display('blank')
                player_flip_list[0].display('blank')
                player_flip_list.pop(0)
                dealer_flip_list.pop(0)
                
        elif self.balance < self.bet:
            showinfo(title = 'Need Money!', message = "You must add more money to balance first.")
        
    def check_bj(self):
        ''' Checks both dealer and player for BlackJack then annunces the winner.
            If dealer and player both have BlackJack, dealer always wins.
        '''
        p_score = self.total(self._player_hand)
        d_score = self.total(self._dealer_hand)
        if d_score == 21 and p_score == 21:
            self.dc1.display('front', self._dealer_hand[0].key())
            showinfo(title='Tie', message="It's a draw!")
            return True
        elif d_score == 21:
            winner = False
            self.score(winner)
            self.calc_bal(winner)
            self.dc1.display('front', self._dealer_hand[0].key())
            showinfo(title = 'Dealer Wins', message = "You lose! Dealer has BlackJack!")
            return True
        elif p_score == 21:
            winner = True
            self.score(winner)
            self.calc_bal(winner)
            self.dc1.display('front', self._dealer_hand[0].key())
            showinfo(title = 'Player Wins', message = "BlackJack! You've won!")
            return True
        return False
        
    def stand(self):
        '''Show the dealers hand and stay where you're at.
           Display message who wins.
        '''
        dealer_flip_list = [self.dc3, self.dc4, self.dc5, self.dc6]
        self.turn_off()
        # Does the player have enough to play? Used mostly if stand is selected blind.
        if self.balance >= self.bet and self.bet != 0:
            # Get total in hand busted or not.
            p_score = self.total(self._player_hand)
            d_score = self.total(self._dealer_hand)
            
            # Flip the dealer's first face down card up.
            self.dc1.display('front', self._dealer_hand[0].key())
            
            while d_score < 17:
                # Computer draws a card and puts it in their hand.
                draw = self._cards.deal(1)
                self._dealer_hand.extend(draw)
                # Display the last card just added to the hand.
                dealer_flip_list[0].display('front', self._dealer_hand[-1].key())
                # Pop first element since we don't need it anymore. We'll use the next element in it's spot next.
                dealer_flip_list.pop(0)
                d_score = self.total(self._dealer_hand)
            
            # Returns True if player or dealer has BlackJack.
            if self.check_bj():
                return
            # The dealer busted.
            elif d_score > 21:
                self.score(winner=True)
                self.calc_bal(winner=True)
                showinfo(title = 'Player Wins', message = "The dealer busted! You've won!")
            # Got the same score except neither got BlackJack.
            elif p_score == d_score:
                showinfo(title = 'Tie', message = "It's a draw!")
            # You have a lesser score, player loses.
            elif p_score < d_score:
                self.score(winner=False)
                self.calc_bal(winner=False)
                showinfo(title = 'Dealer Wins', message = "You've been defeated! Better luck next time.")
            # Player got 21. 
            else:
                self.score(winner=True)
                self.calc_bal(winner=True)
                showinfo(title = 'Player Wins', message = "You're victorious!")
            
    def score(self, winner):
        '''Updates label with score. Winner will be True if player wins. False if computer wins.
           Args - Who won the hand.
           Effects - Updates score labels.
        '''
        if winner == True:
            self.urscore += 1
            self.urscore_label.config(text=self.urscore)
        else:
            self.pcscore += 1
            self.pcscore_label.config(text=self.pcscore)
            

            
    def calc_bal(self, winner):
        ''' Adds or subtracts balance based on who won.
            Args- winner is True if player wins
                  False if dealer wins.
        '''
        if winner == True:
            self.balance += self.bet
        else:
            self.balance -= self.bet 
        self.balance_label.config(text='$'+str(self.balance))
                       

BlackjackFrame(app).pack()       

