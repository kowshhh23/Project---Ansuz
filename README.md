**### Project Ansuz v2.0: The Rune of the Spoken Word:

_Project Ansuz is a specialized Windows desktop Text-to-Speech (TTS) solution engineered to overcome the challenges of high-noise environments. Developed for use in lecture halls, classrooms, and busy laboratories, it addresses the limitations of traditional robotic readers by offering human-like cadence and smart environmental adaptation.

The application utilizes Microsoft Edge Neural voices to deliver high-fidelity audio without the need for API keys, subscriptions, or length restrictions. Its core innovation is a microphone-based interruption system that automatically pauses playback when ambient noise—such as a student speaking or a loud announcement—is detected, resuming seamlessly once the environment settles._

Technical Updates in v2.0:
Neural Voice Engine

The voice engine has been reconstructed to prioritize conversational realism over flat document reading:

High-Expressivity Models: Transitioned to AndrewMultilingualNeural and AvaMultilingualNeural as primary defaults for superior warmth and natural cadence.

SSML Prosody Integration: Implemented mstts:express-as with a "chat" style and a 1.4 style degree to ensure a natural, engaging register.

Rhythmic Micro-Pauses: Integrated automatic 120ms breaks at punctuation marks to mimic human breathing patterns.

Intelligent Fallback: Added a silent retry mechanism that reverts to plain text if a specific voice does not support SSML.

Latency and Performance

The interruption logic has been optimized for near-instantaneous response times:

Thread Optimization: Reduced thread join timeouts from 1.5 seconds to 0.3 seconds.

High-Frequency Polling: Increased polling rates for Pygame (10ms) and the OS player (15ms) to ensure the system reacts immediately to external noise.

Nordic Visual Identity

The interface has undergone a complete professional overhaul, maintaining a "Black and Gold" aesthetic inspired by Elder Futhark runes:

Structural Refinement: Increased the topbar height to 80px and introduced gold accent striping with rune-themed decorations.

Engraved Architecture: Implemented dark engraved blocks for section headers and double-border frames for the main text area.

Status Monitoring: Integrated color-coded dependency indicators and a refined status bar for real-time engine feedback.

Enhanced Environmental Presets

Five distinct noise profiles allow for precise control over the interruption threshold:

Quiet/Normal: Optimized for offices and standard workspaces.

Noisy/Presentation Hall: Configured for high-occupancy areas with PA systems and significant ambient crowds.

Manual Calibration: Users can fine-tune RMS thresholds, sustain durations, and resume delays via dedicated sliders.**
