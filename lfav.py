import csv
import copy
import random

#Global Variables:
unitList = []

#Classes
class Unit:
    def __init__(self, list):
        self.name = list[0]
        self.equipped_weapon = 0
        self.weapon_mastery = list[1]

        #Base Stats
        self.base = {}
        self.base['Lvl'] = int(list[2])
        self.base['HP'] = int(list[3])
        self.base['Str'] = int(list[4])
        self.base['Mag'] = int(list[5])
        self.base['Spd'] = int(list[6])
        self.base['Skl'] = int(list[7])
        self.base['Lck'] = int(list[8])
        self.base['Def'] = int(list[9])
        self.base['Res'] = int(list[10])

        #Current Stats
        self.current = copy.deepcopy(self.base)

        #Caps
        self.cap = {}
        self.cap['Lvl'] = int(list[11])
        self.cap['HP'] = int(list[12])
        self.cap['Str'] = int(list[13])
        self.cap['Mag'] = int(list[14])
        self.cap['Spd'] = int(list[15])
        self.cap['Skl'] = int(list[16])
        self.cap['Lck'] = int(list[17])
        self.cap['Def'] = int(list[18])
        self.cap['Res'] = int(list[19])

        #growth
        self.growth = {}
        self.growth['HP'] = int(list[20])
        self.growth['Str'] = int(list[21])
        self.growth['Mag'] = int(list[22])
        self.growth['Spd'] = int(list[23])
        self.growth['Skl'] = int(list[24])
        self.growth['Lck'] = int(list[25])
        self.growth['Def'] = int(list[26])
        self.growth['Res'] = int(list[27])

    #Printing stuff
    def getName(self):
        return self.name

    def printBase(self):
        print("Lvl: " + str(self.base['Lvl']))
        print("HP:  " + str(self.base['HP']))
        print("Str: " + str(self.base['Str']))
        print("Mag: " + str(self.base['Mag']))
        print("Spd: " + str(self.base['Spd']))
        print("Skl: " + str(self.base['Skl']))
        print("Lck: " + str(self.base['Lck']))
        print("Def: " + str(self.base['Def']))
        print("Res: " + str(self.base['Res']))

    def printCurrent(self):
        print("Lvl: " + str(self.current['Lvl']))
        print("HP:  " + str(self.current['HP']))
        print("Str: " + str(self.current['Str']))
        print("Mag: " + str(self.current['Mag']))
        print("Spd: " + str(self.current['Spd']))
        print("Skl: " + str(self.current['Skl']))
        print("Lck: " + str(self.current['Lck']))
        print("Def: " + str(self.current['Def']))
        print("Res: " + str(self.current['Res']))

    def printGrowth(self):
        print("HP Growth: " + str(self.growth['HP']))
        print("Str Growth: " + str(self.growth['Str']))
        print("Mag Growth: " + str(self.growth['Mag']))
        print("Spd Growth: " + str(self.growth['Spd']))
        print("Skl Growth: " + str(self.growth['Skl']))
        print("Lck Growth: " + str(self.growth['Lck']))
        print("Def Growth: " + str(self.growth['Def']))
        print("Res Growth: " + str(self.growth['Res']))

    def printCap(self):
        print("HP Cap: " + str(self.cap['HP']))
        print("Str Cap: " + str(self.cap['Str']))
        print("Mag Cap: " + str(self.cap['Mag']))
        print("Spd Cap: " + str(self.cap['Spd']))
        print("Skl Cap: " + str(self.cap['Skl']))
        print("Lck Cap: " + str(self.cap['Lck']))
        print("Def Cap: " + str(self.cap['Def']))
        print("Res Cap: " + str(self.cap['Res']))

    def printCurrentNCap(self):
        print("Lvl: " + str(self.current['Lvl']) + "; Lvl Cap: " + str(self.cap['Lvl']))
        print("HP:  " + str(self.current['HP']) + "; HP Cap:  " + str(self.cap['HP']))
        print("Str: " + str(self.current['Str']) + "; Str Cap: " + str(self.cap['Str']))
        print("Mag: " + str(self.current['Mag']) + "; Mag Cap: " + str(self.cap['Mag']))
        print("Spd: " + str(self.current['Spd']) + "; Spd Cap: " + str(self.cap['Spd']))
        print("Skl: " + str(self.current['Skl']) + "; Skl Cap: " + str(self.cap['Skl']))
        print("Lck: " + str(self.current['Lck']) + "; Lck Cap: " + str(self.cap['Lck']))
        print("Def: " + str(self.current['Def']) + "; Def Cap: " + str(self.cap['Def']))
        print("Res: " + str(self.current['Res']) + "; Res Cap: " + str(self.cap['Res']))

    def avgStat(self, lvlInc):
        # (lvl increase * decimal growth) + base
        print("HP Avg:  " + str("%.2f" % ((lvlInc * self.growth['HP']/100) + self.base['HP'])) + " ; HP Cap:  " + str(self.cap['HP']))
        print("Str Avg: " + str("%.2f"% ((lvlInc * self.growth['Str'] / 100) + self.base['Str'])) + " ; Str Cap: " + str(self.cap['Str']))
        print("Mag Avg: " + str("%.2f"% ((lvlInc * self.growth['Mag'] / 100) + self.base['Mag'])) + " ; Mag Cap: " + str(self.cap['Mag']))
        print("Spd Avg: " + str("%.2f"% ((lvlInc * self.growth['Spd'] / 100) + self.base['Spd'])) + " ; Spd Cap: " + str(self.cap['Spd']))
        print("Skl Avg: " + str("%.2f"% ((lvlInc * self.growth['Skl'] / 100) + self.base['Skl'])) + " ; Skl Cap: " + str(self.cap['Skl']))
        print("Lck Avg: " + str("%.2f"% ((lvlInc * self.growth['Lck'] / 100) + self.base['Lck'])) + " ; Lck Cap: " + str(self.cap['Lck']))
        print("Def Avg: " + str("%.2f"% ((lvlInc * self.growth['Def'] / 100) + self.base['Def'])) + " ; Def Cap: " + str(self.cap['Def']))
        print("Res Avg: " + str("%.2f"% ((lvlInc * self.growth['Res'] / 100) + self.base['Res'])) + " ; Res Cap: " + str(self.cap['Res']))

    def setToCap(self):
        self.current = copy.deepcopy(self.cap)

    def chgStats(self, variableName, num):
        print(str(self.current[variableName]))

    #Level Simulations
    def levelSimulate(self, levels):
        #Helper Function:
        def helpGrow(statGrowth):
            randomNum = random.randint(1,100)
            if randomNum <= self.growth[statGrowth] and self.current[statGrowth] < self.cap[statGrowth]:
                self.current[statGrowth] = self.current[statGrowth] + 1
                print(statGrowth + " GROWTH!")

                if self.current[statGrowth] == self.cap[statGrowth]:
                    print("Capped " + statGrowth + "!")
            if randomNum <= self.growth [statGrowth] and self.current[statGrowth] == self.cap[statGrowth]:
                print("OVER " + statGrowth + "!")

        print("Starting Base Stats:")
        self.printCurrentNCap()

        for i in range(1, levels + 1):
            print("Level Simulation: " + str(i))
            self.current['Lvl'] = self.current['Lvl'] + 1
            helpGrow('HP')
            helpGrow('Str')
            helpGrow('Mag')
            helpGrow('Spd')
            helpGrow('Skl')
            helpGrow('Lck')
            helpGrow('Def')
            helpGrow('Res')
        print()
        print("======================================")
        print("Final Level Up:")
        self.printCurrentNCap()

