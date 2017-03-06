


'''
 	2	3	4	5	6	7	8	9	10	J	Q	K	A
♣	0	1	2	3	4	5	6	7	8	9	10	11	12
♦	13	14	15	16	17	18	19	20	21	22	23	24	25
♥	26	27	28	29	30	31	32	33	34	35	36	37	38
♠	39	40	41	42	43	44	45	46	47	48	49	50	51
'''


class Card:
    ''' A class to represent a single card'''
    def __init__(self, n):
        ''' Creates an ID name based on the number'''
        self.n = n
        
    def key(self):
        ''' Returns its name'''
        return self.n
        
    def suit(self):
        '''Uses the card name to find the suit
           return the suit number, with clubs = 0, diamonds = 1, hearts = 2, and spades = 3
        '''
        cat = self.key() // 13
        if cat == 0: return 0
        elif cat == 1: return 1
        elif cat == 2: return 2
        elif cat == 3: return 3

            
    def points(self):
        '''Calculates points for a standard deck
           return 4 if the card is an ace, 3 if it’s a king, 2 if it’s a queen, 1 if it’s a jack, and 0 otherwise
        '''
        c = Card(self.key())
        rank = c.rank()
        if rank <= 8:
            return 0
        elif rank == 9:
            return 1
        elif rank == 10:
            return 2
        elif rank ==11:
            return 3
        elif rank == 12:
            return 4
        
    
    def rank(self):
        '''return a number between 0 and 12, where a 2 has rank 0 and an ace has rank 12
        '''
        c = Card(self.key())
        suit = c.suit()
        fix = 13 * suit
        res = self.key() - fix
        return res
            
    def __lt__(self, other):
        ''' Magic comparison < for more accurate sorting'''
        return self.key() < other.key()
                
    def __repr__(self):
        '''returns print display as card, then symbol'''
        c = Card(self.key())
        rank = c.rank()
        suit = c.suit()
        display = None
        # Club, diamond, heart, and spade.
        suitLst = [ '\u2663', '\u2666', '\u2665', '\u2660' ] 
        symbol = suitLst[suit]
        
        if rank <= 8:
            display = rank + 2
        elif rank == 9:
            display = 'J'
        elif rank == 10:
            display = 'Q'
        elif rank == 11:
            display = 'K'
        elif rank == 12:
            display = 'A'
               
        return '{}{}'.format(display, symbol)


                
