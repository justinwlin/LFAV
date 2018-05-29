import csv
import copy
import random

#Global Variables:
unitList = []
STATS = ["LVL", "HP", "STR", "MAG", "SPD", "SKL", "LCK", "DEF", "RES"]
class Unit:
    def __init__(self, list):
        self.name = list[0]
        self.equipped_weapon = list[1] #allowing this to be the change to stat
        self.weapon_mastery = list[1]
        '''
        ================
        Base Stats Initialization
        ================
        '''
        self.base = {}
        self.cap = {}
        self.current = {}
        self.growth = {}
        #Initializing Base/cap/growth/current
        for i in range(0, 9):
            self.base[STATS[i]] = int(list[i + 2])
            self.cap[STATS[i]] = int(list[i + 11])
            self.growth[STATS[i]] = int(list[i + 19])
        self.current = copy.deepcopy(self.base)

        '''
        ================
        Battle Simulation Stats
        ================
        '''
        #Weapon Adding to Attack:
        self.attack = self.base["STR"]
        self.accuracy = .5 * self.base["SPD"] + 2 * self.base["SKL"]
        self.avoid = self.base["LCK"] + .5 * self.base["SKL"]
        self.crit = .5 * self.base["SKL"]
        self.dodge = 2 * self.base["SPD"] + .5 * self.base["SKL"] + .5 * self.base["LCK"]
    
    def printBattleStat(self):
        print("ATTACK" + ": " + str(self.attack))
        print("ACCURACY" + ": " + str(self.accuracy))
        print("AVOID" + ": " + str(self.avoid))
        print("CRIT" + ": " + str(self.crit))
        print("DODGE" + ": " + str(self.dodge))

    def battleStatWeapon(self, weaponChoice):
        self.attack = self.base["STR"]
        self.accuracy = .5 * self.base["SPD"] + 2 * self.base["SKL"]
        self.avoid = self.base["LCK"] + .5 * self.base["SKL"]
        self.crit = .5 * self.base["SKL"]
        self.dodge = 2 * self.base["SPD"] + .5 * self.base["SKL"] + .5 * self.base["LCK"]

        self.equipped_weapon = weaponChoice
        if(self.equipped_weapon == "iron"):
            self.attack = self.attack + 6
            self.accuracy = self.accuracy + 85
        elif (self.equipped_weapon == "steel"):
            self.attack = self.attack + 11
            self.accuracy = self.accuracy + 75
        else:
            print("The attached weapon has no recorded value so your attack will be sent to your character base strength.")
            self.attack = self.attack
    
    def battleStatCustom(self, might, accuracy):
        self.attack = self.base["STR"]
        self.accuracy = .5 * self.base["SPD"] + 2 * self.base["SKL"]
        self.avoid = self.base["LCK"] + .5 * self.base["SKL"]
        self.crit = .5 * self.base["SKL"]
        self.dodge = 2 * self.base["SPD"] + .5 * self.base["SKL"] + .5 * self.base["LCK"]

        self.attack = self.attack + might
        self.accuracy = self.accuracy + accuracy


    def getName(self):
        return self.name

    def printBase(self):
        for i in range(0, len(STATS)):
            print(STATS[i] + ": " + str(self.base[STATS[i]]))

    def printCurrent(self):
        for i in range(0, len(STATS)):
            print(STATS[i] + ": " + str(self.current[STATS[i]]))

    def printGrowth(self):
        for i in range(0, len(STATS)):
            print(STATS[i] + " Growth: " + str(self.growth[STATS[i]]))

    def printCap(self):
        for i in range(0, len(STATS)):
            print(STATS[i] + " CAP: " + str(self.cap[STATS[i]]))
    
    def printCurrentNCap(self):
        for i in range(0, len(STATS)):
            print(STATS[i] + ": " + str(self.current[STATS[i]]) + "; " + STATS[i] + " Cap: " + str(self.cap[STATS[i]]))

    def avgStat(self, lvlInc):
        for i in range(0, len(STATS)):
            print(STATS[i] + " Avg: "+ str("%.2f" % ((lvlInc * self.growth[STATS[i]]/100) + self.base[STATS[i]])) + " ; " + STATS[i] +  " Cap:  " + str(self.cap[STATS[i]]))

    def setToCap(self):
        self.current = copy.deepcopy(self.cap)

    def chgStats(self, variableName, num):
        print(str(self.current[variableName]))
    
    def levelSimulate(self, levels):
        #Helper Function:
        def helpGrow(statGrowth):
            randomNum = random.randint(1,100)
            if randomNum <= self.growth[statGrowth] and self.current[statGrowth] < self.cap[statGrowth]:
                self.current[statGrowth] = self.current[statGrowth] + 1
                print(statGrowth + " GROWTH!")
                if self.current[statGrowth] == self.cap[statGrowth]:
                    print("Capped " + statGrowth + "!")
            elif randomNum <= self.growth [statGrowth] and self.current[statGrowth] == self.cap[statGrowth]:
                print("OVER " + statGrowth + "!")
        print("Starting Base Stats:")
        self.printCurrentNCap()
        for i in range(1, levels + 1):
            print("Level Simulation: " + str(i))
            self.current['LVL'] = self.current['LVL'] + 1
            for i in range(1, len(STATS)):
                helpGrow(STATS[i])
        print("\n======================================")
        print("Final Level Up:")
        self.printCurrentNCap()


