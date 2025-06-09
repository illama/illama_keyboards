import sys
import os
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import json
from tkinter import font as tkfont
import time
import math
import shlex

# Auto-elevation to admin (UAC)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Relaunch as admin
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)

# Liste étendue des langues et claviers populaires et exotiques
LANGUAGES = [
    # Français
    {
        'tag': 'fr-FR',
        'name': 'Français (France)',
        'keyboards': [
            {'id': '040c:0000040c', 'name': 'Français (AZERTY)'},
            {'id': '040c:0000080c', 'name': 'Belge'},
            {'id': '040c:00001009', 'name': 'US (International)'},
            {'id': '040c:00010409', 'name': 'Dvorak'},
            {'id': '040c:00050409', 'name': 'Colemak'}
        ]
    },
    {
        'tag': 'fr-CA',
        'name': 'Français (Canada)',
        'keyboards': [
            {'id': '0c0c:00011009', 'name': 'Canadien Multilingue Standard'},
            {'id': '0c0c:00001009', 'name': 'US'},
            {'id': '0c0c:00000c0c', 'name': 'Français (Canada)'}
        ]
    },
    # Anglais
    {
        'tag': 'en-US',
        'name': 'Anglais (États-Unis)',
        'keyboards': [
            {'id': '0409:00000409', 'name': 'US'},
            {'id': '0409:00010409', 'name': 'Dvorak'},
            {'id': '0409:00020409', 'name': 'US International'},
            {'id': '0409:00050409', 'name': 'Colemak'},
            {'id': '0409:00030409', 'name': 'Workman'}
        ]
    },
    {
        'tag': 'en-GB',
        'name': 'Anglais (Royaume-Uni)',
        'keyboards': [
            {'id': '0809:00000809', 'name': 'UK'},
            {'id': '0809:00010409', 'name': 'Dvorak UK'}
        ]
    },
    # Espagnol
    {
        'tag': 'es-ES',
        'name': 'Espagnol (Espagne)',
        'keyboards': [
            {'id': '0c0a:0000040a', 'name': 'Espagnol'},
            {'id': '0c0a:0000080a', 'name': 'Latin Américain'}
        ]
    },
    # Allemand
    {
        'tag': 'de-DE',
        'name': 'Allemand (Allemagne)',
        'keyboards': [
            {'id': '0407:00000407', 'name': 'Allemand (QWERTZ)'},
            {'id': '0407:00010407', 'name': 'Allemand (Dvorak)'}
        ]
    },
    # Italien
    {
        'tag': 'it-IT',
        'name': 'Italien (Italie)',
        'keyboards': [
            {'id': '0410:00000410', 'name': 'Italien'}
        ]
    },
    # Portugais
    {
        'tag': 'pt-PT',
        'name': 'Portugais (Portugal)',
        'keyboards': [
            {'id': '0816:00000816', 'name': 'Portugais'}
        ]
    },
    # Néerlandais
    {
        'tag': 'nl-NL',
        'name': 'Néerlandais (Pays-Bas)',
        'keyboards': [
            {'id': '0413:00020409', 'name': 'US International'},
            {'id': '0413:00000413', 'name': 'Néerlandais'}
        ]
    },
    # Russe
    {
        'tag': 'ru-RU',
        'name': 'Russe (Russie)',
        'keyboards': [
            {'id': '0419:00000419', 'name': 'Russe'}
        ]
    },
    # Chinois
    {
        'tag': 'zh-CN',
        'name': 'Chinois (Chine)',
        'keyboards': [
            {'id': '0804:00000804', 'name': 'Chinois Simplifié'},
            {'id': '0804:00000409', 'name': 'US'}
        ]
    },
    # Japonais
    {
        'tag': 'ja-JP',
        'name': 'Japonais (Japon)',
        'keyboards': [
            {'id': '0411:00000411', 'name': 'Japonais'}
        ]
    },
    # Arabe
    {
        'tag': 'ar-SA',
        'name': 'Arabe (Arabie Saoudite)',
        'keyboards': [
            {'id': '0401:00000401', 'name': 'Arabe'}
        ]
    },
    # Hébreu
    {
        'tag': 'he-IL',
        'name': 'Hébreu (Israël)',
        'keyboards': [
            {'id': '040d:00020409', 'name': 'US International'},
            {'id': '040d:0000040d', 'name': 'Hébreu'}
        ]
    },
    # Turc
    {
        'tag': 'tr-TR',
        'name': 'Turc (Turquie)',
        'keyboards': [
            {'id': '041f:0000041f', 'name': 'Turc Q'},
            {'id': '041f:0001041f', 'name': 'Turc F'}
        ]
    },
    # Grec
    {
        'tag': 'el-GR',
        'name': 'Grec (Grèce)',
        'keyboards': [
            {'id': '0408:00000408', 'name': 'Grec'}
        ]
    },
    # Polonais
    {
        'tag': 'pl-PL',
        'name': 'Polonais (Pologne)',
        'keyboards': [
            {'id': '0415:00000415', 'name': 'Polonais'}
        ]
    },
    # Hongrois
    {
        'tag': 'hu-HU',
        'name': 'Hongrois (Hongrie)',
        'keyboards': [
            {'id': '040e:0000040e', 'name': 'Hongrois'}
        ]
    },
    # Suédois
    {
        'tag': 'sv-SE',
        'name': 'Suédois (Suède)',
        'keyboards': [
            {'id': '041d:0000041d', 'name': 'Suédois'}
        ]
    },
    # Finlandais
    {
        'tag': 'fi-FI',
        'name': 'Finnois (Finlande)',
        'keyboards': [
            {'id': '040b:0000040b', 'name': 'Finnois'}
        ]
    },
    # Norvégien
    {
        'tag': 'nb-NO',
        'name': 'Norvégien (Norvège)',
        'keyboards': [
            {'id': '0414:00000414', 'name': 'Norvégien'}
        ]
    },
    # Danois
    {
        'tag': 'da-DK',
        'name': 'Danois (Danemark)',
        'keyboards': [
            {'id': '0406:00000406', 'name': 'Danois'}
        ]
    },
    # Tchèque
    {
        'tag': 'cs-CZ',
        'name': 'Tchèque (République Tchèque)',
        'keyboards': [
            {'id': '0405:00000405', 'name': 'Tchèque'}
        ]
    },
    # Slovaque
    {
        'tag': 'sk-SK',
        'name': 'Slovaque (Slovaquie)',
        'keyboards': [
            {'id': '041b:0000041b', 'name': 'Slovaque'}
        ]
    },
    # Roumain
    {
        'tag': 'ro-RO',
        'name': 'Roumain (Roumanie)',
        'keyboards': [
            {'id': '0418:00000418', 'name': 'Roumain'}
        ]
    },
    # Bulgare
    {
        'tag': 'bg-BG',
        'name': 'Bulgare (Bulgarie)',
        'keyboards': [
            {'id': '0402:00000402', 'name': 'Bulgare'}
        ]
    },
    # Croate
    {
        'tag': 'hr-HR',
        'name': 'Croate (Croatie)',
        'keyboards': [
            {'id': '041a:0000041a', 'name': 'Croate'}
        ]
    },
    # Serbe
    {
        'tag': 'sr-RS',
        'name': 'Serbe (Serbie)',
        'keyboards': [
            {'id': '0c1a:00000c1a', 'name': 'Serbe'}
        ]
    },
    # Ukrainien
    {
        'tag': 'uk-UA',
        'name': 'Ukrainien (Ukraine)',
        'keyboards': [
            {'id': '0422:00000422', 'name': 'Ukrainien'}
        ]
    },
    # Hindi
    {
        'tag': 'hi-IN',
        'name': 'Hindi (Inde)',
        'keyboards': [
            {'id': '0439:00000439', 'name': 'Hindi'}
        ]
    },
    # Thaï
    {
        'tag': 'th-TH',
        'name': 'Thaï (Thaïlande)',
        'keyboards': [
            {'id': '041e:0000041e', 'name': 'Thaï'}
        ]
    },
    # Vietnamien
    {
        'tag': 'vi-VN',
        'name': 'Vietnamien (Vietnam)',
        'keyboards': [
            {'id': '042a:0000042a', 'name': 'Vietnamien'}
        ]
    },
    # Coréen
    {
        'tag': 'ko-KR',
        'name': 'Coréen (Corée du Sud)',
        'keyboards': [
            {'id': '0412:00000412', 'name': 'Coréen'}
        ]
    },
]

