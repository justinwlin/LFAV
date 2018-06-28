
import csv
import copy
import random

unitList = []
weaponDic = {}
STATS = ["Lvl", "HP", "Str", "Mag", "Spd", "Skl", "Lck", "Def", "Res"]

class Weapon:
    def __init__(self, list): #name, typeWeapon, hit, might, crit, weight
        self.name = list[0]
        self.type = list[1]
        self.hit = int(list[2])
        self.might = int(list[3])
        self.crit = int(list[4])
        self.weight = int(list[5])

class Unit:
    def __init__(self, list):
        self.name = list[0]
        self.weapon = 0
        self.weapon_mastery = list[1].split("/")
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
        ===========================
        Battle Stats
        ===========================
        '''
        self.attack = self.current["Str"]
        self.accuracy = .5 * self.current["Spd"] + 2 * self.current["Skl"]
        self.avoid = self.current["Lck"] + .5 * self.current["Skl"]
        self.crit = .5 * self.current["Skl"]
        self.dodge = 2 * self.current["Spd"] + .5 * self.current["Skl"] + .5 * self.current["Lck"]
        self.attackSpeed = self.current["Spd"]

    '''
    =================
    Level Simulator
    =================
    '''
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
        print("Base stats:")
        self.printCurrentNCap()
        for i in range(1, levels + 1):
            print("Level simulation: " + str(i))
            self.current['Lvl'] = self.current['Lvl'] + 1
            for i in range(1, len(STATS)):
                helpGrow(STATS[i])
        print("\n======================================")
        print("Final level-up:")
        self.base = self.current
        self.printCurrentNCap()

    '''
    ==================
    Getter/Setters
    ==================
    '''
    def setBattleStatToBase(self):
        self.attack = self.current["Str"]
        self.accuracy = .5 * self.current["Spd"] + 2 * self.current["Skl"]
        self.avoid = self.current["Lck"] + .5 * self.current["Skl"]
        self.crit = .5 * self.current["Skl"]
        self.dodge = 2 * self.current["Spd"] + .5 * self.current["Skl"] + .5 * self.current["Lck"]
        self.attackSpeed = self.current["Spd"]

    def checkHasWeapon(self):
        if(self.weapon == 0):
            return False
        return True

    def equipWeapon(self):
        print("Choose Weapon for: " + self.name)
        #Check the weapon List if it exists
        inweaponDic = False
        canWield = False
        while(not inweaponDic and not canWield):
            userInput = input()
            if userInput in weaponDic:
                    inweaponDic = True
                    if(inweaponDic):
                        for weaponMastery in self.weapon_mastery:
                            if(weaponDic[userInput].type == weaponMastery):
                                canWield = True
                                #Assign weapon
                                self.weapon = weaponDic[userInput]
                                print("Weapon successfully equipped: " + self.weapon.name)
                                break
                            else:
                                print("You can't wield that weapon!")
            else:
                print("Weapon doesn't exist!")
        #update Stats
        self.updateStats()

    def processWeapon(self):
        self.attack += self.weapon.might
        self.accuracy += self.weapon.hit
        self.crit += self.weapon.crit
        #Attack Speed Calculation
        weightCalc = (self.weapon.weight - self.current["Str"])
        if weightCalc < 0:
            weightCalc = 0
        self.attackSpeed = self.current["Spd"] - weightCalc

    def updateStats(self):
        # Resetting to base stats
        self.setBattleStatToBase()
        #Adjusting based on held Weapon
        self.processWeapon()

    '''
    =========================
    Printing Functions
    =========================
    '''
    def printBattleStat(self):
        print(self.name + ": ")
        print("HP:       " + str(self.current["HP"]) + "/" + str(self.base["HP"]))
        print("Attack:   " + str(self.attack))
        print("Accuracy: " + str(self.accuracy))
        print("Dodge:    " + str(self.dodge))
        print("Critical: " + str(self.crit))
        print("Avoid:    " + str(self.avoid))
        print("Attack Speed: " + str(self.attackSpeed))

    def printBattleStatAttacking(self):
        print(self.name + ": ")
        print("HP:       " + str(self.current["HP"]) + "/" + str(self.base["HP"]))
        print("Attack:   " + str(self.attack))
        print("Accuracy: " + str(self.accuracy))
        print("Critical: " + str(self.crit))
    
    def printBattleStatDefending(self):
        print(self.name + ": ")
        print("HP:       " + str(self.current["HP"]) + "/" + str(self.base["HP"]))
        print("Dodge:    " + str(self.dodge))
        print("Avoid:    " + str(self.avoid) + "\n")

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

'''
================
Battle Functions
================
'''
def battle(unit1, unit2):
    #Variable Controls
    battleLoop = True
    battleMenuLoop = True
    #Logic
    unitsInBattle = [unit1, unit2] #Establing Turn Sequence    
    while (battleLoop):
        '''
        ===================
        Equipping Weapon
        ===================
        '''
        unitsInBattle[0].equipWeapon()
        #If the opposing unit doesn't have any weapon, give them a weapon
        if(not unitsInBattle[1].checkHasWeapon()):
            unitsInBattle[1].equipWeapon()
        
        '''
        ===================
        Battle Menu
        ===================
        '''
        #Display Stats
        print("\n" + unitsInBattle[0].name + "'s turn:")
        print("[1] Attack [2] Heal [3] Quit")
        userInput = int(input())
        while(battleMenuLoop):
            if userInput == 1:
                battleMenuLoop = False
                #Attack First
                damageCalculation(unitsInBattle[0], unitsInBattle[1], True)
                #Retaliation
                damageCalculation(unitsInBattle[1], unitsInBattle[0], False)
                #Check if either units attack twice
                #Check if unit 0 can attack:
                    #knife Adv True
                #Check if unit 1 can attack:
                    #knife Adv False
            elif userInput == 2:
                battleMenuLoop = False
                heal(unitsInBattle[0])
            elif userInput == 3:
                battleMenuLoop = False
            else:
                print("Not recognized input.")

def damageCalculation(unit1, unit2, checkForKnifeAdv):
    '''
    ==============
    Display Stats
    ==============
    '''
    unit1.printBattleStatAttacking()
    print()
    unit2.printBattleStatDefending()

    '''
    =================
    knife Advantage
    =================
    '''
    if(checkForKnifeAdv):
        unit1.weapon.type == "knife":
        

    '''
    =================
    Weapon Triangle
    =================
    '''

    '''
    =================
    Damage Calculation
    =================
    '''

    '''
    ==================
    Reset Stats
    ==================
    '''
    unit1.updateStats()
    unit2.updateStats()



'''
=================
Helper Functions
=================
'''
def listingUnit():
    for unit in unitList:
        print(unit.getName(), end="; ")
    print()
    print("====================")

def listingWeapon():
    for weapon in weaponDic:
        print(weapon.name, end="; ")
    print()
    print("====================")

def searchForUnit(fakeList, unitName):
    for i in fakeList:
        if i.name == unitName:
            return i
    else:
        return("Error")
'''
====================
Individual Unit Work
=====================
'''
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
            print("[5] Display Stats")
            print("[6] List units")

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
                selectedUnit.printCurrent()
            elif menuSelection == 6:
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
        print("The unit was not found.")
        return

'''
=================
Menu
=================
'''
#Regular Menu
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

#Battle Menu
def battleSimulationMenu():
    #Selecting First Unit
    print("Select a unit to initiate battle:")
    userInput = input()
    unit1 = searchForUnit(unitList, userInput)
    #Select Second Unit
    print("Select unit to attack:")
    userInput = input()
    unit2 = searchForUnit(unitList, userInput)
    battle(unit1, unit2)


#=================
# Inits / Main
#=================
def initFile():
    # Initializes the file
    with open('stats.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tempUnit = Unit(row)
            unitList.append(tempUnit)
    with open('weapons.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tempWeapon = Weapon(row)
            weaponDic[tempWeapon.name] = tempWeapon

#Main Function
def main():
    initFile()
    menu()

main()