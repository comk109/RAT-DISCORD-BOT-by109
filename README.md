
# COMK109 Ultimate - คู่มือการใช้งาน

## 🇬🇧 ENGLISH EXPLANATION

### 📋 What is this?
This is a **Remote Access Trojan (RAT)** combined with a **Stealer** and **Ransomware**. It's written in Python and targets **Windows systems only**.

> ⚠️ The malware connects to **Discord** for Command & Control (C2).

---

### 🔥 What can it do?

#### 1. 📂 STEALING DATA (25+ functions)
* **Browser Passwords:** Chrome, Edge, Brave, Opera
* **Browser Data:** Cookies & history from all browsers
* **Financial Info:** Credit card info saved in browsers
* **Accounts & Tokens:**
  * Discord tokens (to steal accounts)
  * Roblox cookies (to steal Roblox accounts)
  * Telegram sessions (take over Telegram accounts)
  * WhatsApp & Signal sessions
* **Network & Credentials:**
  * WiFi passwords saved on the PC
  * VPN configs (NordVPN, ExpressVPN, ProtonVPN)
  * FTP credentials (FileZilla, WinSCP)
  * SSH keys from `.ssh` folder
  * Windows credentials (Vault, saved passwords)
* **Crypto Wallets:** Exodus, Atomic, Electrum, Binance, Ledger
* **System Files & Sensitive Data:**
  * System files (`SAM`, `SYSTEM`, `SECURITY`)
  * Important files with keywords: `password`, `bank`, `crypto`, `wallet`
  * Python scripts from Desktop/Documents
  * Email data from Thunderbird
  * Open ports scanner, running processes & installed programs list
* **Surveillance & Monitoring:**
  * Screenshots (taken every 10 seconds)
  * Webcam photos (taken every 30 seconds)
  * Screen recordings & Microphone recordings
  * Keylogger (records every keypress)
  * Clipboard monitoring (steals copied crypto addresses)

---

#### 2. 🎮 REMOTE CONTROL (20+ functions)
* **System Control:**
  * Remote Shell (execute any CMD command)
  * Download / Upload files
  * Open / Kill applications & View / Kill processes
  * Control Windows Services
  * Enable / Disable RDP
  * Create backdoor user (`Administrator/P@ssw0rd123!`)
* **Device Control:**
  * Lock screen
  * Disable / Enable Keyboard & Mouse
  * Volume control (mute / unmute / set level)

---

#### 3. 💥 SYSTEM DESTRUCTION (10+ functions)
* **Ransomware:** Encrypts 18+ file types, leaves ransom note
* **System & OS Corruption:**
  * Destroy System (Deletes `System32`, Boot files)
  * Destroy Windows (Deletes 30+ Windows folders + Registry)
  * Wipe / Format Drive (Formats entire drive or quick format)
  * Delete All Files (Deletes everything in user profile)
* **System Control & Disabling Security:**
  * BSOD (Blue Screen of Death)
  * Shutdown / Restart PC
  * Disable Windows Defender
  * Block Task Manager

---

#### 4. 🔄 SPREADING (3+ functions)
* **USB Spread:** Copies itself to USB drives
* **AutoRun:** Runs automatically when USB is inserted
* **Persistence:**
  * Starts automatically on Windows boot
  * Registry Run (Adds to Windows Registry)
  * Scheduled Task (Creates automatic task)

---

