#!/usr/bin/python
# Check learning cards in Anki collection
# If any are due in the next 20 minutes, give an alert
import sys
sys.path.append('/usr/share/anki')
from anki import Collection
from anki.utils import intTime
import time

collection_path = "../collection.anki2"
col = Collection(collection_path)

tody = intTime() #anki function returns current integer time
nextTwenty = today + 20*60 #integer time in 20 minutes

query="select count(id) from cards where queue = 1 and due < %s" % nextTwenty
learnAheadCards = col.db.scalar(query)

print("You have %s learning cards due in Anki" % learnAheadCards) 

col.close()

