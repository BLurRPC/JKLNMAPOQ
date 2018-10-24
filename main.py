import nmap
import json
import csv

def createCSVFile():
    with open('scan.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['IP', 'PORT', 'Service', 'Product', 'Version', 'STATUS'])


def addToCSVFile(ip, port, serviceName, productName, productVersion, status):
    with open('scan.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([ip, port, serviceName, productName, productVersion, status])

hosts = ['127.0.0.1-3']
createCSVFile()
for host in hosts:
    nm = nmap.PortScanner()
    result = nm.scan(host, arguments='-p- -sV')
    for address in result["scan"]:
        print("address : " + address)
        #print(result["scan"])
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
            addToCSVFile(address, str(port), serviceName, productName, productVersion, status)
