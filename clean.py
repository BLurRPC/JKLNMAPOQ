import os

answer = input("Do you really want to delete xml files and results ? (y/n) : ")
if(answer == 'y'):
    os.system("rm *.xml discovered.csv sslScanResult.csv scanResult.csv") #clean results and useless files
else:
    print("Operation aborted")