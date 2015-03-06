#!/usr/bin/python

"""
Original Code found in mailing list at http://divmod.org/
http://divmod.org/users/mailman.twistd/pipermail/divmod-commits/2004-April/003206.html

Modified to be 99.99% compatible with the metaphone() function in PHP 5.

"""

vowels = ('a', 'e', 'i', 'o', 'u')
varson = ('c', 's', 'p', 't', 'g')
vafter = ('e', 'i', 'y')

class Token(object):
	def __init__(self, char, prev=None, next=None):
		self.char, self._prev, self._next = char, prev, next

	def __eq__(self, other):
		return self.char == other
	
	def __repr__(self):
		return "%s.%s object with value '%s' at %s" % (__name__, self.__class__.__name__, self.char, hex(id(self)))

	def _getNext(self):
		if self._next == None:
			return Token(None)
		return self._next

	def _setNext(self, obj):
		self._next = obj

	next = property(_getNext, _setNext)
	next2 = property(lambda self: self.next.next)
	next3 = property(lambda self: self.next.next.next)

	def _getPrev(self):
		if self._prev == None:
			return Token(None)
		return self._prev

	def _setPrev(self, obj):
		self._prev = obj

	prev = property(_getPrev, _setPrev)
	prev2 = property(lambda self: self.prev.prev)
	prev3 = property(lambda self: self.prev.prev.prev)
	
	isFirst = property(lambda self: self.prev == None)
	isLast = property(lambda self: self.next == None)

	frontvAfter = property(lambda self: self.next in vafter) # this is kind of a retarded name, will change later

	isVowel = property(lambda self: self.char in vowels)
	isVarson = property(lambda self: self.char in varson)


def tokenizeWord(word):
	tokList = [Token(t) for t in word.lower()]
	for idx, tok in enumerate(tokList):
		if idx != 0:
			tok.prev = tokList[idx-1]
		if idx < len(tokList) - 1:
			tok.next = tokList[idx+1]

	return tokList


def transform(word):
	mphone = []
	tlist = tokenizeWord(word)
	lastChr = len(tlist) - 1
	
	for pos, tok in enumerate(tlist):
		## if a vowel is the first letter
		if tok.isVowel and tok.isFirst:
			mphone.append(tok.char)
			continue
			
		if tok.next==tok:
			continue
		
		if tok == 'b':
			if (tok.isLast or tok.prev == 'm'):  # dumb, plumb, etc.
				continue
			else:
				mphone.append(tok.char)

		elif tok == 'c':
			if tok.prev == 'c':
				mphone.append('k')
				
			
			if not (pos > 1 and tok.prev == 's' and tok.frontvAfter):
				if pos > 0 and tok.next == 'i' and tok.next2 == 'a':
					mphone.append('x')
				elif tok.frontvAfter:
					mphone.append('s')
				elif pos > 1 and tok.prev == 's' and tok.next == 'h':
					mphone.append('x')
					#mphone.append('k')
				elif tok.next == 'h':
					if pos == 0 and tok.next2.isVowel:
						mphone.append('x')
						#mphone.append('k')
					else:
						mphone.append('x')
				else:
					if tok.prev == 'c':
						mphone.append('k')
					else:
						mphone.append('k')
				

		elif tok == 'd':
			if tok.next == 'g' and tok.next.frontvAfter:
				mphone.append('j')
			else:
				mphone.append('t')

		elif tok == 'g':
				
			silent, hard = False, False
			#cond1 = (pos < lastChr - 2 and tok.next == 'h' and tok.next2.isVowel) # tough, rough, stough ;)
			cond2 = (pos == lastChr - 3 and tok.next == 'n' and tok.next2 == 'e' and tok.next3 == 'd') # assigned, aligned, signed
			cond3 = (pos == lastChr - 1 and tok.next == 'n') # sign
			cond4 = (tok.prev == 'd' and tok.frontvAfter) # wedge, ledge

##			 print "lastChr: %s, pos: %s, tok.next: %s, tok.next2: %s, tok.next3: %s" % (lastChr, pos, tok.next, tok.next2, tok.next3)
##			 print "cond1: %s" % cond1
##			 print "cond2: %s" % cond2			
##			 print "cond3: %s" % cond3
##			 print "cond4: %s" % cond4
			
			## process special 'gh' cases
			if tok.next == 'h':
				if tok.isFirst:
					mphone.append('f')
					continue
				if tok.prev2.isVowel or tok.prev.isVowel:
					if tok.prev3 =='b' or tok.prev3 =='d' or tok.prev3 == 'h':
						continue
					else:
						mphone.append('f')
						continue
				#elif tok.prev.isVowel and not tok.prev2.isVowel:
				#	mphone.append('f')
				#	continue
				#if tok.prev2 =='o':
				#		if tok.prev3 in ['r','t','c','g']:
				#			mphone.append('f')
				
				if tok.next2 == 't': # or tok.next2.isVowel or tok.next2.isLast:
					mphone.append('f')
					continue
				if tok.prev not in ['g', 'h', 'w', 'y']:
					mphone.append('f')
					continue
				
				continue
			
			if cond2 or cond3 or cond4:
				silent = True

			if tok.prev == 'g':
				hard = True

#			 print "silent: %s\nhard: %s" % (silent, hard)

			if not silent:
				assert silent == False
				if tok.frontvAfter and not hard:
					mphone.append('j')
				else:
					mphone.append('k')

		elif tok == 'h':
			silent = False
			cond1 = tok.prev.isVarson
			cond2 = tok.prev.isVowel and not tok.next.isVowel
			cond3 = not tok.next.isVowel 
			if cond1 or cond2 or cond3:
				silent = True
			if silent==False:
 			   mphone.append('h')
			continue

		elif tok in ['f', 'j', 'l', 'm', 'n', 'r']:
			mphone.append(tok.char)

		elif tok == 'k':
			if tok.prev == 'c':
				continue
			elif tok.isFirst and tok.next=='n':
				continue
			else:
				mphone.append(tok.char)

		elif tok == 'p':
			if tok.next == 'h':
				mphone.append('f')
				
			else:
				mphone.append('p')

		elif tok == 'q':
			mphone.append('k')

		elif tok == 's':
			if tok.next =='s':
				continue
			if pos > 1 and tok.next == 'i' and (tok.next2 == 'o' or tok.next2 == 'a'):
				mphone.append('x')
			else:
				if tok.next == 'h':
					mphone.append('x')
				else:
					mphone.append('s')

		elif tok == 't':
			if pos > 1 and tok.next == 'i' and (tok.next2 == 'o' or tok.next2 == 'a'):
				mphone.append('x')
			else:
				if tok.next == 'h' and not tok.prev == 't': # the=0, tho=T, tth=T
					if pos > 0 or tok.next2.isVowel:
						mphone.append('0')
					else:
						mphone.append('0')
				elif not (pos < len(tlist) - 2 and tok.next == 'c' and tok.next2 == 'h'):
					mphone.append('t')
				elif(tok.next == 'c' and tok.next2 == 'h'):
					mphone.append('t')

		elif tok == 'v':
			mphone.append('f')

		elif tok in ['w', 'y']:
			if pos < lastChr and tok.next.isVowel:
				mphone.append(tok.char)

		elif tok == 'x':
			mphone.append('ks')

		elif tok == 'z':
			mphone.append('s')

	return ''.join(mphone)
