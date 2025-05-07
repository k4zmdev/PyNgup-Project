import os
import platform
import subprocess
import shutil
from colorama import Fore, init

init(autoreset=True)

def print_colored_message(message, color=Fore.GREEN):
    print(color + message)

def pause():
    input(Fore.YELLOW + "[Press Enter to continue...]")

def get_default_ngup_dir():
    if platform.system() == "Windows":
        return os.path.join(os.getenv("LOCALAPPDATA"), "Programs", "ngup")
    else:
        return os.path.expanduser("~/.local/bin/ngup")

def create_ngup_dir(ngup_dir):
    if not os.path.exists(ngup_dir):
        os.makedirs(ngup_dir)
        print_colored_message(f"[+] Created directory: {ngup_dir}", Fore.CYAN)

def move_ngup_file(ngup_py_path, ngup_dir):
    destination = os.path.join(ngup_dir, "ngup.py")
    shutil.copy2(ngup_py_path, destination)
    print_colored_message(f"[+] Copied ngup.py to: {destination}", Fore.GREEN)
    return destination

def copy_requirements_if_exists(ngup_dir):
    if os.path.exists("requirements.txt"):
        shutil.copy2("requirements.txt", os.path.join(ngup_dir, "requirements.txt"))
        print_colored_message("[+] Copied requirements.txt to ngup folder.", Fore.GREEN)
        return True
    return False

def install_dependencies(ngup_dir):
    req_path = os.path.join(ngup_dir, "requirements.txt")
    if os.path.exists(req_path):
        print_colored_message("[~] Installing dependencies from requirements.txt...", Fore.MAGENTA)
        subprocess.run(f'pip install -r "{req_path}"', shell=True)
        print_colored_message("[+] Dependencies installed successfully.", Fore.GREEN)
    else:
        print_colored_message("[!] No requirements.txt found, skipping dependency install.", Fore.YELLOW)

def add_to_path(ngup_dir):
    current_path = os.environ.get("PATH", "")
    if ngup_dir not in current_path:
        os.environ["PATH"] = ngup_dir + os.pathsep + current_path
        print_colored_message(f"[+] Added {ngup_dir} to PATH for current session.", Fore.CYAN)

def add_to_system_path(ngup_dir):
    if platform.system() == "Windows":
        print_colored_message("[~] Adding ngup folder to system PATH...", Fore.MAGENTA)
        reg_cmd = f'reg add "HKCU\\Environment" /v PATH /t REG_EXPAND_SZ /f /d "%PATH%;{ngup_dir}"'
        subprocess.run(reg_cmd, shell=True)
        print_colored_message("[+] Added to system PATH (restart required).", Fore.GREEN)

def create_ngup_batch(ngup_dir):
    batch_file = os.path.join(ngup_dir, "ngup.bat")
    with open(batch_file, "w") as f:
        f.write(f'@echo off\npython "{ngup_dir}\\ngup.py" %*\n')
    print_colored_message(f"[+] Created ngup.bat for global command usage: {batch_file}", Fore.CYAN)

def setup_ngup():
    username = os.getenv("USERNAME") or os.getenv("USER")
    print_colored_message(f"[i] Setting up ngup for user: {username}", Fore.BLUE)

    ngup_py_path = os.path.join(os.getcwd(), "ngup.py")
    if not os.path.exists(ngup_py_path):
        print_colored_message("[x] ngup.py not found in current directory!", Fore.RED)
        return

    ngup_dir = get_default_ngup_dir()
    create_ngup_dir(ngup_dir)
    move_ngup_file(ngup_py_path, ngup_dir)
    has_requirements = copy_requirements_if_exists(ngup_dir)

    add_to_path(ngup_dir)
    add_to_system_path(ngup_dir)
    create_ngup_batch(ngup_dir)

    if has_requirements:
        install_dependencies(ngup_dir)

    print_colored_message("[✓] ngup is now globally accessible via CMD as 'ngup'", Fore.GREEN)
    pause()

if __name__ == "__main__":
    setup_ngup()
input("")
