import random

class GrabBag:
    """Generates integers from 1 to self.size in a way so that
       each number doesn't show up twice in the same 'set' of integers"""
    def __init__(self, size):
        self.size = size
        if self.size < 0:
            self.size = 0
        self.BagArray = []
        for i in range (0, size):
            self.BagArray.append(i+1)
        print self.BagArray
    def pick(self):
        if self.BagArray.__len__() > 0:
            returnval = self.BagArray.pop(random.randint(0, self.BagArray.__len__()-1))
        else:
            for i in range (0, self.size):
                self.BagArray.append(i+1)
            #print self.BagArray
            returnval = self.BagArray.pop(random.randint(0, self.BagArray.__len__()-1))
        return returnval

#DEBUG        
# g = GrabBag(6)
# for i in range (30):
    # print g.pick()
    