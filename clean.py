import os

def launch():
    answer = input("Es-tu sûr de vouloir supprimer les fichiers *.xml et les résultats des différents scans ? (o/n) : ")
    if(answer == 'o'):
        os.system("rm *.xml *.log discovered.csv sslscanResult.csv scanResult.csv ./screenshots/*") #clean results and useless files
    else:
        print("Operation annulée.")