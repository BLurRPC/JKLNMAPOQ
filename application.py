import nmap
import sslscan
import discover
import clean
import sys

def discoverLaunch(inputFileName="input.csv"):
        discover.launch(inputFileName)

def nmapLaunch(inputFileName="input.csv"):
        nmap.launch(inputFileName)

def sslscanLaunch(inputFileName="input.csv"):
        sslscan.launch(inputFileName)

def allLaunch(inputFileName="input.csv"):
        print("Tout est lancé ...")
        #A faire

def cleanLaunch():
        clean.launch()

def fileCheck(fn):
        try:
                open(fn, "r")
                return True
        except IOError:
                print ("Ce fichier ne semble pas exister...")
                return False

#Option args
options = {0 : discoverLaunch, 1 : nmapLaunch, 2 : sslscanLaunch, 3 : allLaunch, 4 : cleanLaunch}
#Display options
print("Bienvenue, voici les options possibles :\n0 : Scan de découverte\n1 : Scan complet avec recherche de services\n2 : Sslscan\n3 : Combinaison des options 1 et 2\n4 : Supprime les fichiers *.xml et les résultats\n5 : Quitter")
#Get args

while(True):
        ready = False
        while(not ready):
                try:
                        option = int(input("Option numéro ? :\n"))
                        ready = True
                except ValueError:
                        print("Cette option n'est pas un entier.")

        if(option == 5):
                print("Au revoir.")
                sys.exit(0)
        elif(option == 4):
                #Do clean
                cleanLaunch()
        elif(option < 4):
                #Do things
                inputFile = input("Fichier d'entrée ? :\n")
                if(fileCheck(inputFile)):
                        options[option](inputFile)
        else:
                print("Cette option n'existe pas")