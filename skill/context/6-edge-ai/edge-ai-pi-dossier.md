---
title: "Small models on a Raspberry Pi 5"
subtitle: "A dossier for Prayas Abhinav, 7 November 2026"
---

**The question this dossier answers:** how should a Raspberry Pi 5 be set up and used so that Prayas's small models (a frozen encoder with a small trained head, where code decides and the model only returns a number) fit on it, keep up with the world they listen to, stay cool inside a soft toy, and stay honest about what was measured?

It was assembled on 7 November 2026, the day the first Pi 5 (16 GB) was ordered for the Hoja toy, from three things: the research notes gathered the same evening (`research-notes.pdf` beside this file, where every number has its source and its conditions), the first export and timing of AST on the Mac mini, and his direction of the same day: *"I want to go into edge ai heavy with my rpi setup now, my small models direction is aligned to it"*, and *"the constraints for sourav's work are also set by the pi"*.

Hoja is the first project on the Pi: one soft toy that hears its household in 2-second windows and goes darker at gaalis, in two modes. A frozen AST encoder turns each window into 768 numbers; a small scorer trained on clips Prayas has keyed turns those into one of four labels (no gaali, aimed at nobody, aimed at the toy, aimed past it); code decides whether that label darkens the toy. The numbered sections below are the dossier's exhibits.

What it carries: the limits the Pi sets, the choices that follow, and the setup, for listening models first and then for toys and robots (sections 10–14). What it leaves out: the model work itself (the scorer, its keys and labels), the toy's darkening hardware, and anything about [name withheld]'s games beyond the limit the Pi sets on them. The tutorials that teach the setup step by step are a separate document, written from this one.

# The spine

## 1. The budget is one second

![The frozen AST against the one-second hop. Measured numbers only.](assets/budget.svg){width=100%}

**What it is.** The toy hears two-second windows that start one second apart, so each window must be answered in under 1000 ms or the next one is dropped. AST, as it comes from Hugging Face, pads every input to 10.24 s. Measured on a Pi 5 with the Active Cooler, the padded AST took 2,070 ms per window at int8 on four threads, and 9,412 ms at full precision on one thread (syamaner, April 2026, ONNX Runtime). On the Mac mini the same padded model took 256–311 ms on four threads.

**What to do with it.** As AST stands, the Pi cannot keep up: it would answer about one window in two. Every later choice in this dossier exists to bring that bar under the line, and the first and largest one is in section 2. *Keeps up* is measured, not felt: p95 latency under 1000 ms, with `get_throttled` still at `0x0`, over a sustained run inside the closed toy (the length of that run, an hour in this dossier, is a proposal for Prayas to set).

## 2. Trim AST to two seconds

**What it is.** A 10.24 s input becomes 1,212 patches inside AST; a 2 s input would be 228. The cost of attention grows with the square of that number and the rest of the model with the number itself, so a 2-second AST should be more than five times cheaper. Hugging Face has no switch for this: the position embeddings are fixed at 1,212 positions. The original AST code shows the way: keep the middle 19 of the 101 time columns of the stored embeddings and build the model for 198 frames.

**Measured on the Mac, the same evening.** `scripts/export_ast_2s.py` made the trimmed model: 342 MB at full precision and 87 MB at int8, both matching the trimmed PyTorch model (cosine 1.0000 and 0.9955). On the Mac mini it took 65 ms on one thread and 31–41 ms on four, against 256–518 ms for the padded model: about eight times faster, more than the five-times estimate. If the Pi scales the same way, the trimmed int8 model would take about 250 ms there on four threads; that is still arithmetic until the bench runs. The trimmed model's embedding of a clip is not the padded model's: cosine 0.80 between the two for the same 2-second clip. So the scorer has to be trained on embeddings from the trimmed model it will run with, never on padded ones.

**What to do with it.** Bench the padded AST once on the Pi as the reference (section 8), then trim AST to 2 s before any other change, and measure two things: the time (if the five-times estimate holds, about 400 ms at int8 on four threads, which is derived arithmetic, not a measurement) and whether the trimmed encoder still separates the four labels. The checkpoint was fine-tuned on 10-second clips, and nobody has measured what trimming does to its embeddings. That second measurement is model work and rests on his keyed clips.

