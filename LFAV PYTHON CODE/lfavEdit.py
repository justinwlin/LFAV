import csv
import copy
import random

# Global Variables:
unitList = []
STATS = ["Lvl", "HP", "Str", "Mag", "Spd", "Skl", "Lck", "Def", "Res"]


class Unit:
    def __init__(self, list):
        self.name = list[0]
        self.equipped_weapon = list[1].split("/")
        self.weapon_mastery = list[1]
        '''
        ================
        Stat Initialization
        ================
        '''
        self.base = {}
        self.cap = {}
        self.current = {}
        self.growth = {}
        # Initializing base/cap/growth/current
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
        self.attack = self.current["Str"]
        self.accuracy = .5 * self.current["Spd"] + 2 * self.current["Skl"]
        self.avoid = self.current["Lck"] + .5 * self.current["Skl"]
        self.crit = .5 * self.current["Skl"]
        self.dodge = 2 * self.current["Spd"] + .5 * self.current["Skl"] + .5 * self.current["Lck"]

    def setBattleStatToBase(self):
        self.attack = self.current["Str"]
        self.accuracy = .5 * self.current["Spd"] + 2 * self.current["Skl"]
        self.avoid = self.current["Lck"] + .5 * self.current["Skl"]
        self.crit = .5 * self.current["Skl"]
        self.dodge = 2 * self.current["Spd"] + .5 * self.current["Skl"] + .5 * self.current["Lck"]

    def printBattleStat(self):
        print("Attack: " + str(self.attack))
        print("Accuracy: " + str(self.accuracy))
        print("Dodge: " + str(self.dodge))
        print("Critical: " + str(self.crit))
        print("Avoid: " + str(self.avoid))

    def battleStatWeapon(self, weaponChoice):
        # Resetting to base stats
        self.setBattleStatToBase()
        # With weapons
        self.equipped_weapon = weaponChoice
        if(self.equipped_weapon == "iron"):
            print("Iron weapon has been equipped.")
            print("Attack: " + str(self.attack) + " -> " + str(self.attack + 6))
            self.attack = self.attack + 6
            print("Accuracy: " + str(self.accuracy) + " -> " + str(self.accuracy + 85))
            self.accuracy = self.accuracy + 85
        elif (self.equipped_weapon == "steel"):
            print("Steel weapon has been equipped.")
            print("Attack: " + str(self.attack) + " -> "+ str(self.attack + 11))
            self.attack = self.attack + 11
            print("Accuracy: " + str(self.accuracy) + " -> " + str(self.accuracy + 75))
            self.accuracy = self.accuracy + 75
        else:
            print("The attached weapon has no recorded value, so your attack will be set to your character's base strength.")
            self.attack = self.attack
    
    def printBattleStatAttacking(self):
        print("Attack: " + str(self.attack))
        print("Accuracy: " + str(self.accuracy))
        print("Critical: " + str(self.crit))
    
    def printBattleStatDefending(self):
        print("Dodge: " + str(self.dodge))
        print("Avoid: " + str(self.avoid))

    def battleStatCustom(self, might, accuracy):
        # Base
        self.setBattleStatToBase()

        # With Weapon
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
            print(STATS[i] + " Cap: " + str(self.cap[STATS[i]]))

    def printCurrentNCap(self):
        for i in range(0, len(STATS)):
            print(STATS[i] + ": " + str(self.current[STATS[i]]) +
                  "; " + STATS[i] + " Cap: " + str(self.cap[STATS[i]]))

    def avgStat(self, lvlInc):
        for i in range(1, len(STATS)):
            print("LVL: " + str(self.current["LVL"] + lvlInc))
            print(STATS[i] + " Avg: " + str("%.2f" % ((lvlInc * self.growth[STATS[i]]/100) +
                                                      self.base[STATS[i]])) + " ; " + STATS[i] + " Cap:  " + str(self.cap[STATS[i]]))

    def setToCap(self):
        self.current = copy.deepcopy(self.cap)

    def chgStats(self, variableName, num):
        print(str(self.current[variableName]))

    def levelSimulate(self, levels):
        # Helper Function:
        def helpGrow(statGrowth):
            randomNum = random.randint(1, 100)
            if randomNum <= self.growth[statGrowth] and self.current[statGrowth] < self.cap[statGrowth]:
                self.current[statGrowth] = self.current[statGrowth] + 1
                print(statGrowth + " GROWTH!")
                if self.current[statGrowth] == self.cap[statGrowth]:
                    print("Capped " + statGrowth + "!")
            elif randomNum <= self.growth[statGrowth] and self.current[statGrowth] == self.cap[statGrowth]:
                print("OVER " + statGrowth + "!")
        print("Starting Base Stats:")
        self.printCurrentNCap()
        for i in range(1, levels + 1):
            print("Level Simulation: " + str(i))
            self.current['Lvl'] = self.current['Lvl'] + 1
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


