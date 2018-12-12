import json
import csv
import argparse
import sslscan
import os
from lxml import etree

def createCSVFile(fileName):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['IP', 'PORT', 'Service', 'Product', 'Version', 'STATUS'])


def addToCSVFile(ip, port, serviceName, productName, productVersion, status, fileName):
    with open(fileName, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([ip, port, serviceName, productName, productVersion, status])

def readCSVFile(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            return row

def xlmparse(fileName, outputFileName, sslscanFileName):
    tree = etree.parse(fileName)
    root = tree.getroot()
    status = ""
    address = ""
    port = ""
    service = ""
    product = ""
    version = ""

    for host in root.iter('host'):
        for result in host.findall('address'):
                address = result.get("addr")
        for tmpport in host.findall('ports/port'):
                port = tmpport.get("portid")
                status = tmpport.find('state').get("state")
                service = tmpport.find('service').get("name")
                product = tmpport.find('service').get("product")
                version = tmpport.find('service').get("version")
                addToCSVFile(address, port, service, product, version, status, outputFileName)
                if(service == "https" or service == "ssl"):
                        sslscan.sslscan(address, sslscanFileName) #sslscan

inputFileName = "input.csv"
scanResultFileName = "scanResult.csv"
sslscanFileName = "sslscanResult.csv"
hosts = readCSVFile(inputFileName)

createCSVFile(scanResultFileName)
for host in hosts:
    os.system("nmap -v -T2 -sV -oX " + host + "nmap.xml " + host)
    xlmparse(host+"nmap.xml", scanResultFileName, sslscanFileName)
    os.remove(host + "nmap.xml")