from selenium import webdriver

def openAndScreen(service, url):
    browser = webdriver.Firefox()
    try:
        browser.get(service + '://' + url)
        browser.save_screenshot('./screenshots/'+url+'.png')
    except:
        print("Une erreur est survenue en ouvrant la page " + service + '://' + url)
    browser.quit()