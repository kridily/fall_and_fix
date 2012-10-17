import math, sys, random

class ActionCommand:
    def __init__(self,size,letter_array,fixedCommandList = 0):
        #Initalizes the Action Command
        #
        #Size: Size of the Command
        #letter_array: strings that represent commands that can be entered.
        #fixedCommandList: if you input an array here, it will be used instead of the random array.

        self.size = size

        if self.size < 0:
            self.size = 0

        self.CommandArray = []

        if fixedCommandList == 0:
            for i in range (0, size):
                pickletter = letter_array[random.randint(0, letter_array.__len__()-1)]
                self.CommandArray.append(pickletter)
            print self.CommandArray
        else:
            self.CommandArray = list(fixedCommandList)
            print self.CommandArray

    def inputCommand(self,character):
        if self.CommandArray != []:
            if character == self.CommandArray[0]:
                self.CommandArray.pop(0)
                print self.CommandArray
                return True
            else:
                print self.CommandArray
                return False
        else:
            return False
    def isEmpty(self):
        if self.CommandArray == []:
            return True
        else:
            return False
            
#DEBUG            
#AC = ActionCommand(5,['!','@','#','$','%'])

