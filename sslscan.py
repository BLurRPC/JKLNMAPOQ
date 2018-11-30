import os
from lxml import etree
import csv

def addToCSVFileSSLSCANCipher(status, sslversion, bits, cipher, fileName):
    with open(fileName, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([status, sslversion, bits, cipher])

def createCSVFileSSLSCANCipher(fileName, address, port):
    with open(fileName, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([address, port])
        writer.writerow(['STATUS', 'SSLVERSION', 'BITS', 'CIPHER'])

def addToCSVFileSSLSCANCertificate(signature, altnames, issuer, startDate, endDate, fileName):
    with open(fileName, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([signature, altnames, issuer, startDate, endDate])

def createCSVFileSSLSCANCertificate(fileName, address, port):
    with open(fileName, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['SIGNATURE', 'ALTNAMES', 'ISSUER', 'StartDate', 'EndDate'])

def xlmparseSSLSCAN(fileName, outputFileName):
    tree = etree.parse(fileName)
    root = tree.getroot()
    status = ""
    sslversion = ""
    bits = ""
    cipher = ""
    address = ""
    port = ""
    signature = ""
    altnames = ""
    issuer = ""
    startDate = ""
    endDate = ""

    for result in tree.xpath("/document/ssltest"):
        address = result.get("host")
        port = result.get("port")

    createCSVFileSSLSCANCipher(outputFileName, address, port)

    for result in tree.xpath("/document/ssltest/cipher"):
        status = result.get("status")
        sslversion = result.get("sslversion")
        bits = result.get("bits")
        cipher = result.get("cipher")
        addToCSVFileSSLSCANCipher(status, sslversion, bits, cipher, outputFileName)
    
    createCSVFileSSLSCANCertificate(outputFileName, address, port)

    for result in root.findall('ssltest/certificate'):
        signature = result.find('signature-algorithm').text
        altnames = result.find('altnames').text
        issuer = result.find('issuer').text
        startDate = result.find('not-valid-before').text
        endDate = result.find('not-valid-after').text
        addToCSVFileSSLSCANCertificate(signature, altnames, issuer, startDate, endDate, outputFileName)

def sslscan(address, outputFileName):
    resultFileName = address + ".xml"
    os.system("sslscan --xml=" + resultFileName + " " + address)
    xlmparseSSLSCAN(resultFileName, outputFileName)
    #xlmparse("google.xml", outputFileName)
    os.remove(resultFileName)