## 3. The toy is an enclosure, and enclosures are where cooling fails

**What it is.** In open air the Active Cooler holds a fully loaded Pi 5 near 60 °C, and the fan is 35–45 dB. The one actively cooled setup that still throttled in a 30-minute test was the cooler inside a closed case, and its tester called the closed case noisy. Throttling starts at 80 °C and is hard at 85 °C. Nobody has measured a Pi 5 inside fabric and stuffing, or its fan a few centimetres from a microphone.

**What to do with it.** Treat heat and fan noise as part of the model's world, not as a hardware afterthought. The toy needs an air path to the cooler; the model has to be trained with the fan audible at each of its speed steps; and every bench run records start and end temperature and `vcgencmd get_throttled`. A trimmed model (section 2) is also a cooler one, because it works for a fifth of the time. The line to hold is the one the firmware draws: under 80 °C, where throttling begins. If the closed toy crosses it, the choices are a better air path, a smaller encoder (section 6), or answering fewer windows; the last changes how the toy listens and is Prayas's to decide.

## 4. The CPU is the accelerator

**What it is.** The Pi 5's four Cortex-A76 cores have the dot-product int8 instructions, which is what makes int8 faster than full precision on this board. The add-on accelerators do not help these models: the Hailo compiler runs only on an x86 machine with 32 GB of memory, no one has reported compiling AST for it, and other transformers fail at the parsing step; on the AI HAT+ 2 the Pi's own CPU beat the Hailo-10H on language models; Coral's Python library stops at Python 3.9, and Raspberry Pi OS now ships 3.13.

**What to do with it.** Buy no accelerator for now. Run the models on the CPU through ONNX Runtime, the one runtime with a measured AST result on this board, with Python 3.13 wheels for the Pi, and with dynamic int8 for transformer weights without calibration data. Keep ExecuTorch and LiteRT as later comparisons.

## 5. Quantise carefully, and check the answer, not the size

**What it is.** On the Mac, int8 AST came out at 90 MB against 345 MB, with embeddings at cosine 0.9955 to full precision. On the Pi, dynamic int8 cost syamaner 0.54 points of accuracy on his task. For convolutional models on this board, static int8 ran more than four times faster than dynamic int8. Transformer activations are known to quantise badly because of outliers in the residual connections (Bondarenko et al., 2021).

**What to do with it.** Use dynamic int8 for AST, and judge it by whether the scorer gives the same answers on fp32 and int8 embeddings of his own recordings, never by file size or cosine alone. If a convolutional encoder replaces AST (section 6), quantise it statically.

# The setup

## 6. Smaller encoders exist, untimed on a Pi

| Encoder | Parameters | AudioSet mAP | Licence |
|---|---|---|---|
| AST (current) | 86.6 M | 0.459 | BSD-3-Clause |
| EfficientAT mn10 | 4.88 M | 0.471 | MIT |
| EfficientAT mn04 | 0.98 M | 0.432 | MIT |
| CED-Tiny | 5.5 M | 0.481 | GPL-3.0 |

**What to do with it.** EfficientAT's MobileNets were distilled from transformers for exactly this shape of use, one cheap forward pass feeding small heads (Schmid, Koutini and Widmer, EUSIPCO 2023). If the trimmed AST is still too slow or too hot, mn10 is the first replacement to time, with its MIT licence intact for an open release. CED's GPL-3.0 licence would bind the toy's code if it were released. The order of fallbacks: trimmed AST; if it is too slow, too hot, or no longer separates the labels on his keyed clips, EfficientAT mn10; if that fails too, the question goes back to Prayas, since what remains is changing what the toy listens for or how often.

## 7. The Pi itself, as of November 2026

**What it is.** Raspberry Pi OS is now Debian 13 Trixie (images of 6 October 2026, kernel 6.18, Python 3.13). Raspberry Pi Imager 2.0 asks for hostname, a capital city for the locale, the user, the Wi-Fi and the SSH key before writing the card; there is no default `pi` user. `pip` into the system Python is refused, by design, so everything runs in a venv made with `uv`. Swap is compressed memory by default (`/etc/rpi/swap.conf`). The official A2 card reads 5,000 small blocks a second on a Pi 5, which matters for start-up, not for inference, since an always-on program loads its model once. The official 27 W supply matters: on a 3 A supply the same AST run crashed with under-voltage.

