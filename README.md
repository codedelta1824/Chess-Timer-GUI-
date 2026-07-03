# Pro Chess Timer

---

## About this Project & Objectives
**Pro Chess Timer** is a desktop application built in Python using the `tkinter` graphical user interface framework. It provides a dual-clock system optimized for competitive chess matches, mimicking professional digital chess clocks. 

### Core Objectives:
* **Precision Tracking:** Deliver accurate, high-performance timekeeping using microsecond-level precision (`time.perf_counter`).
* **Intuitive Controls:** Allow rapid side-switching by clicking anywhere inside the respective player's half of the screen.
* **Visual Feedback:** Feature dynamic text scaling, visual cues for low-time thresholds, and orientation management for head-to-head match setups.

---

## Core Idea
The application divides a single window into two distinct, interactive clock zones (White and Black). The Black player's interface is inverted by $180^\circ$ to facilitate face-to-face play on a single laptop or tablet screen placed alongside a physical chess board. When the active player finishes their turn, clicking their side of the screen increments their time (if an increment is configured), stops their clock, and instantly activates the opponent's countdown. 

---

## Folder Structure
```text
Pro-Chess-Timer/
├── README.md
├── Python Chess Timer.py
└── click.wav

File Types & Formatting
File Types
.py (Python Script): Contains the primary logic, UI elements, and event bindings for the application.

.md (Markdown): Formats the documentation, architecture breakdowns, and setup guides.

.wav (Waveform Audio File): Uncompressed, low-latency audio file containing the sound effect played when a player ends their turn.

File Formatting
Encoding: All files are encoded in standard UTF-8.

Line Endings: Configured to use standard Unix (LF) or Windows (CRLF) line endings.

Audio Constraints: The click.wav asset must remain in the same root directory as the main script to ensure dynamic runtime resolution.

Code Structure
The application follows a clean, single-class Object-Oriented Programming (OOP) architecture implemented via ChessTimerApp.

Major Architectural Modules:Initialization (__init__): Declares variables, allocates system assets, creates the high-performance drawing canvas, and binds keyboard inputs (Space for Pause/Start, R for Reset).Window Management (layout): Tracks screen resize actions (<Configure>) to calculate bounding coordinates dynamically, keeping the screen split perfectly at $50\%$ width and height.Game Engine (update_clock): Runs on a high-frequency $10\text{ms}$ recursive loop (root.after(10, ...)), computing true delta time against high-resolution system timestamps.Asset Management (play_click & play_beep): Dynamically inspects the host Operating System (platform.system()). On Windows systems, it leverages the native winsound binary interface to thread low-latency asynchronous audio playback (SND_ASYNC). On non-Windows setups, it safely falls back to standard system alerts.

Code Formatting
Style Guide: Adheres to Python standard PEP 8 naming conventions (e.g., snake_case for methods and variables, PascalCase for classes).

Indentation: Enforces 4 spaces per indentation level.

Interface Separation: Completely separates visual rendering (tk.Canvas) from timing math calculations, ensuring UI refreshes do not block time calculations.

Data Types Used in Code
The application utilizes a robust set of native and structured data types to manage state:

Integer (int): Tracks move counters (white_moves, black_moves) and time parameters measured in hundredths of a second.

Float (float): Captures high-precision system time data via time.perf_counter().

Boolean (bool): Evaluates whether the application loop is processing active data (running).

String (str): Manages text formatting states, user dialog windows, and structural identification labels (active = "white" or "black").

Object reference: Retains instances of Tkinter layout handles (tk.Canvas, tk.Frame, text elements).

Click Sound
The repository includes an explicit system dependency on click.wav.

Execution Behavior: When a player taps their screen segment, the application resolves the local path structure using os.path.abspath(__file__) to find the audio file.

Performance Mitigation: The audio file is executed natively on a separate background thread via winsound.SND_ASYNC. This guarantees that audio playback never hangs the UI thread or delays the opponent's clock from starting immediately.

Code OutputThe program opens a modern, responsive GUI window ($500 \times 850$ pixels default) built with a minimal dark-themed aesthetic.Visual Elements:Active Clock Indication: The active player's background changes to a professional steel blue color (#2c3e50).Time Formatting: Clocks display time in standard minutes, seconds, and hundredths of a second format (MM:SS.hs).Warning Thresholds: Text color switches from white to warning red (#ba2525) when a player's remaining time drops below 60 seconds.Game Over Dialogs: When either clock reaches zero, a native pop-up window blocks input, halts the engine, and declares the winner explicitly.