def searchForUnit(fakeList, unitName):
    for i in fakeList:
        if i.name == unitName:
            return i
    else:
        return("Error")

def battleCalculation(unit1, unit2):
    print("Battling between: " + unit1.name + " vs " + unit2.name)
    print("")
    #Listing Unit Battle Stats
    print(unit1.name)
    print(unit1.printBattleStatAttacking())
    print("")
    print(unit2.name)
    print(unit2.printBattleStatDefending())

    #Calculation
    unitAccuracy = unit1.accuracy - unit2.dodge
    unitCritical = unit1.crit - unit2.avoid
    damage = unit1.attack - unit2.current["Def"]
    criticalDamage = False

    if(unitAccuracy >= random.randint(1, 100)):
        print(unit1.getName() + " has hit " + unit2.getName())
        if(unitCritical >= random.randint(1, 100)):
            print(unit1.getName() + " has crit!")
            criticalDamage = True
        if(criticalDamage):
            initHP = unit2.current["HP"]
            unit2.current["HP"] = unit2.current["HP"] - damage * 3
            if(unit2.current["HP"] > 0):
                print(unit2.name + " HP: " + str(initHP) + " -> " + str(unit2.current["HP"]))
            else:
                unit2.current["HP"] = 0
                print(unit2.name + " HP: " + str(initHP) + " -> " + str(unit2.current["HP"]))
        else:
            initHP = unit2.current["HP"]
            unit2.current["HP"] = unit2.current["HP"] - damage
            if(unit2.current["HP"] > 0):
                print(unit2.name + " HP: " + str(initHP) + " -> " + str(unit2.current["HP"]))
            else:
                unit2.current["HP"] = 0
                print(unit2.name + " HP: " + str(initHP) + " -> " + str(unit2.current["HP"]))
    else:
        print("Attack Missed!")

'''
===========================
Battle Menus
============================
'''
#Heal Function
def heal(unit):
    print("Healing: " + unit.name)
    print("[1] 10 [2] 20 [3] 40 [4] Custom HP [5] MAX")
    hpInput = int(input())
    if(hpInput == 1):
        print(str(unit.current["HP"]) + " -> " + str(unit.current["HP"] + 10))
        unit.current["HP"] = unit.current["HP"] + 10
    if(hpInput == 2):
        print(str(unit.current["HP"]) + " -> " + str(unit.current["HP"] + 20))
        unit.current["HP"] = unit.current["HP"] + 20
    if(hpInput == 3):
        print(str(unit.current["HP"]) + " -> " + str(unit.current["HP"] + 40))
        unit.current["HP"] = unit.current["HP"] + 40
    if(hpInput == 4):
        customInput = int(input())
        print(str(unit.current["HP"]) + " -> " + str(unit.current["HP"] + customInput))
        unit.current["HP"] = unit.current["HP"] + customInput
    if(hpInput == 5):
        print(str(unit.current["HP"]) + " -> " + str(unit.base["HP"]))
        unit.current["HP"] = unit.base["HP"]


def checkUnitHealth(unit):
    return unit.current["HP"] > 0

