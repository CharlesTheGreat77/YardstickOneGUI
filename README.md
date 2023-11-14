# YardstickOneGUI
First Yardstick One GUI for your RF Adventures!
This includes receiving, and transmitting RF signals
easily without having to do the hard work! 

![IMG_5570](https://github.com/CharlesTheGreat77/YardstickOneGUI/assets/27988707/3b48b24a-6f7e-4c63-82ca-e56aa058b71d)

# In Progress!
Updates will come in time...

# Prerequisites
| Prerequisite | Version |
|--------------|---------|
| Python3      |  >=3.0  |
| Rfcat        |  >=2.0  |

# requirement
customtkinter
```
pip3 install -r requirements.txt
```
or
```
pip3 install customtkinter
```

# Start GUI
```
python3 yardstick-gui.py
```

# Receive signals
https://github.com/CharlesTheGreat77/YardstickOneGUI/assets/27988707/c19f699a-7f8c-487d-b116-0f1deaf68a25

- best to click modulation in use before hitting configure button
  to ensure yardstick one is configured with appropriate modulation.

# Save signals
https://github.com/CharlesTheGreat77/YardstickOneGUI/assets/27988707/2d04f052-07ba-4b5b-916c-a50f50db6dbf

- Signals are saved in ".cap" file format.
  Frequency:
  Modulation:
  Payload:

# Transmit signals (received) OR Transmit Tesla Charging Port signal
https://github.com/CharlesTheGreat77/YardstickOneGUI/assets/27988707/2947c33f-48bc-44cd-bb0e-6a98586e44ea

- All signals in the output are sent once
- Tesla charging port signal is sent on both 315Mhz & 433.92Mhz

  Note: Configure stick back to frequency and modulation in use
        after charging port is transmitted, or the stick will be
        configured to 433.92Mhz after transmittion.

# Import cap files
https://github.com/CharlesTheGreat77/YardstickOneGUI/assets/27988707/d4a2dfc2-ba38-498d-9855-0fda455a7c13

- Yardstick is configured to the settings set in the cap file

# Key Note
1. Configure button resets the signals list.. so signals still in the text box will NOT be
   in the signals list. You can simply CTRL A and delete to empty the box.
2. "Manually configure Yardstick one" is not working YET! Bear wit meh

# To do
1. Change output for more modern (pretty) asthetic.
2. Allow individual signals to be transmitted.
3. Create tab to manipulate and transmit signals.
4. Allow flipper key files to be transmitted.

# Bug
Spectrum analyzer bugs out and crashes the app... so till then, if you're using it..
you'll have to rerun the app after it closes..

# Yardstick One playground CLI
https://github.com/CharlesTheGreat77/YardstickOnePlayground

### 💬 Contact Me 

![Gmail Badge](https://img.shields.io/badge/-doobthegoober@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white)

### 🚦 Stats

<a href="https://github.com/CharlesTheGreat77">
  <img src="https://github-readme-stats.vercel.app/api?username=CharlesTheGreat77&show_icons=true&hide=commits" />
</a>
<a href="https://github.com/CharlesTheGreat77">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=CharlesTheGreat77&layout=compact" />
</a>

<p align="center"> 
  <img src="https://profile-counter.glitch.me/CharlesTheGreat77/count.svg" />
</p>
