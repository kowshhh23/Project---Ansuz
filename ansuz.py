"""
PROJECT ANSUZ v1.2 - Neural TTS with Nordic Black/Gold UI
ᚨ  The rune of communication, divine breath, and the spoken word.

Author:   Kowshick Kishore
Email:    Kowshickkishore775@gmail.com
GitHub:   https://github.com/kowshhh23/Project---Ansuz
License:  MIT — Copyright (c) 2026 Kowshick Kishore

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

# ── Voice lists (FIX 2) ───────────────────────────────────────────────────────
MALE_VOICES = [
    ("Andrew  — US Natural",        "en-US-AndrewNeural"),          # fast, warm default
    ("Andrew  — US Conversational", "en-US-AndrewMultilingualNeural"),
    ("Brian   — US Expressive",     "en-US-BrianNeural"),
    ("Ryan    — UK Natural",        "en-GB-RyanNeural"),
    ("Steffan — US Deep",           "en-US-SteffanNeural"),
]
FEMALE_VOICES = [
    ("Emma    — US Natural",        "en-US-EmmaNeural"),            # fast, warm default
    ("Ava     — US Conversational", "en-US-AvaMultilingualNeural"),
    ("Jane    — US Expressive",     "en-US-JaneNeural"),
    ("Sonia   — UK Natural",        "en-GB-SoniaNeural"),
    ("Aria    — US Neural",         "en-US-AriaNeural"),
]

# ── Preset modes ──────────────────────────────────────────────────────────────
PRESETS = {
    "Quiet Room":       (300,  150, 0.5,  "Low noise — office / studio"),
    "Normal Room":      (600,  250, 0.8,  "Some background noise"),
    "Noisy Room":       (1000, 400, 1.2,  "Crowd noise / AC / traffic"),
    "Presentation Hall":(1600, 600, 1.8,  "300+ people, PA system, high ambient"),
    "Custom":           (None, None, None, "Set manually below"),
}


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
                    time.sleep(0.01)
                return True
            except Exception as e:
                print(f"pygame error: {e}")
        return self._os_play(path)

    def stop(self):
        self._alive = False
        if _PG_OK:
            try: pygame.mixer.music.stop()
            except: pass

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
                time.sleep(0.015)
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
        """Plain edge-tts call — fast, reliable, no SSML overhead. (FIX 1)"""
        c = edge_tts.Communicate(
            text, self.voice,
            rate=self.rate,
            volume=self.volume,
            pitch=self.pitch,
        )
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
    """
    Smart mic interruption engine with sustained-speech detection.
    """
    def __init__(self, on_speak_start, on_speak_end,
                 energy_threshold=1600, sustain_ms=600, resume_delay_s=1.8,
                 on_calibrated=None):
        self._on_start      = on_speak_start
        self._on_end        = on_speak_end
        self._on_calibrated = on_calibrated
        self.energy_threshold  = energy_threshold
        self.sustain_ms        = sustain_ms
        self.resume_delay_s    = resume_delay_s
        self._running          = False
        self._thread           = None
        self.ambient_level     = 0

    def start(self):
        if self._running: return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def calibrate_ambient(self, duration_s=1.5, callback=None):
        def _do():
            if not _SR_OK: return
            try:
                import audioop
                CHUNK_SECS = 0.05
                samples = []
                with sr.Microphone() as src:
                    sample_rate  = src.SAMPLE_RATE
                    sample_width = src.SAMPLE_WIDTH
                    chunk_size   = int(sample_rate * CHUNK_SECS)
                    n_chunks = int(duration_s / CHUNK_SECS)
                    for _ in range(n_chunks):
                        raw = src.stream.read(chunk_size)
                        samples.append(audioop.rms(raw, sample_width))
                if samples:
                    samples.sort()
                    p95 = samples[int(len(samples)*0.95)]
                    self.ambient_level = p95
                    if callback:
                        callback(p95)
            except Exception as e:
                print(f"Calibration error: {e}")
        threading.Thread(target=_do, daemon=True).start()

    def _loop(self):
        if not _SR_OK: return
        try:
            import audioop
            CHUNK_SECS    = 0.03
            speaking      = False
            loud_since    = None
            silent_since  = None

            with sr.Microphone() as src:
                sample_rate  = src.SAMPLE_RATE
                sample_width = src.SAMPLE_WIDTH
                chunk_size   = int(sample_rate * CHUNK_SECS)
                src.stream.read(chunk_size)

                while self._running:
                    try:
                        raw    = src.stream.read(chunk_size)
                        energy = audioop.rms(raw, sample_width)
                        now    = time.time()

                        if energy >= self.energy_threshold:
                            silent_since = None
                            if not speaking:
                                if loud_since is None:
                                    loud_since = now
                                elif (now - loud_since) * 1000 >= self.sustain_ms:
                                    speaking   = True
                                    loud_since = None
                                    self._on_start()
                        else:
                            loud_since = None
                            if speaking:
                                if silent_since is None:
                                    silent_since = now
                                elif (now - silent_since) >= self.resume_delay_s:
                                    speaking     = False
                                    silent_since = None
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
            self._thread.join(timeout=0.3)
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

            audio_path = prefetch_future.result() if prefetch_future else _synth_to_file(sentence)
            prefetch_future = None

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
    BG     = "#070706"
    PANEL  = "#0d0d0b"
    PANEL2 = "#121210"
    GOLD   = "#d4a840"
    GOLD2  = "#f7d668"
    GOLD3  = "#3c2c08"
    GOLDD  = "#8a7038"
    TEXT   = "#ede5cf"
    DIM    = "#6a5e44"
    BTN_BG = "#171510"
    GREEN  = "#4caf76"
    REDC   = "#c94c4c"
    BLUE   = "#4c8ccf"

    def __init__(self):
        super().__init__()
        self.title("Project Ansuz")
        self.geometry("1160x860")
        self.minsize(940, 720)
        self.configure(bg=self.BG)
        self.resizable(True, True)

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

        self._thresh_var  = tk.IntVar(value=1600)
        self._sustain_var = tk.IntVar(value=600)
        self._resume_var  = tk.DoubleVar(value=1.8)
        self._preset_var  = tk.StringVar(value="Presentation Hall")

        self.tts      = NeuralTTS()
        self.ctrl     = SpeechController(self.tts, self._set_status, self._set_progress)
        self.listener = InterruptionListener(
            self._on_mic_speak, self._on_mic_silence,
            energy_threshold=1600, sustain_ms=600, resume_delay_s=1.8,
            on_calibrated=self._on_calibrated)

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

    # ── Build UI ───────────────────────────────────────────────────────────
    def _build(self):
        self._topbar()
        wrap = tk.Frame(self, bg=self.BG)
        wrap.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))
        wrap.columnconfigure(0, weight=3)
        wrap.columnconfigure(1, weight=1, minsize=300)
        wrap.rowconfigure(0, weight=1)
        self._left(wrap)
        self._right(wrap)
        self._statusbar()
        self._styles()

    # ── FIX 3: _topbar with Canvas gradient ───────────────────────────────
    def _topbar(self):
        bar = tk.Frame(self, bg=self.GOLD3, height=82)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        cv = tk.Canvas(bar, height=82, highlightthickness=0, bd=0)
        cv.place(x=0, y=0, relwidth=1, height=82)

        def _draw_topbar(event=None):
            cv.delete("all")
            w = cv.winfo_width() or 1200
            steps = 60
            for i in range(steps):
                t = i / steps
                mid = 1 - abs(t - 0.5) * 2
                r = int(0x1a + mid * 0x26)
                g = int(0x10 + mid * 0x18)
                b = int(0x00 + mid * 0x04)
                color = f"#{r:02x}{g:02x}{b:02x}"
                x0 = int(w * i / steps)
                x1 = int(w * (i + 1) / steps) + 1
                cv.create_rectangle(x0, 0, x1, 82, fill=color, outline="")
            cv.create_line(0, 0, w, 0, fill="#f7d668", width=2)
            cv.create_line(0, 1, w, 1, fill="#c9a840", width=1)
            cv.create_line(0, 80, w, 80, fill="#1a1000", width=1)
            cv.create_line(0, 81, w, 81, fill="#0a0800", width=1)
            runes = "ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ ᚺ ᚾ ᛁ ᛃ ᛇ ᛈ ᛉ ᛊ ᛏ ᛒ ᛖ ᛗ ᛚ ᛜ ᛞ ᛟ "
            tiled = (runes * 8)[:120]
            cv.create_text(w // 2, 70, text=tiled,
                           font=("Segoe UI", 7), fill="#3a2a08",
                           anchor="center")

        cv.bind("<Configure>", _draw_topbar)
        bar.bind("<Configure>", lambda e: _draw_topbar())
        self.after(50, _draw_topbar)

        icon_shown = False
        if _PIL_OK and _ICON_PNG:
            try:
                img = Image.open(_ICON_PNG).resize((48, 48), Image.LANCZOS)
                self._rune_photo = ImageTk.PhotoImage(img)
                tk.Label(bar, image=self._rune_photo,
                         bg=self.GOLD3, padx=14).pack(side=tk.LEFT)
                icon_shown = True
            except Exception:
                pass
        if not icon_shown:
            tk.Label(bar, text="ᚨ",
                     font=font.Font(family="Segoe UI", size=34),
                     bg=self.GOLD3, fg=self.GOLD2, padx=16).pack(side=tk.LEFT)

        title_block = tk.Frame(bar, bg=self.GOLD3)
        title_block.pack(side=tk.LEFT, padx=4)
        tk.Label(title_block, text="PROJECT  ANSUZ",
                 font=font.Font(family="Trebuchet MS", size=22, weight="bold"),
                 bg=self.GOLD3, fg=self.GOLD2).pack(anchor="w")
        tk.Label(title_block,
                 text="Human-like Neural Voices  \u00b7  Smart Interruption  \u00b7  No Limits  \u00b7  \u00a9 2026 Kowshick Kishore",
                 font=font.Font(family="Trebuchet MS", size=9),
                 bg=self.GOLD3, fg="#c0a060").pack(anchor="w")

        tk.Label(bar, text="ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ",
                 font=font.Font(family="Segoe UI", size=13),
                 bg=self.GOLD3, fg=self.GOLDD, padx=14).pack(side=tk.RIGHT)
        self._mic_lbl = tk.Label(bar, text="  Checking mic...",
                                  font=font.Font(size=9),
                                  bg=self.GOLD3, fg=self.TEXT, padx=16)
        self._mic_lbl.pack(side=tk.RIGHT)

    def _left(self, parent):
        f = tk.Frame(parent, bg=self.BG)
        f.grid(row=0, column=0, sticky="nsew", padx=(0,14))
        f.rowconfigure(1, weight=1)
        f.columnconfigure(0, weight=1)

        hrow = tk.Frame(f, bg=self.BG)
        hrow.grid(row=0, column=0, sticky="ew", pady=(18,6))
        tk.Label(hrow, text="ᚠ  INPUT TEXT",
                 font=font.Font(family="Trebuchet MS", size=10, weight="bold"),
                 bg=self.BG, fg=self.GOLD2).pack(side=tk.LEFT)
        self._info_lbl = tk.Label(hrow, text="0 chars  |  0 sentences",
                                   font=font.Font(size=8), bg=self.BG, fg=self.DIM)
        self._info_lbl.pack(side=tk.RIGHT)

        outer = tk.Frame(f, bg="#1a1200", bd=0)
        outer.grid(row=1, column=0, sticky="nsew")
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)
        border = tk.Frame(outer, bg=self.GOLD3, bd=1)
        border.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        border.rowconfigure(0, weight=1)
        border.columnconfigure(0, weight=1)

        self.text_area = tk.Text(border,
            font=font.Font(family="Consolas", size=12),
            bg="#090907", fg=self.TEXT, insertbackground=self.GOLD2,
            selectbackground="#3d2c08", selectforeground=self.GOLD2,
            relief=tk.FLAT, bd=0, wrap=tk.WORD, undo=True, padx=18, pady=16,
            spacing1=2, spacing3=6)
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

        rune_row = tk.Label(border, text="ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ ᚺ ᚾ ᛁ ᛃ ᛇ ᛈ ᛉ ᛊ ᛏ ᛒ ᛖ ᛗ ᛚ ᛜ ᛞ ᛟ",
                             font=font.Font(family="Segoe UI", size=7),
                             bg="#090907", fg="#2a2018", anchor="w", padx=18)
        rune_row.grid(row=1, column=0, sticky="ew")

        prow = tk.Frame(f, bg=self.BG)
        prow.grid(row=2, column=0, sticky="ew", pady=(6,2))
        tk.Label(prow, text="ᛇ  PROGRESS",
                 font=font.Font(size=8, weight="bold"), bg=self.BG, fg=self.GOLD).pack(side=tk.LEFT)
        self._prog_lbl = tk.Label(prow, text="0 / 0 sentences",
                                   font=font.Font(size=8), bg=self.BG, fg=self.DIM)
        self._prog_lbl.pack(side=tk.RIGHT)

        self._prog_bar = ttk.Progressbar(f, orient="horizontal", mode="determinate",
                                          style="Gold.Horizontal.TProgressbar", length=400)
        self._prog_bar.grid(row=3, column=0, sticky="ew", pady=(0,8))

        crow = tk.Frame(f, bg=self.BG)
        crow.grid(row=4, column=0, sticky="ew")
        self.btn_speak  = self._mk_btn(crow,"ᚨ  SPEAK",  self._do_speak,  self.GOLD,   "#080600", 10)
        self.btn_pause  = self._mk_btn(crow,"⏸  PAUSE",  self._do_pause,  self.BTN_BG, self.TEXT, 10)
        self.btn_resume = self._mk_btn(crow,"▶  RESUME", self._do_resume, "#121a0c",   "#7ae87a", 10)
        self.btn_stop   = self._mk_btn(crow,"■  STOP",   self._do_stop,   "#1a0808",   self.REDC, 8)
        self.btn_clear  = self._mk_btn(crow,"✕  CLEAR",  self._do_clear,  self.BTN_BG, self.DIM,  8)
        for b in (self.btn_speak, self.btn_pause, self.btn_resume, self.btn_stop, self.btn_clear):
            b.pack(side=tk.LEFT, padx=(0,6))

    def _mk_btn(self, parent, label, cmd, bg, fg, w):
        b = tk.Button(parent, text=label, command=cmd, bg=bg, fg=fg,
                      font=font.Font(family="Trebuchet MS", size=10, weight="bold"),
                      relief=tk.FLAT, bd=0, padx=14, pady=11,
                      activebackground=self.GOLD2, activeforeground="#060400",
                      cursor="hand2", width=w)
        orig = bg
        b.bind("<Enter>", lambda e, b=b, o=orig: b.config(bg=self._lighter(o)))
        b.bind("<Leave>", lambda e, b=b, o=orig: b.config(bg=o))
        return b

    def _lighter(self, c):
        try:
            r,g,bv = int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
            return f"#{min(255,r+55):02x}{min(255,g+38):02x}{min(255,bv+14):02x}"
        except: return c

    def _right(self, parent):
        f = tk.Frame(parent, bg=self.PANEL, bd=0)
        f.grid(row=0, column=1, sticky="nsew", padx=(4,0))

        # ── FIX 4: sec() with Canvas divider ─────────────────────────────
        def sec(title, rune="ᚱ"):
            tk.Frame(f, bg=self.PANEL, height=6).pack(fill=tk.X)
            hdr = tk.Frame(f, bg="#0f0f0d")
            hdr.pack(fill=tk.X)
            tk.Label(hdr, text=f"{rune}  {title}",
                     font=font.Font(family="Trebuchet MS", size=9, weight="bold"),
                     bg="#0f0f0d", fg=self.GOLD2,
                     anchor="w", padx=14, pady=5).pack(fill=tk.X)
            div = tk.Canvas(f, height=3, highlightthickness=0, bg=self.PANEL)
            div.pack(fill=tk.X, padx=8)
            def _draw_div(e, div=div):
                div.delete("all")
                w = div.winfo_width() or 300
                div.create_line(0, 2, w, 2, fill="#3d2c08", width=1)
                div.create_line(0, 1, w, 1, fill="#c9a840", width=1)
                div.create_line(0, 0, w, 0, fill="#f7d668", width=1)
            div.bind("<Configure>", _draw_div)
            self.after(60, _draw_div)

        def slider_row(parent, label, var, from_, to, cmd, fmt=str):
            row = tk.Frame(parent, bg=self.PANEL)
            row.pack(fill=tk.X, pady=(4,0))
            tk.Label(row, text=label, font=font.Font(size=8),
                     bg=self.PANEL, fg=self.DIM, width=14, anchor="w").pack(side=tk.LEFT)
            lbl = tk.Label(row, text=fmt(var.get()), font=font.Font(size=8),
                           bg=self.PANEL, fg=self.TEXT, width=6, anchor="e")
            lbl.pack(side=tk.RIGHT)
            def _upd(val, lbl=lbl, fmt=fmt):
                lbl.config(text=fmt(float(val)))
                cmd(val)
                self._preset_var.set("Custom")
                if hasattr(self, '_preset_lbl'):
                    self._preset_lbl.config(text="Custom")
            tk.Scale(row, from_=from_, to=to, orient=tk.HORIZONTAL,
                      variable=var, command=_upd,
                      bg=self.PANEL, fg=self.TEXT, troughcolor="#1e1608",
                      activebackground=self.GOLD, highlightthickness=0,
                      sliderrelief=tk.FLAT, showvalue=False,
                      resolution=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4,4))
            return lbl

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
        intf.pack(fill=tk.X, padx=14, pady=(6,0))

        tk.Checkbutton(intf, text="Enable mic detection",
                        variable=self._int_on, command=self._on_int_toggle,
                        bg=self.PANEL, fg=self.TEXT, selectcolor="#241c00",
                        activebackground=self.PANEL, activeforeground=self.TEXT,
                        font=font.Font(size=9), cursor="hand2").pack(anchor="w")

        pf = tk.Frame(intf, bg=self.PANEL)
        pf.pack(fill=tk.X, pady=(8,2))
        tk.Label(pf, text="Room Preset", font=font.Font(size=8, weight="bold"),
                 bg=self.PANEL, fg=self.GOLD).pack(anchor="w")
        self._preset_lbl = tk.Label(pf, text="Presentation Hall",
                                     font=font.Font(size=8, slant="italic"),
                                     bg=self.PANEL, fg=self.DIM)
        self._preset_lbl.pack(anchor="w")

        preset_row1 = tk.Frame(intf, bg=self.PANEL)
        preset_row1.pack(fill=tk.X, pady=(2,0))
        preset_row2 = tk.Frame(intf, bg=self.PANEL)
        preset_row2.pack(fill=tk.X, pady=(2,6))
        rows = [preset_row1, preset_row1, preset_row2, preset_row2, preset_row2]
        for i, (name, (thresh, sustain, resume, desc)) in enumerate(PRESETS.items()):
            is_active = (name == "Presentation Hall")
            bg = self.GOLD3 if is_active else "#1a1a12"
            fg = self.GOLD2 if is_active else self.DIM
            b = tk.Button(rows[i], text=name,
                           command=lambda n=name: self._apply_preset(n),
                           bg=bg, fg=fg,
                           font=font.Font(family="Trebuchet MS", size=7, weight="bold"),
                           relief=tk.FLAT, bd=0, padx=5, pady=7, cursor="hand2",
                           wraplength=60)
            b.pack(side=tk.LEFT, padx=(0,3), fill=tk.X, expand=True)
            if not hasattr(self, '_preset_btns'): self._preset_btns = {}
            self._preset_btns[name] = b

        adv = tk.Frame(intf, bg=self.PANEL)
        adv.pack(fill=tk.X, pady=(2,0))
        tk.Label(adv, text="Advanced Controls",
                 font=font.Font(size=8, weight="bold"),
                 bg=self.PANEL, fg=self.GOLD).pack(anchor="w", pady=(4,2))
        slider_row(adv, "Threshold (RMS)", self._thresh_var, 100, 3000,
                   self._on_thresh, fmt=lambda v: f"{int(float(v))}")
        slider_row(adv, "Sustain (ms)", self._sustain_var, 50, 1500,
                   self._on_sustain, fmt=lambda v: f"{int(float(v))}ms")
        slider_row(adv, "Resume delay (s)", self._resume_var, 0.2, 4.0,
                   self._on_resume, fmt=lambda v: f"{float(v):.1f}s")

        cal_row = tk.Frame(intf, bg=self.PANEL)
        cal_row.pack(fill=tk.X, pady=(8,0))
        self._cal_btn = tk.Button(cal_row, text="ᛉ  Auto-Calibrate Room",
                                   command=self._do_calibrate,
                                   bg="#0a1a2a", fg=self.BLUE,
                                   font=font.Font(family="Trebuchet MS", size=9, weight="bold"),
                                   relief=tk.FLAT, padx=10, pady=7, cursor="hand2")
        self._cal_btn.pack(fill=tk.X)
        self._cal_lbl = tk.Label(intf, text="Measures room noise and sets threshold automatically.",
                                  font=font.Font(size=7), bg=self.PANEL, fg=self.DIM)
        self._cal_lbl.pack(anchor="w", pady=(2,0))

        sec("ENGINE STATUS", "ᛟ")
        eng_frame = tk.Frame(f, bg=self.PANEL)
        eng_frame.pack(fill=tk.X, padx=14, pady=(4,8))
        for pkg, ok, note in [
            ("edge-tts", _EDGE_OK, "TTS engine"),
            ("pygame",   _PG_OK,   "Audio playback"),
            ("mic / SR", _SR_OK,   "Interruption"),
            ("PIL",      _PIL_OK,  "Icon rendering"),
        ]:
            row = tk.Frame(eng_frame, bg=self.PANEL)
            row.pack(fill=tk.X, pady=1)
            dot_color = self.GREEN if ok else self.REDC
            tk.Label(row, text="●", font=font.Font(size=7),
                     bg=self.PANEL, fg=dot_color, width=2).pack(side=tk.LEFT)
            tk.Label(row, text=f"{pkg:<10}", font=font.Font(family="Consolas", size=8),
                     bg=self.PANEL, fg=self.TEXT if ok else self.DIM).pack(side=tk.LEFT)
            tk.Label(row, text=note, font=font.Font(size=7),
                     bg=self.PANEL, fg=self.DIM).pack(side=tk.LEFT, padx=(4,0))

        tk.Frame(f, bg=self.PANEL).pack(fill=tk.BOTH, expand=True)

    # ── FIX 5: _statusbar with Canvas separator ────────────────────────────
    def _statusbar(self):
        sep = tk.Canvas(self, height=2, highlightthickness=0)
        sep.pack(fill=tk.X, side=tk.BOTTOM)
        def _draw_sep(e=None):
            sep.delete("all")
            w = sep.winfo_width() or 1200
            sep.create_line(0, 0, w, 0, fill="#3d2c08", width=1)
            sep.create_line(0, 1, w, 1, fill="#c9a840", width=1)
        sep.bind("<Configure>", _draw_sep)
        self.after(60, _draw_sep)

        bar = tk.Frame(self, bg="#060605", height=32)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)

        tk.Label(bar, text="ᚨ",
                 font=font.Font(family="Segoe UI", size=11),
                 bg="#060605", fg="#3d2c08", padx=6).pack(side=tk.LEFT)

        self._status_lbl = tk.Label(bar, text="Ready",
            font=font.Font(family="Trebuchet MS", size=9),
            bg="#060605", fg=self.GOLD, padx=4, anchor="w")
        self._status_lbl.pack(side=tk.LEFT, fill=tk.Y)

        tk.Frame(bar, bg="#3d2c08", width=1).pack(
            side=tk.LEFT, fill=tk.Y, pady=6, padx=10)

        tk.Label(bar,
                 text="\u00a9 2026 Kowshick Kishore  \u00b7  github.com/kowshhh23/Project---Ansuz  \u00b7  Microsoft Neural TTS  \u00b7  Free",
                 font=font.Font(size=7),
                 bg="#060605", fg="#4a3e28", padx=6).pack(side=tk.RIGHT)

    def _styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Gold.Horizontal.TProgressbar",
                     troughcolor="#100e06", background=self.GOLD,
                     bordercolor="#1a1200", lightcolor=self.GOLD2,
                     darkcolor=self.GOLD3, thickness=10)
        s.configure("Gold.Vertical.TScrollbar",
                     background="#1a1608", troughcolor="#0a0900",
                     bordercolor=self.BG, arrowcolor=self.GOLD,
                     relief="flat", arrowsize=12)
        s.map("Gold.Vertical.TScrollbar",
              background=[("active", self.GOLD3), ("pressed", self.GOLDD)])
        s.configure("Gold.TCombobox",
                     fieldbackground="#0b0b09", background=self.BTN_BG,
                     foreground=self.TEXT, selectbackground="#3d2c08",
                     selectforeground=self.GOLD2, arrowcolor=self.GOLD,
                     bordercolor="#2a2010", lightcolor="#1a1608",
                     darkcolor="#080600")
        s.map("Gold.TCombobox",
              fieldbackground=[("readonly","#0b0b09")],
              foreground=[("readonly", self.TEXT)],
              arrowcolor=[("active", self.GOLD2)])

    # ── Placeholder ────────────────────────────────────────────────────────
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
        # FIX 1: hard-reset controller so new text always takes effect immediately
        if self._ph_on:
            return
        raw = self.text_area.get("1.0", tk.END).strip()
        if not raw:
            self._set_status("Nothing to speak — paste some text first.")
            return
        if not _EDGE_OK:
            messagebox.showerror("Missing Package",
                "edge-tts is not installed.\n\nRun:  pip install edge-tts pygame")
            return
        self._paused = False; self._mic_paused = False
        self.btn_pause.config(text="PAUSE")
        self.ctrl.stop()
        self.ctrl._sentences = []
        self.ctrl._idx = 0
        self.ctrl.speak(raw)
        if self._int_on.get() and self._mic_ok:
            self.listener.start()

    def _do_pause(self):
        if not self._paused:
            self.ctrl.pause(); self.listener.stop()
            self._mic_paused = False
            self.btn_pause.config(text="UNPAUSE")
            self._paused = True
        else:
            self._paused = False; self._mic_paused = False
            self.btn_pause.config(text="PAUSE")
            if self._int_on.get() and self._mic_ok: self.listener.start()
            self.ctrl.unpause()

    def _do_resume(self):
        self._mic_paused = False
        if self._int_on.get() and self._mic_ok: self.listener.start()
        self.ctrl.resume()

    def _do_stop(self):
        self.ctrl.stop(); self.listener.stop()
        self._paused = False; self._mic_paused = False
        self.btn_pause.config(text="PAUSE")

    def _do_clear(self):
        self.ctrl.stop(); self.listener.stop()
        self._paused = False; self._mic_paused = False
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
            self._set_status("ᛗ  Voice detected — TTS paused…")

    def _on_mic_silence(self):
        if self._int_on.get() and self._mic_paused:
            self._mic_paused = False
            self.ctrl.unpause()
            self._set_status("ᚠ  Silence — TTS resuming…")

    def _on_calibrated(self, rms):
        suggested = int(rms * 2.5)
        suggested = max(200, min(suggested, 2800))
        self.after(0, lambda: self._apply_calibration(rms, suggested))

    def _apply_calibration(self, ambient, suggested):
        self._thresh_var.set(suggested)
        self.listener.energy_threshold = suggested
        self._cal_lbl.config(
            text=f"Ambient: {ambient} RMS  →  Threshold set to {suggested}",
            fg=self.GREEN)
        self._preset_var.set("Custom")
        if hasattr(self, '_preset_lbl'): self._preset_lbl.config(text="Custom (calibrated)")
        self._set_status(f"ᛉ Calibrated: ambient={ambient} → threshold={suggested}")

    # ── Preset & slider controls ───────────────────────────────────────────
    def _apply_preset(self, name):
        thresh, sustain, resume, desc = PRESETS[name]
        if thresh is None: return
        self._thresh_var.set(thresh)
        self._sustain_var.set(sustain)
        self._resume_var.set(resume)
        self.listener.energy_threshold = thresh
        self.listener.sustain_ms       = sustain
        self.listener.resume_delay_s   = resume
        self._preset_lbl.config(text=desc)
        for n, b in self._preset_btns.items():
            if n == name:
                b.config(bg=self.GOLD3, fg=self.GOLD2)
            else:
                b.config(bg="#1a1a12", fg=self.DIM)
        self._set_status(f"Preset: {name} — {desc}")

    def _do_calibrate(self):
        self._cal_btn.config(text="Calibrating…", state=tk.DISABLED, fg=self.DIM)
        self._cal_lbl.config(text="Measuring room noise for 1.5 seconds — stay quiet…", fg=self.GOLD)
        self._set_status("ᛉ  Calibrating ambient noise… stay quiet…")
        self.listener.calibrate_ambient(duration_s=1.5, callback=self._on_calibrated)
        self.after(2000, lambda: self._cal_btn.config(
            text="ᛉ  Auto-Calibrate Room", state=tk.NORMAL, fg=self.BLUE))

    def _on_thresh(self, val):
        self.listener.energy_threshold = int(float(val))

    def _on_sustain(self, val):
        self.listener.sustain_ms = int(float(val))

    def _on_resume(self, val):
        self.listener.resume_delay_s = float(val)

    def _on_int_toggle(self):
        if not self._int_on.get():
            self.listener.stop()
            self._mic_paused = False

    # ── Voice controls ─────────────────────────────────────────────────────
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
        self.ctrl.stop(); self.listener.stop()
        if _PG_OK:
            try: pygame.mixer.quit()
            except: pass
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
