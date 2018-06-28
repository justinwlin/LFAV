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
    def getAdv(self):
        self.attack += 1
        self.accuracy += 15
        print()
        print("Weapon advantage!")
        print(self.name)
        print("Attack: " + str(self.attack - 1) + " -> " + str(self.attack))
        print("Accuracy: " + str(self.accuracy - 15) + " -> " + str(self.accuracy))
        print()
    
    def getDisadv(self):
        self.attack -= 1
        self.accuracy += 15
        print()
        print("Weapon disadvantage!")
        print(self.name)
        print("Attack: " + str(self.attack + 1) + " -> " + str(self.attack))
        print("Accuracy: " + str(self.accuracy + 15) + " -> " + str(self.accuracy))
        print()
    
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
        print("Choose weapon for " + self.name + ":")
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
                                print(self.weapon.name + " successfully equipped." )
                                break
                            else:
                                print(self.name + "cannot wield that weapon.")
            else:
                print("The weapon cannot be found.")
        #update Stats
        self.updateStats()

    def processWeapon(self):
        if (self.weapon.type == "magic"):
            self.attack = self.current["Mag"]
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
    def checkHealth(self):
        if(self.current["HP"] <= 0):
            print(self.name + "'s HP has fallen to 0!")
            return True
        return False

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
        print("Defense:  " + str(self.current["Def"] + "\n"))
        print("Res:      " + str(self.current["Res"] + "\n"))

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
            print("Lvl: " + str(self.current["Lvl"] + lvlInc))
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
    battleMenuLoop = True
    unitsInBattle = [unit1, unit2] #Establing Turn Sequence    
    while(battleMenuLoop):
        
        '''
        ===================
        Battle Menu
        ===================
        '''
        #Display Stats
        #Note: Anytime there is a "break" during the battle, it means a unit has lost all HP.
        print("\n" + unitsInBattle[0].name + "'s turn:")
        print("[1] Attack [2] Heal [3] Quit")
        userInput = int(input())
        if userInput == 1:
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
            ==============
            Damage Order
            ==============
            '''
            #Attack First
            if(damageCalculation(unitsInBattle[0], unitsInBattle[1], True)):
                #Retaliation
                if(damageCalculation(unitsInBattle[1], unitsInBattle[0], False)):
                    #Check if either units attack twice
                    if(unitsInBattle[0].attackSpeed >= unitsInBattle[1].attackSpeed + 4 and (unitsInBattle[0].attackSpeed >= unitsInBattle[1].attackSpeed * 1.2)):
                        print("\n" + unitsInBattle[0].name + " attacks twice!")
                        damageCalculation(unitsInBattle[0], unitsInBattle[1], True)
                        if(unitsInBattle[1].checkHealth()):
                            battleLoop = False
                            break
                    if(unitsInBattle[1].attackSpeed >= unitsInBattle[0].attackSpeed + 4 and (unitsInBattle[1].attackSpeed >= unitsInBattle[0].attackSpeed * 1.2)):
                        print("\n" + unitsInBattle[1].name + " attacks twice!")
                        damageCalculation(unitsInBattle[1], unitsInBattle[0], False)
                        if(unitsInBattle[0].checkHealth()):
                            battleLoop = False
                            break
                else:
                    if(unitsInBattle[0].checkHealth() or unitsInBattle[1].checkHealth()):
                        battleLoop = False
                        break
            else:
                if unitsInBattle[0].checkHealth() or unitsInBattle[1].checkHealth():
                    battleLoop = False
                    break
            #Switch Turn
            unitsInBattle[0], unitsInBattle[1] = unitsInBattle[1], unitsInBattle[0]
        elif userInput == 2:
            battleLoop = False
            heal(unitsInBattle[0])
            #Switch Turn
            unitsInBattle[0], unitsInBattle[1] = unitsInBattle[1], unitsInBattle[0]
        elif userInput == 3:
            battleLoop = False
            break
        else:
            print("Input was not recognized.")
    print("The battle has ended.")
    unit1.weapon = 0
    unit2.weapon = 0
    #Healing
    print("Would you like to restore " + unitsInBattle[0].getName() + "? Enter [Y].")
    userHeal = input()
    if(userHeal == "Y" or userHeal == "y"):
        unitsInBattle[0].current["HP"] = unitsInBattle[0].base["HP"]
        unitsInBattle[0].printCurrent()
    print("Would you like to restore " + unitsInBattle[1].getName() + "? Enter [Y].")
    userHeal = input()
    if(userHeal == "Y" or userHeal == "y"):
        unitsInBattle[1].current["HP"] = unitsInBattle[1].base["HP"]
        unitsInBattle[1].printCurrent()

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
    if(checkForKnifeAdv and unit1.weapon.type == "knife"):
        unit1.getAdv()
    if(not checkForKnifeAdv and unit1.weapon.type == "knife"):
        unit1.getDisadv()

    '''
    =================
    Weapon Triangle
    =================
    '''
    weaponTriangle = [("sword", "axe"), ("axe", "lance"), ("lance", "sword")]
    for i in range(0, len(weaponTriangle)):
        if(weaponTriangle[i][0] == unit1.weapon.type):
            if(weaponTriangle[i][1] == unit2.weapon.type):
                unit1.getAdv()
                break
        if(weaponTriangle[i][1] == unit1.weapon.type):
            if(weaponTriangle[i][0]==unit2.weapon.type):
                unit1.getDisadv()
                break
    '''
    =================
    Damage Calculation
    =================
    '''
    #PreCalculation
    unitAccuracy = unit1.accuracy - unit2.dodge
    unitCritical = unit1.crit - unit2.avoid
    if(unit2.weapon.type == "magic"):
        damage = unit1.attack - unit2.current["Res"]
    else:
        damage = unit1.attack - unit2.current["Def"]
    criticalDamage = False

    #Damage Calculation
    #Check if hits
    if(unitAccuracy >= random.randint(1, 100)):
        print(unit1.getName() + " has hit " + unit2.getName())
        #Check if crits
        if(unitCritical >= random.randint(1, 100)):
            print(unit1.getName() + " has crit!")
            criticalDamage = True
        #If it crits multiply damage by three
        if(criticalDamage):
            initHP = unit2.current["HP"]
            #Subtract from health
            unit2.current["HP"] = unit2.current["HP"] - damage * 3
            #Print
            if(unit2.current["HP"] > 0):
                print(unit2.name + "'s HP: " + str(initHP) + " -> " + str(unit2.current["HP"]))
            else:
                unit2.current["HP"] = 0
                print(unit2.name + "'s HP: " + str(initHP) + " -> " + str(unit2.current["HP"]))
        else:
            #If there is no crit...
            initHP = unit2.current["HP"]
            #Subtract Normal Damage
            unit2.current["HP"] = unit2.current["HP"] - damage
            if(unit2.current["HP"] > 0):
                print(unit2.name + "'s HP: " + str(initHP) + " -> " + str(unit2.current["HP"]))
            else:
                unit2.current["HP"] = 0
                print(unit2.name + "'s HP: " + str(initHP) + " -> " + str(unit2.current["HP"]))
    else:
        print("Attack missed!")
    
        '''
    ==================
    Reset Stats
    ==================
    '''
    unit1.updateStats()
    unit2.updateStats()

    '''
    ===============
    Return Statement
    ===============
    '''
    if(unit1.current["HP"] == 0 or unit2.current["HP"] == 0):
        return False
    else:
        return True
#Heal Function
def heal(unit):
    print("Healing: " + unit.name)
    print("[1] 10 [2] 20 [3] 40 [4] Custom [5] Restore max HP")
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
            print("[5] Display stats")
            print("[6] List units")
            print("[0] Exit")

            menuSelection = int(input())
            if menuSelection == 0:
                running = False
            elif menuSelection == 1:
                print("Current stats:")
                selectedUnit.printCurrentNCap()
                print("Enter the number of levels to raise the unit.")
                levelUp = int(input())
                selectedUnit.levelSimulate(levelUp)
                print("Would you like to save this unit? Enter [Y]. ")
                answer = input()
                if(answer == "Y" or answer == "y"):
                    print("Give the unit a name.")
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
                print("Current stats:")
                selectedUnit.printCurrentNCap()
                print("Enter the number of levels to calculate average stats.")
                levelUp = int(input())
                selectedUnit.avgStat(levelUp)
            elif menuSelection == 3:
                selectedUnit.setToCap()
                selectedUnit.printCurrentNCap()
                print("Would you like to save this unit? Enter [Y]. ")
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
                print("Current stats:")
                selectedUnit.printCurrentNCap()
                print("What stat do you want to change?")
                for i in range(0, len(STATS)):
                    print("[" + str(i + 1) + "] " + STATS[i])
                userInput = int(input())
                print("You want to change: " + STATS[userInput - 1])
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
    print("Select unit to initiate battle:")
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
    with open('stats.csv - finished.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tempUnit = Unit(row)
            unitList.append(tempUnit)
    with open('stats.csv - weapons.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tempWeapon = Weapon(row)
            weaponDic[tempWeapon.name] = tempWeapon

#Main Function
def main():
    initFile()
    menu()

main()