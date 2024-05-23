import os
import re
import time
import pickle
from colorama import Fore, Style

class DeskRam:
    def __init__(self):
        self.logo = self.generate_logo()

    def generate_logo(self):
        # Create a professional logo
        logo = f"""{Fore.GREEN}
 ▄▄▄· ▄▄▄· .▄▄ ·       ▄▄▄  ▄▄▄▄▄
▐█ ▄█▐█ ▀█ ▐█ ▀. ▪     ▀▄ █·•██  
 ██▀·▄█▀▀█ ▄▀▀▀█▄ ▄█▀▄ ▐▀▀▄  ▐█.▪
▐█▪·•▐█ ▪▐▌▐█▄▪▐█▐█▌.▐▌▐█•█▌ ▐█▌·
.▀    ▀  ▀  ▀▀▀▀  ▀█▄▀▪.▀  ▀ ▀▀▀ 
{Style.RESET_ALL}"""
        return logo

    def animate_text(self, text, delay=0.05):
        # Animation for printing text
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def input_text_animation(self, text, delay=0.05):
        # Animation for INPUT prompt
        input_text = f"{Fore.BLUE}{text}{Style.RESET_ALL}"
        for char in input_text:
            print(char, end='', flush=True)
            time.sleep(delay)
        user_input = input()
        return user_input

    
    def extract_subdomains_and_ips(self, input_file):
        subdomains = set()
        ip_addresses = set()
        network_ranges = set()
        domain_pattern = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,6}\b", re.IGNORECASE)
        ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
        network_range_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b")
        with open(input_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            clean_line = self.clean_line(line)
            matches = domain_pattern.findall(clean_line)
            for match in matches:
                subdomains.add(match)
            ip_matches = ip_pattern.findall(clean_line)
            for ip_match in ip_matches:
                ip_addresses.add(ip_match)
            network_range_matches = network_range_pattern.findall(clean_line)
            for network_range_match in network_range_matches:
                network_ranges.add(network_range_match)
        return sorted(subdomains), sorted(ip_addresses), sorted(network_ranges)

    def clean_line(self, line):
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        return ansi_escape.sub('', line)

    def save_to_file(self, data, output_file):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            for item in data:
                f.write("%s\n" % item)

    def load_previous_results(self, pickle_file):
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                return pickle.load(f)
        else:
            return None

    def save_current_results(self, pickle_file, data):
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)

    def main(self):
        print(self.logo)
        self.animate_text(f"{Fore.YELLOW}Dev Py >> DeskRam", delay=0.05)
        input_file = self.input_text_animation("Enter the path of the input file: ")
        output_folder = self.input_text_animation("Enter the path of the output folder: ")
        pickle_file = os.path.join(output_folder, f"{input_file[:-3]}_previous_results.pkl")

        previous_results = self.load_previous_results(pickle_file)

        if previous_results:
            subdomains, ip_addresses, network_ranges = previous_results
            self.animate_text("Previous results loaded.", delay=0.05)
        else:
            subdomains, ip_addresses, network_ranges = self.extract_subdomains_and_ips(input_file)

        subdomains_output_file = os.path.join(output_folder, input_file)
        ip_output_file = os.path.join(output_folder, f"ip_addresses_{input_file}")
        network_range_output_file = os.path.join(output_folder, f"network_ranges_{input_file}")
        self.save_to_file(subdomains, subdomains_output_file)
        self.save_to_file(ip_addresses, ip_output_file)
        self.save_to_file(network_ranges, network_range_output_file)

        self.animate_text(f"{Fore.CYAN}Subdomains saved to: {subdomains_output_file}", delay=0.05)
        self.animate_text(f"{Fore.CYAN}IP addresses saved to: {ip_output_file}", delay=0.05)
        self.animate_text(f"{Fore.CYAN}Network ranges saved to: {network_range_output_file}", delay=0.05)

        current_results = (subdomains, ip_addresses, network_ranges)
        self.save_current_results(pickle_file, current_results)
        self.animate_text(f"{Fore.GREEN}Current results saved.", delay=0.05)

if __name__ == "__main__":
    try:
        desk_ram = DeskRam()
        desk_ram.main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Exiting.. ")