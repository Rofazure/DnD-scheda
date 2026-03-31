# ⚔ D&D 5e — Generatore Schede Personaggio

Un programma con interfaccia grafica per creare e salvare schede personaggio per **D&D 5e**, con output in formato **TXT** e **PDF**.

---

## Requisiti

- Python 3
- Tkinter
- Reportlab

---

## Installazione

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

---

## Avvio

```bash
python3 dnd_scheda.py
```

---

## Funzionalità

- Interfaccia grafica con tema scuro ispirato a D&D
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

## Output

I file vengono salvati nella cartella `~/d&d/personaggi/` con il nome del personaggio:

```
NomePersonaggio.txt
NomePersonaggio.pdf
```

La cartella di destinazione è modificabile direttamente dall'interfaccia.

---

## Aggiornamenti

Per scaricare l'ultima versione:

```bash
git pull
```

---

## Testato su

- Linux Mint 22
- Python 3.12

---

*Creato per uso personale. Buone avventure!* 🎲