# Base de détection avancée pour chaque clavier (positions clés)
KEYBOARD_DETECTION_DB = [
    {'name': 'Français (AZERTY)', 'answers': ['A', 'Q', 'M']},
    {'name': 'Belge', 'answers': ['A', 'Q', 'M']},
    {'name': 'US', 'answers': ['Q', 'A', ';']},
    {'name': 'US (International)', 'answers': ['Q', 'A', ';']},
    {'name': 'Dvorak', 'answers': ["'", ',', 'S']},
    {'name': 'Colemak', 'answers': ['Q', 'A', 'N']},
    {'name': 'Workman', 'answers': ['Q', 'A', 'V']},
    {'name': 'Dvorak UK', 'answers': ["'", ',', 'S']},
    {'name': 'Allemand (QWERTZ)', 'answers': ['Q', 'A', 'Ö']},
    {'name': 'Allemand (Dvorak)', 'answers': ["'", ',', 'S']},
    {'name': 'Espagnol', 'answers': ['Q', 'A', 'Ñ']},
    {'name': 'Latin Américain', 'answers': ['Q', 'A', 'Ñ']},
    {'name': 'Italien', 'answers': ['Q', 'A', 'M']},
    {'name': 'Portugais', 'answers': ['Q', 'A', 'Ç']},
    {'name': 'Néerlandais', 'answers': ['Q', 'A', ';']},
    {'name': 'Russe', 'answers': ['Й', 'Ф', 'Ь']},
    {'name': 'Chinois Simplifié', 'answers': ['Q', 'A', ';']},
    {'name': 'Japonais', 'answers': ['Q', 'A', 'む']},
    {'name': 'Canadien Multilingue Standard', 'answers': ['Q', 'A', ';']},
    {'name': 'Français (Canada)', 'answers': ['Q', 'A', 'M']},
    {'name': 'Arabe', 'answers': ['ض', 'ص', 'م']},
    {'name': 'Hébreu', 'answers': ['ק', 'ש', 'ף']},
    {'name': 'Turc Q', 'answers': ['Q', 'A', 'Ş']},
    {'name': 'Turc F', 'answers': ['F', 'G', 'Ö']},
    {'name': 'Grec', 'answers': [';','ς','Λ']},
    {'name': 'Polonais', 'answers': ['Q', 'A', 'Ł']},
    {'name': 'Hongrois', 'answers': ['Q', 'A', 'É']},
    {'name': 'Suédois', 'answers': ['Q', 'A', 'Ö']},
    {'name': 'Finnois', 'answers': ['Q', 'A', 'Ö']},
    {'name': 'Norvégien', 'answers': ['Q', 'A', 'Ø']},
    {'name': 'Danois', 'answers': ['Q', 'A', 'Æ']},
    {'name': 'Tchèque', 'answers': [';','Q','M']},
    {'name': 'Slovaque', 'answers': [';','Q','M']},
    {'name': 'Roumain', 'answers': ['Q', 'A', 'L']},
    {'name': 'Bulgare', 'answers': ['Я', 'Ф', 'Ю']},
    {'name': 'Croate', 'answers': ['Q', 'A', 'L']},
    {'name': 'Serbe', 'answers': ['Љ', 'А', 'Њ']},
    {'name': 'Ukrainien', 'answers': ['Й', 'Ф', 'Ь']},
    {'name': 'Hindi', 'answers': ['ऍ', 'अ', 'म']},
    {'name': 'Thaï', 'answers': ['ๆ', 'ไ', 'ฒ']},
    {'name': 'Vietnamien', 'answers': ['Q', 'A', 'L']},
    {'name': 'Coréen', 'answers': ['ㅂ', 'ㅁ', 'ㅡ']},
]

