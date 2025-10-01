import pyautogui
import time

def nextpage():
    try:
        nextpage = pyautogui.locateOnScreen("images/nextpage.png", confidence=0.9)
    except pyautogui.ImageNotFoundException:
        nextpage = None

    if nextpage:
        pyautogui.click(nextpage)
    else:
        print("Nächste Seite nicht gefunden.")

def playvideo():
    try:
        playbutton = pyautogui.locateOnScreen("images/playsymbol.png", confidence=0.8)
    except pyautogui.ImageNotFoundException:
        playbutton = None

    print(playbutton)
    if playbutton:
        pyautogui.click(playbutton)
        return True      # <-- Rückgabewert für Erfolg
    else:
        print("Play-Button nicht gefunden.")
        return False     # <-- Rückgabewert für Misserfolg

def sonderbonus():
    try:
        sonderbonus = pyautogui.locateOnScreen("images/sonderbonus.png", confidence=0.8)
    except pyautogui.ImageNotFoundException:
        sonderbonus = None

    if sonderbonus:
        pyautogui.click(sonderbonus)
        return True
    else:
        print("Sonderbonus nicht gefunden.")
        return False

def closesondermenu():
    try:
        closesondermenu = pyautogui.locateOnScreen("images/closesondermenu.png", confidence=0.8)
    except pyautogui.ImageNotFoundException:
        closesondermenu = None

    if closesondermenu:
        pyautogui.click(closesondermenu)
    else:
        print("Schließen-Symbol nicht gefunden.")

def redeem():
    try:
        redeem = pyautogui.locateOnScreen("images/redeem.png", confidence=0.8)
    except pyautogui.ImageNotFoundException:
        redeem = None

    if redeem:
        pyautogui.click(redeem)
        return True
    else:
        print("Redeem-Symbol nicht gefunden.")
        return False

def closeadmenu():
    try:
        closeadmenu = pyautogui.locateOnScreen("images/closeadmenu.png", confidence=0.8)
    except pyautogui.ImageNotFoundException:
        closeadmenu = None

    print(closeadmenu)
    if closeadmenu:
        pyautogui.click(closeadmenu)
    else:
        print("Schließen-Symbol nicht gefunden.")
    
    try:
        closeadmenu2 = pyautogui.locateOnScreen("images/abbrechen.png")
    except pyautogui.ImageNotFoundException:
        closeadmenu2 = None
    if closeadmenu2:
        pyautogui.click(closeadmenu2)
    else:
        print("Abbrechen-Symbol nicht gefunden.")

def fehlerbehebung():
    closeadmenu()
    closesondermenu()
    redeem()
    nextpage()
    playvideo()
    sonderbonus()

running = True
while running:
    try:
        adsymbol = pyautogui.locateOnScreen("images/adsymbol.png", confidence=0.8)
        if not adsymbol:
            adsymbol = pyautogui.locateOnScreen("images/adsymbol2.png", confidence=0.8)
    except pyautogui.ImageNotFoundException:
        print("Ad-Symbol nicht gefunden, suche nach Collectmoney-Symbol.")
        adsymbol = None
        try:
            collectmoney = pyautogui.locateOnScreen("images/collectmoney.png")
            if not collectmoney:
                collectmoney = pyautogui.locateOnScreen("images/collectmoney2.png", confidence=0.7)
        except pyautogui.ImageNotFoundException:
            print("Collectmoney-Symbol nicht gefunden, suche nach der nächsten Seite.")
            collectmoney = None
            if nextpage():
                print("Nächste Seite gefunden und geklickt.")
                time.sleep(2)
                continue
    if adsymbol:
        print("Ad-Symbol gefunden.")
        pyautogui.click(adsymbol)
        time.sleep(2)
        if playvideo():
            print("Video gestartet")
            for _ in range(60):
                if sonderbonus():
                    print("Sonderbonus gefunden und geklickt.")
                    break
                else:
                    print("Versuch"+str(_+1)+"/60")
                time.sleep(1)
                if _ == 59:
                    print("Sonderbonus nicht gefunden, fehlerbehebung wird ausgeführt.")
                    fehlerbehebung()
            time.sleep(2)
            if playvideo():
                print("Sonderbonusvideo gestartet")
                for _ in range(60):
                    if closesondermenu() or redeem():
                        print("Sonderbonusvideo erfolgreich geschlossen oder eingelöst.")
                        break
                    else:
                        print("versuch"+str(_+1)+"/60")
                    time.sleep(1)
                    if _ == 59:
                        print("Sonderbonusvideo nicht geschlossen, fehlerbehebung wird ausgeführt.")
                        fehlerbehebung()
    elif collectmoney:
        print("Collectmoney-Symbol gefunden.")
        pyautogui.click(collectmoney)
        time.sleep(2)
        continue