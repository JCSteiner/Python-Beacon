# Python Beacons
###### This post is strictly educational.
This repository is meant to provide a wrapper and helper scripts for shellcode to be executed using python.
As of the time I am posting, it evades Microsoft Defender on Windows 11 with Cloud Protection Enabled.
Current Version: 1

## Credit
I used this github and the accompanying youtube webinar as a base for this project. I added extra stuff to try and make it my own, but I highly recommend watching the youtube series for extra background.
https://github.com/RiverGumSecurity/PythonShellcode
https://www.youtube.com/watch?v=n-nU2jCK5-c&t=1100s&ab_channel=BlackHillsInformationSecurity

## How this works:
1. shellcode is decoded using a bitwise xor and a key provided in plaintext, this is not meant to encrypt shellcode, just to add an extra layer of EDR evasion
2. a process of your choosing is spawned. the filepath is a variable you must change, I have cmd.exe by default. Some processes work better than others in testing.
3. that process is injected into via Windows API calls
4. python exits after completing, leaving your injected into process orphaned

## Steps to use this for your research:

### Encode your shellcode
1. Generate python shellcode with your C2 of choice.
2. Copy and paste into encode_buf.py where I have the comment saying to paste raw shellcode. You need to paste here as a byte string meaning it can't just be buf = "nastycode" it needs to be buf = b"nastycode"
3. Change the key to whatever you desire
4. Run this file and open the text file it spits out

### Assemble template
1. In beacon_template.py, copy and paste the contents of xor_buf.txt to overwrite rand_key and rand_buf. This time I put the byte string conversion for the shellcode for you :)
2. Change the variable rand_inject to whatever you want to launch and inject into. I have cmd as default, different executables seem to behave slightly differently when reacting to being orphaned, I would recommend trying another executable besides cmd.
3. Make sure you haven't changed variable or function names to not have the "rand_" prefix, this is important for the next step

### Randomize your beacon's signature
1. run "randomize_beacon.py" and give the full filepath for your desired input (the template) and output (your final beacon) when prompted
2. review the randomized beacon output, it should have randomized every variable and function to be a 16 character string of letters and removed all comments
3. find a way to get this to the target windows machine and run with python
4. In my experience with evading EDR thus far, malicious scripts are primarily caught for behavioral detection (use sleepmask to avoid this) and specific commands in the script. By putting pretty much every hard-coded value into a variable, and randomizing all those variable names, it becomes very difficult for us to be caught at least on static signatures. Theoretically, if you randomize the beacon signature each time.

## Disclaimers and Future plans
1. Process injection is a very old technique. This evadies MS Defender with Cloud Protection Enabled, but implementing another technique would probably be stealthier.
2. This uses Windows API calls which are hooked by EDR. Implementing indirect syscalls would be stealthier.