**What to do with it.** Flash Raspberry Pi OS Lite 64-bit with the SSH key, never upgrade in place across OS versions, run every program as a systemd service in a venv, keep logs in memory to spare the card, and do not overclock a Pi that lives inside a toy.

## 8. What is already done on the Mac

**What it is.** On 7 November 2026: Raspberry Pi Imager 2.0.12 is installed; `[path withheld]` has a `hoja` entry (hoja.local, user prayas, the Mac's key); the Hoja repository has `toy/export_ast.py` (AST to ONNX at fp32 and int8, checked against PyTorch, timed), `pi/card.txt` (writing the card), `pi/setup.sh` (first boot), and `pi/bench.txt` with `pi/bench_ast.py` (timing on the Pi with temperature and throttling). The ONNX files sit in the repository's `runs/ast-onnx/`, in Dropbox and out of git.

**What to do with it.** When the parts arrive: write the card, fit the cooler, `ssh hoja`, run the setup, run the bench. The first number the Pi gives is the padded AST, which should land near the 2,070 ms in section 1; if it does, the bench agrees with the published measurement and the trimmed model can be timed next.

# Beyond the toy

## 9. The same limit for every small model

**What it is.** The Pi now sets the limit for his other small-model work too, [name withheld]'s craft games included. His reason, in his words of 7 November 2026: *"with all the concurrent computation needs of a game - a pi is a good container environment to simulate how much computation it can access"*. A game running in Unreal takes most of a player's machine for drawing, physics and sound; the model gets what is left, and a Pi 5 is a fixed, cheap stand-in for that remainder. Measured on Pi 5 boards: small language models through llama.cpp at 4-bit generate about 29–34 tokens a second for a 0.5 B model and 4–6 for a 3 B model; a MiniLM sentence encoder at int8 took 501 ms for a 512-token input through ExecuTorch. ungli's models are of the encoder-and-pointer kind, not the language-model kind.

**What to do with it.** Size each model for the Pi first, then let it run wherever else it has to. If it keeps up on the Pi, it will keep up beside a game on a player's PC. A model that fits the Pi's budget also needs no server, sends nothing away and can be counted by nobody, which keeps the not-knowing rule by its shape. For a game, the budget is the time between the player's act and the moment the game needs the model's answer, instead of the toy's one-second hop, and it is measured in the same way.

# Toys and robots

Added the same evening, on his word: *"edge ai includes robotics and toys"*. The facts and their sources are in `research-notes-robotics.pdf` beside this file.

## 10. The model decides; something else holds the waveform

![The three boards and their jobs.](assets/split.svg){width=100%}

**What it is.** Linux on the Pi is not real-time. Under heavy load the stock Pi 5 kernel's worst scheduling delay was 36.8 ms in an hour-long test, against 124 µs with a real-time kernel. That does not matter for a decision (a light or a motor that starts a few tens of milliseconds late), but it matters for a waveform: a servo pulse, a stepper's steps, an LED's bit stream, where one late wake-up is a visible twitch. A logic-analyser study found the Pi 5's software PWM clean at light load and with outliers of 238.7 µs at 75 % CPU load, and Hoja's model will keep the CPU busy. The old fixes are gone: RPi.GPIO and pigpio do not run on a Pi 5; gpiozero on lgpio does, and the GPIO chip is now `gpiochip0`, which breaks older tutorials. The clean routes are the Pi 5's four hardware PWM channels (GPIO 12, 13, 18, 19), its RP1 chip's PIO (four state machines in all), a PCA9685 board, or a Raspberry Pi Pico 2 (₹544, twelve PIO state machines) taking orders from the Pi over USB.

**What to do with it.** Prayas now has three boards (his words, 7 November 2026: *"now I can use all 3 - design with that"*), and each has one job. The **Pi 5** hears, runs the model, and its code decides, sending one number. The **Pico H** (RP2040, eight PIO state machines) is the toy's own board: one job, steadily, inside the toy, such as Hoja's LEDs, its heater with the thermistor read on the Pico's own ADC, or its lining motor. The **Pico 2** (RP2350, twelve) is the bench and robot board: several servos, motors, encoders and sensors, fast local reflexes the Pi only steers, and an outside instrument that times the Pi's own pulses with a clock the Pi's load cannot touch. The Pi 5's own hardware PWM or PIO stays available for a toy too simple to need a Pico. Each Pico answers `who` with its name, so the Pi can tell them apart. Use GPIO 12 and 13 for PWM, which leaves 18 and 19 free for an I2S microphone if one ever replaces the USB one. Plan for the Pi failing: the Pico should switch every actuator off if it hears nothing from the Pi for a set time, and a heater's switching transistor needs a pull-down so the heater stays off while the Pi boots or after its program dies. The length of that silence is a design choice for each toy.

## 11. LEDs and power

**What it is.** The WS2812B LEDs considered for Hoja have only young drivers on a Pi 5: `rpi_ws281x` is experimental there, and the working routes are the SPI method or Adafruit's PIO-based library, still a release candidate. The Pi's 3.3 V data line is not guaranteed to be read by every WS2812B, so a level shifter belongs on the line. One LED at full white drew 33.5–52.5 mA depending on the maker, and about 0.4–1 mA when dark; a 16-LED ring at full white is therefore 0.54–0.84 A at 5 V (derived). Every source puts motors and large LED loads on their own supply with the grounds joined; a shared rail shows on the Pi as under-voltage in `get_throttled`. No measured runtime of a Pi 5 on a power bank with the load stated was found.

**What to do with it.** Power the Pi from its own 5 V 5 A supply or bank, and the LEDs, motor or pump from a second rail with a common ground. Budget the LEDs by their brightest resting state, not their darkest. Measure the battery life on the bench with the model running; the notes' figures for a 10,000 mAh bank are arithmetic: about 6 hours at 5 W and about 4 hours at 8 W, and a Pi 5 under full load draws 8.9–9.8 W.

## 12. What a toy owes the people around it

**What it is.** Every documented failure of a connected toy needed voices or data to leave the toy: CloudPets left 2.2 million children's voice recordings in an open cloud store; Germany banned the Cayla doll in 2017 because its Bluetooth let strangers listen; a 2024 study found an AI toy streaming continuously to its servers while switched on. A toy whose model runs on its own Pi, which keeps no recording and has its radios off, has none of those paths, but the Pi 5 has Wi-Fi and Bluetooth on board, so that holds only if it is set up and checked that way (`rfkill list`, and what the program writes to the card). Two Indian rules attach to a toy and to children's data. The Toys (Quality Control) Order requires a BIS licence and the ISI mark for products intended for play by children under 14, in force from 1 January 2021; an electric toy is tested to IS 15644, whose heating-and-abnormal-operation clause a licensed maker must test in-house, which bears on the heater method. Section 9 of the Digital Personal Data Protection Act, 2023 forbids tracking or behavioural monitoring of anyone under 18, with the rules for children's data due to apply around May 2027 (derived). Whether a prototype, an artwork or an on-device classifier that keeps nothing falls under either is not settled by the texts.

**What to do with it.** Build every toy so that nothing leaves it, check that on the finished object, and say so only after the check. Before Hoja is given, lent, shown to children or sold, the question of the Order and the Act goes to a lawyer or to BIS; that decision is Prayas's.

## 13. Robot software and the vision range

**What it is.** ROS 2 does not install natively on Raspberry Pi OS: the supported routes are Ubuntu on the Pi or ROS 2 in Docker on Raspberry Pi OS. At toy scale its machinery (many processes passing messages, standard drivers, simulation) buys nothing; one Python process, with a serial line to a Pico where needed, does the same job. For vision, the Pi 5's CPU ran YOLO26n, the smallest current YOLO model, in 67 ms per 640 × 640 image at full precision through NCNN, about 15 images a second (Ultralytics' own benchmark), and a whole camera pipeline in another study reached 6.6–7.5 frames a second; the AI Camera runs its detector on the sensor at 30 frames a second; a Hailo-8L board reached 41–82 frames a second on YOLOv8s.

