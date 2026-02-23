"""
PROJECT ANSUZ v1.0 - Neural TTS with Nordic Black/Gold UI
ᚨ  The rune of communication, divine breath, and the spoken word.
Uses Microsoft Edge Neural Voices via edge-tts (free, no API key needed)
Male: en-US-AndrewNeural | Female: en-US-EmmaNeural
"""

import sys, os, re, time, asyncio, threading, subprocess, tempfile, platform
import base64 as _b64, concurrent.futures
import tkinter as tk
from tkinter import ttk, font, messagebox

# ── Optional deps ─────────────────────────────────────────────────────────────
try:
    import speech_recognition as sr
    _SR_OK = True
except ImportError:
    _SR_OK = False

try:
    import edge_tts
    _EDGE_OK = True
except ImportError:
    _EDGE_OK = False

try:
    import pygame
    pygame.mixer.pre_init(frequency=24000, size=-16, channels=1, buffer=512)
    pygame.mixer.init()
    _PG_OK = True
except Exception:
    _PG_OK = False

try:
    from PIL import Image, ImageTk
    _PIL_OK = True
except ImportError:
    _PIL_OK = False

# ── Embedded icon (base64) ────────────────────────────────────────────────────
_ICO_B64 = "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"
_PNG_B64 = "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"

def _write_temp(b64data, suffix):
    try:
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(_b64.b64decode(b64data))
        tmp.close()
        return tmp.name
    except Exception:
        return None

_ICON_ICO = _write_temp(_ICO_B64, ".ico")
_ICON_PNG = _write_temp(_PNG_B64, ".png")

# ── Voice lists ───────────────────────────────────────────────────────────────
MALE_VOICES = [
    ("Andrew  — US Natural",  "en-US-AndrewNeural"),
    ("Brian   — US Expressive","en-US-BrianNeural"),
    ("Steffan — US Deep",     "en-US-SteffanNeural"),
    ("Ryan    — UK Natural",  "en-GB-RyanNeural"),
    ("Davis   — US Neural",   "en-US-DavisNeural"),
]
FEMALE_VOICES = [
    ("Emma    — US Natural",  "en-US-EmmaNeural"),
    ("Ava     — US Expressive","en-US-AvaNeural"),
    ("Jane    — US Warm",     "en-US-JaneNeural"),
    ("Sonia   — UK Natural",  "en-GB-SoniaNeural"),
    ("Aria    — US Neural",   "en-US-AriaNeural"),
]


# ─────────────────────────────────────────────────────────────────────────────
class AudioPlayer:
    def __init__(self):
        self._alive = True

    def play(self, path):
        self._alive = True
        if _PG_OK:
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    if not self._alive:
                        pygame.mixer.music.stop()
                        return False
                    time.sleep(0.025)
                return True
            except Exception as e:
                print(f"pygame error: {e}")
        return self._os_play(path)

    def stop(self):
        self._alive = False
        if _PG_OK:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

    def _os_play(self, path):
        s = platform.system()
        try:
            if s == "Windows":
                cmd = ["powershell", "-c", f'(New-Object Media.SoundPlayer "{path}").PlaySync()']
            elif s == "Darwin":
                cmd = ["afplay", path]
            else:
                cmd = ["aplay", path]
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            while proc.poll() is None:
                if not self._alive:
                    proc.terminate()
                    return False
                time.sleep(0.04)
            return True
        except Exception:
            return False


# ─────────────────────────────────────────────────────────────────────────────
class NeuralTTS:
    def __init__(self):
        self.voice  = "en-US-AndrewNeural"
        self.rate   = "+0%"
        self.volume = "+0%"
        self.pitch  = "+0Hz"
        self._player = AudioPlayer()
        self._stop_requested = False

    def set_voice(self, vid):  self.voice = vid
    def set_rate(self, offset):
        self.rate = f"+{offset}%" if offset >= 0 else f"{offset}%"
    def set_volume(self, pct):
        off = pct - 100
        self.volume = f"+{off}%" if off >= 0 else f"{off}%"

    async def _synth(self, text, out):
        c = edge_tts.Communicate(text, self.voice, rate=self.rate,
                                  volume=self.volume, pitch=self.pitch)
        await c.save(out)

    def stop(self):
        self._stop_requested = True
        self._player.stop()

    def _fallback(self, text):
        try:
            import pyttsx3
            e = pyttsx3.init(); e.say(text); e.runAndWait(); e.stop()
            return True
        except Exception:
            return False


