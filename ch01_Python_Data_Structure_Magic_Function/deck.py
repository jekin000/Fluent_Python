##########################################
# 1.1 The deck by __getitem__, __len__
## collections.nametuple, only property,no method's object
## for use __getitem__,__len__, the FrenchDeck get benefit like
### 1. could use  python standard method, such as len,
### 2. could use  python standard module, such as random.choice
### 3. list[12::13] = get list[12] then get a item for per interval 13
## other note: #doctest: +ELLIPSIS
## key:
### 0. dunder method
### 1. collections.nametuple
### 2. __getitem__, __len__
### 3. random.choice
### 5. list[12::13]
### 6. #doctest: +ELLIPSIS
### 7. reversed, sorted
### 8. in, e.g. Card('Q','hearts') in deck
### 9. order
## note:
### FrenchDeck can not  Shuffle(change order), because it is fixed order & no __setitem__

##########################################

import collections

Card = collections.namedtuple('Card',['rank','suit'])

class FrenchDeck:
	ranks = [str(n) for n in range(2,11)] +list('JQKA')
	suits = 'spades diamonds clubs hearts'.split()
	
	def __init__(self):
		self._cards = [Card(rank,suit) for suit in self.suits
						for rank in self.ranks]
	def __len__(self):
		return len(self._cards)

	def __getitem__(self,position):
		return self._cards[position]


suit_values = dict(spades=3,hearts=2,diamonds=1,clubs=0)	
def spades_high(card):
	rank_value = FrenchDeck.ranks.index(card.rank)
	return rank_value * len(suit_values) +suit_values[card.suit]

if __name__ == '__main__':
	beer_card = Card('7','diamonds')
	print(beer_card)

	#len
	deck = FrenchDeck()
	print(len(deck))

	#access by position
	print(deck[0])
	print(deck[-1])

	#directly use random.choice
	from random import choice
	print (choice(deck))
	print (choice(deck))

	#in summary
	#1. you need not remember standard function. Instead, you just use such as len(),sorted() etc.
	#2. you could easily use Python standard lib

	#slice, __getitem__ use [] on self._cards
	print(deck[:2])
	print(deck[12::13])

	#by use __getitem__ we could iterator the deck or reverse(deck)
	for card in deck: #doctest: +ELLIPSIS
		print(card)

	#if we do not implement __contains__  'in' will search by order
	print('-->The ordered "in" ')
	print(Card('Q','hearts') in deck)
	print(Card('7','beasts') in deck)

	for card in sorted(deck,key=spades_high):
		print(card)
