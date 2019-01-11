import os
from lxml import etree
import csv

def readCSVFile(filename, outputFileName):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:                        
                if(row[2]=="https" or row[2]=="ldaps" or row[2]=="sftp"):
                        sslscan(row[0], row[1], outputFileName)

def addToCSVFileSSLSCANCipher(address, port, status, sslversion, bits, cipher, signature, altnames, issuer, startDate, endDate, fileName):
    with open(fileName, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([address, port, status, sslversion, bits, cipher, signature, altnames, issuer, startDate, endDate])

def createCSVFileSSLSCANCipher(fileName):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['IP', 'PORT', 'STATUS', 'SSLVERSION', 'BITS', 'CIPHER', 'SIGNATURE', 'ALTNAMES', 'ISSUER', 'StartDate', 'EndDate'])

def xlmparseSSLSCAN(fileName, outputFileName):
    tree = etree.parse(fileName)
    root = tree.getroot()
    status = ""
    sslversion = ""
    bits = ""
    cipher = ""
    address = root.find('ssltest').get('host')
    port = root.find('ssltest').get('port')
    signature = root.find('ssltest/certificate/signature-algorithm').text
    altnames = root.find('ssltest/certificate/altnames').text
    issuer = root.find('ssltest/certificate/issuer').text
    startDate = root.find('ssltest/certificate/not-valid-before').text
    endDate = root.find('ssltest/certificate/not-valid-after').text

    for result in tree.xpath("/document/ssltest/cipher"):
        status = result.get("status")
        sslversion = result.get("sslversion")
        bits = result.get("bits")
        cipher = result.get("cipher")
        addToCSVFileSSLSCANCipher(address, port, status, sslversion, bits, cipher, signature, altnames, issuer, startDate, endDate, outputFileName)

def sslscan(address, port, outputFileName):
    resultFileName = address + ".xml"
    os.system("sslscan --no-failed --xml=" + resultFileName + " " + address + ":" + port)
    xlmparseSSLSCAN(resultFileName, outputFileName)
    os.remove(resultFileName)

def launch(inputFileName):
    sslscanFileName = "sslscanResult.csv"
    createCSVFileSSLSCANCipher(sslscanFileName)
    readCSVFile(inputFileName, sslscanFileName)
