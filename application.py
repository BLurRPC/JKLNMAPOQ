import nmap
import sslscan
import discover
import clean
import sys
import argparse

def fileCheck(fn):
        try:
                open(fn, "r")
                return True
        except IOError:
                print ("Ce fichier ne semble pas exister...")
                return False

#Get Args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--discover', metavar="filename", help="Scan de decouverte.")
parser.add_argument('-n', '--nmap', metavar="filename", help="Scan nmap avec recherche de service.")
parser.add_argument('-s', '--sslscan', metavar="filename", help="Scan ssl.")
parser.add_argument('-c', '--clean', action="store_true", help="Nettoie le répertoire.")
parser.add_argument('-a', '--all', metavar="filename", help="Scan nmap suivi d'un scan ssl.")
parser.add_argument('-T3', '--force', action="store_true", help="Change la force du scan en -T3 au lieu de -T2")
args = parser.parse_args()

if(args.clean):
        clean.launch()
        
if(args.discover!=None):
        inputFileName = args.discover
        if(fileCheck(inputFileName)):
                discover.launch(inputFileName)

if(args.nmap!=None):
        inputFileName = args.nmap
        if(fileCheck(inputFileName)):
                if(args.force!=None):
                        nmap.launch(inputFileName, '-T3')
                else:
                        nmap.launch(inputFileName)

if(args.sslscan!=None):
        inputFileName = args.sslscan
        if(fileCheck(inputFileName)):
                sslscan.launch(inputFileName)

if(args.all!=None): #nmap then sslscan using nmap's results
        inputFileName = args.all
        if(fileCheck(inputFileName)):
                if(args.force):
                        nmap.launch(inputFileName, '-T3')
                else:
                        nmap.launch(inputFileName)
        inputFileName = "scanResult.csv"
        if(fileCheck(inputFileName)):
                sslscan.launch(inputFileName)