#Battle Loop
def battle(unit1, unit2):
    unitsInBattle = [unit1, unit2]
    control = True
    print("Both characters will start at default with iron")
    unitsInBattle[0].battleStatWeapon("iron")
    unitsInBattle[1].battleStatWeapon("iron")
    while(control):
        print(unitsInBattle[0].name + " versus " + unitsInBattle[1].name)
        print("[1] Attack [2] Heal [3] Quit")
        userInput = int(input())
        if(userInput == 1):
            print("Select a weapon: [1] Iron [2] Steel [3] Custom")
            userWeapon = int(input())
            #Setting Weapon
            if(userWeapon == 1):
                unitsInBattle[0].battleStatWeapon("iron")
            if (userWeapon == 2):
                unitsInBattle[0].battleStatWeapon("steel")
            if (userWeapon == 3):
                print("Set the weapon Might")
                might = int(input())
                print("Set the weapon accuracy")
                accuracy = int(input())
                unitsInBattle[0].battleStatCustom(might, accuracy)
            #Battle Calculation
            battleCalculation(unitsInBattle[0], unitsInBattle[1]) #First Battle
            if(checkUnitHealth(unitsInBattle[1])): #Check Health
                battleCalculation(unitsInBattle[1], unitsInBattle[0]) #Retaliate
                if(checkUnitHealth(unitsInBattle[0])): #Check Health
                    #Second Attack
                    if(unitsInBattle[0].current["Spd"] >= unitsInBattle[1].current["Spd"] + 4):
                        print(unitsInBattle[0].name + " gets to attack twice!")
                        battleCalculation(unitsInBattle[0], unitsInBattle[1])
                    if(unitsInBattle[1].current["Spd"] >= unitsInBattle[0].current["Spd"] + 4):
                        print(unitsInBattle[1].name + " gets to attack twice!")
                        battleCalculation(unitsInBattle[1], unitsInBattle[0])
            if not checkUnitHealth(unitsInBattle[0]): 
                print(unitsInBattle[0].name + " HP has fallen to 0.")
                control = False
            if not checkUnitHealth(unitsInBattle[1]):
                print(unitsInBattle[1].name + " HP has fallen to 0.")
                control = False
            #Swap: New Turn
            unitsInBattle[0], unitsInBattle[1] = unitsInBattle[1], unitsInBattle[0]

        elif(userInput == 2):
            heal(unitsInBattle[0])
            #Swap: New Turn
            unitsInBattle[0], unitsInBattle[1] = unitsInBattle[1], unitsInBattle[0]
        else:
            control = False
            print("Quitting Battle...")
            #Healing
            print("Would you like to heal, enter (Y) if so. Or anything else if no: " + unitsInBattle[0])
            userHeal = input()
            if(userHeal == "Y" or userHeal = "y"):
                unitsInBattle[0].current["HP"] = unitsInBattle[0].base["HP"]
                unitsInBattle[0].printCurrent()
            
            print("Would you like to heal, enter (Y) if so. Or anything else if no: " + unitsInBattle[1])
            userHeal = input()
            if(userHeal == "Y" or userHeal = "y"):
                unitsInBattle[1].current["HP"] = unitsInBattle[1].base["HP"]
                unitsInBattle[1].printCurrent()
            


#Battle Menu
def battleSimulationMenu():
    #Selecting First Unit
    print("Select the first unit to initiate battle.")
    userInput = input()
    unit1 = searchForUnit(unitList, userInput)

    #Select Second Unit
    print("Select the second unit to initiate battle.")
    userInput = input()
    unit2 = searchForUnit(unitList, userInput)

    battle(unit1, unit2)






'''
===========================
Menu System Regular
============================
'''


def menu():
    listingUnit()
    running = True
    while(running):
        # MENU OPTION
        print("Menu")
        print("Enter the number corresponding to the action you would like to take.")
        print("[1] Select a unit to work with.")
        print("[2] List all units again.")
        print("[3] Initiate battle.")
        print("[0] Exit")
        # LOGIC
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
                if(answer == "Y" or answer == "y"):
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
                    newUnit.setBattleStatToBase()
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

    # User Interface
    print("Which unit you would like to work with?")
    unitName = input()
    selectedUnit = searchForUnit(unitList, unitName)
    if unitName != "Error":
        print(selectedUnit.name + " has been selected.")
        menuSingleUnit()
    else:
        print("Your unit was not found.")
        return


'''
===========================
Init and Main
============================
'''


def initFile():
    # Initializes the file
    with open('stats.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tempUnit = Unit(row)
            unitList.append(tempUnit)


def main():
    initFile()
    menu()


main()
