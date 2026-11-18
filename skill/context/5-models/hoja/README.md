# Hoja: a rig

*Started 7 November 2026 on Prayas's word ("start prototyping the project - build a rig first, make 3d realistic, soft toy with the darkening mechanism, make it in 3js, only tht model work should be left"); a Koher project on his word the same day ("this is a koher project"). The names are fixed on his word (7 November 2026, "a is fixed"): **Hoja Kaala** (become black) and **Hoja Maila** (become soiled), in the form of MoVD's *Hoja Asli*. They were two sibling toys until the evening, when he made it one toy with two modes ("make it one toy with two modes") and chose that the name follows the mode, on the body that had been Hoja Kaala's; Chot Lagi and Nazar Lagi, final at 15:29, were replaced when he asked for names like Hoja Asli (`name-family.md`). The folder keeps its working name. The spec and the tasks are in the two emails to [name withheld], `[path withheld]` (4 Nov) and `prerit-gaali-toy-character/` (7 Nov).*

One soft toy with two modes (his word, 7 November 2026, about 19:30: "make it one toy with two modes"), named by the mode: as **Hoja Kaala**, in target mode, it darkens at gaalis aimed at it; as **Hoja Maila**, in bystander mode, at gaalis it overhears, aimed at someone else. It has a Raspberry Pi 5, a microphone and a model. A sound model (AST, frozen, with a small scorer trained on clips Prayas labels) answers with one number per two seconds, and code decides whether that number darkens the toy. Switching the mode keeps the darkness the toy already has. Earlier the same day it was two toys for two people in one household ("it is two toy tandem - family"); that version is in the git history up to commit 13dee90.

## What is here

- `toy/brain.py` is the code meant for the Raspberry Pi. It listens in 2-second windows that overlap by a second, skips quiet windows, asks the model, applies the rule (which answers darken in which mode, how much each time, whether it lightens by itself) and drives the body. A window that overlaps the one that counted cannot count again. Windows that go by while the model is busy are counted as dropped.
- `toy/model.py` is **the one part left**. `score(clip, sample_rate)` answers `None` (don't know) until the model is written. `LABELS` is a proposal for the two modes: 0 no gaali, 1 aimed at nobody, 2 aimed at the toy, 3 aimed past it.
- `toy/body_sim.py` is the body, simulated, for each of the five ways of darkening:
  - LEDs inside;
  - heat-sensitive pigment, with a heater, a thermistor and a 40°C cut-off;
  - UV-sensitive pigment;
  - a lining pulled up by a motor;
  - an ink pump with a 10 ml reservoir.

  Every number in it is an estimate with a name, to be replaced by a measured one. On the Pi, this file gives way to the driver for the method chosen from the swatches (task 8).
- `MODEL-SPEC.md` says how to model the toy so the rig uses the model in place of its drawn shape; `rig/templates/hoja-template.glb` is the drawn shape to start from, and `rig/models/hoja.glb` is loaded on the next page load.
- `rig/` is the toy in three.js: an odd, lumpy, mismatched crocheted body drawn in code (his words: "make odd looking toys", "not generic geometric"), with the mode and the name it carries chosen in the panel; darkening spreads in 3D, so a modelled shape darkens the same way, lit in a room, darkening as the brain reports. Click to squeeze it; *Show inside* shows the Pi, the power bank, the microphone and the parts for the chosen method at real size. three.js 0.165 is kept in `rig/vendor/`, so it runs offline.

## Running it

See `run.txt`. Without `--mic`, the rig's four buttons stand in for the model.

## What the rig has already shown

- The computer is a Raspberry Pi 5 (his word, 7 November 2026, in place of the Pi 4 in the emails to [name withheld]). For the bench (task 4), ordered from ElectroPi on 7 November 2026 (confirmed that evening, ₹37,398.80 with GST): a Pi 5 with 16 GB, the official 27 W USB-C supply (5.1 V 5 A), the official Active Cooler, a USB-C microSD reader for the Mac mini, and a USB desktop microphone on a 90 cm cable, so its head can sit at the fabric while the Pi sits in the belly. The microSD card, ElectroPi having none rated A2, was ordered from Robu the same evening: the official Raspberry Pi 128 GB A2, blank (₹5,148 with Bluedart Air), to be written with Raspberry Pi Imager from the Mac. A Pi 5 in a vented case and a 10,000 mAh power bank fill the belly at real size, so the toy is about 30 cm tall.
- At 7 W for the Pi 5 with its fan (an estimate), the power bank lasts about 5 hours; the LEDs at full take that to about 4.
- Inside stuffing, a Pi 5 running the model all the time needs its active cooler, and the fan is a sound the microphone will hear; the model has to be trained with it running.
- A Pi 5 wants 5 V at 5 A over USB-C; at 3 A it runs, with its USB ports limited, so the power bank has to say 5 V 5 A.
- Heat pigment cannot go dark in a room above about 31°C without cooling, and sun warms it pale.
- Sunlight darkens UV pigment by itself: at a third of full sun, it was 90% dark with the toy asking for half.
- Ink cannot be taken back. The toy has to be cleaned and refilled to lighten it.
- A quiet room is not silent to a microphone. The Mac's webcam microphone (Brio 100) read a silent room at about −30 dB: most of it drift below 100 Hz, the rest a machine hum in harmonics about 70 Hz apart, much of it added after the gain stage. So the brain measures loudness above 100 Hz only and sends a window to the models only 6 dB above the room's own floor (the quietest fifth of the last 30 windows), never against a fixed level. With the input gain at 27% the Mac's own speech did not rise above that noise; at 100% it rose about 11 dB. The Pi 5's fan will be the same problem inside the toy.
