import argparse
import ngup  # this is the official Ngup module, you can use it with: ngup.hash("<your_hash_file>")
import hashlib
import requests
import os
import sys
import mimetypes
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = r"""{color}
    )                      
 ( /(                      
 )\()) (  (     (          
((_)\  )\))(   ))\  `  )   
 _((_)((_))\  /((_) /(/(   
| \| | (()(_)(_))( ((_)_\  
| .` |/ _` | | || || '_ \) 
|_|\_|\__, |  \_,_|| .__/  
      |___/        |_|     
""".replace("{color}", Fore.CYAN) + Style.RESET_ALL

def get_hashes(filepath):
    hashes = {
        'md5': hashlib.md5(),
        'sha1': hashlib.sha1(),
        'sha256': hashlib.sha256(),
        'sha512': hashlib.sha512()
    }
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            for h in hashes.values():
                h.update(chunk)
    return {name: h.hexdigest() for name, h in hashes.items()}

def get_file_info(filepath):
    size = os.path.getsize(filepath)
    mime_type, _ = mimetypes.guess_type(filepath)
    stat_info = os.stat(filepath)
    readable = os.access(filepath, os.R_OK)
    writable = os.access(filepath, os.W_OK)
    executable = os.access(filepath, os.X_OK)

    def ts(t): return datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

    line_count = None
    try:
        with open(filepath, 'r', errors='ignore') as f:
            line_count = sum(1 for _ in f)
    except:
        line_count = "N/A (binary or unreadable)"

    return {
        'filename': os.path.basename(filepath),
        'abspath': os.path.abspath(filepath),
        'filesize': size,
        'mime': mime_type or "Unknown",
        'created': ts(stat_info.st_ctime),
        'modified': ts(stat_info.st_mtime),
        'accessed': ts(stat_info.st_atime),
        'readable': readable,
        'writable': writable,
        'executable': executable,
        'lines': line_count
    }

def check_malwarebazaar(sha256):
    url = "https://mb-api.abuse.ch/api/v1/"
    data = {"query": "get_info", "hash": sha256}
    try:
        res = requests.post(url, data=data)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"{Fore.RED}[!] API error: {e}{Style.RESET_ALL}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="PyNgup - File hash & malware lookup")
    parser.add_argument('--get', action='store_true', help="Analyze file & check if it's malicious")
    parser.add_argument('--hash', action='store_true', help="Lookup hash")
    parser.add_argument('-i', metavar='FILE', help="Path to the file to scan")
    parser.add_argument('-t', metavar='HASH', help="Hash to lookup")

    args = parser.parse_args()

    print(BANNER)

    if args.get and args.i:
        path = args.i
        if not os.path.isfile(path):
            print(f"{Fore.RED}[!] File not found: {path}{Style.RESET_ALL}")
            sys.exit(1)

        info = get_file_info(path)
        print(f"{Fore.YELLOW}[+] Analyzing file: {info['filename']}\n{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    ➤ Absolute path : {info['abspath']}")
        print(f"    ➤ Size          : {info['filesize']} bytes")
        print(f"    ➤ MIME type     : {info['mime']}")
        print(f"    ➤ Created        : {info['created']}")
        print(f"    ➤ Modified       : {info['modified']}")
        print(f"    ➤ Accessed       : {info['accessed']}")
        print(f"    ➤ Readable       : {info['readable']}")
        print(f"    ➤ Writable       : {info['writable']}")
        print(f"    ➤ Executable     : {info['executable']}")
        print(f"    ➤ Line count     : {info['lines']}\n{Style.RESET_ALL}")

        hashes = get_hashes(path)
        print(f"{Fore.YELLOW}[+] Hashes:{Style.RESET_ALL}")
        for algo, val in hashes.items():
            print(f"{Fore.BLUE}    {algo.upper():<8}: {val}{Style.RESET_ALL}")

        print(f"\n{Fore.YELLOW}[*] Checking SHA256...{Style.RESET_ALL}")
        result = check_malwarebazaar(hashes['sha256'])

        if result["query_status"] == "ok":
            data = result["data"][0]
            print(f"{Fore.RED}[🚨] MALICIOUS FILE DETECTED!{Style.RESET_ALL}\n")
            
            malware_family = data.get('malware_family', 'Unknown')
            signature = data.get('signature', 'No signature available')
            first_seen = data.get('first_seen', 'Unknown')
            tags = ', '.join(data.get('tags', ['None']))

            print(f"{Fore.RED}    ➤ Malware family : {malware_family}")
            print(f"{Fore.RED}    ➤ Signature      : {signature}")
            print(f"{Fore.RED}    ➤ First seen     : {first_seen}")
            print(f"{Fore.RED}    ➤ Tags           : {tags}{Style.RESET_ALL}")
        elif result["query_status"] == "hash_not_found":
            print(f"{Fore.GREEN}[✅] File not found (probably clean){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Unexpected response: {result['query_status']}{Style.RESET_ALL}")

    elif args.hash and args.t:
        hash_value = args.t
        print(f"{Fore.YELLOW}[*] Checking hash {hash_value}...{Style.RESET_ALL}")
        result = check_malwarebazaar(hash_value)

        if result["query_status"] == "ok":
            data = result["data"][0]
            print(f"{Fore.RED}[🚨] MALICIOUS HASH DETECTED!{Style.RESET_ALL}\n")
            
            malware_family = data.get('malware_family', 'Unknown')
            signature = data.get('signature', 'No signature available')
            first_seen = data.get('first_seen', 'Unknown')
            tags = ', '.join(data.get('tags', ['None']))

            print(f"{Fore.RED}    ➤ Malware family : {malware_family}")
            print(f"{Fore.RED}    ➤ Signature      : {signature}")
            print(f"{Fore.RED}    ➤ First seen     : {first_seen}")
            print(f"{Fore.RED}    ➤ Tags           : {tags}{Style.RESET_ALL}")
        elif result["query_status"] == "hash_not_found":
            print(f"{Fore.GREEN}[✅] Hash not found (probably clean){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Unexpected response: {result['query_status']}{Style.RESET_ALL}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
    

