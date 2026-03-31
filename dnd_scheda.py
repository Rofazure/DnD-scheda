#!/usr/bin/env python3
"""
D&D 5e - Generatore Schede Personaggio
GUI con Tkinter + output TXT e PDF
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime

# ── dipendenze opzionali ──────────────────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                     Table, TableStyle, HRFlowable)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

# ── cartella di salvataggio di default ────────────────────────────────────────
DEFAULT_DIR = os.path.expanduser("~/d&d/personaggi")
os.makedirs(DEFAULT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTE / STILE
# ─────────────────────────────────────────────────────────────────────────────
BG       = "#1a1a2e"   # sfondo scuro
BG2      = "#16213e"   # sfondo pannello
ACCENT   = "#e94560"   # rosso D&D
GOLD     = "#f5a623"   # oro
TEXT     = "#eaeaea"   # testo chiaro
ENTRY_BG = "#0f3460"   # sfondo campo
ENTRY_FG = "#ffffff"

FONT_TITLE  = ("Georgia", 18, "bold")
FONT_SEC    = ("Georgia", 11, "bold")
FONT_LBL    = ("Helvetica", 9)
FONT_ENTRY  = ("Courier", 10)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: etichetta + campo su griglia
# ─────────────────────────────────────────────────────────────────────────────
def labeled_entry(parent, label, row, col, width=14, colspan=1):
    tk.Label(parent, text=label, bg=BG2, fg=GOLD,
             font=FONT_LBL).grid(row=row, column=col,
                                  sticky="w", padx=4, pady=1)
    var = tk.StringVar()
    e = tk.Entry(parent, textvariable=var, width=width,
                 bg=ENTRY_BG, fg=ENTRY_FG, font=FONT_ENTRY,
                 insertbackground=ENTRY_FG, relief="flat",
                 highlightthickness=1, highlightcolor=ACCENT,
                 highlightbackground="#333355")
    e.grid(row=row+1, column=col, columnspan=colspan,
           sticky="ew", padx=4, pady=2)
    return var

def labeled_text(parent, label, row, col, width=30, height=3, colspan=1):
    tk.Label(parent, text=label, bg=BG2, fg=GOLD,
             font=FONT_LBL).grid(row=row, column=col,
                                  sticky="w", padx=4, pady=1)
    t = tk.Text(parent, width=width, height=height,
                bg=ENTRY_BG, fg=ENTRY_FG, font=FONT_ENTRY,
                insertbackground=ENTRY_FG, relief="flat",
                highlightthickness=1, highlightcolor=ACCENT,
                highlightbackground="#333355")
    t.grid(row=row+1, column=col, columnspan=colspan,
           sticky="ew", padx=4, pady=2)
    return t

# ─────────────────────────────────────────────────────────────────────────────
# FINESTRA PRINCIPALE
# ─────────────────────────────────────────────────────────────────────────────
class DnDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("D&D 5e — Generatore Schede Personaggio")
        self.configure(bg=BG)
        self.resizable(True, True)

        # ── titolo ──
        hdr = tk.Frame(self, bg=ACCENT, pady=6)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⚔  D&D 5e  —  Scheda Personaggio  ⚔",
                 font=FONT_TITLE, bg=ACCENT, fg="white").pack()

        # ── scrollable body ──
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=10, pady=6)

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.body = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=self.body, anchor="nw")

        def _on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(win_id, width=canvas.winfo_width())
        self.body.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(win_id, width=e.width))
        self.body.bind("<MouseWheel>",
                       lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        self._build_form()
        self._build_buttons()

    # ── sezione decorativa ────────────────────────────────────────────────────
    def _section(self, title):
        f = tk.LabelFrame(self.body, text=f"  {title}  ",
                          bg=BG2, fg=ACCENT, font=FONT_SEC,
                          bd=1, relief="groove",
                          labelanchor="nw")
        f.pack(fill="x", padx=8, pady=6)
        return f

    # ── costruzione form ──────────────────────────────────────────────────────
    def _build_form(self):
        # ── IDENTITÀ ──
        s = self._section("📋  Identità del Personaggio")
        self.nome        = labeled_entry(s, "NOME",          0, 0, 20)
        self.eta         = labeled_entry(s, "ETA'",          0, 1, 10)
        self.background  = labeled_entry(s, "BACKGROUND",    0, 2, 16)
        self.specie      = labeled_entry(s, "SPECIE",        0, 3, 16)
        self.classe      = labeled_entry(s, "CLASSE",        0, 4, 14)
        self.sottoclasse = labeled_entry(s, "SOTTO-CLASSE",  0, 5, 14)
        self.livello     = labeled_entry(s, "LV",            0, 6,  5)
        self.edizione    = labeled_entry(s, "EDIZIONE D&D",  0, 7, 10)

        # ── STATISTICHE ──
        s2 = self._section("🎲  Statistiche")
        stats = [("FOR", 0), ("DES", 2), ("COS", 4),
                 ("INT", 6), ("SAG", 8), ("CAR", 10)]
        self.stats = {}
        for nome, col in stats:
            self.stats[nome] = labeled_entry(s2, nome, 0, col, 7)

        # ── TIRI SALVEZZA ──
        s3 = self._section("🛡  Tiri Salvezza & Competenze")
        ts_names = ["TS FOR", "TS DES", "TS COS", "TS INT", "TS SAG", "TS CAR"]
        self.ts = {}
        for i, n in enumerate(ts_names):
            self.ts[n] = labeled_entry(s3, n, 0, i*2, 8)

        tk.Label(s3, text="Competenze (una per riga):",
                 bg=BG2, fg=GOLD, font=FONT_LBL).grid(
                 row=3, column=0, columnspan=4, sticky="w", padx=4, pady=(8,1))
        self.competenze = tk.Text(s3, width=80, height=4,
                                  bg=ENTRY_BG, fg=ENTRY_FG, font=FONT_ENTRY,
                                  insertbackground=ENTRY_FG, relief="flat",
                                  highlightthickness=1, highlightcolor=ACCENT,
                                  highlightbackground="#333355")
        self.competenze.grid(row=4, column=0, columnspan=12,
                             sticky="ew", padx=4, pady=2)

        # ── COMBATTIMENTO ──
        s4 = self._section("⚔  Combattimento")
        combat = [("HP Max", 0), ("CA", 2), ("Iniziativa", 4),
                  ("Velocità", 6), ("Grandezza", 8), ("Per. Passiva", 10)]
        self.combat = {}
        for nome, col in combat:
            self.combat[nome] = labeled_entry(s4, nome, 0, col, 9)

        # ── ARMAMENTO ──
        s5 = self._section("🗡  Armamento")
        self.armamento = labeled_text(s5, "Armi (una per riga: nome, t.p.c, danni):",
                                      0, 0, colspan=6, height=4, width=80)

        # ── EQUIPAGGIAMENTO ──
        s6 = self._section("🎒  Equipaggiamento")
        self.equipaggiamento = labeled_text(s6, "Oggetti:", 0, 0,
                                            colspan=6, height=4, width=80)
        self.extra = labeled_text(s6, "Extra (dotazione):", 2, 0,
                                  colspan=6, height=3, width=80)

        # ── ABILITA' DI CLASSE ──
        s7 = self._section("✨  Abilità di Classe & Tratti")
        self.abilita = labeled_text(s7, "Abilità:", 0, 0,
                                    colspan=6, height=4, width=80)

        # ── MAGIA ──
        s8 = self._section("🔮  Magia")
        self.trucchetti = labeled_entry(s8, "Trucchetti:", 0, 0, 60, colspan=4)

        slot_frame = tk.Frame(s8, bg=BG2)
        slot_frame.grid(row=2, column=0, columnspan=6, sticky="ew", pady=4)
        self.slots = {}
        for i in range(1, 10):
            tk.Label(slot_frame, text=f"{i}°", bg=BG2, fg=GOLD,
                     font=FONT_LBL).grid(row=0, column=(i-1)*2, padx=4)
            var = tk.StringVar()
            e = tk.Entry(slot_frame, textvariable=var, width=8,
                         bg=ENTRY_BG, fg=ENTRY_FG, font=FONT_ENTRY,
                         insertbackground=ENTRY_FG, relief="flat",
                         highlightthickness=1, highlightcolor=ACCENT,
                         highlightbackground="#333355")
            e.grid(row=1, column=(i-1)*2, padx=4, pady=2)
            self.slots[i] = var

        self.incantesimi = labeled_text(s8, "Incantesimi noti:", 3, 0,
                                        colspan=6, height=5, width=80)

        # ── NOTE ──
        s9 = self._section("📝  Note")
        self.note = labeled_text(s9, "Note libere:", 0, 0,
                                 colspan=6, height=4, width=80)

        # ── CARTELLA OUTPUT ──
        sdir = self._section("📁  Cartella di salvataggio")
        self.save_dir = tk.StringVar(value=DEFAULT_DIR)
        tk.Entry(sdir, textvariable=self.save_dir, width=60,
                 bg=ENTRY_BG, fg=ENTRY_FG, font=FONT_ENTRY,
                 insertbackground=ENTRY_FG, relief="flat").grid(
                 row=0, column=0, padx=6, pady=6, sticky="ew")
        tk.Button(sdir, text="Sfoglia…", bg=ACCENT, fg="white",
                  font=FONT_LBL, relief="flat", cursor="hand2",
                  command=self._browse_dir).grid(row=0, column=1, padx=4)

    # ── pulsanti ──────────────────────────────────────────────────────────────
    def _build_buttons(self):
        bar = tk.Frame(self.body, bg=BG, pady=10)
        bar.pack(fill="x", padx=8)

        btn_style = dict(font=("Helvetica", 11, "bold"), relief="flat",
                         cursor="hand2", padx=20, pady=8)
        tk.Button(bar, text="💾  Salva TXT + PDF", bg=ACCENT, fg="white",
                  command=self._salva, **btn_style).pack(side="left", padx=6)
        tk.Button(bar, text="🗑  Pulisci tutto", bg="#444", fg=TEXT,
                  command=self._pulisci, **btn_style).pack(side="left", padx=6)
        if not REPORTLAB_OK:
            tk.Label(bar,
                     text="⚠ reportlab non trovato: solo TXT disponibile",
                     bg=BG, fg=GOLD, font=FONT_LBL).pack(side="left", padx=10)

    # ── browse ────────────────────────────────────────────────────────────────
    def _browse_dir(self):
        d = filedialog.askdirectory(initialdir=self.save_dir.get())
        if d:
            self.save_dir.set(d)

    # ── raccolta dati ─────────────────────────────────────────────────────────
    def _get(self):
        d = {}
        d["nome"]        = self.nome.get().strip()
        d["eta"]         = self.eta.get().strip()
        d["background"]  = self.background.get().strip()
        d["specie"]      = self.specie.get().strip()
        d["classe"]      = self.classe.get().strip()
        d["sottoclasse"] = self.sottoclasse.get().strip()
        d["livello"]     = self.livello.get().strip()
        d["edizione"]    = self.edizione.get().strip()
        d["stats"]       = {k: v.get().strip() for k, v in self.stats.items()}
        d["ts"]          = {k: v.get().strip() for k, v in self.ts.items()}
        d["competenze"]  = self.competenze.get("1.0", "end").strip()
        d["combat"]      = {k: v.get().strip() for k, v in self.combat.items()}
        d["armamento"]   = self.armamento.get("1.0", "end").strip()
        d["equipaggiamento"] = self.equipaggiamento.get("1.0", "end").strip()
        d["extra"]       = self.extra.get("1.0", "end").strip()
        d["abilita"]     = self.abilita.get("1.0", "end").strip()
        d["trucchetti"]  = self.trucchetti.get().strip()
        d["slots"]       = {i: v.get().strip() for i, v in self.slots.items()}
        d["incantesimi"] = self.incantesimi.get("1.0", "end").strip()
        d["note"]        = self.note.get("1.0", "end").strip()
        return d

    # ── salvataggio ───────────────────────────────────────────────────────────
    def _salva(self):
        d = self._get()
        if not d["nome"]:
            messagebox.showwarning("Attenzione", "Inserisci almeno il nome!")
            return

        folder = self.save_dir.get()
        os.makedirs(folder, exist_ok=True)
        safe = d["nome"].replace(" ", "_")

        txt_path = os.path.join(folder, f"{safe}.txt")
        self._salva_txt(d, txt_path)

        pdf_path = None
        if REPORTLAB_OK:
            pdf_path = os.path.join(folder, f"{safe}.pdf")
            self._salva_pdf(d, pdf_path)

        msg = f"✅ Salvato in:\n{txt_path}"
        if pdf_path:
            msg += f"\n{pdf_path}"
        messagebox.showinfo("Salvato!", msg)

    # ── TXT ───────────────────────────────────────────────────────────────────
    def _salva_txt(self, d, path):
        W = 72
        sep  = "=" * W
        sep2 = "-" * W

        def center(t): return t.center(W)
        def field(label, val, w=18):
            return f"{label+':':<{w}}{val}"

        lines = [
            sep,
            center("⚔  D&D 5e  —  SCHEDA PERSONAGGIO  ⚔"),
            sep,
            "",
            field("NOME",         d["nome"]),
            field("ETA'",         d["eta"]),
            field("BACKGROUND",   d["background"]),
            field("SPECIE",       d["specie"]),
            field("CLASSE",       d["classe"]),
            field("SOTTO-CLASSE", d["sottoclasse"]),
            field("LIVELLO",      d["livello"]),
            field("EDIZIONE D&D", d["edizione"]),
            "",
            sep2,
            center("STATISTICHE E COMPETENZE"),
            sep2,
        ]

        st = d["stats"]
        lines.append(
            f"FOR: {st.get('FOR',''):<8}  DES: {st.get('DES',''):<8}  "
            f"COS: {st.get('COS',''):<8}  INT: {st.get('INT',''):<8}  "
            f"SAG: {st.get('SAG',''):<8}  CAR: {st.get('CAR','')}"
        )
        lines.append("")

        ts = d["ts"]
        lines.append(
            f"TS FOR:{ts.get('TS FOR',''):<6}  TS DES:{ts.get('TS DES',''):<6}  "
            f"TS COS:{ts.get('TS COS',''):<6}  TS INT:{ts.get('TS INT',''):<6}  "
            f"TS SAG:{ts.get('TS SAG',''):<6}  TS CAR:{ts.get('TS CAR','')}"
        )
        if d["competenze"]:
            lines.append("")
            lines.append("Competenze:")
            for row in d["competenze"].splitlines():
                lines.append(f"  {row}")

        lines += ["", sep2, center("COMBATTIMENTO"), sep2]
        cb = d["combat"]
        lines.append(
            f"HP Max: {cb.get('HP Max',''):<8}  CA: {cb.get('CA',''):<6}  "
            f"Iniziativa: {cb.get('Iniziativa',''):<6}  Velocità: {cb.get('Velocità',''):<8}  "
            f"Grandezza: {cb.get('Grandezza',''):<8}  Per.Passiva: {cb.get('Per. Passiva','')}"
        )

        def section(title, content):
            out = ["", sep2, center(title.upper()), sep2]
            if content:
                for row in content.splitlines():
                    out.append(f"  {row}")
            else:
                out.append("  —")
            return out

        lines += section("Armamento",        d["armamento"])
        lines += section("Equipaggiamento",  d["equipaggiamento"])
        if d["extra"]:
            lines += section("Extra (dotazione)", d["extra"])
        lines += section("Abilità di Classe", d["abilita"])

        lines += ["", sep2, center("MAGIA"), sep2]
        lines.append(f"Trucchetti: {d['trucchetti']}")
        slots_str = "  ".join(
            f"{i}°: {v}" for i, v in d["slots"].items() if v
        )
        if slots_str:
            lines.append(f"Slot: {slots_str}")
        if d["incantesimi"]:
            lines.append("Incantesimi:")
            for row in d["incantesimi"].splitlines():
                lines.append(f"  {row}")

        if d["note"]:
            lines += section("Note", d["note"])

        lines += ["", sep,
                  center(f"Generato il {datetime.now().strftime('%d/%m/%Y %H:%M')}"),
                  sep]

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # ── PDF ───────────────────────────────────────────────────────────────────
    def _salva_pdf(self, d, path):
        doc = SimpleDocTemplate(
            path, pagesize=A4,
            leftMargin=1.8*cm, rightMargin=1.8*cm,
            topMargin=1.5*cm, bottomMargin=1.5*cm
        )

        styles = getSampleStyleSheet()
        S = lambda name, **kw: ParagraphStyle(name, **kw)

        sTitle = S("sTitle", fontSize=20, textColor=colors.HexColor("#e94560"),
                   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
        sSub   = S("sSub",   fontSize=10, textColor=colors.HexColor("#888"),
                   fontName="Helvetica", alignment=TA_CENTER, spaceAfter=12)
        sSec   = S("sSec",   fontSize=12, textColor=colors.HexColor("#f5a623"),
                   fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)
        sNorm  = S("sNorm",  fontSize=9,  textColor=colors.HexColor("#222"),
                   fontName="Helvetica",  spaceAfter=2)
        sLabel = S("sLabel", fontSize=8,  textColor=colors.HexColor("#555"),
                   fontName="Helvetica-Bold")

        # colori tabelle
        HDR_BG  = colors.HexColor("#1a1a2e")
        ROW_BG1 = colors.HexColor("#e8e8f0")
        ROW_BG2 = colors.white
        ACCENT_C= colors.HexColor("#e94560")

        def table_style(header=True):
            base = [
                ("FONTNAME",   (0,0), (-1,-1), "Helvetica"),
                ("FONTSIZE",   (0,0), (-1,-1), 8),
                ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1,-1),
                 [ROW_BG1, ROW_BG2]),
                ("GRID",       (0,0), (-1,-1), 0.3, colors.HexColor("#ccccdd")),
                ("LEFTPADDING",(0,0), (-1,-1), 5),
                ("RIGHTPADDING",(0,0),(-1,-1), 5),
                ("TOPPADDING", (0,0), (-1,-1), 3),
                ("BOTTOMPADDING",(0,0),(-1,-1),3),
            ]
            if header:
                base += [
                    ("BACKGROUND",  (0,0), (-1,0), HDR_BG),
                    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
                    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
                    ("FONTSIZE",    (0,0), (-1,0), 9),
                ]
            return TableStyle(base)

        story = []

        # ── intestazione ──
        story.append(Paragraph("⚔  D&amp;D 5e  —  Scheda Personaggio  ⚔", sTitle))
        story.append(Paragraph(
            f"Generata il {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            sSub
        ))
        story.append(HRFlowable(width="100%", thickness=2,
                                color=ACCENT_C, spaceAfter=6))

        # ── identità ──
        story.append(Paragraph("📋  Identità del Personaggio", sSec))
        id_data = [
            ["Nome", "Età", "Background", "Specie"],
            [d["nome"], d["eta"], d["background"], d["specie"]],
            ["Classe", "Sotto-Classe", "Livello", "Edizione D&D"],
            [d["classe"], d["sottoclasse"], d["livello"], d["edizione"]],
        ]
        t = Table(id_data, colWidths=[4*cm, 3*cm, 4*cm, 4*cm])
        ts_ = table_style(header=False)
        ts_.add("FONTNAME", (0,0), (-1,-1), "Helvetica")
        ts_.add("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
        ts_.add("FONTNAME", (0,2), (-1,2), "Helvetica-Bold")
        ts_.add("BACKGROUND",(0,0),(-1,0), colors.HexColor("#f0e8d0"))
        ts_.add("BACKGROUND",(0,2),(-1,2), colors.HexColor("#f0e8d0"))
        t.setStyle(ts_)
        story.append(t)

        # ── statistiche ──
        story.append(Paragraph("🎲  Statistiche", sSec))
        st = d["stats"]
        stat_data = [
            ["FOR", "DES", "COS", "INT", "SAG", "CAR"],
            [st.get("FOR",""), st.get("DES",""), st.get("COS",""),
             st.get("INT",""), st.get("SAG",""), st.get("CAR","")]
        ]
        t2 = Table(stat_data, colWidths=[2.5*cm]*6)
        t2.setStyle(table_style())
        story.append(t2)

        # ── tiri salvezza ──
        story.append(Paragraph("🛡  Tiri Salvezza", sSec))
        ts_d = d["ts"]
        ts_data = [
            ["TS FOR", "TS DES", "TS COS", "TS INT", "TS SAG", "TS CAR"],
            [ts_d.get("TS FOR",""), ts_d.get("TS DES",""), ts_d.get("TS COS",""),
             ts_d.get("TS INT",""), ts_d.get("TS SAG",""), ts_d.get("TS CAR","")]
        ]
        t3 = Table(ts_data, colWidths=[2.5*cm]*6)
        t3.setStyle(table_style())
        story.append(t3)

        if d["competenze"]:
            story.append(Paragraph("Competenze:", sLabel))
            for row in d["competenze"].splitlines():
                if row.strip():
                    story.append(Paragraph(f"• {row.strip()}", sNorm))

        # ── combattimento ──
        story.append(Paragraph("⚔  Combattimento", sSec))
        cb = d["combat"]
        cb_data = [
            ["HP Max", "CA", "Iniziativa", "Velocità", "Grandezza", "Per. Passiva"],
            [cb.get("HP Max",""), cb.get("CA",""), cb.get("Iniziativa",""),
             cb.get("Velocità",""), cb.get("Grandezza",""), cb.get("Per. Passiva","")]
        ]
        t4 = Table(cb_data, colWidths=[2.5*cm]*6)
        t4.setStyle(table_style())
        story.append(t4)

        # ── sezioni testo ──
        def text_section(icon_title, content):
            if not content:
                return
            story.append(Paragraph(icon_title, sSec))
            for row in content.splitlines():
                if row.strip():
                    story.append(Paragraph(row.strip(), sNorm))

        text_section("🗡  Armamento",           d["armamento"])
        text_section("🎒  Equipaggiamento",     d["equipaggiamento"])
        if d["extra"]:
            text_section("📦  Extra (dotazione)", d["extra"])
        text_section("✨  Abilità di Classe",   d["abilita"])

        # ── magia ──
        story.append(Paragraph("🔮  Magia", sSec))
        if d["trucchetti"]:
            story.append(Paragraph(f"Trucchetti: {d['trucchetti']}", sNorm))
        slots_filled = {i: v for i, v in d["slots"].items() if v}
        if slots_filled:
            slot_hdr = [f"{i}°" for i in slots_filled.keys()]
            slot_val = [v for v in slots_filled.values()]
            ts_ = Table([slot_hdr, slot_val],
                        colWidths=[1.5*cm]*len(slots_filled))
            ts_.setStyle(table_style())
            story.append(ts_)
        if d["incantesimi"]:
            story.append(Paragraph("Incantesimi noti:", sLabel))
            for row in d["incantesimi"].splitlines():
                if row.strip():
                    story.append(Paragraph(f"• {row.strip()}", sNorm))

        if d["note"]:
            text_section("📝  Note", d["note"])

        doc.build(story)

    # ── pulizia ───────────────────────────────────────────────────────────────
    def _pulisci(self):
        if not messagebox.askyesno("Conferma", "Pulire tutti i campi?"):
            return
        for var in [self.nome, self.eta, self.background, self.specie,
                    self.classe, self.sottoclasse, self.livello, self.edizione,
                    self.trucchetti]:
            var.set("")
        for v in self.stats.values():   v.set("")
        for v in self.ts.values():      v.set("")
        for v in self.combat.values():  v.set("")
        for v in self.slots.values():   v.set("")
        for w in [self.competenze, self.armamento, self.equipaggiamento,
                  self.extra, self.abilita, self.incantesimi, self.note]:
            w.delete("1.0", "end")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = DnDApp()
    app.mainloop()
