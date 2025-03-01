#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table

init(autoreset=True)
console = Console()

class AutoSQLMap:
    def __init__(self):
        self.banner = f"""
{Fore.CYAN}
╔═══════════════════════════════════════════════╗
║             Auto SQLMap Pro v2.0              ║
║         Advanced Penetration Testing          ║
╠═══════════════════════════════════════════════╣
║ Author: LIMBO-2018                           ║
║ GitHub: github.com/LIMBO-2018/auto-sqlmap-pro║
╚═══════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        self.settings = {
            "threads": 10,
            "level": 5,
            "risk": 3,
            "tamper": "space2comment,between",
            "time_sec": 10,
            "proxy": None,
            "tor": False
        }

    def verify_sqlmap(self):
        try:
            subprocess.run(['sqlmap', '--version'], capture_output=True)
            return True
        except FileNotFoundError:
            console.print("[bold red]SQLMap not found! Please install SQLMap first.[/bold red]")
            return False

    def show_menu(self):
        table = Table(title="Available Options")
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="green")
        
        options = [
            ["1", "Full Automatic Scan"],
            ["2", "Database Enumeration"],
            ["3", "Table Enumeration"],
            ["4", "Column Enumeration"],
            ["5", "Data Dumping"],
            ["6", "Custom Attack"],
            ["7", "Configure Settings"],
            ["8", "Exit"]
        ]
        
        for opt in options:
            table.add_row(opt[0], opt[1])
        
        console.print(table)

    def get_base_options(self):
        return [
            "--batch",
            "--random-agent",
            f"--level={self.settings['level']}",
            f"--risk={self.settings['risk']}",
            f"--threads={self.settings['threads']}",
            f"--tamper={self.settings['tamper']}",
            f"--time-sec={self.settings['time_sec']}"
        ]

    def full_auto_scan(self):
        console.print("\n[bold cyan]Full Automatic Scan[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        options = self.get_base_options() + ["--dbs", "--tables", "--dump"]
        command = f"sqlmap -u {target} {' '.join(options)}"
        self.execute_command(command)

    def database_enumeration(self):
        console.print("\n[bold cyan]Database Enumeration[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        options = self.get_base_options() + ["--dbs"]
        command = f"sqlmap -u {target} {' '.join(options)}"
        self.execute_command(command)

    def table_enumeration(self):
        console.print("\n[bold cyan]Table Enumeration[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        database = console.input("[bold green]Enter database name: [/bold green]")
        options = self.get_base_options() + [f"-D {database}", "--tables"]
        command = f"sqlmap -u {target} {' '.join(options)}"
        self.execute_command(command)

    def column_enumeration(self):
        console.print("\n[bold cyan]Column Enumeration[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        database = console.input("[bold green]Enter database name: [/bold green]")
        table = console.input("[bold green]Enter table name: [/bold green]")
        options = self.get_base_options() + [f"-D {database}", f"-T {table}", "--columns"]
        command = f"sqlmap -u {target} {' '.join(options)}"
        self.execute_command(command)

    def data_dumping(self):
        console.print("\n[bold cyan]Data Dumping[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        database = console.input("[bold green]Enter database name: [/bold green]")
        table = console.input("[bold green]Enter table name: [/bold green]")
        columns = console.input("[bold green]Enter column names (comma-separated) or * for all: [/bold green]")
        options = self.get_base_options() + [f"-D {database}", f"-T {table}"]
        if columns != "*":
            options.append(f"-C {columns}")
        options.append("--dump")
        command = f"sqlmap -u {target} {' '.join(options)}"
        self.execute_command(command)

    def custom_attack(self):
        console.print("\n[bold cyan]Custom Attack[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        custom_params = console.input("[bold green]Enter custom SQLMap parameters: [/bold green]")
        command = f"sqlmap -u {target} {custom_params}"
        self.execute_command(command)

    def configure_settings(self):
        console.print("\n[bold cyan]Configure Settings[/bold cyan]")
        self.settings["threads"] = int(console.input(f"[bold green]Enter number of threads ({self.settings['threads']}): [/bold green]") or self.settings["threads"])
        self.settings["level"] = int(console.input(f"[bold green]Enter level (1-5) ({self.settings['level']}): [/bold green]") or self.settings["level"])
        self.settings["risk"] = int(console.input(f"[bold green]Enter risk (1-3) ({self.settings['risk']}): [/bold green]") or self.settings["risk"])
        self.settings["tamper"] = console.input(f"[bold green]Enter tamper scripts ({self.settings['tamper']}): [/bold green]") or self.settings["tamper"]
        self.settings["time_sec"] = int(console.input(f"[bold green]Enter time delay ({self.settings['time_sec']}): [/bold green]") or self.settings["time_sec"])
        self.settings["proxy"] = console.input("[bold green]Enter proxy (e.g., http://127.0.0.1:8080) or press Enter to skip: [/bold green]") or None
        self.settings["tor"] = console.input("[bold green]Use Tor? (y/N): [/bold green]").lower() == 'y'
        console.print("[bold green]Settings updated successfully![/bold green]")

    def execute_command(self, command):
        if self.settings["proxy"]:
            command += f" --proxy={self.settings['proxy']}"
        if self.settings["tor"]:
            command += " --tor --check-tor"
            
        console.print(f"\n[bold yellow]Executing:[/bold yellow] {command}")
        try:
            process = subprocess.run(command, shell=True)
            if process.returncode != 0:
                console.print("[bold red]Command execution failed![/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")

def main():
    tool = AutoSQLMap()
    if not tool.verify_sqlmap():
        sys.exit(1)

    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(tool.banner)
        tool.show_menu()
        choice = console.input("\n[bold green]Select an option: [/bold green]")
        
        options = {
            "1": tool.full_auto_scan,
            "2": tool.database_enumeration,
            "3": tool.table_enumeration,
            "4": tool.column_enumeration,
            "5": tool.data_dumping,
            "6": tool.custom_attack,
            "7": tool.configure_settings
        }
        
        if choice in options:
            options[choice]()
        elif choice == "8":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid option! Please try again.[/bold red]")
            time.sleep(2)

if __name__ == "__main__":
    main()
