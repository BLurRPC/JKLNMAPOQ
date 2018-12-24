import csv
import os
import screenshot
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

def xlmparse(fileName, outputFileName):
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
                screenshoted = False
                port = tmpport.get("portid")
                status = tmpport.find('state').get("state")
                service = tmpport.find('service').get("name")
                product = tmpport.find('service').get("product")
                version = tmpport.find('service').get("version")
                addToCSVFile(address, port, service, product, version, status, outputFileName)
                if((service == "https" or service == "http") and not screenshoted):
                        screenshoted = True #Evite de faire 2 fois la même capture
                        screenshot.openAndScreen(service, address) #Fait une capture d'écran de la page

def launch(inputFileName, mode='-T3'):
    scanResultFileName = "scanResult.csv"
    hosts = readCSVFile(inputFileName)

    createCSVFile(scanResultFileName)
    for host in hosts:
        os.system("nmap -v " + mode +" -sV -oX " + host + "nmap.xml " + host)
        xlmparse(host+"nmap.xml", scanResultFileName)
        os.remove(host + "nmap.xml")