**What to do with it.** Use plain Python for toys; leave ROS 2 for robots that need its drivers, and then run it in Docker so the Pi keeps its own GPIO and camera support. For vision, the AI Camera is the first thing to try when a model has to see, since it leaves the Pi's CPU free for the rest; this is the one place where an accelerator earns its place, unlike for AST.

## 14. A first bench of parts

| Part | For | Price (7 Nov 2026) | Shop |
|---|---|---|---|
| WS2812B 16-LED ring | LEDs that darken | ₹87 | robu |
| Bidirectional level converter | the LEDs' 5 V data line | ₹20 | robocraze |
| DRV8833 motor driver | lining motor or ink pump | ₹72 | robu, robocraze |
| MG90S servo | timing tests, small robots | ₹159 | robocraze |
| Raspberry Pi Pico 2 (with headers) | the bench and robot board | ₹609 | robu, bought 7 Nov 2026 |
| Raspberry Pi Pico H (with headers) | the toy's own board | ₹467 | robu, bought 7 Nov 2026 |
| MPR121 capacitive touch | touch through fabric | ₹144 | robocraze |
| ADS1115 ADC | reading the thermistor | ₹145 | robocraze |
| 10k NTC thermistor | heat pigment's temperature | ₹6 | robocraze |
| 10 kΩ fixed resistor | the thermistor's divider | not looked up | |
| VL53L1X distance | how near someone is | ₹880 | robocraze |

