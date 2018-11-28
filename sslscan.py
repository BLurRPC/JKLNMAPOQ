import os
from lxml import etree

def xlmparse(fileName):
    tree = etree.parse(fileName)
    for cipher in tree.xpath("/document/ssltest/cipher"):
        print(cipher.get("cipher"))
    for certificate in tree.xpath("/document/ssltest/certificate/signature-algorithm"):
        print(certificate.text)

def sslscan(address):
    resultFileName = address + ".xml"
    #os.system("sslscan --xml=" + resultFileName + " " + address)
    #xlmparse(resultFileName)
    xlmparse("google.xml")
    #os.remove(resultFileName)

sslscan("127.0.0.1")