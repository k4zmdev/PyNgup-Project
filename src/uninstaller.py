import os
import platform
import shutil
import subprocess
from colorama import Fore, init

init(autoreset=True)

def print_colored_message(message, color=Fore.GREEN):
    print(color + message)

def get_default_ngup_dir():
    if platform.system() == "Windows":
        return os.path.join(os.getenv("LOCALAPPDATA"), "Programs", "ngup")
    else:
        return os.path.expanduser("~/.local/bin/ngup")

def remove_ngup_dir(ngup_dir):
    if os.path.exists(ngup_dir):
        shutil.rmtree(ngup_dir)
        print_colored_message(f"[+] Deleted ngup directory: {ngup_dir}", Fore.RED)
    else:
        print_colored_message("[!] ngup directory not found.", Fore.YELLOW)

def remove_from_system_path(ngup_dir):
    if platform.system() == "Windows":
        print_colored_message("[~] Removing ngup folder from system PATH...", Fore.MAGENTA)
        # Lire la clé actuelle
        output = subprocess.check_output('reg query "HKCU\\Environment" /v PATH', shell=True).decode(errors='ignore')
        if "PATH" in output:
            current_path = output.split("    ")[-1].strip()
            new_path = current_path.replace(f";{ngup_dir}", "").replace(f"{ngup_dir};", "").replace(ngup_dir, "")
            reg_cmd = f'reg add "HKCU\\Environment" /v PATH /t REG_EXPAND_SZ /f /d "{new_path}"'
            subprocess.run(reg_cmd, shell=True)
            print_colored_message("[+] Removed ngup from system PATH (restart required).", Fore.GREEN)
        else:
            print_colored_message("[!] Could not read PATH from registry.", Fore.YELLOW)

def pause():
    input(Fore.YELLOW + "[Press Enter to finish uninstall...]")

def uninstall_ngup():
    print_colored_message("[i] Starting ngup uninstallation...", Fore.BLUE)
    ngup_dir = get_default_ngup_dir()
    remove_ngup_dir(ngup_dir)
    remove_from_system_path(ngup_dir)
    print_colored_message("[✓] ngup successfully uninstalled.", Fore.GREEN)
    pause()

if __name__ == "__main__":
    uninstall_ngup()
input("")
