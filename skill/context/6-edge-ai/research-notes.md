# Small models on a Raspberry Pi 5: research notes

Gathered 7 November 2026, 19:36 onwards (IST), for the soft-toy project: a Pi 5 16 GB that hears speech in 2-second windows, runs AST (`MIT/ast-finetuned-audioset-10-10-0.4593`) frozen, and passes its output to a small scorer that returns one of four labels. These notes are the research layer only. Every number carries its source and the conditions it was measured under. Where a figure is my own arithmetic rather than a measurement, it says "derived". Where I looked and found nothing, it says "not found". Prices and software versions date quickly; each carries the date it was read or published.

A note on sources: community benchmarks are reported as what their authors measured, not as settled. One page I read (fuzzypoint.uk, "Benchmarking LLMs on Raspberry Pi 5 + AI HAT+ 2", <https://fuzzypoint.uk/benchmarking-small-scale-llm-inference-on-raspberry-pi-5-for>) describes the Pi 5 as having "LPDDR5" and runs ONNX on the AI HAT+ 2 "NPU" through an execution provider that Raspberry Pi's own documentation does not describe; the Pi 5 uses LPDDR4X (<https://www.raspberrypi.com/products/raspberry-pi-5/>). I have left its numbers out.

## 1. The Pi 5 as an AI machine

### CPU

The Pi 5 uses the Broadcom BCM2712: four Arm Cortex-A76 cores at up to 2.4 GHz, 64 KB L1 instruction and data caches, 512 KB L2 per core, 2 MB shared L3, built on 16 nm (<https://www.raspberrypi.com/documentation/computers/processors.html>). Production is promised until at least January 2036 (product brief, published April 2026, <https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008348-DS-6-raspberry-pi-5-product-brief.pdf>).

The instruction set matters for int8 inference. Arm's technical reference manual lists the Cortex-A76 as Armv8-A with the v8.1 and v8.2 extensions, the Cryptographic Extension, and the `SDOT`/`UDOT` dot-product instructions introduced in Armv8.4 (<https://support.arm.com/documentation/100798/0401/Introduction-to-the-Cortex-A76-core/Supported-standards-and-specifications>). The same manual does not list the int8 matrix-multiply extension (FEAT_I8MM), which Arm makes mandatory only from Armv8.6 (<https://support.arm.com/documentation/ddi0487/md/-Part-A-Arm-Architecture-Introduction-and-Overview/-Chapter-A2-A-profile-Architecture-Extensions/-A2-2-Armv8-A-architecture-extensions/-A2-2-3-The-Armv8-2-architecture-extension>). So the Pi 5 has NEON and dot-product int8 instructions but no `SMMLA`/`USDOT`, no SVE and no BF16 (absence inferred from the A76 TRM's list; confirm on the board with `grep -o -E 'asimddp|i8mm|bf16|sve' /proc/cpuinfo | sort -u`). FP16 arithmetic is part of Armv8.2 and optional there (same Arm reference); whether a given runtime uses it on the A76 is not established here.

Why the dot-product instruction matters: a 2026 measurement study held one ONNX model and its quantisation scales fixed across seven hardware classes and found that the sign of the int8 speed-up was set by the CPU's dot-product ISA: cores with Arm dotprod/SDOT or x86 VNNI sped up by up to 2.1×, cores without it slowed down by up to 1.7× (Shin, "Is INT8 Portable?", arXiv 2026, <https://arxiv.org/abs/2609.16085>; preprint, see §6). A Japanese practitioner's ONNX Runtime 1.25.1 test of MobileNetV2 shows the same shape: static per-channel int8 ran 2.4× faster than fp32 on a Pi 5 (A76, with `sdot`) and 2.2× faster on a Pi 4 (A72, without) (<https://zenn.dev/ux_xu/articles/ort-int8-ptq-cnn>).

### Memory

32-bit LPDDR4X interface, "up to 17 GB/s of memory bandwidth" (official processor documentation, <https://www.raspberrypi.com/documentation/computers/processors.html>; same figure in <https://threedots.ovh/blog/2023/09/gathering-some-raspberry-pi-5-details/>). A measured STREAM-style bandwidth figure for the Pi 5: not found in this pass. Jeff Geerling reports that NUMA emulation, added in 2024, speeds up the Pi 5 (<https://www.jeffgeerling.com/blog/2024/numa-emulation-speeds-pi-5-and-other-improvements/>); I did not record the size of the effect.

For AST the memory picture is simple. The fp32 ONNX export is 345 MB and the dynamic-int8 export 89.9 MB (syamaner, measured on his export of a fine-tuned AST, <https://dev.to/syamaner/part-4-edge-deployment-of-an-86m-parameter-audio-transformer-1821>). Both fit many times over in 16 GB.

### Thermals and throttling

Official thresholds: the firmware limit is 85 °C on all models. Between 80 °C and 85 °C the Arm cores are progressively throttled; at 85 °C both Arm cores and GPU are throttled (<https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc>). A forum reply explains the soft region as a linear cut of 100 MHz per degree from 80 °C to 85 °C, after which the idle frequency is forced (<https://forums.raspberrypi.com/viewtopic.php?t=368073>; posted by a forum user, not an official document). Martin Rowan, running 30-minute all-core stressberry tests on Raspberry Pi OS 2023-12-05, saw the clock drop from 2400 MHz to 1500 MHz at 85 °C and to 1000 MHz at 90 °C (<https://www.martinrowan.co.uk/2024/01/official-raspberry-pi-5-case/>). The 90 °C observation sits awkwardly with the documented 85 °C ceiling; both are recorded here as found.

Without cooling: in Raspberry Pi's own lab test with `stress --cpu 4`, the bare board idled around 65 °C and under sustained load sat just above 85 °C with sustained throttling (<https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/>). Jeff Geerling found throttling began in under 30 seconds with no fan and no heatsink, and a small heatsink alone held it off for 5 minutes (launch video transcript, 28 September 2023, <https://www.youtube.com/watch?v=nBtOEmUqASQ>). A May 2025 test (sysbench plus 5 minutes of `stress-ng` on 4 threads) ended at 84.5 °C with `throttled=0xe0008` passively and 54.9 °C with no throttling on the Active Cooler, and the cooled run completed 218,499 bogo-ops against 176,667 (<https://medium.com/@mahinshanazeer/raspberry-pi-5-thermal-showdown-active-cooler-vs-passive-cooling-796d5f68b8fb>).

With the Active Cooler in open air: idle about 45 °C; under extended load the fan ran at low speed and held 60 °C, peaking at 62–63 °C; the fan never needed full speed (Raspberry Pi lab test, <https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/>). With the cooler's fan unplugged (heatsink only), throttling arrived about 200 seconds into the load (same source).

Fan curve: Raspberry Pi's blog says the fan turns on at 60 °C, steps up at 67.5 °C and goes to full speed at 75 °C (<https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/>). A reseller wiki gives a finer curve: off below 50 °C, 30 % at 50 °C, 50 % at 60 °C, 70 % at 67.5 °C, 100 % at 75 °C, with 5 °C hysteresis on the way down (52Pi, <https://wiki.52pi.com/index.php?title=ER-0056>). The two disagree on where the fan starts (50 °C or 60 °C); the official documentation page carries the current default mapping (<https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc>) and is the one to read on the day. The same page notes that the fan connector draws from the same current limit as the USB peripherals. Active Cooler specification: 8000 RPM ±15 % maximum, 1.09 CFM maximum airflow, PWM with tachometer (<https://www.raspberrypi.com/products/active-cooler/>).

Enclosures change everything, and a soft toy is an enclosure. Martin Rowan found that the only actively cooled configuration that still throttled (to 1500 MHz) was the Active Cooler inside the official case with its lid on, because the blower exhausts sideways towards the unvented back of the case (<https://www.martinrowan.co.uk/2024/01/official-raspberry-pi-5-case/>). Digitec's tester reported the same combination "hisses with an annoying noise level as soon as you close the housing cover" (<https://www.digitec.ch/en/page/raspberry-pi-5-is-the-active-cooler-or-the-housing-with-fan-worth-it-31545>). Sustained temperature inside fabric and stuffing: not found.

### Fan noise

Raspberry Pi measured 35–40 dB while the fan ran during its load test; distance from the board not stated (<https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/>). Jeff Geerling said it "maxed out around 40 decibels [well, 45ish]" during benchmarks and only reached 100 % when overclocking; distance not stated (<https://www.youtube.com/watch?v=nBtOEmUqASQ>). A forum user in a silent room at 22 °C ambient, 70 cm away, describes the low-load fan as quiet and a louder step at 67.5 °C, and warns of a "pumping" noise when the fan hunts between two speeds (<https://forums.raspberrypi.com/viewtopic.php?t=367374>). Noise at a microphone a few centimetres away inside a toy: not found.

### Power draw

Jeff Geerling, measured at the wall: idle 2.8 W; `stress-ng --matrix 0` 9.7 W; Geekbench multicore 7.9 W; HPL 13.8 W (sbc-reviews issue for the Pi 5, <https://github.com/geerlingguy/sbc-reviews/issues/21>). In a later comparison with identical tests: idle 2.4 W (2 GB, D0 stepping) against 3.3 W (4 GB C1) and 3.2 W (8 GB C1); `stress-ng` 8.9 W against 9.8 W and 9.8 W (<https://www.jeffgeerling.com/blog/2024/new-2gb-pi-5-has-33-smaller-die-30-idle-power-savings/>). The 16 GB board's idle and load draw: not found. Geerling's early 1.8 W idle used the official 5 A supply and a Kill-A-Watt; with a Radxa supply he saw up to 3 W idle, and a cheap inline USB-C meter read 2–3 W while the Kill-A-Watt read 1.8–2 W (<https://www.jeffgeerling.com/blog/2023/answering-some-questions-about-raspberry-pi-5/>). That last point is the caution for USB-C meters: cheap ones disagree with wall meters by around a watt at idle. Geerling also notes the SoC is allowed about 10 W (<https://www.jeffgeerling.com/blog/2026/raspberry-pi-ai-hat-2/>). When shut down, a Pi 5 still draws 1.2–1.6 W unless the EEPROM is set to power the SoC off on halt (<https://www.jeffgeerling.com/blog/2023/reducing-raspberry-pi-5s-power-consumption-140x/>).

The supply matters for inference specifically. syamaner's AST run on a Pi 5 crashed at 2 threads on an Apple 96 W charger, which negotiates 5 V at 3 A; `vcgencmd get_throttled` returned `0x50000` (under-voltage has occurred, throttling has occurred), and the fix was a 27 W supply plus active cooling (<https://dev.to/syamaner/part-4-edge-deployment-of-an-86m-parameter-audio-transformer-1821>; the PR notes the same, <https://github.com/syamaner/coffee-first-crack-detection/pull/23>). Raspberry Pi's white paper: the Pi 5 only requests 5 V PDOs; with a 5 V 5 A supply the USB ports get 1.6 A, otherwise 600 mA, and USB boot is disabled; `PSU_MAX_CURRENT` in the EEPROM or `usb_max_current_enable=1` in `config.txt` override this (<https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf>). The official 27 W supply delivers 5.1 V at 5 A (robu.in listing of the official part, <https://oldwp.robu.in/product-tag/raspberry-pi-5/>).

### Storage

microSD: the Pi 5 supports SDR104 (product brief, above). Geerling read 90 MB/s on a SanDisk Extreme card against 46 MB/s on a Pi 4 (launch video, above). The official Raspberry Pi A2 cards (the ones on order) are specified at 5,000 random 4 KB read IOPS and 2,000 write IOPS on a Pi 5, against 3,200 and 1,200 on a Pi 4 (<https://www.raspberrypi.com/products/sd-cards/>; product brief <https://pip-assets.raspberrypi.com/categories/1270-sd-card/documents/RP-008381-DS-1-sd-card-product-brief.pdf>). Those figures depend on command queueing, which is Pi 5 only (<https://www.raspberrypi.com/news/sd-cards-and-bumper/>). Command queueing first needed `dtparam=sd_cqe` in `config.txt` (<https://github.com/raspberrypi/linux/pull/6046>); a forum note dated 10 January 2025 says CQ is now restricted by default to known-good card implementations (<https://forums.raspberrypi.com/viewtopic.php?t=367459>). The kernel limits posted writes in CQ mode to one, to keep power-loss behaviour sane, at a 2–3 % cost in sequential write (<https://www.raspberrypi.com/news/sd-cards-and-bumper/>). Check on first boot with `dmesg | grep -i "command queue"`.

NVMe: the M.2 HAT+ is PCIe 2.0 ×1, "up to 450 Mbytes/s" (robu.in listing of the official part, <https://oldwp.robu.in/product-tag/raspberry-pi-5/>). Geerling measured 450 MB/s at Gen 2 and 900 MB/s with the uncertified Gen 3 setting (launch video, above).

Why it matters for model loading (derived, not measured): reading the 345 MB fp32 AST file at the ~80–90 MB/s microSD figure takes about 4 seconds, the 89.9 MB int8 file about 1 second; at 450 MB/s NVMe, under a second for either. After the first read the file sits in the page cache, and an always-on service loads it once at start. For this project storage speed affects boot-to-ready time and SD wear more than inference speed. One community llama.cpp report notes swapping from RAM to a microSD made a 1.6 GB-oversized model unusably slow (<https://anil.recoil.org/ideas/embedded-whisper>), which is a 4 GB-board problem and does not arise at 16 GB.

## 2. Accelerators

| Device | Chip / rating | Memory | What it is built for | List price (USD) |
| --- | --- | --- | --- | --- |
| AI HAT+ 13 TOPS | Hailo-8L, INT8 | uses Pi RAM | vision post-processing | from $70 (<https://www.raspberrypi.com/products/ai-hat/>) |
| AI HAT+ 26 TOPS | Hailo-8, INT8 | uses Pi RAM | vision, several models at once | $110 at launch (<https://www.phoronix.com/news/Raspberry-Pi-AI-HAT-2>) |
| AI HAT+ 2 | Hailo-10H, 40 TOPS INT4 | 8 GB LPDDR4X on board | LLMs and VLMs up to about 6 B parameters, plus vision | $130 at launch 15 January 2026; $200 on the product page and brief now |
| AI Camera | Sony IMX500 | 8,388,480 bytes for firmware, weights and working memory | on-sensor vision | $70 |
| Coral USB Accelerator | Edge TPU | n/a | quantised TFLite vision | rating and price not checked in this pass |

Sources for the AI HAT+ 2 row: Raspberry Pi announcement (<https://www.raspberrypi.com/news/introducing-the-raspberry-pi-ai-hat-plus-2-generative-ai-on-raspberry-pi-5/>), product page "Available now for $200" (<https://www.raspberrypi.com/products/ai-hat-plus-2/>), product brief "List price $200" (<https://pip-assets.raspberrypi.com/categories/1319-raspberry-pi-ai-hat-2/documents/RP-009655-MM-6-raspberry-pi-ai-hat-plus-2-product-brief.pdf>), launch price $130 (<https://www.jeffgeerling.com/blog/2026/raspberry-pi-ai-hat-2/>), and the ~6 B parameter ceiling from the documentation (<https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html>). The Pi 5 16 GB itself was $120 at launch in January 2025 (<https://www.nodebench.com/articles/raspberry-pi-5-16gb-launched>) and is listed at $305 in the product brief published April 2026 (brief, above). Both price rises are recorded as found; the cause is not stated in these sources.

### AI HAT+ (Hailo-8L / Hailo-8)

It connects over PCIe Gen 3 and is auto-detected; `rpicam-apps` and Picamera2 offload object detection, segmentation and pose estimation to it (<https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html>; <https://www.sparkfun.com/raspberry-pi-ai-hat-13-tops.html>). The AI Kit (Hailo-8L on an M.2 board) is out of production (same documentation). Ambient operating range 0–50 °C (product page, above), lower than the Pi's own 0–70 °C.

Toolchain: models are converted to Hailo's HEF format with the Hailo Dataflow Compiler (parse, optimise/quantise with calibration data, compile), and run on the Pi through HailoRT (<https://developer.ridgerun.com/wiki/index.php/Hailo/Hailo-8/AI_Software_and_Tools/Hailo_Dataflow_Compiler>). The compiler runs only on x86 Linux; Hailo staff say it needs 32 GB of RAM (<https://community.hailo.ai/t/availability-of-data-flow-compiler-on-raspberry-pi-and-python-3-11/899>), and the AI Software Suite Docker needs Ubuntu 22.04 or 24.04 and "a good NVIDIA GPU for some optimizations" (<https://community.hailo.ai/t/hailo-rpi5-image-v3-27-0-bookworm-arm64-zip/17856>). Model Zoo v2.x with DFC v3.x serves Hailo-8/8L; the Model Zoo `master` branch is for Hailo-10 and Hailo-15 only (<https://github.com/hailo-ai/hailo_model_zoo>).

Audio and transformers on Hailo: a Hailo staff answer says audio classifiers can be compiled if they are ONNX/TF/TFLite, use supported operators, have static input shapes and quantise, naming YAMNet, MobileNet-on-spectrogram, keyword-spotting and CRNN models (<https://community.hailo.ai/t/audio-classification-model/13498>). A later thread reports YAMNet failing to parse because its input is a 1-D waveform; a Hailo engineer replied that Hailo's own Whisper tiny/base port needed Conv1D replaced by Conv2D, fewer input features and a fixed decoder length, and that transformer models outside the Model Zoo "can be converted from scratch, but the complexity of this operation may vary" (<https://community.hailo.ai/t/raspberry-pi-ai-hat-disappointment/18099>). A user converting Whisper hit an unsupported `Transpose` inside self-attention (<https://community.hailo.ai/t/using-rpi5-hailo8-ai-hat-26-tops-for-local-voice-transcription/16092>). Supported operators listed by Hailo staff include GeLU only as "preview" and no STFT (<https://community.hailo.ai/t/supported-operators/5046>). A report of AST compiled for any Hailo chip: not found.

### AI HAT+ 2 (Hailo-10H)

40 TOPS INT4, 8 GB on-board RAM; vision performance "broadly equivalent" to the 26 TOPS HAT; launch LLMs were DeepSeek-R1-Distill 1.5B, Llama 3.2 1B, Qwen2.5-Coder 1.5B, Qwen2.5-Instruct 1.5B and Qwen2 1.5B, served through `hailo-ollama`; LoRA adapters are compiled with the DFC (<https://www.raspberrypi.com/news/introducing-the-raspberry-pi-ai-hat-plus-2-generative-ai-on-raspberry-pi-5/>). Hailo's announcement mentions "larger Whisper" and voice-to-action as fits (<https://community.hailo.ai/t/introducing-the-raspberry-pi-ai-hat-2/18659>). Jeff Geerling, testing every Hailo-released model on an 8 GB Pi 5 against the same models on the Pi's CPU, found "the Pi's built-in CPU trounces the Hailo 10H", with near-parity only on Qwen2.5 Coder 1.5B; the Hailo is limited to about 3 W against about 10 W for the SoC, and running two models at once gave segmentation faults (<https://www.jeffgeerling.com/blog/2026/raspberry-pi-ai-hat-2/>). His per-model token rates are in charts I did not transcribe. Geerling also gives the Hailo-10H as "40 TOPS of INT8" (same post) where Raspberry Pi says 40 TOPS INT4; Raspberry Pi's figure is the manufacturer's.

### AI Camera (Sony IMX500)

12.3 MP sensor with an on-sensor accelerator; input tensor at most 640 × 640, int8 or uint8, 8,388,480 bytes for firmware, network weights and working memory; integrated RP2040 manages the network firmware; works with every Pi model (product brief, <https://pip-assets.raspberrypi.com/categories/1044-raspberry-pi-ai-camera/documents/RP-008147-DS-1-ai-camera-product-brief.pdf>). Models are converted with Sony's IMX500 Converter and Packager (AITRIOS documentation, referenced at <https://www.raspberrypi.com/news/raspberry-pi-ai-camera-on-sale-now/>). It is a vision device; it has no audio input, so it does nothing for the toy's listening.

### Coral USB Accelerator

PyCoral wheels exist only for Python 3.9; Bookworm ships 3.11 and Trixie 3.13 (<https://github.com/google-coral/pycoral/issues/137>). A maintained fork of `libedgetpu` works through `tflite_runtime`; its maintainer wrote in April 2025: "Support for Coral EdgeTPU is pretty much dead" (same issue). The Edge TPU compiler runs only on x86_64 Linux, and Ultralytics notes the project "saw no updates between 2021 and 2025" (<https://docs.ultralytics.com/guides/coral-edge-tpu-on-raspberry-pi>). Only fully int8-quantised TFLite models compiled for the Edge TPU run on it; unsupported ops fall back to the CPU (<https://pidiylab.com/coral-tpu-raspberry-pi-5-setup/>).

### Indian prices (read 7 November 2026; page dates not shown)

| Item | robu.in | Silverline (approved reseller) | other |
| --- | --- | --- | --- |
| Pi 5 16 GB | ₹34,191 incl. GST (<https://oldwp.robu.in/product-category/microcontroller-development-board/raspberry-pi-microcontroller-development-board/official-boards-and-accessories/>) | ₹36,900 (<https://www.silverlineelectronics.in/collections/raspberry-pi-5-official-accessories>) | robocraze ₹34,029, sold out, 1 Sept 2026 (via <https://fron.in/products/raspberry-pi-5-16gb-sc1113>) |
| AI HAT+ 13 TOPS | ₹7,469 (<https://oldwp.robu.in/product-tag/raspberry-pi-ai-hat/>) | not listed on the page read | e2u ₹6,350 (<https://e2u.in/collections/raspberry-pi-5-official-accessories>) |
| AI HAT+ 26 TOPS | ₹11,444 (same robu page) | ₹10,100 | robocraze ₹11,309 (<https://robocraze.com/collections/ai-hats>) |
| AI HAT+ 2 | not found | not found | not found |
| AI Camera | not found | not found | not found |
| Active Cooler | ₹488 (<https://oldwp.robu.in/product-tag/raspberry-pi-5/>) | ₹430 | e2u ₹430 |
| 27 W USB-C PSU | ₹1,235 (Indian plug) | ₹1,020 | |
| M.2 HAT+ | ₹1,059 | | |

electropi.in: no listing came back in the searches I ran (not found). The robu pages were served from `oldwp.robu.in`; whether that mirror carries current prices is not established.

## 3. Setting up for headless, always-on use

### Which OS

Raspberry Pi OS moved to Debian 13 "Trixie" on 2 October 2025; upgrading a running Bookworm install in place is "not recommended or supported", and a clean flash is the recommended route (<https://www.raspberrypi.com/news/trixie-the-new-version-of-raspberry-pi-os/>). The current images are dated 6 October 2026, kernel 6.18, Debian 13; Lite 64-bit is a 525 MB download (<https://www.raspberrypi.com/software/operating-systems/>). Debian Trixie's `python3` is 3.13.5 (<https://packages.debian.org/trixie/python3>). Trixie groups the desktop into meta-packages (`rpd-wayland-core`, `rpd-x-core`), so a Lite image can later gain a desktop and the reverse (Trixie announcement, above). Raspberry Pi OS also supports cloud-init provisioning from 27 November 2025 (<https://www.raspberrypi.com/news/category/os/raspberry-pi-os/>).

### Raspberry Pi Imager

Imager 2.0 is a step-by-step wizard: device, OS, storage, then customisation (hostname, localisation, user, Wi-Fi, remote access, Raspberry Pi Connect, interface options), then write (<https://www.raspberrypi.com/news/a-new-raspberry-pi-imager/>). In 2.0 the localisation step (pick a capital city) sets time zone, keyboard and the wireless regulatory country; the Wi-Fi step no longer has a country field; there is no default `pi` user; the remote-access step enables SSH with either a password or a pasted public key (<https://raspberry.tips/en/raspberrypi-tutorials/raspberry-pi-imager-guide-en>, 3 May 2026; the same author documents version 2.0.12, <https://raspberry.tips/en/raspberrypi-tutorials/enable-ssh-on-raspberry-pi-new-method-for-bookworm-2026>). Without Imager customisation, an empty `ssh` file and a `userconf.txt` on the boot partition still enable SSH and create a user; a `wpa_supplicant.conf` there has not been read since 2023, so Wi-Fi cannot be set that way (same raspberry.tips page). After first boot the Pi is reachable at `hostname.local` (<https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/getting-started/configuring.adoc>).

### Firmware and bootloader

`sudo apt update && sudo apt full-upgrade` updates the OS and kernel (<https://www.raspberrypi.com/news/sd-cards-and-bumper/>). The bootloader EEPROM has `default` and `latest` release channels; `sudo rpi-eeprom-update` shows the state, `sudo rpi-eeprom-update -a` applies the latest image at next reboot, `sudo rpi-eeprom-config --edit` edits settings such as `PSU_MAX_CURRENT` or `POWER_OFF_ON_HALT` (<https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/boot-eeprom.adoc>).

### Python environments

From Bookworm onwards, `pip install` into the system Python fails with `error: externally-managed-environment`; this comes from PEP 668, not from Raspberry Pi; the official answer is a venv (`python -m venv env`), and `--system-site-packages` lets a venv see apt-installed packages such as Picamera2 or `python3-lgpio` (<https://www.raspberrypi.com/documentation/computers/os.html>, section "Use Python on a Raspberry Pi"). `--break-system-packages` exists and is the route the error message warns against (same page). `uv` publishes manylinux aarch64 wheels (0.13.7 on PyPI, read 7 November 2026, <https://pypi.org/project/uv/>). aarch64 wheels for CPython 3.13 exist for `torch` 2.15.0 (uploaded 28 October 2026), `onnxruntime` 1.31.1 (26 October 2026), `ai-edge-litert` 2.3.0 (6 October 2026) and `executorch` 1.6.0 (4 November 2026) (PyPI JSON, read 7 November 2026: <https://pypi.org/project/torch/>, <https://pypi.org/project/onnxruntime/>, <https://pypi.org/project/ai-edge-litert/>, <https://pypi.org/project/executorch/>). The ExecuTorch release was three days old when read.

### USB microphone

Raspberry Pi OS uses PulseAudio or PipeWire by default; Raspberry Pi advises creating `[path withheld]` only when an application talks to ALSA directly or runs where neither is present, and shows `alsamixer` as the headless volume control (<https://www.raspberrypi.com/documentation/accessories/audio.html>). Whether the Lite image installs PipeWire: not established in this pass; `systemctl --user status pipewire` on the board settles it. The practical ALSA path: `arecord -l` lists cards; `plughw:<card>` lets ALSA convert format and rate where the device's native format differs; capture gain is set in `alsamixer` (F4 or F5 shows capture controls) and saved with `sudo alsactl store`, or it may revert at reboot; one user needed `-f S16_LE` explicitly (<https://forums.raspberrypi.com/viewtopic.php?t=37873>). A typical 16 kHz mono capture line, as used with a ReSpeaker USB array on Bookworm Lite: `arecord -D plughw:CARD=Lite,DEV=0 -r 16000 -c 1 -f S16_LE -t wav out.wav`; the same thread shows a USB audio device dropping off the bus after minutes of capture on a Zero 2 W (<https://forum.seeedstudio.com/t/respeaker-lite-usb-connections-issues-stops-working-after-couple-of-minutes/281341>). Card numbers can change between boots; addressing the card by name (`CARD=<name>`) avoids that, and pinning the index through `snd-usb-audio index=` in modprobe configuration is the older method (forum thread above). Under PipeWire, Seeed's Pi 5 guide forces 16 kHz with `pw-metadata -n settings 0 clock.force-rate 16000` (<https://wiki.seeedstudio.com/respeaker_lite_pi5/>).

### Running as a service, logs and SD wear

systemd service units, restart policies (`Restart=`, `RestartSec=`) and `WantedBy=multi-user.target` are documented in `systemd.service(5)` (<https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html>); journald's size and storage limits (`SystemMaxUse=`, `RuntimeMaxUse=`, `Storage=volatile`) in `journald.conf(5)` (<https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html>). I did not fetch these two pages in this pass; they are the primary references a tutorial should cite.

Swap: Trixie replaces `dphys-swapfile` with `rpi-swap`, defaulting to `zram+file`, compressed RAM swap that writes idle pages back to `/var/swap` on a 24-hour cycle to spare the card (Raspberry Pi forum announcement of the package, <https://forums.raspberrypi.com/viewtopic.php?t=390708>). Configuration lives in `/etc/rpi/swap.conf` and drop-ins under `/etc/rpi/swap.conf.d/`; `Mechanism=` takes `auto`, `swapfile`, `zram`, `zram+file` or `none`; changes take effect only after a reboot (<https://github.com/raspberrypi/rpi-swap>). A third-party write-up shows `/var/swap` (2 GB by default) does not appear in `swapon` or `free` because it is zram's writeback target, visible only through `/sys/block/zram0/backing_dev` (<https://homelabpostmortem.com/2026/08/19/trixie-rpi-swap-writeback-file/>). With 16 GB and a model under 400 MB, `Mechanism=zram` (no file) is an option the documentation supports.

Reducing writes: move `/tmp` to tmpfs, keep `/var/log` in RAM with `log2ram` (azlux repository) or a tmpfs, add `noatime`, optionally `commit=900` on the root mount at the cost of losing up to 15 minutes of writes in a crash; do not disable filesystem journaling (Chris Dzombak, <https://www.dzombak.com/blog/2024/04/pi-reliability-reduce-writes-to-your-sd-card/>). A fully read-only root is described for Bullseye through Trixie at <https://www.dzombak.com/blog/2024/03/running-a-raspberry-pi-with-a-read-only-root-filesystem/>. `raspi-config` offers an Overlay File System under Performance Options; one tutorial reports it unreliable on 64-bit Bookworm on the Pi 5 and uses the `overlayroot` package instead (<https://pidiylab.com/raspberry-pi-read-only-root-filesystem-setup/>, March 2026, a single community source). On Trixie the overlay behaviour: not established.

### Overclocking

The Pi 5's default `arm_freq` is 2400 MHz. `over_voltage_delta` adds a microvolt offset to the DVFS voltage on the Pi 4 and Pi 5. Setting `force_turbo=1` together with any `over_voltage_*` above 0 sets a permanent bit in the SoC that shows the board was overclocked (<https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/config_txt/overclocking.adoc>). Geerling found 2.6 GHz stable and 2.8 GHz "a little unstable" on an early board, and recommends a fan for any overclock (<https://www.jeffgeerling.com/blog/2023/answering-some-questions-about-raspberry-pi-5/>; <https://www.jeffgeerling.com/blog/2023/overclocking-and-underclocking-raspberry-pi-5/>). More clock means more heat inside the toy, which §1 shows is the constraint already.

### Measuring temperature, throttling and power

`vcgencmd measure_temp` reads the SoC temperature from the firmware, which the documentation calls more accurate than Linux's reading (frequency-management page, above). `vcgencmd get_throttled` returns a bit field: 0x1 under-voltage now, 0x2 Arm frequency capped, 0x4 throttled now, 0x8 soft temperature limit active, and 0x10000, 0x20000, 0x40000, 0x80000 for "has occurred since boot" (<https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/os/graphics-utilities.adoc>). `vcgencmd measure_clock arm` gives the current clock (Raspberry Pi's own logging script uses it, <https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/>). The Pi 5's PMIC has ADCs readable with `vcgencmd pmic_read_adc` (overclocking documentation, above; Geerling's launch video). For power at the plug, a wall meter and a USB-C inline meter can disagree by about a watt at idle (Geerling, above).

## 4. Inference runtimes on the Pi 5 CPU

### ONNX Runtime

The measurement closest to this project: AST fine-tuned from `MIT/ast-finetuned-audioset-10-10-0.4593` (86M parameters), 10-second windows at 16 kHz, exported with Optimum and dynamically quantised with `quantize_dynamic(weight_type=QInt8)`, run on a Pi 5 with ONNX Runtime CPU (<https://dev.to/syamaner/part-4-edge-deployment-of-an-86m-parameter-audio-transformer-1821>; scripts in <https://github.com/syamaner/coffee-first-crack-detection/pull/23>):

| Precision | Threads | Cooling | p50 latency per 10-s window | Source note |
| --- | --- | --- | --- | --- |
| fp32 | 1 | not stated | 9,412 ms | v1 test set |
| int8 dynamic | 1 | none | 4,441 ms | PR table |
| int8 dynamic | 2 | none | 2,436 ms, 77 °C, throttled | PR table |
| int8 dynamic | 4 | Active Cooler | 2,070 ms (PR) / 2,092 ms (article), 45 °C | |
| int8 dynamic | 2 | Active Cooler, 27 W PSU | 2.45 s (production profile) | |

Feature extraction took 49 ms of the 4-thread total; inference 2,019 ms (PR). Accuracy cost of int8 on his 191-sample test set: 0.54 points and one extra false positive, identical on Mac and Pi (article). He reports the PyTorch CPU wheel was still needed for `ASTFeatureExtractor`; the Hugging Face source shows the extractor falls back to a NumPy filterbank when torchaudio is unavailable (<https://github.com/huggingface/transformers/blob/main/src/transformers/models/audio_spectrogram_transformer/feature_extraction_audio_spectrogram_transformer.py>), so that dependency may be avoidable; whether the NumPy path's features match closely enough is a bench question.

Static versus dynamic int8 on the A76: a Pi 5 study first claimed one ONNX quantisation format ran slower than fp32, then retracted that reading in August 2026 after finding its "QOperator" files were dynamically quantised. Its corrected statement: static QOperator ran 1.65–2.70× faster than fp32 on seven of nine ImageNet CNNs; ShuffleNet and SqueezeNet were slower quantised; dynamic against static is worth more than 4×; the two static formats differ by a median 1.5 %; `ORT_ENABLE_ALL` graph optimisation is what makes the quantised graph pay (Raspberry Pi 5, 64-bit Raspberry Pi OS, Python 3.11, ONNX Runtime 1.24.4, CPU execution provider; <https://github.com/manunicholasjacob/rpi5-quantization-benchmark>). The same pattern for MobileNetV2 on a Pi 5 with ONNX Runtime 1.25.1: fp32 15.01 ms, int8 dynamic 14.62 ms, int8 static per-tensor 6.28 ms, per-channel 6.37 ms; per-channel kept top-1 at 57.44 % against 51.69 % per-tensor (<https://zenn.dev/ux_xu/articles/ort-int8-ptq-cnn>). Both are CNNs; for transformers the matrix multiplications dominate, and dynamic quantisation is what syamaner used for AST.

Arm's own Pi 5 figure for a hybrid detector: RT-DETR-L with static int8 convolutions, dynamic int8 transformer matmuls and some parts left fp32, ONNX Runtime 1.27.0 CPU execution provider "(MLAS, KleidiAI)", batch 1, 5,000 runs: p50 1,782 ms baseline to 673 ms, model 125.8 MB to 38.4 MB, mAP@0.5:0.95 50.75 % (<https://huggingface.co/Arm/rtdetr-l-onnx-raspberry>). The XNNPACK execution provider's state in current ONNX Runtime on aarch64: not checked in this pass.

### PyTorch

Official aarch64 CPU wheels exist (PyPI, above). Arm's ExecuTorch course on a Raspberry Pi measured MobileNetV2 at a mean 72.55 ms in PyTorch eager against 10.89 ms in ExecuTorch with XNNPACK, 10 warm-ups and 50 runs; board model not stated in the excerpt read (<https://learn.arm.com/courses/executorch-on-arm/optimize-image-classification/benchmark-pytorch-and-fp32-executorch-on-the-raspberry-pi/interpret-latency-and-classification-output/>). The PyTorch blog shows a "significant latency reduction" for OPT-125M on a Pi 5 with ExecuTorch and XNNPACK over PyTorch eager, numbers only in a chart, no active cooling, with latency rising over runs from thermal throttling (<https://pytorch.org/blog/efficient-edge-ai-on-arm-cpus-and-npus/>). `torch.compile` on aarch64 Linux: status not established in this pass.

### LiteRT (TFLite)

TensorFlow Lite is now LiteRT; the Python package changes from `tflite-runtime` to `ai-edge-litert` with the same `Interpreter` API (<https://developers.google.com/edge/litert/migration>). On Trixie there was a gap: `tflite-runtime` was withdrawn before `ai-edge-litert` had Python 3.13 wheels, which a Picamera2 maintainer (davidplowman) described in November 2025 (<https://github.com/raspberrypi/picamera2/issues/1339>). Wheels for 3.13 aarch64 now exist (PyPI, above). A Pi 5 audio project (BirdNET, 3-second windows) measured 63.1 ms per segment through native `ai-edge-litert` against 70.5 ms through a wrapper, with about 201 MB RSS; thread count not stated (<https://docs.silvasonic.de/adr/0027-birdnet-inference-engine/>).

### ExecuTorch

Arm publishes an int8 MiniLM-L6-v2 ExecuTorch program for the Pi 5: p50 500.77 ms per request at sequence length 512, batch 1, ExecuTorch 1.1.0, XNNPACK with KleidiAI, Recall@10 79.64 % against 80.81 % for fp32 (<https://developer.arm.com/ai/models/hugging-face/Arm/minilm-l6-v2-int8-xnnpack-executorch-raspberrypi5/minilm-l6-v2-int8-pte>). ExecuTorch without the XNNPACK delegate is often slower than PyTorch (PyTorch blog, above); on Android a portable-kernel MobileNetV3 ran about 80× slower than the XNNPACK path (<https://github.com/sangsoolee/android-edge-ai-benchmark-lab>, a phone, not a Pi).

### ncnn

Not researched in this pass (not found).

### llama.cpp (small language models)

| Model | Quant | Generation tok/s | Prompt tok/s | Conditions | Source |
| --- | --- | --- | --- | --- | --- |
| Qwen2.5 0.5B Instruct | Q4_0 | 33.8 | 173.7 | Pi 5 2 GB | llama.cpp discussion #30069, via <https://edgellm-bench.vercel.app/boards/raspberry-pi-5> |
| Qwen2.5 0.5B Instruct | Q4_K_M | 29.1 | 91.5 | Pi 5 16 GB, 4 threads | ai-tier.com, via edgellm-bench |
| Llama 3.2 1B Instruct | Q4_K_M | 10.8 | 72.9 | 16 GB, llama.cpp b9307 CPU with OpenBLAS, NVMe, Active Cooler, pp512/tg128, 4 threads | davidscarth, <https://github.com/davidscarth/edge-ai-study/blob/main/RASPI5.md> |
| Llama 3.2 1B Instruct | Q4_K_M | 14.5 (aggregator flags as unusual) | 85.0 | 16 GB, 4 threads | ai-tier.com, via edgellm-bench |
| Gemma 3 1B IT | Q4_K_M | 10.4 | 60.2 | as davidscarth row | davidscarth |
| Qwen2.5 1.5B Instruct | Q4_K_M | 11.9 | 61.4 | 16 GB, 4 threads | ai-tier.com |
| SmolLM2 1.7B Instruct | Q4_K_M | 7.2 | 43.1 | as davidscarth row | davidscarth |
| Qwen2.5 3B Instruct | Q4_K_M | 6.0 | 29.2 | 16 GB, 4 threads | ai-tier.com |
| Llama 3.2 3B Instruct | Q4_K_M | 4.4 | 26.7 | as davidscarth row | davidscarth |
| Llama 3.2 3B Instruct | Q4_K_M | 5.9 | 28.9 | 16 GB, 4 threads | ai-tier.com |

The two sources disagree by about a third on the 1B and 3B Llama models; the davidscarth rows state cooling, build and storage, the ai-tier rows do not. A different engine, distributed-llama 0.12.3, gave 5.95 tok/s generation and 14.30 tok/s evaluation for Llama 3.2 3B Q40 on one Pi 5 8 GB (<https://github.com/b4rtaz/distributed-llama/discussions/165>). For the same LLMs on the AI HAT+ 2, see Geerling above: the CPU was faster. A how-to's warning worth keeping: a run without start and end temperatures is not a benchmark (<https://overnightdesk.hashnode.dev/how-to-benchmark-llms-on-a-raspberry-pi-5-llama-cpp-step-by-step>).

### Sentence-embedding encoders (MiniLM)

Pi 5 measurements found: Arm's ExecuTorch figure above (500.77 ms at 512 tokens). A product blog reports all-MiniLM-L6-v2 at 34 ms per embedding on a Pi 4 through the Rust `ort` crate, 97 % of it model inference; sequence length not stated (<https://www.shodh-memory.com/blog/embedding-models-edge-devices>). A Pi 5 ONNX Runtime figure for MiniLM at typical short lengths: not found.

### Practical default for a frozen transformer encoder

What the sources above support, stated as their findings: ONNX Runtime's CPU execution provider has a measured AST result on this exact board (syamaner), ships Python 3.13 aarch64 wheels, uses Arm's KleidiAI kernels in recent versions (Arm's RT-DETR card), and supports dynamic int8 for transformer matmuls without calibration data. ExecuTorch with XNNPACK beat PyTorch eager by large factors in Arm's Pi tests but has no AST measurement on a Pi found here. LiteRT has a measured audio-CNN result on the Pi 5 (BirdNET) but would need AST converted to TFLite, for which no Pi result was found. Which of these is fastest for AST at 2 seconds is a bench question (§8).

## 5. Audio models for the edge

### AST and what a 2-second window costs

AST splits a 128-bin log-mel spectrogram into 16 × 16 patches with stride 10 in both directions; the AudioSet checkpoint takes 1024 frames (10.24 s) and has 12 × 101 = 1212 patches plus two special tokens; reported AudioSet mAP is 0.459 for the single weight-averaged model and 0.485 for an ensemble; Speech Commands V2 98.1 % (<https://github.com/YuanGongND/ast>; paper §6). The Hugging Face checkpoint's `config.json` has `frequency_stride` 10 and `hidden_size` 768, and its `preprocessor_config.json` has `max_length` 1024, 128 mel bins, 16 kHz, mean −4.2677393 and std 4.5689974 (<https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/raw/main/preprocessor_config.json>).

The important finding for the toy: the Hugging Face feature extractor pads or truncates every input to `max_length` frames (`_extract_fbank_features(waveform, max_length=self.max_length)`, padding with `ZeroPad2d`), and the model sizes its position embeddings from `config.max_length` with no interpolation path (feature extractor source, above; model source <https://github.com/huggingface/transformers/blob/main/src/transformers/models/audio_spectrogram_transformer/modeling_audio_spectrogram_transformer.py>). So a 2-second clip passed through the default pipeline is padded to 10.24 s and costs the full 1212-patch forward pass. The extractor uses 400-sample windows with a 160-sample hop at 16 kHz (same source). Derived arithmetic from those settings: 2 s of audio is 32,000 samples, giving 198 frames; with 16-frame patches at stride 10 that is 19 time positions × 12 frequency positions = 228 patches, against 1212, about 19 % of the tokens. Self-attention cost grows with the square of token count and the feed-forward layers linearly, so the forward pass should shrink by more than 5×; the real figure is a bench measurement.

How to shorten it: the original AST code builds the model for any `input_tdim`; for the AudioSet-pretrained weights it reshapes the stored position embeddings to a 12 × 101 grid and, when the new time dimension is under 101, takes the centre `t_dim` columns (for 2 s, columns 41–59), otherwise interpolates bilinearly (<https://github.com/YuanGongND/ast/blob/master/src/models/ast_models.py>, lines 141–154; the comment above the branch says the reverse of what the code does, the code is what runs). In Hugging Face, the equivalent is setting `max_length` in both the feature extractor and the config and slicing the `position_embeddings` parameter the same way before loading; no built-in helper was found. What truncation does to the frozen encoder's representations, and so to a scorer trained on them: no measurement found. The README's own example builds a 100-frame model (<https://github.com/YuanGongND/ast>), so short inputs are an intended use of the architecture; the AudioSet-finetuned checkpoint itself was trained on 10-second clips.

### Efficient alternatives

| Model | Params | AudioSet mAP | Input | Licence | Pi latency found |
| --- | --- | --- | --- | --- | --- |
| AST (the brief's checkpoint) | 86.6M (brief) | 0.459 single / 0.485 ensemble | 128 mel, 10.24 s | BSD-3-Clause (repo) | yes, §4 |
| EfficientAT mn04_as | 0.983M | 43.2 | 128 mel, 10 ms hop | MIT (repo) | not found |
| EfficientAT mn05_as | 1.43M | 44.3 | same | MIT | not found |
| EfficientAT mn10_as | 4.88M, 0.54 GMACs | 47.1 | same | MIT | not found |
| EfficientAT mn40_as | 68.43M | 48.4 | same | MIT | not found |
| EfficientAT dymn10_as | 10.57M, 0.58 GMACs | 47.7 | same | MIT | not found |
| CED-Tiny | 5.5M | 48.1 (AS-2M) | 64 mel, 16 kHz | GPL-3.0 (repo) | not found |
| CED-Mini | 9.6M | 49.0 | same | GPL-3.0 | not found |
| CED-Base | 86M | 50.0 | same | GPL-3.0 | not found |
| PANNs CNN14 | not recorded here | 0.431 (0.438 for the 16 kHz model) | log-mel | not checked | not found |
| YAMNet | 3.7M weights, 69.2M multiplies per 0.96 s frame | balanced mAP 0.306 | 64 mel, 0.96 s frames | not checked | not found |
| Dasheng-Base | 86M | 49.7 (AudioSet fine-tuned) | 64 mel, up to 10 s | not checked | not found |
| BEATs iter3+ | not checked | 50.6 % on AS-2M (abstract) | | not checked | not found |

Sources: EfficientAT table (<https://github.com/fschmid56/EfficientAT>; MACs depend on spectrogram resolution, default 128 mel bands and 10 ms hop; all models were trained in fp16 and "you might notice a slight performance degradation" in fp32 CPU inference). CED table and the note that CED-Tiny "should be faster than MobileNets on a single x86 CPU", ONNX export scripts and kaldi-native-fbank for C++ features (<https://github.com/RicherMans/CED>). PANNs checkpoints (<https://github.com/qiuqiangkong/audioset_tagging_cnn>). YAMNet figures (<https://github.com/tensorflow/models/blob/master/research/audioset/yamnet/README.md>). Dasheng sizes, HEAR scores and the 49.7 mAP AudioSet head (<https://github.com/RicherMans/Dasheng>; paper <https://arxiv.org/abs/2406.06992>, which states Dasheng processes at most 10 s at once). BEATs abstract (<https://arxiv.org/abs/2212.09058>). Licences are as shown on the repositories' GitHub pages; CED's GPL-3.0 matters if the toy's code is released openly.

Two further routes from the papers in §6: MobileNet-based audio embedding extractors trained by distillation from transformer ensembles, studied explicitly so that "a single costly forward pass" feeds several shallow task heads on edge devices (Schmid et al., EUSIPCO 2023), which is the frozen-encoder-plus-small-head shape of this project; and transformer-based models built to do keyword spotting and audio tagging together on phones, 2–6× faster than MobileNetV2 across four mobile platforms (Dinkel et al., ICASSP 2023).

### Speech-related edge models

Silero VAD: one 30 ms+ chunk takes under 1 ms on a single CPU thread (CPU not named), the JIT model is about 2 MB, 8 kHz and 16 kHz supported, PyTorch and ONNX builds (<https://github.com/snakers4/silero-vad>). A Pi 5 measurement: not found. A VAD in front of AST is how a toy avoids running the encoder on silence; whether it helps depends on how often the toy hears nothing.

Vosk offline recognition: small models of 40 MB (US English, `vosk-model-small-en-us-0.15`), 36 MB (Indian English, `vosk-model-small-en-in-0.4`) and 42 MB (Hindi, `vosk-model-small-hi-0.22`) (<https://alphacephei.com/vosk/models>). Pi 5 speed: not found.

Whisper and whisper.cpp: Whisper is an OpenAI model, so these results are reported and not recommended. On a 4 GB Pi (board model as stated on the page: Pi with 4 GB), whisper.cpp took 18 s for an 11-second sample, 11.9 s with `base-q4_k`; q2_k and q3_k were slower; Moonshine base did the same sample in 2.76 s against 21 s for whisper.cpp base, at slightly lower word error rate; the author notes Whisper's encoder always takes a 30-second input, so a 2-second chunk is padded to 30 s, while Moonshine accepts any length (<https://anil.recoil.org/ideas/embedded-whisper>). Moonshine is from Useful Sensors, not OpenAI.

Keyword-spotting scale: models of tens of thousands of parameters reach the mid-90s on Google Speech Commands, for example 62k parameters at 96.4 % with Sinc-convolutions on raw audio (Mittermaier et al., ICASSP 2020, DOI 10.1109/icassp40776.2020.9053395, Consensus record <https://consensus.app/papers/details/dded3fb82c1b586194868fbf1df349e6/>; not put through the verification chain, so treat as found, not verified).

## 6. Papers

Search: six Consensus calls, one at a time (`mcp__consensus__search`, page sizes 10–20). Verification status needs explaining first. Stage 2, the `find-research-papers` MCP, failed on every call this session: `get_paper` returned a bare error and `search_papers` skipped all five sources with "Could not find a suitable TLS CA certificate bundle, invalid path: …/.cache/uv/archive-v0/1GAwoeAt1Zx-UEv6/…/certifi/cacert.pem". Stage 3, the `crossref` MCP, failed with "No module named 'httpcore'". Both look like a pruned uv cache under a running server. I used the named fallback for stage 3, `[path withheld] <DOI>`, which reads the Crossref API directly and prints full author lists, all three date fields and any `update-to` (retraction or correction) notice. For stage 2 I substituted a direct OpenAlex API query per DOI for the retraction flag, author list and open-access copy. Under the protocol as written, all 15 papers are therefore UNVERIFIED at stage 2. The labels below are the provisional result of Crossref (via `cite`) against Consensus, with OpenAlex as the stage-2 stand-in; none of the 15 is flagged retracted by OpenAlex, and `cite` printed no `update-to` notice for any. Rerunning stage 2 once the MCP servers are restarted would settle them.

1. **AST: Audio Spectrogram Transformer.** Yuan Gong, Yu-An Chung, James Glass. Interspeech 2021, pp. 571–575. DOI 10.21437/Interspeech.2021-698. Consensus: <https://consensus.app/papers/details/301a21ef86b4525d852c2c20c43ba77a/>. The architecture being deployed, its patch arithmetic and its variable-length input. CORRECTED: Consensus gave the arXiv DOI 10.48550/arxiv.2104.01778 dated 5 April 2021; Crossref holds the published Interspeech record, published online 30 August 2021. Full text: arXiv <https://arxiv.org/abs/2104.01778>.

2. **PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition.** Qiuqiang Kong, Yin Cao, Turab Iqbal, Yuxuan Wang, Wenwu Wang, Mark D. Plumbley. IEEE/ACM TASLP 28 (2020), pp. 2880–2894. DOI 10.1109/taslp.2020.3030497. Consensus: <https://consensus.app/papers/details/48587c2857625a868bae4e295c2d2f11/>. The CNN baseline family with a performance-against-complexity analysis. CORRECTED: Consensus dated it 21 December 2019 (the preprint) and spelled the first author "Qiu-Qiang Kong"; Crossref gives 2020. Full text: <https://arxiv.org/pdf/1912.10211>.

3. **Efficient Large-Scale Audio Tagging Via Transformer-to-CNN Knowledge Distillation.** Florian Schmid, Khaled Koutini, Gerhard Widmer. ICASSP 2023, pp. 1–5. DOI 10.1109/icassp49357.2023.10096110. Consensus: <https://consensus.app/papers/details/8a0d425adaa15e5e9afd2b45c87c3968/>. The EfficientAT MobileNetV3 models distilled from transformers, the main candidates for replacing AST on a CPU. CORRECTED: Consensus 9 November 2022 (preprint); Crossref 4 June 2023. Full text: <https://arxiv.org/pdf/2211.04772>.

4. **Dynamic Convolutional Neural Networks as Efficient Pre-Trained Audio Models.** Florian Schmid, Khaled Koutini, Gerhard Widmer. IEEE/ACM TASLP 32 (2024), pp. 2227–2241. DOI 10.1109/taslp.2024.3376984. Consensus: <https://consensus.app/papers/details/a43a23ed0fe15f958ec98280278a7797/>. The dynamic MobileNets (dymn), with downstream fine-tuning results against transformers. CORRECTED: Consensus 24 October 2023; Crossref 2024. Full text: open-access IEEE PDF reported by OpenAlex, <https://ieeexplore.ieee.org/ielx7/6570655/6633080/10472152.pdf>.

5. **Low-Complexity Audio Embedding Extractors.** Florian Schmid, Khaled Koutini, Gerhard Widmer. EUSIPCO 2023, pp. 451–455. DOI 10.23919/eusipco58844.2023.10289815. Consensus: <https://consensus.app/papers/details/f0183385f18255eabb5a7de43379d95c/>. Directly about a frozen low-cost encoder whose embeddings feed shallow heads on edge devices. VERIFIED (provisional): year agrees; Consensus date 3 March 2023 is the preprint, Crossref 4 September 2023. Full text: <https://arxiv.org/pdf/2303.01879>.

6. **CED: Consistent Ensemble Distillation for Audio Tagging.** Heinrich Dinkel, Yongqing Wang, Zhiyong Yan, Junbo Zhang, Yujun Wang. ICASSP 2024, pp. 291–295. DOI 10.1109/icassp48485.2024.10446348. Consensus: <https://consensus.app/papers/details/a51dffdc16595537bb1df032b93e61ec/>. Small transformers (5.5M–86M) distilled from ensembles, with 64-mel inputs; a 10M model reaches 49.0 mAP. CORRECTED: Consensus 23 August 2023; Crossref 14 April 2024. Full text: <https://arxiv.org/pdf/2308.11957>.

7. **CMKD: CNN/Transformer-Based Cross-Model Knowledge Distillation for Audio Classification.** Yuan Gong, Sameer Khurana, Andrew Rouditchenko, James Glass. IEEE TPAMI 48(3), pp. 3571–3585. DOI 10.1109/tpami.2025.3644853. Consensus: <https://consensus.app/papers/details/0bbd85ed373251e781dfeac110d6145b/>. From AST's authors: CNN and AST teaching each other, so a CNN student can match its AST teacher. CORRECTED: Consensus dated it 13 March 2022 (preprint); Crossref gives the issue as March 2026; OpenAlex says 2025. Crossref wins: 2026. Full text: <https://arxiv.org/pdf/2203.06760>.

8. **Efficient Training of Audio Transformers with Patchout.** Khaled Koutini, Jan Schlüter, Hamid Eghbal-zadeh, Gerhard Widmer. Interspeech 2022, pp. 2753–2757. DOI 10.21437/interspeech.2022-227. Consensus: <https://consensus.app/papers/details/bb93815dbc2d5f3095c63f6a47191655/>. PaSST, the transformer teacher behind EfficientAT, and a direct treatment of transformer cost growing with input length. CORRECTED: Consensus 11 October 2021 (preprint); Crossref 18 September 2022. Full text: <https://arxiv.org/pdf/2110.05069>.

9. **Unified Keyword Spotting and Audio Tagging on Mobile Devices with Transformers.** Heinrich Dinkel, Yongqing Wang, Zhiyong Yan, Junbo Zhang, Yujun Wang. ICASSP 2023, pp. 1–5. DOI 10.1109/icassp49357.2023.10095534. Consensus: <https://consensus.app/papers/details/fa22a66b37db5b31a8c921a108136d40/>. Deployment-minded transformers benchmarked on four mobile platforms, 2–6× faster than MobileNetV2. VERIFIED (provisional): year agrees; Consensus 3 March 2023 (preprint), Crossref 4 June 2023. Full text: <https://arxiv.org/pdf/2303.01812>.

10. **Understanding and Overcoming the Challenges of Efficient Transformer Quantization.** Yelysei Bondarenko, Markus Nagel, Tijmen Blankevoort. EMNLP 2021, pp. 7947–7969. DOI 10.18653/v1/2021.emnlp-main.627. Consensus: <https://consensus.app/papers/details/71bc42e064ed51b789785555e9aaa808/>. Why transformer activations quantise badly (structured outliers in residual connections) and what fixes it; the reason to check int8 AST accuracy and not assume it. VERIFIED (provisional). Full text: <https://aclanthology.org/2021.emnlp-main.627.pdf>.

11. **Is INT8 Portable? A Cross-Platform Measurement Study of Quantized Inference on Embedded and Automotive Accelerators.** Yuyeong Shin. arXiv, 14 September 2026. DOI 10.48550/arxiv.2609.16085. Consensus: <https://consensus.app/papers/details/f853d12444575ea1a167cd917d7928d1/>. The dotprod finding in §1, and that int8 outputs differ slightly between kernels even where top-1 is unchanged. UNVERIFIED: arXiv only (DataCite DOI), not in Crossref; preprint, not peer reviewed; Consensus gave the author as "Yu-Len T. Shin" where arXiv and OpenAlex give "Yuyeong Shin". Full text: <https://arxiv.org/pdf/2609.16085>.

12. **Performance Characterization of Using Quantization for DNN Inference on Edge Devices.** Hyunho Ahn, Tian Chen, Nawras Alnaasan, Aamir Shafi, Mustafa Abduljabbar, Hari Subramoni, Dhabaleswar K. Panda. IEEE ICFEC 2023, pp. 1–6. DOI 10.1109/icfec57925.2023.00009. Consensus: <https://consensus.app/papers/details/f58ed524f99f5fa789634edbbee12f11/>. FP16/int8, static and dynamic schemes across TFLite, ONNX and PyTorch on a Raspberry Pi with MLPerf methodology; reports int8 3.7× over fp32 with TFLite on the Pi in the offline scenario. CORRECTED: Consensus gave the second author as "Tianrun Chen"; Crossref and OpenAlex give "Tian Chen". Full text: <https://arxiv.org/pdf/2303.05016>.

13. **DeepEdgeBench: Benchmarking Deep Neural Networks on Edge Devices.** Stephan Patrick Baller, Anshul Jindal, Mohak Chadha, Michael Gerndt. IEEE IC2E 2021, pp. 20–30. DOI 10.1109/ic2e52221.2021.00016. Consensus: <https://consensus.app/papers/details/007bc445c7c25c1387a855dfd6d7ba34/>. A method for measuring inference time and power together on a Pi 4, Coral Dev Board, Jetson Nano and others. CORRECTED: Consensus gave the arXiv DOI 10.48550/arxiv.2108.09457; Crossref holds the IC2E record dated October 2021. Full text: <https://arxiv.org/pdf/2108.09457>.

14. **Review of large YOLOv8 and RT-DETR energy efficiency on edge devices for real-time detection.** Ivan Suchý, Michal Turčaník. Scientific Reports 16(1), 2026. DOI 10.1038/s41598-026-46453-6. Consensus: <https://consensus.app/papers/details/bab80e9409b955f0aeae53f9f8015a5a/>. A Pi 5 study comparing CPU and NPU offload end to end, separating model latency from pipeline throughput, which is the measurement discipline the toy needs. VERIFIED (provisional): published online 27 March 2026. Full text: <https://www.nature.com/articles/s41598-026-46453-6> (Scientific Reports, open access per OpenAlex).

15. **Lightweight Deep Learning for Resource-Constrained Environments: A Survey.** Hou-I Liu, Marco Galindo, Hongxia Xie, Lai-Kuan Wong, Hong-Han Shuai, Yung-Hui Li, Wen-Huang Cheng. ACM Computing Surveys 56(10), pp. 1–42. DOI 10.1145/3657282. Consensus: <https://consensus.app/papers/details/4d571d7ed48a56f2b20acec1e9f75c81/>. Survey of lightweight architectures, compression and hardware acceleration, including TinyML and LLM deployment. VERIFIED (provisional): year agrees; online 24 June 2024, issue 31 October 2024. Full text: <https://arxiv.org/pdf/2404.07236>.

Provisional counts: VERIFIED 5 (papers 5, 9, 10, 14, 15), CORRECTED 9 (papers 1, 2, 3, 4, 6, 7, 8, 12, 13), UNVERIFIED 1 (paper 11). Strictly under the three-stage protocol, all 15 are UNVERIFIED at stage 2 until the `find-research-papers` server works again. Most corrections are the same error: Consensus reports the arXiv preprint date or DOI where a published version exists.

Found but not kept: MLPerf Tiny (microcontroller scale, arXiv 2106.07597), Temporal Knowledge Distillation for on-device audio classification (Choi et al., ICASSP 2022), I-BERT (integer-only BERT), and two 2026 IEEE Access Pi 5 papers whose topics sit away from audio.

## 7. Web sources used most

Primary and dated where time-sensitive: Raspberry Pi product pages and briefs for the Pi 5, Active Cooler, AI HAT+, AI HAT+ 2, AI Camera and SD cards (read 7 November 2026; Pi 5 brief published April 2026, AI HAT+ 2 brief undated in the excerpt); Raspberry Pi documentation on GitHub (frequency management, `vcgencmd`, overclocking, boot EEPROM, Python, audio); Raspberry Pi news posts (thermals; Trixie, 2 October 2025; AI HAT+ 2, 15 January 2026; SD cards and command queueing; Imager 2.0); the USB Power Delivery white paper; Hailo community threads (2024–2026); Jeff Geerling's blog and sbc-reviews (2023–2026); Arm developer pages and Hugging Face model cards (2026); PyPI package metadata (read 7 November 2026); the AST, EfficientAT, CED, Dasheng, PANNs, YAMNet and Silero repositories; the Hugging Face transformers source for AST. The single most relevant community source is syamaner's AST-on-Pi-5 write-up (29 April 2026, edited 2 May 2026) and its PR.

## 8. Open questions for the bench

Only measurement on his own Pi can settle these.

1. AST latency per 2-second window with the position-embedding slice (228 patches), against the default padded 1212-patch path, at fp32 and dynamic int8 in ONNX Runtime, at 1, 2 and 4 threads, with `ORT_ENABLE_ALL`; p50 and p95 over at least a few hundred runs, with start and end temperature and `get_throttled` recorded.

2. Whether the sliced 2-second AST still separates his four labels: the frozen encoder was fine-tuned on 10-second clips, and no measurement of truncation's effect was found. Compare the scorer's results on embeddings from sliced 2-s inputs, from padded 2-s inputs, and from an EfficientAT encoder (mn10 or mn04) on the same clips.

3. Whether the NumPy fallback in `ASTFeatureExtractor` produces features close enough to the torchaudio path to drop the PyTorch dependency on the Pi, and how long feature extraction takes for 2 s.

4. Int8 accuracy for this use: dynamic int8 cost syamaner 0.54 points on his task; Bondarenko et al. explain why transformer int8 can cost more. Measure the scorer's agreement between fp32 and int8 embeddings on his own recordings.

5. ONNX Runtime against ExecuTorch (XNNPACK) and LiteRT for the same encoder on this board; no AST comparison across runtimes was found.

6. Sustained SoC temperature and clock inside the closed toy, with the Active Cooler, over hours of duty cycle (inference every 2 s or every hop the design chooses), at the room temperatures of Ahmedabad; the Pi's rated range is 0–70 °C and the official case with lid already throttled in a 30-minute test.

7. Fan noise at the microphone, and whether the fan's speed steps (including the hunting "pumping" sound) show up in the scorer's input; record the fan alone at each speed step through the toy's own microphone.

8. Idle and loaded power of the 16 GB board with the microphone attached, measured at the wall and with a USB-C meter, since no 16 GB figure was found and the two kinds of meter disagree.

9. Whether the official A2 card enables command queueing on this kernel (`dmesg`), and cold-start time from power-on to the first classification.

10. Silero VAD's cost on the Pi 5 and how much of the day the toy hears nothing, which decides whether gating AST behind a VAD saves anything.

11. USB microphone stability over days of continuous capture, given the reported USB audio drop-outs on another Pi model.

12. Whether PipeWire is present on the Lite image he flashes, which decides whether capture goes through ALSA directly or through PipeWire.