#### 5. 🛠️ EXTRA FUNCTIONS
* **Crypto Mining:** Bitcoin Miner (Uses victim's CPU to mine crypto)
* **Discord Injector:** Injects code into Discord client
* **Evasion & Defense:**
  * **Anti-Sandbox:** Detects and avoids virtual machines
  * **Anti-Debug:** Detects debuggers (Cheat Engine, OllyDbg, etc.)

---

### 📊 How it works

```text
1. Victim runs the file
   ↓
2. Hides console window
   ↓
3. Disables Windows Defender
   ↓
4. Adds itself to startup (registry + scheduled task)
   ↓
5. Sends victim info to Discord (hostname, IP, user, OS, CPU, RAM)
   ↓
6. Starts stealing data (browsers, wallets, passwords, etc.)
   ↓
7. Packs everything into a ZIP file
   ↓
8. Uploads ZIP to GoFile or sends via Discord
   ↓
9. Starts running background tasks:
   • Screenshot every 10 seconds
   • Webcam photo every 30 seconds
   • Keylogger (records all keys)
   • Clipboard monitoring
   • Bitcoin mining
   • USB spreading
   • Ransomware
   • System destruction
   ↓
10. Listens for commands from Discord:
    • Through Bot messages (!commands)
    • Through Webhook messages

```

```

```
# 📋 What is this part?
>>This is the Command & Control (C2) Server for the malware. It's a Discord Bot that acts as a remote control panel. The hacker uses this bot to send commands to infected victims.

# 🔧 How it works
1. Discord Bot runs on hacker's machine
   ↓
2. Bot connects to Discord using Token
   ↓
3. Bot listens for commands (!command)
   ↓
4. When hacker types !command:
   - Bot sends command to Webhook
   - Webhook forwards to infected victims
   - Victims execute the command
   - Results come back via Discord

# 📊 What it can do (ALL COMMANDS)

1. AUTHENTICATION
Command	Function
!login 109ontop	Authenticate to use the bot

2. STATUS & INFO
Command	Function
!status	Show bot status (online, victims, uptime)
!victims	List all connected victims
!info <ip>	Show detailed victim info
!history	Show command history
!clearhistory	Clear command history

3. SYSTEM CONTROL
Command	Function
!shell <ip> <cmd>	Execute CMD command on victim
!shutdown <ip>	Shutdown victim PC
!restart <ip>	Restart victim PC
!bsod <ip>	Blue Screen of Death
!lock <ip>	Lock victim screen

4. MONITORING
Command	Function
!screenshot <ip>	Take screenshot of victim
!webcam <ip>	Capture victim's webcam
!record <ip> [sec]	Record victim's screen
!keylog <ip>	Get keylogger data

5. FILE OPERATIONS
Command	Function
!download <ip> <file>	Download file from victim
!upload <ip> <file>	Upload file to victim
!deleteall <ip>	Delete all files on victim

6. DESTRUCTION
Command	Function
!ransomware <ip>	Encrypt victim's files
!destroy <ip>	Destroy system
!destroywindows <ip>	Destroy Windows only
!wipe <ip>	Wipe entire drive
!formatdrive <ip> [drive]	Format drive

7. CREDENTIALS
Command	Function
!creds <ip>	Dump all passwords
!rdp <ip>	Enable Remote Desktop
!backdoor <ip>	Create backdoor user

8. APPLICATIONS
Command	Function
!openapp <ip> <app>	Open application
!killapp <ip> <app>	Kill application
!disableav <ip>	Disable Antivirus

9. INPUT CONTROL
Command	Function
!disablekb <ip>	Disable keyboard
!enablekb <ip>	Enable keyboard
!disablemouse <ip>	Disable mouse
!enablemouse <ip>	Enable mouse

10. VOLUME CONTROL
Command	Function
!mute <ip>	Mute volume
!unmute <ip>	Unmute volume
!volume <ip> <0-100>	Set volume level

11. NETWORK
Command	Function
!network <ip>	Get network info
!ports <ip>	Scan open ports
!ping <ip>	Ping victim
!dns <ip>	Get DNS info

12. SERVICES
Command	Function
!services <ip>	List all services
!startservice <ip> <service>	Start a service
!stopservice <ip> <service>	Stop a service

13. TASKS
Command	Function
!tasklist <ip>	List all processes
!killpid <ip> <pid>	Kill process by PID

14. MASS ATTACK (ALL VICTIMS)
Command	Function
!screenshotall	Screenshot all victims
!shutdownall	Shutdown all victims
!restartall	Restart all victims
!destroyall	Destroy all victims
!destroywindowsall	Destroy Windows on all
!ransomwareall	Ransomware all victims

15. BROADCAST
Command	Function
!broadcast <cmd>	Send command to all victims

16. SECURITY
Command	Function
!blocktaskmgr <ip>Block Task Manager
!firewall <ip>	Check firewall status
!disablefirewall <ip>	Disable firewall

## 🚀 Quick Installation

Clone the repository:
```bash
git clone https://github.com/comk109/RAT-DISCORD-BOT-by109.git
```

Navigate to the directory:
```bash
cd RAT-DISCORD-BOT-by109
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### discord supprots
> dis > discord.gg/CWkGWU6U2z
