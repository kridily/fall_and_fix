import math, sys, random

class ActionCommand:
    def __init__(self,size,letter_array,fixedCommandList = 0):
        #Initalizes the Action Command
        #
        #Size: Size of the Command
        #letter_array: strings that represent commands that can be entered.
        #fixedCommandList: if you input an array here, it will be used
        #   instead of the random array.

        self.size = size

        if self.size < 0:
            self.size = 0

        self.CommandArray = []
        self.Original = []

        if fixedCommandList == 0:
            for i in range (0, size):
                pickletter = letter_array[random.randint(0, letter_array.__len__()-1)]
                self.CommandArray.append(pickletter)
            #print self.CommandArray
        else:
            self.CommandArray = list(fixedCommandList)
            #print self.CommandArray

        self.Original = self.CommandArray

    def inputCommand(self,character):
        #Lets you input something into the action command.
        if self.CommandArray != []:
            if character == self.CommandArray[0]:
                self.CommandArray.pop(0)
                #print self.CommandArray
                return True
            else:
                #print self.CommandArray
                return False
        else:
            return False

    def inputCommandNoOrder(self,character):
        #Lets you input something into the action command.
        #This version does not take the order of commands into account
        if self.CommandArray != []:
            for i in range (0,len(self.CommandArray)):
                if character == self.CommandArray[i]:
                    self.CommandArray.pop(i)
                    #print self.CommandArray
                    return True
            else:
                #print self.CommandArray
                pass
        return False

    def isEmpty(self):
        if self.CommandArray == []:
            print "EMPTY"
            return True
        else:
            print "NOT EMPTY"
            return False

    def getCommand(self):
        return self.CommandArray

    def getOriginal(self):
        return self.Original

    def resetCommand(self):
        self.CommandArray = self.Original

    def blankCommand(self):
        self.CommandArray = []

#DEBUG
#AC = ActionCommand(5,['!','@','#','$','%'])