# ─────────────────────────────────────────────────────────────────────────────
class InterruptionListener:
    def __init__(self, on_speak_start, on_speak_end, energy_threshold=300):
        self._on_start = on_speak_start
        self._on_end   = on_speak_end
        self.energy_threshold = energy_threshold
        self._running  = False
        self._thread   = None

    def start(self):
        if self._running: return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self): self._running = False

    def _loop(self):
        if not _SR_OK: return
        try:
            import audioop
            SILENCE_SECS = 0.5
            CHUNK_SECS   = 0.03
            speaking     = False
            silent_since = None
            with sr.Microphone() as src:
                sample_rate  = src.SAMPLE_RATE
                sample_width = src.SAMPLE_WIDTH
                chunk_size   = int(sample_rate * CHUNK_SECS)
                src.stream.read(chunk_size)
                while self._running:
                    try:
                        raw    = src.stream.read(chunk_size)
                        energy = audioop.rms(raw, sample_width)
                        if energy >= self.energy_threshold:
                            if not speaking:
                                speaking = True; silent_since = None
                                self._on_start()
                            else:
                                silent_since = None
                        else:
                            if speaking:
                                if silent_since is None:
                                    silent_since = time.time()
                                elif (time.time() - silent_since) >= SILENCE_SECS:
                                    speaking = False; silent_since = None
                                    self._on_end()
                    except Exception:
                        time.sleep(0.05)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
class SpeechController:
    def __init__(self, tts, on_status, on_progress):
        self.tts         = tts
        self.on_status   = on_status
        self.on_progress = on_progress
        self._sentences  = []
        self._idx        = 0
        self._thread     = None
        self._stop_evt   = threading.Event()
        self._speaking   = False

    def speak(self, text):
        self._hard_stop()
        self._sentences = self._split(text)
        self._idx = 0
        self._launch(0)

    def pause(self):
        self._stop_evt.set()
        self.tts.stop()
        self.on_status("⏸  Paused")

    def unpause(self):
        self._stop_evt.clear()
        self.tts._stop_requested = False
        self._launch(self._idx)

    def resume(self):
        if not self._sentences: return
        self._stop_evt.clear()
        self.tts._stop_requested = False
        self._launch(self._idx)

    def stop(self):
        self._hard_stop()
        self._sentences = []
        self.on_status("Stopped")
        self.on_progress(0, 0)

    def _hard_stop(self):
        self._stop_evt.set()
        self.tts.stop()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.5)
        self._speaking = False
        self._stop_evt.clear()
        self.tts._stop_requested = False

    def _launch(self, from_idx):
        self._stop_evt.clear()
        self._thread = threading.Thread(target=self._loop, args=(from_idx,), daemon=True)
        self._thread.start()

    def _loop(self, start):
        self._speaking = True
        self.tts._stop_requested = False
        total = len(self._sentences)

        def _synth_to_file(sentence):
            if self._stop_evt.is_set() or self.tts._stop_requested:
                return None
            tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            tmp.close()
            path = tmp.name
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.tts._synth(sentence, path))
                loop.close()
                return path
            except Exception as e:
                print(f"Synth error: {e}")
                try: os.unlink(path)
                except: pass
                return None

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        prefetch_future = None

        # Kick off first sentence prefetch
        for i in range(start, total):
            if self._sentences[i].strip():
                prefetch_future = executor.submit(_synth_to_file, self._sentences[i].strip())
                break

        if prefetch_future is None:
            self._speaking = False
            executor.shutdown(wait=False)
            return

        for i in range(start, total):
            if self._stop_evt.is_set(): break
            self._idx = i
            sentence  = self._sentences[i].strip()
            if not sentence: continue

            preview = sentence[:65] + ("..." if len(sentence) > 65 else "")
            self.on_status(f"[{i+1}/{total}]  {preview}")
            self.on_progress(i, total)

            # Wait for this sentence's audio
            audio_path = prefetch_future.result() if prefetch_future else _synth_to_file(sentence)
            prefetch_future = None

            # Start next sentence fetching immediately
            for j in range(i + 1, total):
                if self._sentences[j].strip():
                    prefetch_future = executor.submit(_synth_to_file, self._sentences[j].strip())
                    break

            if audio_path is None or self._stop_evt.is_set():
                if audio_path:
                    try: os.unlink(audio_path)
                    except: pass
                self.on_status(f"Interrupted at sentence {i+1} — press Resume to replay")
                self._speaking = False
                executor.shutdown(wait=False)
                return

            self.tts._stop_requested = False
            finished = self.tts._player.play(audio_path)
            try: os.unlink(audio_path)
            except: pass

            if self.tts._stop_requested or not finished:
                self.on_status(f"Interrupted at sentence {i+1} — press Resume to replay")
                self._speaking = False
                executor.shutdown(wait=False)
                return

        executor.shutdown(wait=False)
        if not self._stop_evt.is_set() and self._sentences:
            self.on_status("✓  Finished")
            self.on_progress(total, total)
        self._speaking = False

    @staticmethod
    def _split(text):
        parts = re.split(r'(?<=[.!?])\s+', text.strip())
        result = []
        for p in parts:
            for ln in p.split('\n'):
                s = ln.strip()
                if s: result.append(s)
        return result


