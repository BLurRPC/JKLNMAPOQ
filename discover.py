import json
import csv
import argparse
import os
from lxml import etree

def addToCSVFileDiscover(ip, fileName):
    with open(fileName, 'a+', newline='') as csvfile:
        csvfile.write(ip + ",")

def readCSVFileDiscover(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            return row

def xlmparseDiscover(fileName, outputFileName):
    tree = etree.parse(fileName)
    root = tree.getroot()
    address = ""

    for host in root.iter('host'):
        for result in host.findall('address'):
                if(result.get("addrtype") == "ipv4"):
                        address = result.get("addr")
                        addToCSVFileDiscover(address, outputFileName)

def launch(inputFileName):
        scanResultFileName = "discovered.csv"
        hosts = readCSVFileDiscover(inputFileName)
        for host in hosts:
                name = host.split("/")[0]
                os.system("nmap -sP -oX " + name + "discover.xml " + host)
                xlmparseDiscover(name + "discover.xml", scanResultFileName)
                os.remove(name + "discover.xml")