def listingUnit():
    for unit in unitList:
        print(unit.getName(), end="; ")
    print()
    print("====================")

def searchForUnit(list, unitName):
    for i in list:
        if i.name == unitName:
            return i
    else:
        return("Error")

def selectingUnit():
    def menuSingleUnit():
        running = True
        while (running):
            print("Menu")
            print("Enter the number corresponding to the action you would like to take.")
            print("[1] Simulate level-up")
            print("[2] Average stats")
            print("[3] Cap stats")
            print("[4] Set stats")
            print("[5] List units")

            print("[0] Exit")

            menuSelection = int(input())
            if menuSelection == 0:
                running = False
            elif menuSelection == 1:
                print("Unit's current stats:")
                selectedUnit.printCurrentNCap()
                print("Enter the number of levels to raise the unit.")
                levelUp = int(input())
                selectedUnit.levelSimulate(levelUp)
                print("Would you like to save this unit?: Y or N")
                answer = input()
                if(answer == "Y"):
                    print("Give this unit a name.")
                    newname = input()
                    newUnit = copy.deepcopy(selectedUnit)
                    newUnit.name = newname
                    selectedUnit.current = copy.deepcopy(selectedUnit.base)
                    unitList.append(newUnit)
                    print("The unit has been saved.")
                else:
                    print("The unit was not saved.")
                    selectedUnit.current = copy.deepcopy(selectedUnit.base)
            elif menuSelection == 2:
                print("Unit's current stats:")
                selectedUnit.printCurrentNCap()
                print("Enter the number of levels to use for average stats.")
                levelUp = int(input())
                selectedUnit.avgStat(levelUp)
            elif menuSelection == 3:
                selectedUnit.setToCap()
                selectedUnit.printCurrentNCap()
                print("Would you like to save this unit?: Y or N")
                answer = input()
                if (answer == "Y"):
                    print("Give this unit a name.")
                    newname = input()
                    newUnit = copy.deepcopy(selectedUnit)
                    newUnit.name = newname
                    selectedUnit.current = copy.deepcopy(selectedUnit.base)
                    unitList.append(newUnit)
                    print("The unit has been saved.")
                else:
                    print("The unit was not saved.")
                    selectedUnit.current = copy.deepcopy(selectedUnit.base)
            elif menuSelection == 4:
                print("Current Stats")
                selectedUnit.printCurrentNCap()
                print("What stat do you want to change?")
                print("[1] HP")
                print("[2] Str")
                print("[3] Mag")
                print("[4] Spd")
                print("[5] Skl")
                print("[6] Lck")
                print("[7] Def")
                print("[8] Res")

                userInput = int(input())
                if userInput == 1:
                    print("What do you want to change it to?")
                    num = input()
                    selectedUnit.current['HP'] = num
                if userInput == 2:
                    print("What do you want to change it to?")
                    num = input()
                    selectedUnit.current['Str'] = num
                if userInput == 3:
                    print("What do you want to change it to?")
                    num = input()
                    selectedUnit.current['Mag'] = num
                if userInput == 4:
                    print("What do you want to change it to?")
                    num = input()
                    selectedUnit.current['Spd'] = num
                if userInput == 5:
                    print("What do you want to change it to?")
                    num = input()
                    selectedUnit.current['Skl'] = num
                if userInput == 6:
                    print("What do you want to change it to?")
                    num = input()
                    selectedUnit.current['Lck'] = num
                if userInput == 7:
                    print("What do you want to change it to?")
                    num = input()
                    selectedUnit.current['Def'] = num
                if userInput == 8:
                    print("What do you want to change it to?")
                    num = input()
                    selectedUnit.current['Res'] = num
                selectedUnit.printCurrentNCap()
            elif menuSelection == 5:
                listingUnit()
            else:
                print("Please choose from the provided options.")
    #User Interface
    print("Which unit you would like to work with?")
    unitName = input()
    selectedUnit = searchForUnit(unitList, unitName)
    if unitName != "Error":
        print(selectedUnit.name + " has been selected.")
        menuSingleUnit()
    else:
        return

def menu():
    running = True
    while(running):
        print("Menu")
        print("Enter the number corresponding to the action you would like to take.")
        print("[1] Select a unit to work with.")
        print("[2] List all units again.")
        print("[0] Exit")

        menuSelection = int(input())
        if menuSelection == 0:
            running = False
        elif menuSelection == 1:
            selectingUnit()
        elif menuSelection == 2:
            listingUnit()
        else:
            print("Please choose from the provided options.")

def initFile():
    #Initializes the file
    with open('stats.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tempUnit = Unit(row)
            unitList.append(tempUnit)
    listingUnit()

def main():
    initFile()
    menu()

main()
