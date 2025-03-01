#!/usr/bin/env python3
import os
import sys
import time
import argparse
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
║ Author: Your Name                             ║
║ GitHub: github.com/yourusername/auto-sqlmap-pro║
╚═══════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        
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

    def full_auto_scan(self):
        console.print("\n[bold cyan]Full Automatic Scan[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        
        options = [
            "--batch",
            "--random-agent",
            "--level=5",
            "--risk=3",
            "--threads=10",
            "--tamper=space2comment,between",
            "--time-sec=10",
            "--dbs"
        ]
        
        command = f"sqlmap -u {target} {' '.join(options)}"
        self.execute_command(command)

    def database_enumeration(self):
        console.print("\n[bold cyan]Database Enumeration[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        command = f"sqlmap -u {target} --batch --random-agent --dbs"
        self.execute_command(command)

    def table_enumeration(self):
        console.print("\n[bold cyan]Table Enumeration[/bold cyan]")
        target = console.input("[bold green]Enter target URL: [/bold green]")
        database = console.input("[bold green]Enter database name: [/bold green]")
        command = f"sqlmap -u {target} --batch --random-agent -D {database} --tables"
        self.execute_command(command)

    def execute_command(self, command):
        console.print(f"\n[bold yellow]Executing:[/bold yellow] {command}")
        os.system(command)
        console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")

def main():
    tool = AutoSQLMap()
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(tool.banner)
        tool.show_menu()
        choice = console.input("\n[bold green]Select an option: [/bold green]")
        
        options = {
            "1": tool.full_auto_scan,
            "2": tool.database_enumeration,
            "3": tool.table_enumeration
        }
        
        if choice in options:
            options[choice]()
        elif choice == "8":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main()
