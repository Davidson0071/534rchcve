from vulners import VulnersApi
import os
from prettytable import PrettyTable
from termcolor import colored
import sys
import time

def print_banner():
    banner = """
███████╗██████╗ ██╗  ██╗██████╗  ██████╗██╗  ██╗ ██████╗██╗   ██╗███████╗
██╔════╝╚════██╗██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██║   ██║██╔════╝
███████╗ █████╔╝███████║██████╔╝██║     ███████║██║     ██║   ██║█████╗  
╚════██║ ╚═══██╗╚════██║██╔══██╗██║     ██╔══██║██║     ╚██╗ ██╔╝██╔══╝  
███████║██████╔╝     ██║██║  ██║╚██████╗██║  ██║╚██████╗ ╚████╔╝ ███████╗
╚══════╝╚═════╝      ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚═══╝  ╚══════╝
                                                                         
    """
    print(colored(banner, 'cyan'))
    print(colored("Developed by: ", 'white') + colored("D4X3D", 'green'))
    print(colored("GitHub: ", 'white') + colored("https://github.com/d4x3d", 'blue'))
    print("\n" + "="*80 + "\n")

def load_api_key():
    try:
        if not os.path.exists('api.txt'):
            key = input(colored("Please enter your Vulners API key: ", 'yellow'))
            with open('api.txt', 'w') as f:
                f.write(key)
            print(colored("\n[+] API key saved successfully!", 'green'))
        else:
            with open('api.txt', 'r') as f:
                key = f.read().strip()
        return key
    except Exception as e:
        print(colored(f"\n[-] Error loading API key: {str(e)}", 'red'))
        sys.exit(1)

def get_search_parameters():
    query = input(colored("\nEnter search query (e.g., 'php 8.1'): ", 'yellow'))
    while True:
        try:
            limit = int(input(colored("Enter result limit (3-5 recommended): ", 'yellow')))
            if limit < 1:
                print(colored("[-] Limit must be at least 1", 'red'))
                continue
            break
        except ValueError:
            print(colored("[-] Please enter a valid number", 'red'))
    return query, limit

def search_vulnerabilities(api_key, query, limit):
    try:
        vulners_api = VulnersApi(api_key=api_key)
        results = vulners_api.find_all(query=query, limit=limit)
        return results
    except Exception as e:
        print(colored(f"\n[-] Error during search: {str(e)}", 'red'))
        return None

def get_cvss_score(result):

    cvss = result.get('cvss')
    if isinstance(cvss, dict):
       
        for key in ['score', 'baseScore', 'cvss', 'CVSS']:
            if key in cvss:
                return str(cvss[key])
        return 'N/A'
    elif cvss is not None:
        return str(cvss)
    return 'N/A'

def display_results(results):
    if not results:
        print(colored("\n[-] No results found", 'red'))
        return

    table = PrettyTable()
    table.field_names = [
        colored("Title", 'cyan'),
        colored("CVSS", 'yellow'),
        colored("CVE List", 'green'),
        colored("Type", 'magenta'),
        colored("URL", 'blue')
    ]
    table.align = "l"
    table.max_width = 40

    for result in results:
        cvss_str = get_cvss_score(result)
        
        if cvss_str == 'N/A':
            cvss_colored = colored(cvss_str, 'white')
        else:
            try:
                cvss_float = float(cvss_str)
                cvss_colored = colored(cvss_str, 
                                    'red' if cvss_float >= 7.0 else
                                    'yellow' if cvss_float >= 4.0 else
                                    'green')
            except ValueError:
                cvss_colored = colored(cvss_str, 'white')
        
        table.add_row([
            result.get('title', 'N/A')[:40] + ('...' if len(result.get('title', '')) > 40 else ''),
            cvss_colored,
            '\n'.join(result.get('cvelist', ['N/A']))[:30],
            result.get('bulletinFamily', 'N/A'),
            result.get('href', 'N/A')[:40]
        ])

    print("\n" + str(table))

def main():
    print_banner()
    api_key = load_api_key()
    
    while True:
        query, limit = get_search_parameters()
        print(colored("\n[+] Searching...", 'cyan'))
        time.sleep(1)  # Add a small delay for better UX
        
        results = search_vulnerabilities(api_key, query, limit)
        if results:
            display_results(results)
        
        if input(colored("\nWould you like to perform another search? (y/n): ", 'yellow')).lower() != 'y':
            break
    
    print(colored("\nThanks  534rchCVE! Goodbye!\n", 'green'))

if __name__ == "__main__":
	main()