# Questions de détection (positions clés)
DETECTION_QUESTIONS = [
    ("Tapez la lettre en haut à gauche de votre clavier (ex: 'A' ou 'Q')", 0),
    ("Tapez la lettre à gauche de 'Z' (ex: 'A' ou 'Q')", 1),
    ("Tapez la lettre à droite de 'L' (ex: 'M', ';', 'Ö', etc.)", 2)
]

class ClavierApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Illama Keyboards - Gestionnaire de Langues et Claviers")
        self.geometry("800x600")
        self.resizable(True, True)
        self.configure(bg="#F6F7EB")  # Fond principal très clair

        # Ombre portée simulée pour le cadre principal
        self.shadow = tk.Frame(self, bg="#E0E1DD")
        self.shadow.place(relx=0.03, rely=0.04, relwidth=0.94, relheight=0.92)

        # Cadre principal
        self.main_container = tk.Frame(self, bg="#F6F7EB", padx=30, pady=30)
        self.main_container.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.93)

        # Styles
        self.style = ttk.Style()
        self.style.configure("Custom.TNotebook", background="#F6F7EB")
        self.style.configure("Custom.TNotebook.Tab", padding=[10, 5], font=("Segoe UI", 10), background="#F6F7EB", foreground="#393E41")
        self.style.map("Custom.TNotebook.Tab", background=[("selected", "#393E41")], foreground=[("selected", "#F6F7EB")])
        self.style.configure("Custom.TCombobox", fieldbackground="#F6F7EB", background="#F6F7EB", foreground="#393E41", bordercolor="#E0E1DD", lightcolor="#F6F7EB", darkcolor="#F6F7EB")
        self.style.map("Custom.TCombobox", fieldbackground=[("readonly", "#F6F7EB")], foreground=[("readonly", "#393E41")])

        self.selected_language = tk.StringVar()
        self.selected_keyboard = tk.StringVar()

        self.notebook = ttk.Notebook(self.main_container, style="Custom.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_clavier_tab()
        self.create_audio_tab()
        self.create_apps_tab()
        self.after(100, self.animate_startup)
        self.animate_titles()

    def animate_startup(self):
        """Animation de démarrage de l'application"""
        self.attributes('-alpha', 0)
        for i in range(10):
            self.attributes('-alpha', i/10)
            self.update()
            time.sleep(0.02)

    def animate_titles(self):
        """Animation continue pour les titres"""
        def update_title_color(label, base_color="#3498db"):
            current_color = label.cget("fg")
            if current_color == base_color:
                label.configure(fg="#2ecc71")
            else:
                label.configure(fg=base_color)
            self.after(2000, lambda: update_title_color(label, base_color))
        
        # Appliquer l'animation aux titres principaux
        for tab in [self.clavier_frame, self.audio_frame, self.apps_frame]:
            for widget in tab.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label) and child.cget("font")[1] == 24:
                            update_title_color(child)

    def create_clavier_tab(self):
        self.clavier_frame = tk.Frame(self.notebook, bg="#F6F7EB")
        self.notebook.add(self.clavier_frame, text="Claviers")

        title_frame = tk.Frame(self.clavier_frame, bg="#F6F7EB")
        title_frame.pack(pady=(30, 30))
        title = tk.Label(title_frame, text="Illama Keyboards", font=("Segoe UI", 24, "bold"), bg="#F6F7EB", fg="#393E41")
        title.pack()
        subtitle = tk.Label(title_frame, text="Gestionnaire de Langues et Claviers", font=("Segoe UI", 12), bg="#F6F7EB", fg="#393E41")
        subtitle.pack()

        controls_frame = tk.Frame(self.clavier_frame, bg="#F6F7EB")
        controls_frame.pack(pady=20, padx=40, fill="x")
        label_style = {"font": ("Segoe UI", 11), "bg": "#F6F7EB", "fg": "#393E41"}

        lang_label = tk.Label(controls_frame, text="Choisissez la langue à conserver :", **label_style)
        lang_label.pack(pady=(0, 8), anchor="w")
        self.lang_combo = ttk.Combobox(controls_frame, values=[l['name'] for l in LANGUAGES], textvariable=self.selected_language, state="readonly", font=("Segoe UI", 11), style="Custom.TCombobox", width=40)
        self.lang_combo.pack(pady=(0, 24))
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_language_selected)

        kb_label = tk.Label(controls_frame, text="Choisissez le clavier :", **label_style)
        kb_label.pack(pady=(0, 8), anchor="w")
        self.kb_combo = ttk.Combobox(controls_frame, values=[], textvariable=self.selected_keyboard, state="readonly", font=("Segoe UI", 11), style="Custom.TCombobox", width=40)
        self.kb_combo.pack(pady=(0, 24))

        # Style boutons arrondis et ombre
        def rounded_button(master, **kwargs):
            btn = tk.Button(master, relief='flat', highlightthickness=0, bd=0, **kwargs)
            btn.configure(bg="#E94F37", fg="#F6F7EB", font=("Segoe UI", 11), padx=24, pady=12, activebackground="#393E41", activeforeground="#F6F7EB")
            btn.bind("<Enter>", lambda e: btn.configure(bg="#393E41", fg="#F6F7EB"))
            btn.bind("<Leave>", lambda e: btn.configure(bg="#E94F37", fg="#F6F7EB"))
            return btn

        button_frame = tk.Frame(controls_frame, bg="#F6F7EB")
        button_frame.pack(pady=20)
        detect_btn = rounded_button(button_frame, text="Détecter automatiquement le clavier", command=self.detect_keyboard)
        detect_btn.pack(side="left", padx=16)
        apply_btn = rounded_button(button_frame, text="Appliquer la configuration", command=self.apply_config)
        apply_btn.pack(side="left", padx=16)

    def create_audio_tab(self):
        self.audio_frame = tk.Frame(self.notebook, bg="#F6F7EB")
        self.notebook.add(self.audio_frame, text="Gestion audio")
        title_frame = tk.Frame(self.audio_frame, bg="#F6F7EB")
        title_frame.pack(pady=(30, 30))
        title = tk.Label(title_frame, text="Illama Audio", font=("Segoe UI", 24, "bold"), bg="#F6F7EB", fg="#393E41")
        title.pack()
        subtitle = tk.Label(title_frame, text="Gestion des périphériques audio", font=("Segoe UI", 12), bg="#F6F7EB", fg="#393E41")
        subtitle.pack()

        main_frame = tk.Frame(self.audio_frame, bg="#F6F7EB", padx=40)
        main_frame.pack(fill="both", expand=True, pady=20)
        section_style = {"font": ("Segoe UI", 13, "bold"), "bg": "#F6F7EB", "fg": "#393E41"}

        entry_frame = tk.Frame(main_frame, bg="#F6F7EB")
        entry_frame.pack(fill="x", pady=(0, 20))
        entry_label = tk.Label(entry_frame, text="Entrées audio (microphones)", **section_style)
        entry_label.pack(pady=(0, 10), anchor="w")
        listbox_style = {"font": ("Segoe UI", 11), "bg": "#F6F7EB", "fg": "#393E41", "selectbackground": "#E94F37", "selectforeground": "#F6F7EB", "relief": "flat", "borderwidth": 1}
        self.entries_listbox = tk.Listbox(entry_frame, selectmode=tk.MULTIPLE, width=60, height=6, **listbox_style)
        self.entries_listbox.pack(pady=(0, 10))
        entry_btns = tk.Frame(entry_frame, bg="#F6F7EB")
        entry_btns.pack(pady=5)
        self.disable_entry_btn = tk.Button(entry_btns, text="Désactiver sélection", state="disabled", command=self.disable_selected_entries, relief='flat', highlightthickness=0, bd=0, bg="#E94F37", fg="#F6F7EB", font=("Segoe UI", 11), padx=18, pady=8, activebackground="#393E41", activeforeground="#F6F7EB")
        self.disable_entry_btn.pack(side=tk.LEFT, padx=8)
        self.restore_entry_btn = tk.Button(entry_btns, text="Restaurer sélection", state="disabled", command=self.restore_selected_entries, relief='flat', highlightthickness=0, bd=0, bg="#E94F37", fg="#F6F7EB", font=("Segoe UI", 11), padx=18, pady=8, activebackground="#393E41", activeforeground="#F6F7EB")
        self.restore_entry_btn.pack(side=tk.LEFT, padx=8)
        for btn in [self.disable_entry_btn, self.restore_entry_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#393E41", fg="#F6F7EB"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#E94F37", fg="#F6F7EB"))

        output_frame = tk.Frame(main_frame, bg="#F6F7EB")
        output_frame.pack(fill="x")
        output_label = tk.Label(output_frame, text="Sorties audio (haut-parleurs, casques)", **section_style)
        output_label.pack(pady=(0, 10), anchor="w")
        self.outputs_listbox = tk.Listbox(output_frame, selectmode=tk.MULTIPLE, width=60, height=6, **listbox_style)
        self.outputs_listbox.pack(pady=(0, 10))
        output_btns = tk.Frame(output_frame, bg="#F6F7EB")
        output_btns.pack(pady=5)
        self.disable_output_btn = tk.Button(output_btns, text="Désactiver sélection", state="disabled", command=self.disable_selected_outputs, relief='flat', highlightthickness=0, bd=0, bg="#E94F37", fg="#F6F7EB", font=("Segoe UI", 11), padx=18, pady=8, activebackground="#393E41", activeforeground="#F6F7EB")
        self.disable_output_btn.pack(side=tk.LEFT, padx=8)
        self.restore_output_btn = tk.Button(output_btns, text="Restaurer sélection", state="disabled", command=self.restore_selected_outputs, relief='flat', highlightthickness=0, bd=0, bg="#E94F37", fg="#F6F7EB", font=("Segoe UI", 11), padx=18, pady=8, activebackground="#393E41", activeforeground="#F6F7EB")
        self.restore_output_btn.pack(side=tk.LEFT, padx=8)
        for btn in [self.disable_output_btn, self.restore_output_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#393E41", fg="#F6F7EB"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#E94F37", fg="#F6F7EB"))

        self.audio_devices = {'entries': [], 'outputs': []}
        self.entries_listbox.bind('<<ListboxSelect>>', self.on_entry_select)
        self.outputs_listbox.bind('<<ListboxSelect>>', self.on_output_select)
        self.disabled_devices_file = 'disabled_audio_devices.json'
        self.load_disabled_devices()
        self.refresh_audio_lists()

    def create_apps_tab(self):
        self.apps_frame = tk.Frame(self.notebook, bg="#F6F7EB")
        self.notebook.add(self.apps_frame, text="Apps")
        title_frame = tk.Frame(self.apps_frame, bg="#F6F7EB")
        title_frame.pack(pady=(30, 10))
        title = tk.Label(title_frame, text="Illama Apps", font=("Segoe UI", 24, "bold"), bg="#F6F7EB", fg="#393E41")
        title.pack()
        subtitle = tk.Label(title_frame, text="Désinstallez n'importe quelle application, même celles protégées !", font=("Segoe UI", 12), bg="#F6F7EB", fg="#393E41")
        subtitle.pack()

        # Barre de recherche
        search_frame = tk.Frame(self.apps_frame, bg="#F6F7EB")
        search_frame.pack(pady=(10, 10))
        search_label = tk.Label(search_frame, text="Recherche :", font=("Segoe UI", 11), bg="#F6F7EB", fg="#393E41")
        search_label.pack(side=tk.LEFT)
        self.apps_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.apps_search_var, font=("Segoe UI", 11), bg="#F6F7EB", fg="#393E41", relief='solid', bd=1, width=30)
        search_entry.pack(side=tk.LEFT, padx=8)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_apps_list())

        # Liste des apps avec type
        self.apps_list_frame = tk.Frame(self.apps_frame, bg="#F6F7EB")
        self.apps_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.apps_scrollbar = tk.Scrollbar(self.apps_list_frame)
        self.apps_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Utilisation d'une Listbox custom pour afficher nom + type
        self.apps_listbox = tk.Listbox(self.apps_list_frame, font=("Segoe UI", 11), bg="#F6F7EB", fg="#393E41", selectbackground="#E94F37", selectforeground="#F6F7EB", yscrollcommand=self.apps_scrollbar.set, width=80, height=15, relief='flat', borderwidth=1)
        self.apps_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.apps_scrollbar.config(command=self.apps_listbox.yview)
        self.apps_listbox.bind('<<ListboxSelect>>', self.on_app_select)
        self.apps_listbox.bind('<Motion>', self.on_app_hover)
        self.apps_tooltip = None

        # Bouton désinstaller
        self.uninstall_btn = tk.Button(self.apps_frame, text="Désinstaller l'application sélectionnée", state="disabled", command=self.uninstall_selected_app, relief='flat', highlightthickness=0, bd=0, bg="#E94F37", fg="#F6F7EB", font=("Segoe UI", 11), padx=24, pady=12, activebackground="#393E41", activeforeground="#F6F7EB")
        self.uninstall_btn.pack(pady=16)
        self.uninstall_btn.bind("<Enter>", lambda e: self.uninstall_btn.configure(bg="#393E41", fg="#F6F7EB"))
        self.uninstall_btn.bind("<Leave>", lambda e: self.uninstall_btn.configure(bg="#E94F37", fg="#F6F7EB"))

        self.all_apps = []
        self.filtered_apps = []
        self.refresh_apps_list(force_reload=True)

    def on_language_selected(self, event=None):
        lang = self.selected_language.get()
        for l in LANGUAGES:
            if l['name'] == lang:
                kb_names = [k['name'] for k in l['keyboards']]
                self.kb_combo['values'] = kb_names
                if kb_names:
                    self.kb_combo.current(0)
                break

    def detect_keyboard(self):
        # Vérifie si une langue est sélectionnée
        if not self.selected_language.get():
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner une langue avant de détecter le clavier.")
            return
        answers = []
        for question, idx in DETECTION_QUESTIONS:
            ans = simpledialog.askstring("Détection du clavier", question, parent=self)
            if not ans:
                messagebox.showwarning("Détection annulée", "Détection annulée.")
                return
            answers.append(ans.strip())
        # Calcul du score de correspondance pour chaque clavier
        best_score = -1
        best_kb = None
        for kb in KEYBOARD_DETECTION_DB:
            score = 0
            for i, user_ans in enumerate(answers):
                expected = kb['answers'][i]
                if user_ans.upper() == expected.upper():
                    score += 1
            if score > best_score:
                best_score = score
                best_kb = kb['name']
        if best_score == len(answers):
            kb_type = best_kb
        elif best_score > 0:
            kb_type = best_kb + " (probable)"
        else:
            kb_type = None
        if kb_type:
            lang = self.selected_language.get()
            found = False
            for l in LANGUAGES:
                if l['name'] == lang:
                    for k in l['keyboards']:
                        if best_kb.lower() in k['name'].lower():
                            self.selected_keyboard.set(k['name'])
                            self.kb_combo.set(k['name'])
                            messagebox.showinfo("Clavier détecté", f"Clavier détecté : {kb_type}")
                            found = True
                            break
                    break
            if not found:
                messagebox.showinfo("Clavier détecté", f"Clavier détecté : {kb_type}, mais il n'est pas proposé pour cette langue.")
        else:
            messagebox.showwarning("Détection échouée", "Clavier non reconnu. Veuillez choisir manuellement.")

    def apply_config(self):
        lang = self.selected_language.get()
        kb = self.selected_keyboard.get()
        if not lang or not kb:
            messagebox.showerror("Erreur", "Veuillez sélectionner une langue et un clavier.")
            return
        lang_tag = None
        kb_id = None
        for l in LANGUAGES:
            if l['name'] == lang:
                lang_tag = l['tag']
                for k in l['keyboards']:
                    if k['name'] == kb:
                        kb_id = k['id']
                        break
        if not lang_tag or not kb_id:
            messagebox.showerror("Erreur", "Impossible de trouver la configuration sélectionnée.")
            return
        ps_cmd = f"$list = New-WinUserLanguageList '{lang_tag}'; $list[0].InputMethodTips.Clear(); $list[0].InputMethodTips.Add('{kb_id}'); Set-WinUserLanguageList -LanguageList $list -Force"
        try:
            completed = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
            if completed.returncode == 0:
                messagebox.showinfo("Succès", "Configuration appliquée avec succès ! Un redémarrage peut être nécessaire.")
            else:
                messagebox.showerror("Erreur PowerShell", completed.stderr)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def on_entry_select(self, event=None):
        sel = self.entries_listbox.curselection()
        self.disable_entry_btn.config(state="normal" if sel else "disabled")
        self.restore_entry_btn.config(state="normal" if sel else "disabled")

    def on_output_select(self, event=None):
        sel = self.outputs_listbox.curselection()
        # Force l'activation si au moins un élément est sélectionné
        state = "normal" if len(sel) > 0 else "disabled"
        self.disable_output_btn.config(state=state)
        self.restore_output_btn.config(state=state)

    def load_disabled_devices(self):
        try:
            with open(self.disabled_devices_file, 'r', encoding='utf-8') as f:
                self.disabled_devices = set(json.load(f))
        except Exception:
            self.disabled_devices = set()

    def save_disabled_devices(self):
        try:
            with open(self.disabled_devices_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.disabled_devices), f)
        except Exception:
            pass

    def disable_selected_entries(self):
        indices = self.entries_listbox.curselection()
        for idx in indices:
            dev = self.audio_devices['entries'][idx]
            self.disable_device(dev)
        self.refresh_audio_lists()

    def restore_selected_entries(self):
        indices = self.entries_listbox.curselection()
        for idx in indices:
            dev = self.audio_devices['entries'][idx]
            self.restore_device(dev)
        self.refresh_audio_lists()

    def disable_selected_outputs(self):
        indices = self.outputs_listbox.curselection()
        for idx in indices:
            dev = self.audio_devices['outputs'][idx]
            self.disable_device(dev)
        self.refresh_audio_lists()

    def restore_selected_outputs(self):
        indices = self.outputs_listbox.curselection()
        for idx in indices:
            dev = self.audio_devices['outputs'][idx]
            self.restore_device(dev)
        self.refresh_audio_lists()

    def disable_device(self, dev):
        try:
            ps_cmd = f"Disable-PnpDevice -InstanceId '{dev['InstanceId']}' -Confirm:$false"
            completed = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
            if completed.returncode == 0:
                self.disabled_devices.add(dev['InstanceId'])
                self.save_disabled_devices()
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la désactivation : {completed.stderr}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def restore_device(self, dev):
        try:
            ps_cmd = f"Enable-PnpDevice -InstanceId '{dev['InstanceId']}' -Confirm:$false"
            completed = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
            if completed.returncode == 0:
                if dev['InstanceId'] in self.disabled_devices:
                    self.disabled_devices.remove(dev['InstanceId'])
                    self.save_disabled_devices()
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la restauration : {completed.stderr}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def refresh_audio_lists(self):
        # Utilise PowerShell pour lister tous les périphériques audio (entrées/sorties) sur une seule ligne
        ps_script = (
            "$list = Get-PnpDevice -Class AudioEndpoint | ForEach-Object { "
            "$props = Get-PnpDeviceProperty -InstanceId $_.InstanceId -KeyName 'DEVPKEY_Device_FriendlyName'; "
            "$name = $props.Data; "
            "$direction = if ($_.FriendlyName -match 'Microphone|Input|Entrée') { 'entry' } else { 'output' }; "
            "[PSCustomObject]@{ Name = $name; InstanceId = $_.InstanceId; Direction = $direction; Status = $_.Status } }; "
            "$list | ConvertTo-Json -Compress"
        )
        try:
            completed = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
            if completed.returncode == 0 and completed.stdout:
                try:
                    devices = json.loads(completed.stdout)
                except Exception as e:
                    messagebox.showerror("Erreur JSON", f"Erreur de décodage JSON:\n{e}\n\nSortie PowerShell:\n{completed.stdout}\n\nErreur PowerShell:\n{completed.stderr}")
                    return
                self.audio_devices = {'entries': [], 'outputs': []}
                self.entries_listbox.delete(0, tk.END)
                self.outputs_listbox.delete(0, tk.END)
                for dev in devices:
                    if dev['Direction'] == 'entry':
                        self.audio_devices['entries'].append(dev)
                        self.entries_listbox.insert(tk.END, f"{dev['Name']} ({dev['Status']})")
                    else:
                        self.audio_devices['outputs'].append(dev)
                        self.outputs_listbox.insert(tk.END, f"{dev['Name']} ({dev['Status']})")
                # Rafraîchit l'état des boutons après mise à jour
                self.on_entry_select()
                self.on_output_select()
            else:
                messagebox.showerror("Erreur", f"Impossible de lister les périphériques audio.\n\nSortie PowerShell:\n{completed.stdout}\n\nErreur PowerShell:\n{completed.stderr}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def refresh_apps_list(self, force_reload=False):
        if force_reload or not self.all_apps:
            self.all_apps = self.get_installed_apps()
        search = self.apps_search_var.get().lower()
        self.filtered_apps = [app for app in self.all_apps if search in app['name'].lower()]
        self.apps_listbox.delete(0, tk.END)
        for app in self.filtered_apps:
            app_type = 'Edge' if app.get('force_edge') else ('Win32' if app['type'] == 'win32' else 'UWP')
            self.apps_listbox.insert(tk.END, f"{app['name']}   [{app_type}]")
        self.uninstall_btn.config(state="disabled")

    def on_app_select(self, event=None):
        sel = self.apps_listbox.curselection()
        self.uninstall_btn.config(state="normal" if sel else "disabled")

    def get_installed_apps(self):
        # Récupère les apps Win32 (.exe) via la base de registre et les apps UWP via PowerShell
        import subprocess, re
        apps = []
        # Win32 via registre
        try:
            import winreg
            for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                for path in [r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", r"SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"]:
                    try:
                        reg = winreg.OpenKey(root, path)
                        for i in range(0, winreg.QueryInfoKey(reg)[0]):
                            try:
                                subkey = winreg.EnumKey(reg, i)
                                appkey = winreg.OpenKey(reg, subkey)
                                name, _ = winreg.QueryValueEx(appkey, "DisplayName")
                                exe = winreg.QueryValueEx(appkey, "DisplayIcon")[0] if 'DisplayIcon' in [winreg.EnumValue(appkey, j)[0] for j in range(winreg.QueryInfoKey(appkey)[1])] else ''
                                apps.append({'name': name, 'type': 'win32', 'exe': exe, 'key': (root, path, subkey)})
                            except Exception:
                                continue
                    except Exception:
                        continue
        except Exception:
            pass
        # UWP via PowerShell
        try:
            ps = subprocess.run(["powershell", "Get-AppxPackage | Select Name,PackageFullName | ConvertTo-Json -Compress"], capture_output=True, text=True, encoding='utf-8', errors='replace')
            if ps.returncode == 0 and ps.stdout:
                import json
                try:
                    uwp = json.loads(ps.stdout)
                    if isinstance(uwp, dict): uwp = [uwp]
                    for app in uwp:
                        if 'Name' in app and 'PackageFullName' in app:
                            apps.append({'name': app['Name'], 'type': 'uwp', 'package': app['PackageFullName']})
                except Exception:
                    pass
        except Exception:
            pass
        # Edge (forçage spécial)
        for app in apps:
            if app['name'].lower().startswith('microsoftedge') or app['name'].lower() == 'microsoft edge':
                app['force_edge'] = True
        return sorted(apps, key=lambda x: x['name'].lower())

    def uninstall_selected_app(self):
        sel = self.apps_listbox.curselection()
        if not sel:
            return
        app = self.filtered_apps[sel[0]]
        import tkinter.messagebox as mb
        if not mb.askyesno("Confirmation", f"Voulez-vous vraiment désinstaller '{app['name']}' ? Cette action est irréversible."):
            return
        import subprocess
        try:
            if app.get('force_edge'):
                # Désinstallation spéciale Edge
                ps_cmd = r"cd 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\*' ; .\\Installer\\setup.exe --uninstall --force-uninstall --system-level"
                subprocess.run(["powershell", "-Command", ps_cmd], shell=True, encoding='utf-8', errors='replace')
            elif app['type'] == 'uwp':
                # Directly use Remove-AppxPackage with -PackageFullName
                ps_cmd = f"Remove-AppxPackage -PackageFullName '{app['package']}' -Confirm:$false"
                completed = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
                if completed.returncode == 0:
                    mb.showinfo("Succès", f"{app['name']} a été désinstallé avec succès.")
                else:
                    mb.showerror("Erreur PowerShell", f"Erreur lors de la désinstallation de l'application UWP :\\n{completed.stderr}")
            elif app['type'] == 'win32':
                import winreg, os, shutil, shlex
                root, path, subkey = app['key']
                uninstall_cmd = None
                try:
                    reg = winreg.OpenKey(root, path + '\\\\' + subkey)
                    uninstall_cmd, _ = winreg.QueryValueEx(reg, 'UninstallString')
                except Exception:
                    pass
                if uninstall_cmd:
                    # Nettoyage des guillemets et parsing
                    uninstall_cmd = uninstall_cmd.strip()
                    if uninstall_cmd.startswith('"') and uninstall_cmd.endswith('"'):
                        uninstall_cmd = uninstall_cmd[1:-1]
                    # Utilisation de shlex pour séparer le chemin et les arguments
                    try:
                        parts = shlex.split(uninstall_cmd, posix=False)
                        exe_path = parts[0]
                        args = parts[1:]
                        if exe_path.lower().endswith('.exe') and os.path.exists(exe_path):
                            subprocess.run([exe_path] + args, encoding='utf-8', errors='replace')
                        else:
                            # Si ce n'est pas un .exe ou le chemin n'existe pas, fallback
                            subprocess.run(uninstall_cmd, shell=True, encoding='utf-8', errors='replace')
                        mb.showinfo("Succès", f"{app['name']} a été désinstallé (ou supprimé). Redémarrez si besoin.")
                        self.refresh_apps_list(force_reload=True)
                        return
                    except Exception as e:
                        mb.showerror("Erreur", f"Erreur lors de l'exécution de la commande de désinstallation : {e}")
                # Si pas d'uninstall string ou échec, suppression du dossier
                exe = app.get('exe', '')
                if exe and os.path.exists(exe):
                    folder = os.path.dirname(exe)
                    shutil.rmtree(folder, ignore_errors=True)
                    mb.showinfo("Succès", f"{app['name']} a été supprimé (dossier supprimé). Redémarrez si besoin.")
                    self.refresh_apps_list(force_reload=True)
                    return
                mb.showerror("Erreur", "Impossible de désinstaller ou de supprimer cette application (pas de commande de désinstallation trouvée et pas de dossier détecté).")
                return
            else:
                mb.showerror("Erreur", "Type d'application non supporté.")
                return
            mb.showinfo("Succès", f"{app['name']} a été désinstallé (ou supprimé). Redémarrez si besoin.")
            self.refresh_apps_list(force_reload=True)
        except Exception as e:
            mb.showerror("Erreur", f"Erreur lors de la désinstallation : {e}")

    def on_app_hover(self, event):
        # Affiche le chemin ou le package en tooltip
        import tkinter as tk
        idx = self.apps_listbox.nearest(event.y)
        if idx < 0 or idx >= len(self.filtered_apps):
            if self.apps_tooltip:
                self.apps_tooltip.destroy()
                self.apps_tooltip = None
            return
        app = self.filtered_apps[idx]
        if app['type'] == 'win32':
            info = app.get('exe', '(Aucun chemin)')
        elif app['type'] == 'uwp':
            info = app.get('package', '(Aucun package)')
        elif app.get('force_edge'):
            info = 'Microsoft Edge (désinstallation spéciale)'
        else:
            info = ''
        if not info:
            if self.apps_tooltip:
                self.apps_tooltip.destroy()
                self.apps_tooltip = None
            return
        x, y, _, _ = self.apps_listbox.bbox(idx)
        x += self.apps_listbox.winfo_rootx() + 30
        y += self.apps_listbox.winfo_rooty() + 20
        if self.apps_tooltip:
            self.apps_tooltip.destroy()
        self.apps_tooltip = tk.Toplevel(self.apps_listbox)
        self.apps_tooltip.wm_overrideredirect(True)
        self.apps_tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.apps_tooltip, text=info, bg="#393E41", fg="#F6F7EB", font=("Segoe UI", 10), padx=8, pady=4)
        label.pack()
        def hide_tooltip(_):
            if self.apps_tooltip:
                self.apps_tooltip.destroy()
                self.apps_tooltip = None
        self.apps_tooltip.after(2000, hide_tooltip, None)

if __name__ == "__main__":
    app = ClavierApp()
    app.mainloop()