**What to do with it.** Both Picos are bought (₹467 and ₹609, each with ₹149 Bluedart Air). The rest, one of each, comes to ₹1,513 before delivery, from two shops, with the resistor unpriced; the notes' total of ₹2,404 was for a slightly larger list that also had a Pico 2 (both servos, a second motor driver, a second level converter). Jumper wires, a breadboard and a second 5 V supply come on top. The robu prices were read from its old mirror and may lag the live site. Buying them is his.

# Recommendation

1. **Bench the padded AST once as the reference, then trim AST to 2 seconds** before any other change (sections 2, 8).
2. **Run on the CPU with ONNX Runtime and dynamic int8**; buy no accelerator until a measurement says the CPU cannot do it (sections 4, 5).
3. **Make the bench the source of every number**, and judge *keeps up* as p95 under 1000 ms with no throttling over a sustained run: p50 and p95 over hundreds of runs, start and end temperature, `get_throttled`, at 1, 2 and 4 threads, recorded with the date and the model file.
4. **Design the toy around heat and the fan**: an air path to the cooler, the fan recorded at each speed step through the toy's own microphone, and the scorer trained with it audible (section 3).
5. **Judge int8 by the scorer's answers on his own keyed recordings**, not by size or cosine (section 5).
6. **Time EfficientAT mn10 next to the trimmed AST** on the same clips, so the choice of encoder rests on two measurements (section 6).
7. **Hold every new small model, [name withheld]'s included, to the Pi's budget from its first day** (section 9).
8. **Let the Pi decide and something else keep time**: the Pico H for the toy's one job, the Pico 2 for robots and for measuring, each named and each switching off when the Pi goes silent (section 10).
9. **Give motors and LEDs their own power rail**, grounds joined, and measure battery life with the model running (section 11).
10. **Build every toy so nothing leaves it, check that on the finished object**, and take the BIS and DPDP question to a lawyer or BIS before any toy goes to children or is sold (section 12).
11. **Plain Python for toys, ROS 2 in Docker for robots, the AI Camera first for vision** (section 13).

The lead choices are 1, 2 and 3; the rest follow from what the bench shows.

# Sources

Every figure above is sourced and conditioned in `research-notes.pdf`, beside this file. The ones this dossier leans on most: syamaner, "Edge deployment of an 86M-parameter audio transformer" (dev.to, April 2026) for AST on the Pi 5; Raspberry Pi, "Heating and cooling Raspberry Pi 5" and the frequency-management documentation for heat; Martin Rowan, "Official Raspberry Pi 5 case" (January 2024) for the closed case; Jeff Geerling, "Raspberry Pi AI HAT+ 2" (2026) for the Hailo-10H; Gong, Chung and Glass, "AST: Audio Spectrogram Transformer" (Interspeech 2021) and the AST repository for the patch arithmetic; Schmid, Koutini and Widmer, "Low-Complexity Audio Embedding Extractors" (EUSIPCO 2023) and the EfficientAT repository; Bondarenko, Nagel and Blankevoort, "Understanding and Overcoming the Challenges of Efficient Transformer Quantization" (EMNLP 2021). The papers' verification is provisional: two of the three checking tools were broken on 7 November 2026, and the notes say which step each paper passed.
