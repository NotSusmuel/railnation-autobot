# Railnation Autobot
Ein Bot um in Railnation Werbung zu gucken

## Features
- 🎨 **Modern UI** - Benutzerfreundliche grafische Oberfläche mit dunklem Theme
- ⚡ **Keyboard Shortcuts** - F5 zum Starten, F6 zum Stoppen
- ⚙️ **Konfigurierbare Einstellungen** - Wartezeiten und Intervalle anpassen
- 📊 **Echtzeit-Logging** - Alle Bot-Aktivitäten im Blick behalten

## Installation

1. Python 3 installieren (falls noch nicht vorhanden)
2. Benötigte Pakete installieren:
```bash
pip install -r requirements.txt
```
Oder manuell:
```bash
pip install pyautogui pillow
```

## Verwendung

### Mit UI (empfohlen)
```bash
python3 railnation_ui.py
```

**Tastenkombinationen:**
- `F5` - Bot starten
- `F6` - Bot stoppen

**Einstellungen:**
- **Video Wait Time** - Wie lange auf Sonderbonus-Symbol gewartet wird (Standard: 60s)
- **Check Interval** - Wie oft nach Symbolen gesucht wird (Standard: 1s)
- **Click Delay** - Pause nach Klicks (Standard: 2s)

### Ohne UI (Original-Skript)
```bash
python3 railnation_autoad.py
```

## Screenshots
Füge deine Screenshots in den `images/` Ordner ein, wenn du das Spiel in einer anderen Sprache spielst.
