# ⚔ D&D 5e — Generatore Schede Personaggio

Un programma con interfaccia grafica per creare e salvare schede personaggio per **D&D 5e**, con output in formato **TXT** e **PDF**.

All'avvio il programma chiede dove vuoi salvare le schede, così puoi scegliere la cartella che preferisci su qualsiasi sistema operativo.

---

## Funzionalità

- Interfaccia grafica con tema scuro ispirato a D&D
- Dialogo di selezione cartella all'avvio
- Campi per tutti i dati del personaggio:
  - Identità (nome, età, specie, classe, sotto-classe, livello, edizione)
  - Statistiche e modificatori (FOR, DES, COS, INT, SAG, CAR)
  - Tiri salvezza e competenze
  - Combattimento (HP, CA, iniziativa, velocità, grandezza, percezione passiva)
  - Armamento ed equipaggiamento
  - Abilità di classe
  - Magia (trucchetti, slot per livello, incantesimi noti)
  - Note libere
- Salvataggio automatico in **TXT** e **PDF** nella cartella scelta
- Pulsante per pulire tutti i campi

---

## Installazione su Linux (Ubuntu / Mint e derivate)

### 1. Clona il repository

```bash
git clone https://github.com/Rofazure/DnD-scheda.git
cd DnD-scheda
```

### 2. Installa le dipendenze

```bash
sudo apt install python3 python3-tk
pip install reportlab --break-system-packages
```

### 3. Avvia il programma

```bash
python3 dnd_scheda.py
```

---

## Installazione su Windows

### 1. Installa Python

- Scarica Python da [python.org](https://www.python.org/downloads/)
- Durante l'installazione spunta **"Add Python to PATH"** — importante!

### 2. Clona il repository

Apri il **Prompt dei comandi** (cerca `cmd` nel menu Start) e scrivi:

```cmd
git clone https://github.com/Rofazure/DnD-scheda.git
cd DnD-scheda
```

> Se git non è installato, scaricalo da [git-scm.com](https://git-scm.com/download/win)

### 3. Installa le dipendenze

```cmd
pip install reportlab
```

> Tkinter è già incluso nell'installazione di Python su Windows, non serve installarlo separatamente.

### 4. Avvia il programma

```cmd
python dnd_scheda.py
```

---

## Aggiornamenti

Per scaricare l'ultima versione del programma:

```bash
git pull
```

---

## Testato su

- Linux Mint 22 — Python 3.12
- Windows 10/11 — Python 3.12

---

*Creato per uso personale. Buone avventure!* 🎲
