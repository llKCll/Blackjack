
from Card import *
from random import shuffle


class Deck(list):
    ''' A class to represent a list of a standard deck of cards'''
    
    def __init__(self):
        '''Creates a list with 52 cards as objects'''
        list.__init__(self)
        for i in range(52):
            self.append(Card(i))
            
    def shuffle(self):
        '''rearrange the cards into a new random permutation'''
        return shuffle(self)
    
    def deal(self, n):
        '''remove the first n cards from the deck and return them in a list'''
        hand = [ ]
        for i in range(n):
            hand.append(self.pop(0))
        return hand
    
    def restore(self, h):
        '''add the cards in list to the end of the deck'''
        return self.extend(h)

