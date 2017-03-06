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
        self.count = 0
        #set deck and hands up
        self._cards = Deck()
        self._cards.shuffle()
        #these are lists
        self._player_hand = self._cards.deal(2)
        self._dealer_hand = self._cards.deal(2)
        #set initial display up dc = dealer card pc = player card
        self.dc1 = CardLabel(self)
        self.dc1.grid(row = 0, column = 0)
        self.dc1.display('back', self._dealer_hand[0].key())
        self.dc2 = CardLabel(self)
        self.dc2.grid(row = 0, column = 1)
        self.dc2.display('back', self._dealer_hand[1].key())
        self.dc3 = CardLabel(self)
        self.dc3.grid(row = 0, column = 2)
        self.dc3.display('blank')
        self.dc4 = CardLabel(self)
        self.dc4.grid(row = 0, column = 3)
        self.dc4.display('blank')
        self.dc5 = CardLabel(self)
        self.dc5.grid(row = 0, column = 4)
        self.dc5.display('blank')
        self.dc6 = CardLabel(self)
        self.dc6.grid(row = 0, column = 5)
        self.dc6.display('blank')
        self.pc1 = CardLabel(self)
        self.pc1.grid(row = 1, column = 0)
        self.pc1.display('back', self._player_hand[0].key())
        self.pc2 = CardLabel(self)
        self.pc2.grid(row = 1, column = 1)
        self.pc2.display('back', self._player_hand[1].key())
        self.pc3 = CardLabel(self)
        self.pc3.grid(row = 1, column = 2)
        self.pc3.display('blank')
        self.pc4 = CardLabel(self)
        self.pc4.grid(row = 1, column = 3)
        self.pc4.display('blank')
        self.pc5 = CardLabel(self)
        self.pc5.grid(row = 1, column = 4)
        self.pc5.display('blank')
        self.pc6 = CardLabel(self)
        self.pc6.grid(row = 1, column = 5)
        self.pc6.display('blank')
        #keep score and buy in
        self.bet = 0
        self.balance = 0
        self.pcscore = 0
        self.urscore = 0
        self.balance_entry = tk.Entry(self)
        self.balance_entry.grid(row=3, column=1, padx = 20)
        self.bet_entry = tk.Entry(self)
        self.bet_entry.grid(row=3, column=3, padx = 20)
        self.balance_label = tk.Label(self, text='$'+str(self.balance))
        self.balance_label.grid(row=2, column=1, sticky=tk.W, padx = 20, pady = 20)
        self.bet_label = tk.Label(self, text='$'+str(self.bet))
        self.bet_label.grid(row=2, column=3, sticky=tk.W, padx = 20, pady = 20)
        self.urscore_label = tk.Label(self, text=self.urscore)
        self.urscore_label.grid(row=2, column=7, sticky=tk.W, padx = 20, pady = 20)
        self.pcscore_label = tk.Label(self, text=self.pcscore)
        self.pcscore_label.grid(row=2, column=5, sticky=tk.W, padx = 20, pady = 20)
        bet_label = tk.Label(self, text='Bet:')
        bet_label.grid(row=2, column=2, sticky=tk.W, padx = 20, pady = 20)
        balance_label = tk.Label(self, text='Balance:')
        balance_label.grid(row=2, column=0, sticky=tk.W, padx = 20, pady = 20)
        pcscore_label = tk.Label(self, text='Dealer Score:')
        pcscore_label.grid(row=2, column=4, sticky=tk.W, padx = 20, pady = 20)
        urscore_label = tk.Label(self, text='Your Score:')
        urscore_label.grid(row=2, column=6, sticky=tk.W, padx = 20, pady = 20)
        #flip lists
        self.player_flip_list = [self.pc3, self.pc4, self.pc5, self.pc6]
        self.dealer_flip_list = [self.dc3, self.dc4, self.dc5, self.dc6]
        #buttons
        betcb = tk.Button(self, text='Bet', command=self.bet_press) 
        betcb.grid(row=3, column=2)
        balcb = tk.Button(self, text='Buy-in', command=self.buy_in) 
        balcb.grid(row=3, column=0)
        dealcb = tk.Button(self, text='Deal', command=self.deal) 
        dealcb.grid(row=4, column=1, pady = 30, padx = 70)
        hitcb = tk.Button(self, text='Hit', command=self.hit) 
        hitcb.grid(row=4, column=2, pady = 30, padx = 70)
        standcb = tk.Button(self, text='Stand', command=self.stand) 
        standcb.grid(row=4, column=3, pady = 30, padx = 70)
        
    def bet_press(self):
        ''' checks for all numbers and updates current bet
        '''
        cur_bet = self.bet_entry.get()
        if cur_bet.isalnum():
            cur_bet = int(cur_bet)
            self.bet = cur_bet
            self.bet_label.config(text='$'+str(self.bet))
        if self.balance >= self.bet and self.bet != 0:
            self.dc2.display('front', self._dealer_hand[1].key())
            self.pc1.display('front', self._player_hand[0].key())
            self.pc2.display('front', self._player_hand[1].key())
            self.check_bj()
        elif self.balance < self.bet:
            showinfo(title = 'Need Money!', message = "You must add more money to balance first.")
        
    def buy_in(self):
        ''' add money to balance to keep playing
        '''
        add = self.balance_entry.get()
        if add.isalnum():
            add = int(add)
            self.balance += add
            self.balance_label.config(text='$'+str(self.balance))
        if self.balance >= self.bet and self.bet != 0:
            self.dc2.display('front', self._dealer_hand[1].key())
            self.pc1.display('front', self._player_hand[0].key())
            self.pc2.display('front', self._player_hand[1].key())
            self.check_bj()
        elif self.balance < self.bet:
            showinfo(title = 'Need Money!', message = "You must add more money to balance first.")
        
    def rank(self, acard):
        '''args- a card
           returns a cards rank
        '''
        ranked = acard.key()
        if ranked > 12:
            ranked = ranked % 13
            return ranked
        else:
            return ranked
        
    def total(self, hand):
        '''returns the value of the blackjack hand'''
        values = {0:2, 1:3, 2:4, 3:5, 4:6, 5:7, 6:8, 7:9, 8:10, 9:10, 10:10, 11:10, 12:11}
        total_hand = 0
        num_Ace = 0
        for cards in hand:
            total_hand += values[self.rank(cards)]
            if self.rank(cards) == 12:
                num_Ace += 1
        while total_hand > 21 and num_Ace > 0:
            total_hand -= 10
            num_Ace -= 1
        return total_hand
        
    def deal(self):
        '''resets the game'''
        if self.balance >= self.bet and self.bet != 0: 
            self.count = 0
            self._cards.restore(self._player_hand)
            self._cards.restore(self._dealer_hand)
            self._cards.shuffle()
            self._player_hand = self._cards.deal(2)
            self._dealer_hand = self._cards.deal(2)
            self.dc1.display('back', self._dealer_hand[0].key())
            self.dc2.display('front', self._dealer_hand[1].key())
            self.pc1.display('front', self._player_hand[0].key())
            self.pc2.display('front', self._player_hand[1].key())
            for i in range(2,6):
                self.dealer_flip_list[self.count].display('blank')
                self.player_flip_list[self.count].display('blank')
                self.count += 1
            self.count = 0
            self.check_bj()
        elif self.balance < self.bet:
            showinfo(title = 'Need Money!', message = "You must add more money to balance first.")
        
    def check_bj(self):
        ''' checks for automatic BlackJack when the game is restarted
            If dealer and player both have BlackJack, dealer always wins
        '''
        p_score = self.total(self._player_hand)
        d_score = self.total(self._dealer_hand)
        if d_score == 21:
            self.score(winner=False)
            self.calc_bal(winner=False)
            self.dc1.display('front', self._dealer_hand[0].key())
            showinfo(title = 'Dealer Wins', message = "You lose! Dealer has BlackJack!")
        elif p_score == 21:
            self.score(winner=True)
            self.calc_bal(winner=True)
            self.dc1.display('front', self._dealer_hand[0].key())
            showinfo(title = 'Player Wins', message = "BlackJack! You've won!")
        
        
    def stand(self):
        '''show the dealers hand and stay where you're at
           display message who wins
        '''
        if self.balance >= self.bet and self.bet != 0:
            p_score = self.total(self._player_hand)
            d_score = self.total(self._dealer_hand)
            self.count = 0
            self.dc1.display('front', self._dealer_hand[0].key())
            for i in range(2,6):
                if d_score < 17:
                    draw = self._cards.deal(1)
                    self._dealer_hand.extend(draw)
                    self.dealer_flip_list[self.count].display('front', self._dealer_hand[i].key())
                    self.count += 1
                    d_score = self.total(self._dealer_hand)
            if d_score > 21:
                self.score(winner=True)
                self.calc_bal(winner=True)
                showinfo(title = 'Player Wins', message = "The dealer busted! You've won!")
            elif p_score == d_score:
                showinfo(title = 'Tie', message = "It's a draw!")
            elif p_score < d_score:
                self.score(winner=False)
                self.calc_bal(winner=False)
                showinfo(title = 'Dealer Wins', message = "You've been defeated! Better luck next time.")
            else:
                self.score(winner=True)
                self.calc_bal(winner=True)
                showinfo(title = 'Player Wins', message = "You're victorious!")
            
    def score(self, winner):
        '''updates label with score. Winner will be true if player wins. False if computer wins.
           args - who won the hand
           effects - updates score labels
        '''
        if winner == True:
            self.urscore += 1
            self.urscore_label.config(text=self.urscore)
        else:
            self.pcscore += 1
            self.pcscore_label.config(text=self.pcscore)
            
    def hit(self):
        '''add another card to your hand
           if players busts, you automatically lose
           displays message if you bust
        '''
        if self.balance >= self.bet and self.bet != 0:
            p_score = self.total(self._player_hand)
            d_score = self.total(self._dealer_hand)
            if self.count <= 3:
                card_index = [2, 3, 4, 5]
                draw = self._cards.deal(1)
                self._player_hand.extend(draw)
                self.player_flip_list[self.count].display('front', self._player_hand[card_index[self.count]].key())
                self.count += 1
                p_score = self.total(self._player_hand)
            if p_score > 21:
                self.score(winner=False)
                self.calc_bal(winner=False)
                showinfo(title = 'Bust', message = "Bust! You've been defeated! Better luck next time.")
        elif self.balance < self.bet:
            showinfo(title = 'Need Money!', message = "You must add more money to balance first.")
            
    def calc_bal(self, winner):
        ''' adds or subtracts balance based on who won
            args- winner is true if player wins
                  False if dealer wins.
        '''
        if winner == True:
            self.balance += self.bet
        else:
            self.balance -= self.bet 
        self.balance_label.config(text='$'+str(self.balance))
                       

BlackjackFrame(app).pack()       