'''
===========================
BackEnd Functions
============================
'''

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

def battle_(unit1, unit2):
    unit1Accuracy = unit1.accuracy - unit2.dodge
    unit1Crit = unit1.crit - unit2.avoid
    crit = False
    if(unit1Accuracy <= random.randint(1, 100)):
        print(unit1.getName() + " has hit " + unit2.getName())
        if(unit1Crit <= random.randint(1, 100)):
            print(unit1.getName() + " has crit " + unit2.getName() + "!!!")
            crit = True
        damage = unit1.attack - unit2.current["DEF"]
        if(crit):
            damage = damage * 3
        unit2.current["HP"] = unit2.current["HP"] - damage

        if(unit2.current["HP"] < 0):
            unit2.current["HP"] = 0

        print(unit2.getName() + " has taken " + str(damage) + "!")
        print(unit2.getName() + " current health is " + str(unit2.current["HP"]))
    else:
        print("ATTACK MISSED!")
    

'''
===========================
Battle Menus
============================
'''

def battleSimulationMenu():
    unitSuccessSelected = False

    unit1 = False
    unit2 = False

    print("Select which units that you would like to do battle?")

    while (not unitSuccessSelected):
        listingUnit()
        unitName = input()
        selectedUnit = searchForUnit(unitList, unitName)
        if unitName != "Error":
            print(selectedUnit.name + " has been selected.")
            if(unit1 == False):
                unit1 = selectedUnit
                print("Please choose another unit for battle")
            else:
                unit2 = selectedUnit
                unitSuccessSelected = True
        else:
            print("Your unit was mispelled or not found please enter a proper input")
    battleSimulate(unit1, unit2)

def weaponSelect(unit):
    running = True
    while(running):
        #MENU OPTION
        print("Item Choice")
        print("Select Weapon")
        print("[1] Iron")
        print("[2] Steel")
        print("[3] Custom")
        #LOGIC
        menuSelection = int(input())
        if menuSelection == 1:
            unit.battleStatWeapon("iron")
            running = False
        elif menuSelection == 2:
            unit.battleStatWeapon("steel")
            running = False
        elif menuSelection == 3:
            print("Please choose a given might for your weapon")
            might = int(input())
            print("Please give your weapon an accuracy")
            accuracy = int(input())
            unit.battleStatCustom(might, accuracy)
            running = False
        else:
            print("Please choose from the provided options.")


def battleSimulate(unit1, unit2):
    #Battle Loop
    battle = True
    unit1Turn = True
    while(battle):
        if(unit1.current["HP"] <= 0 and unit2.current["HP"] <= 0):
            print("Both units have lost their HP!")
            battle = False
        elif(unit1.current["HP"] <= 0):
            print(unit1.getName() + " has lost all HP!")
            battle = False
        elif unit2.current["HP"] <= 0:
            print(unit2.getName() + " has lost all HP!")
            battle = False
        else:
            attackerName = unit1.name
            defenderName = unit2.name
            if(unit1Turn != True):
                attackerName = unit2.name
                defenderName = unit1.name

            attackerUnit = searchForUnit(unitList, attackerName)
            defenseUnit = searchForUnit(unitList, defenderName)
            
            print(attackerName + " is attacking " + defenderName)
            print("What weapon do you want the attacker to use?")
            weaponSelect(attackerUnit)
            print("What weapon do you want the defender to use?")
            weaponSelect(defenseUnit)
            unit1Turn = not unit1Turn

            print("Stat of Current Unit")
            print(attackerUnit.name)
            attackerUnit.printCurrent()
            attackerUnit.printBattleStat()
            print()
            print(defenseUnit.name)
            defenseUnit.printCurrent()
            defenseUnit.printBattleStat()
            print()
            battle_(attackerUnit, defenseUnit)

'''
===========================
Menu System Regular
============================
'''

def menu():
    running = True
    while(running):
        #MENU OPTION
        print("Menu")
        print("Enter the number corresponding to the action you would like to take.")
        print("[1] Select a unit to work with.")
        print("[2] List all units again.")
        print("[3] Battle Simulation")
        print("[0] Exit")
        #LOGIC
        menuSelection = int(input())
        if menuSelection == 0:
            running = False
        elif menuSelection == 1:
            selectingUnit()
        elif menuSelection == 2:
            listingUnit()
        elif menuSelection == 3:
            battleSimulationMenu()
        else:
            print("Please choose from the provided options.")


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
                for i in range(0, len(STATS)):
                    print("[" + str(i + 1) + "] " + STATS[i])
                userInput = int(input())
                print("You selected to change: " + STATS[userInput - 1])
                print("What do you want to change it to?")
                num = input()
                selectedUnit.current[STATS[userInput - 1]] = num
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
        print("Your unit was mispelled or not found")
        return
'''
===========================
Init and Main
============================
'''

def initFile():
    #Initializes the file
    with open('stats.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tempUnit = Unit(row)
            unitList.append(tempUnit)
def main():
    initFile()
    menu()

main()