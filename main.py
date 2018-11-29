import nmap
import json
import csv
import argparse
import sslscan

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

inputFileName = "input.csv"
scanResultFileName = "scanResult.csv"
hosts = readCSVFile(inputFileName)

createCSVFile(scanResultFileName)
for host in hosts:
    nm = nmap.PortScanner()
    result = nm.scan(host, arguments='-p- -sV')
    print(result["scan"])
    for address in result["scan"]:
        print("address : " + address)
        if('tcp' in result["scan"][address]):
            ip = result["scan"][address]['addresses']['ipv4'] #Save ip address
            for port in result["scan"][address]['tcp']:
                serviceName = result["scan"][address]['tcp'][port]['name'] #Name of the service
                print("service name on port "+ str(port) + " : " + serviceName)

                productName = result["scan"][address]['tcp'][port]['product'] #Product
                print("product on port "+ str(port) + " : " + productName)

                productVersion = result["scan"][address]['tcp'][port]['version']
                print("product version on port "+ str(port) + " : " + productVersion)

                status = result["scan"][address]['tcp'][port]['state']
                print("status on port "+ str(port)+ " : " + status)
                addToCSVFile(address, str(port), serviceName, productName, productVersion, status, scanResultFileName)