# ─────────────────────────────────────────────────────────────────────────────
class ProjectAnsuzApp(tk.Tk):
    BG     = "#0a0a0a"
    PANEL  = "#111111"
    PANEL2 = "#161612"
    GOLD   = "#c9a84c"
    GOLD2  = "#f0cc6e"
    GOLD3  = "#4a3810"
    GOLDD  = "#7a6030"
    TEXT   = "#e8e0cc"
    DIM    = "#5a5040"
    BTN_BG = "#1a1a12"
    GREEN  = "#4caf76"
    REDC   = "#c94c4c"

    def __init__(self):
        super().__init__()
        self.title("Project Ansuz")
        self.geometry("1120x820")
        self.minsize(900, 680)
        self.configure(bg=self.BG)
        self.resizable(True, True)

        # Apply rune icon to window
        if _ICON_ICO:
            try: self.iconbitmap(_ICON_ICO)
            except: pass

        self._gender     = "male"
        self._paused     = False
        self._mic_ok     = False
        self._mic_paused = False
        self._int_on     = tk.BooleanVar(value=True)
        self._rate_var   = tk.IntVar(value=0)
        self._vol_var    = tk.IntVar(value=100)
        self._thresh_var = tk.IntVar(value=300)

        self.tts      = NeuralTTS()
        self.ctrl     = SpeechController(self.tts, self._set_status, self._set_progress)
        self.listener = InterruptionListener(self._on_mic_speak, self._on_mic_silence)

        self._build()
        self._apply_voice()
        threading.Thread(target=self._check_mic, daemon=True).start()

    def _check_mic(self):
        ok = False
        if _SR_OK:
            try:
                r = sr.Recognizer()
                with sr.Microphone() as src:
                    r.adjust_for_ambient_noise(src, duration=0.1)
                ok = True
            except: pass
        self._mic_ok = ok
        self.after(0, lambda: self._mic_lbl.config(
            text="  ᛗ Mic: Active" if ok else "  ᛗ Mic: Not found",
            fg=self.GREEN if ok else self.REDC))

    def _build(self):
        self._topbar()
        wrap = tk.Frame(self, bg=self.BG)
        wrap.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))
        wrap.columnconfigure(0, weight=3)
        wrap.columnconfigure(1, weight=1, minsize=280)
        wrap.rowconfigure(0, weight=1)
        self._left(wrap)
        self._right(wrap)
        self._statusbar()
        self._styles()

    def _topbar(self):
        bar = tk.Frame(self, bg=self.GOLD3, height=68)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        # Ansuz rune icon
        icon_shown = False
        if _PIL_OK and _ICON_PNG:
            try:
                img = Image.open(_ICON_PNG).resize((44,44), Image.LANCZOS)
                self._rune_photo = ImageTk.PhotoImage(img)
                tk.Label(bar, image=self._rune_photo,
                         bg=self.GOLD3, padx=10).pack(side=tk.LEFT)
                icon_shown = True
            except: pass
        if not icon_shown:
            tk.Label(bar, text="ᚨ",
                     font=font.Font(family="Segoe UI", size=26),
                     bg=self.GOLD3, fg=self.GOLD2, padx=12).pack(side=tk.LEFT)

        title_block = tk.Frame(bar, bg=self.GOLD3)
        title_block.pack(side=tk.LEFT, padx=4)
        tk.Label(title_block, text="PROJECT  ANSUZ",
                 font=font.Font(family="Trebuchet MS", size=20, weight="bold"),
                 bg=self.GOLD3, fg=self.GOLD2).pack(anchor="w")
        tk.Label(title_block, text="ᚨ  Neural Voices  ᛟ  Smart Interruption  ᛗ  No Limits",
                 font=font.Font(family="Trebuchet MS", size=9),
                 bg=self.GOLD3, fg="#c0a060").pack(anchor="w")

        tk.Label(bar, text="ᛁ ᛇ ᛉ",
                 font=font.Font(family="Segoe UI", size=14),
                 bg=self.GOLD3, fg=self.GOLDD, padx=8).pack(side=tk.RIGHT)

        self._mic_lbl = tk.Label(bar, text="  Checking mic...",
                                  font=font.Font(size=9), bg=self.GOLD3, fg=self.TEXT, padx=16)
        self._mic_lbl.pack(side=tk.RIGHT)

    def _left(self, parent):
        f = tk.Frame(parent, bg=self.BG)
        f.grid(row=0, column=0, sticky="nsew", padx=(0,14))
        f.rowconfigure(1, weight=1)
        f.columnconfigure(0, weight=1)

        hrow = tk.Frame(f, bg=self.BG)
        hrow.grid(row=0, column=0, sticky="ew", pady=(16,4))
        tk.Label(hrow, text="INPUT TEXT",
                 font=font.Font(family="Trebuchet MS", size=10, weight="bold"),
                 bg=self.BG, fg=self.GOLD).pack(side=tk.LEFT)
        self._info_lbl = tk.Label(hrow, text="0 chars  |  0 sentences",
                                   font=font.Font(size=8), bg=self.BG, fg=self.DIM)
        self._info_lbl.pack(side=tk.RIGHT)

        border = tk.Frame(f, bg=self.GOLD3, bd=1)
        border.grid(row=1, column=0, sticky="nsew")
        border.rowconfigure(0, weight=1)
        border.columnconfigure(0, weight=1)

        self.text_area = tk.Text(
            border,
            font=font.Font(family="Consolas", size=12),
            bg="#0c0c0a", fg=self.TEXT,
            insertbackground=self.GOLD2,
            selectbackground=self.GOLD3,
            selectforeground=self.TEXT,
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD, undo=True,
            padx=16, pady=14, spacing3=5)
        self.text_area.grid(row=0, column=0, sticky="nsew")
        vsb = ttk.Scrollbar(border, orient="vertical",
                             command=self.text_area.yview, style="Gold.Vertical.TScrollbar")
        vsb.grid(row=0, column=1, sticky="ns")
        self.text_area["yscrollcommand"] = vsb.set
        self.text_area.bind("<KeyRelease>", self._on_text_key)

        self._ph = "Paste or type your text here. No length limit."
        self._ph_on = True
        self.text_area.insert("1.0", self._ph)
        self.text_area.config(fg=self.DIM)
        self.text_area.bind("<FocusIn>",  self._ph_clear)
        self.text_area.bind("<FocusOut>", self._ph_restore)

        prow = tk.Frame(f, bg=self.BG)
        prow.grid(row=2, column=0, sticky="ew", pady=(6,2))
        tk.Label(prow, text="PROGRESS",
                 font=font.Font(size=8, weight="bold"), bg=self.BG, fg=self.DIM).pack(side=tk.LEFT)
        self._prog_lbl = tk.Label(prow, text="0 / 0 sentences",
                                   font=font.Font(size=8), bg=self.BG, fg=self.DIM)
        self._prog_lbl.pack(side=tk.RIGHT)

        self._prog_bar = ttk.Progressbar(f, orient="horizontal", mode="determinate",
                                          style="Gold.Horizontal.TProgressbar")
        self._prog_bar.grid(row=3, column=0, sticky="ew", pady=(0,8))

        crow = tk.Frame(f, bg=self.BG)
        crow.grid(row=4, column=0, sticky="ew")
        self.btn_speak  = self._mk_btn(crow,"SPEAK",  self._do_speak,  self.GOLD,   "#0a0a0a", 10)
        self.btn_pause  = self._mk_btn(crow,"PAUSE",  self._do_pause,  self.BTN_BG, self.TEXT, 10)
        self.btn_resume = self._mk_btn(crow,"RESUME", self._do_resume, "#1a2210",   "#88ff88", 10)
        self.btn_stop   = self._mk_btn(crow,"STOP",   self._do_stop,   "#1f0808",   self.REDC, 8)
        self.btn_clear  = self._mk_btn(crow,"CLEAR",  self._do_clear,  self.BTN_BG, self.DIM,  8)
        for b in (self.btn_speak, self.btn_pause, self.btn_resume, self.btn_stop, self.btn_clear):
            b.pack(side=tk.LEFT, padx=(0,6))

    def _mk_btn(self, parent, label, cmd, bg, fg, w):
        b = tk.Button(parent, text=label, command=cmd, bg=bg, fg=fg,
                      font=font.Font(family="Trebuchet MS", size=11, weight="bold"),
                      relief=tk.FLAT, bd=0, padx=16, pady=10,
                      activebackground=self.GOLD2, activeforeground="#0a0a0a",
                      cursor="hand2", width=w)
        orig = bg
        b.bind("<Enter>", lambda e, b=b, o=orig: b.config(bg=self._lighter(o)))
        b.bind("<Leave>", lambda e, b=b, o=orig: b.config(bg=o))
        return b

    def _lighter(self, c):
        try:
            r,g,bv = int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
            return f"#{min(255,r+40):02x}{min(255,g+28):02x}{min(255,bv+10):02x}"
        except: return c

    def _right(self, parent):
        f = tk.Frame(parent, bg=self.PANEL)
        f.grid(row=0, column=1, sticky="nsew")

        def sec(title, rune="ᚱ"):
            tk.Label(f, text=f"{rune}  {title}",
                     font=font.Font(family="Trebuchet MS", size=9, weight="bold"),
                     bg=self.PANEL, fg=self.GOLD, anchor="w", padx=14).pack(fill=tk.X, pady=(16,0))
            tk.Frame(f, bg=self.GOLD3, height=1).pack(fill=tk.X, padx=14, pady=(2,0))

        sec("VOICE GENDER", "ᚷ")
        gf = tk.Frame(f, bg=self.PANEL)
        gf.pack(fill=tk.X, padx=14, pady=8)
        self.btn_m = tk.Button(gf, text="MALE",
                                command=lambda: self._set_gender("male"),
                                bg=self.GOLD, fg="#0a0a0a",
                                font=font.Font(family="Trebuchet MS", size=11, weight="bold"),
                                relief=tk.FLAT, padx=12, pady=9, cursor="hand2", width=7)
        self.btn_m.pack(side=tk.LEFT, padx=(0,6))
        self.btn_f = tk.Button(gf, text="FEMALE",
                                command=lambda: self._set_gender("female"),
                                bg=self.BTN_BG, fg=self.DIM,
                                font=font.Font(family="Trebuchet MS", size=11, weight="bold"),
                                relief=tk.FLAT, padx=12, pady=9, cursor="hand2", width=7)
        self.btn_f.pack(side=tk.LEFT)

        self._voice_active_lbl = tk.Label(f, text="",
                                           font=font.Font(size=8, slant="italic"),
                                           bg=self.PANEL, fg=self.DIM, padx=14, anchor="w")
        self._voice_active_lbl.pack(fill=tk.X, pady=(2,0))

        sec("MALE VOICE", "ᛏ")
        mf = tk.Frame(f, bg=self.PANEL)
        mf.pack(fill=tk.X, padx=14, pady=6)
        self._m_combo = ttk.Combobox(mf, values=[v[0] for v in MALE_VOICES],
                                      state="readonly", style="Gold.TCombobox",
                                      font=font.Font(size=9))
        self._m_combo.set(MALE_VOICES[0][0])
        self._m_combo.pack(fill=tk.X)
        self._m_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_voice())

        sec("FEMALE VOICE", "ᛒ")
        ff = tk.Frame(f, bg=self.PANEL)
        ff.pack(fill=tk.X, padx=14, pady=6)
        self._f_combo = ttk.Combobox(ff, values=[v[0] for v in FEMALE_VOICES],
                                      state="readonly", style="Gold.TCombobox",
                                      font=font.Font(size=9))
        self._f_combo.set(FEMALE_VOICES[0][0])
        self._f_combo.pack(fill=tk.X)
        self._f_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_voice())

        sec("SPEECH RATE", "ᚹ")
        rf = tk.Frame(f, bg=self.PANEL)
        rf.pack(fill=tk.X, padx=14, pady=6)
        self._rate_lbl = tk.Label(rf, text="Normal (0%)", font=font.Font(size=8),
                                   bg=self.PANEL, fg=self.TEXT)
        self._rate_lbl.pack(side=tk.RIGHT)
        tk.Scale(rf, from_=-50, to=100, orient=tk.HORIZONTAL,
                  variable=self._rate_var, command=self._on_rate,
                  bg=self.PANEL, fg=self.TEXT, troughcolor="#1e1608",
                  activebackground=self.GOLD, highlightthickness=0,
                  sliderrelief=tk.FLAT, showvalue=False).pack(side=tk.LEFT, fill=tk.X, expand=True)

        sec("VOLUME", "ᛝ")
        vf = tk.Frame(f, bg=self.PANEL)
        vf.pack(fill=tk.X, padx=14, pady=6)
        self._vol_lbl = tk.Label(vf, text="100%", font=font.Font(size=8),
                                  bg=self.PANEL, fg=self.TEXT)
        self._vol_lbl.pack(side=tk.RIGHT)
        tk.Scale(vf, from_=10, to=150, orient=tk.HORIZONTAL,
                  variable=self._vol_var, command=self._on_vol,
                  bg=self.PANEL, fg=self.TEXT, troughcolor="#1e1608",
                  activebackground=self.GOLD, highlightthickness=0,
                  sliderrelief=tk.FLAT, showvalue=False).pack(side=tk.LEFT, fill=tk.X, expand=True)

        sec("ᚨ SMART INTERRUPT", "ᛗ")
        intf = tk.Frame(f, bg=self.PANEL)
        intf.pack(fill=tk.X, padx=14, pady=8)
        tk.Checkbutton(intf, text="Enable mic detection",
                        variable=self._int_on, command=self._on_int_toggle,
                        bg=self.PANEL, fg=self.TEXT, selectcolor="#241c00",
                        activebackground=self.PANEL, activeforeground=self.TEXT,
                        font=font.Font(size=9), cursor="hand2").pack(anchor="w")
        tk.Label(intf, text="Speak → TTS pauses  ·  Silence → TTS resumes.",
                 font=font.Font(size=8), bg=self.PANEL, fg=self.DIM,
                 justify=tk.LEFT).pack(anchor="w", pady=(4,0))

        sf = tk.Frame(intf, bg=self.PANEL)
        sf.pack(fill=tk.X, pady=(8,0))
        tk.Label(sf, text="ᛉ Sensitivity", font=font.Font(size=8, weight="bold"),
                 bg=self.PANEL, fg=self.GOLD).pack(side=tk.LEFT)
        self._thresh_lbl = tk.Label(sf, text="300", font=font.Font(size=8),
                                     bg=self.PANEL, fg=self.TEXT)
        self._thresh_lbl.pack(side=tk.RIGHT)
        sens_row = tk.Frame(intf, bg=self.PANEL)
        sens_row.pack(fill=tk.X, pady=(2,0))
        tk.Label(sens_row, text="quiet", font=font.Font(size=7),
                 bg=self.PANEL, fg=self.DIM).pack(side=tk.LEFT)
        tk.Scale(sens_row, from_=100, to=2000, orient=tk.HORIZONTAL,
                  variable=self._thresh_var, command=self._on_thresh,
                  bg=self.PANEL, fg=self.TEXT, troughcolor="#1e1608",
                  activebackground=self.GOLD, highlightthickness=0,
                  sliderrelief=tk.FLAT, showvalue=False).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(sens_row, text="loud", font=font.Font(size=7),
                 bg=self.PANEL, fg=self.DIM).pack(side=tk.RIGHT)

        sec("ENGINE STATUS", "ᛟ")
        edge_s = "edge-tts ✓" if _EDGE_OK else "edge-tts ✗  MISSING"
        pg_s   = "pygame    ✓" if _PG_OK  else "pygame    ✗  MISSING"
        sr_s   = "mic/SR    ✓" if _SR_OK  else "mic/SR    ✗  (optional)"
        pil_s  = "PIL       ✓" if _PIL_OK else "PIL       ✗  (optional)"
        tk.Label(f, text=f"{edge_s}\n{pg_s}\n{sr_s}\n{pil_s}",
                 font=font.Font(size=8), bg=self.PANEL, fg=self.DIM,
                 justify=tk.LEFT, padx=14, pady=6).pack(fill=tk.X)

        tk.Frame(f, bg=self.PANEL).pack(fill=tk.BOTH, expand=True)

    def _statusbar(self):
        bar = tk.Frame(self, bg="#070707", height=30)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)
        self._status_lbl = tk.Label(bar, text="Ready",
            font=font.Font(family="Trebuchet MS", size=9),
            bg="#070707", fg=self.GOLD, padx=16, anchor="w")
        self._status_lbl.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(bar, text="Project Ansuz  |  Microsoft Neural TTS  |  Free  |  No API Keys",
                 font=font.Font(size=8), bg="#070707", fg=self.DIM, padx=14).pack(side=tk.RIGHT)

    def _styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Gold.Horizontal.TProgressbar",
                     troughcolor="#181408", background=self.GOLD,
                     bordercolor=self.BG, lightcolor=self.GOLD2, darkcolor=self.GOLD3)
        s.configure("Gold.Vertical.TScrollbar",
                     background=self.GOLD3, troughcolor=self.PANEL2,
                     bordercolor=self.BG, arrowcolor=self.GOLD)
        s.configure("Gold.TCombobox",
                     fieldbackground="#0c0c08", background=self.BTN_BG,
                     foreground=self.TEXT, selectbackground=self.GOLD3,
                     selectforeground=self.TEXT, arrowcolor=self.GOLD)
        s.map("Gold.TCombobox",
              fieldbackground=[("readonly","#0c0c08")],
              foreground=[("readonly", self.TEXT)])

    # ── Placeholder helpers ────────────────────────────────────────────────
    def _ph_clear(self, e=None):
        if self._ph_on:
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg=self.TEXT)
            self._ph_on = False

    def _ph_restore(self, e=None):
        if not self.text_area.get("1.0","end-1c").strip():
            self._ph_on = True
            self.text_area.insert("1.0", self._ph)
            self.text_area.config(fg=self.DIM)

    def _get_text(self):
        t = self.text_area.get("1.0", tk.END).strip()
        return "" if (self._ph_on or t == self._ph) else t

    def _on_text_key(self, e=None):
        if self._ph_on: return
        text = self._get_text()
        chars = len(text)
        sents = len(SpeechController._split(text)) if text else 0
        self._info_lbl.config(text=f"{chars:,} chars  |  {sents} sentences")

    # ── Button actions ─────────────────────────────────────────────────────
    def _do_speak(self):
        text = self._get_text()
        if not text:
            messagebox.showwarning("No Text", "Enter or paste some text first.")
            return
        if not _EDGE_OK:
            messagebox.showerror("Missing Package",
                "edge-tts is not installed.\n\nRun:  pip install edge-tts pygame")
            return
        self._paused = False
        self._mic_paused = False
        self.btn_pause.config(text="PAUSE")
        self.ctrl.speak(text)
        if self._int_on.get() and self._mic_ok:
            self.listener.start()

    def _do_pause(self):
        if not self._paused:
            self.ctrl.pause()
            self.listener.stop()
            self._mic_paused = False
            self.btn_pause.config(text="UNPAUSE")
            self._paused = True
        else:
            self._paused = False
            self._mic_paused = False
            self.btn_pause.config(text="PAUSE")
            if self._int_on.get() and self._mic_ok:
                self.listener.start()
            self.ctrl.unpause()

    def _do_resume(self):
        self._mic_paused = False
        if self._int_on.get() and self._mic_ok:
            self.listener.start()
        self.ctrl.resume()

    def _do_stop(self):
        self.ctrl.stop()
        self.listener.stop()
        self._paused = False
        self._mic_paused = False
        self.btn_pause.config(text="PAUSE")

    def _do_clear(self):
        self.ctrl.stop()
        self.listener.stop()
        self._paused = False
        self._mic_paused = False
        self.btn_pause.config(text="PAUSE")
        self.text_area.delete("1.0", tk.END)
        self._ph_on = True
        self.text_area.insert("1.0", self._ph)
        self.text_area.config(fg=self.DIM)
        self._set_status("Ready")
        self._set_progress(0, 0)
        self._info_lbl.config(text="0 chars  |  0 sentences")

    # ── Mic callbacks ──────────────────────────────────────────────────────
    def _on_mic_speak(self):
        if self._int_on.get() and not self._mic_paused and not self._paused:
            self._mic_paused = True
            self.ctrl.pause()
            self._set_status("ᛗ  Mic detected speech — TTS paused…")

    def _on_mic_silence(self):
        if self._int_on.get() and self._mic_paused:
            self._mic_paused = False
            self.ctrl.unpause()
            self._set_status("ᚠ  Silence detected — TTS resuming…")

    # ── Controls ───────────────────────────────────────────────────────────
    def _on_thresh(self, val):
        v = int(float(val))
        self._thresh_lbl.config(text=str(v))
        self.listener.energy_threshold = v

    def _on_int_toggle(self):
        if not self._int_on.get():
            self.listener.stop()
            self._mic_paused = False

    def _set_gender(self, g):
        self._gender = g
        if g == "male":
            self.btn_m.config(bg=self.GOLD, fg="#0a0a0a")
            self.btn_f.config(bg=self.BTN_BG, fg=self.DIM)
        else:
            self.btn_f.config(bg=self.GOLD, fg="#0a0a0a")
            self.btn_m.config(bg=self.BTN_BG, fg=self.DIM)
        self._apply_voice()

    def _apply_voice(self):
        if self._gender == "male":
            idx, pool = self._m_combo.current(), MALE_VOICES
        else:
            idx, pool = self._f_combo.current(), FEMALE_VOICES
        idx = max(0, idx)
        name, vid = pool[idx]
        self.tts.set_voice(vid)
        self.tts.set_rate(self._rate_var.get())
        self.tts.set_volume(self._vol_var.get())
        self._voice_active_lbl.config(text=f"Active: {name}")

    def _on_rate(self, val):
        v = int(float(val))
        self._rate_lbl.config(
            text="Normal (0%)" if v==0 else (f"+{v}% faster" if v>0 else f"{v}% slower"))
        self.tts.set_rate(v)

    def _on_vol(self, val):
        v = int(float(val))
        self._vol_lbl.config(text=f"{v}%")
        self.tts.set_volume(v)

    def _set_status(self, msg):
        self.after(0, lambda: self._status_lbl.config(text=msg))

    def _set_progress(self, idx, total):
        def _do():
            if total > 0:
                self._prog_bar["maximum"] = 100
                self._prog_bar["value"]   = (idx/total)*100
                self._prog_lbl.config(text=f"{idx} / {total} sentences")
            else:
                self._prog_bar["value"] = 0
                self._prog_lbl.config(text="0 / 0 sentences")
        self.after(0, _do)

    def on_close(self):
        self.ctrl.stop()
        self.listener.stop()
        if _PG_OK:
            try: pygame.mixer.quit()
            except: pass
        # Clean up temp icon files
        for p in (_ICON_ICO, _ICON_PNG):
            if p:
                try: os.unlink(p)
                except: pass
        self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
def main():
    app = ProjectAnsuzApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

if __name__ == "__main__":
    main()
