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

def xlmparse(fileName, outputFileName):
    tree = etree.parse(fileName)
    status = ""
    sslversion = ""
    bits = ""
    cipher = ""
    address = ""
    port = ""

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
    
    for certificate in tree.xpath("/document/ssltest/certificate/signature-algorithm"):
        print(certificate.text)

def sslscan(address, outputFileName):
    resultFileName = address + ".xml"
    os.system("sslscan --xml=" + resultFileName + " " + address)
    xlmparse(resultFileName, outputFileName)
    #xlmparse("google.xml", outputFileName)
    os.remove(resultFileName)

sslscanFileName = "sslscanResult.csv"
sslscan("127.0.0.1", sslscanFileName)