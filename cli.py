import sys
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import print as rprint
from rich.layout import Layout
from rich.align import Align
from rich.text import Text

from bank_backend import Bank

console = Console()

def print_header(title, style="bold cyan"):
    console.print(Panel(Align.center(f"[{style}]{title}[/{style}]"), border_style="cyan"))

def loader(text="Processing..."):
    with console.status(f"[bold green]{text}[/bold green]", spinner="dots"):
        sleep(1)

def create_account():
    print_header("ACCOUNT REGISTRATION MODULE", style="bold green")
    
    name = Prompt.ask("[bold blue]Enter your full name[/bold blue]").strip()
    
    while True:
        try:
            age = IntPrompt.ask("[bold blue]Enter your age for account creation[/bold blue]")
            if age < 18:
                console.print("[bold red]Age validation failed. You must be at least 18 years old.[/bold red]")
                return
            console.print("[bold green]✔ Age validated successfully. Proceeding to account setup.[/bold green]")
            break
        except ValueError:
            console.print("[bold red]Invalid input. Age must be a number.[/bold red]")

    email = Prompt.ask("[bold blue]Enter your email address[/bold blue]").strip()
    phone = Prompt.ask("[bold blue]Enter your phone number[/bold blue]").strip()
    address = Prompt.ask("[bold blue]Enter your residential address[/bold blue]").strip()
    
    acc_type_choice = Prompt.ask("[bold blue]Select Account Type (1: Savings, 2: Current)[/bold blue]", choices=["1", "2"], default="1")
    acc_type = "Savings" if acc_type_choice == "1" else "Current"
    
    while True:
        pin = Prompt.ask("[bold blue]Please set up a secure 4-digit PIN[/bold blue]", password=True).strip()
        if len(pin) == 4 and pin.isdigit():
            console.print("[bold green]✔ PIN verified successfully.[/bold green]")
            break
        console.print("[bold red]Invalid input. PIN must be exactly 4 digits.[/bold red]")

    loader("Registering account in VaultX...")
    user, msg = Bank.create_account(name, age, email, pin, phone, address, acc_type)
    
    if user:
        console.print(f"\n[bold green]{msg}[/bold green]")
        
        table = Table(title="Account Details", show_header=False, box=None)
        table.add_column("Key", style="bold cyan")
        table.add_column("Value", style="bold yellow")
        for k, v in user.items():
            if k == 'transactions': continue
            table.add_row(k.capitalize(), str(v))
        
        console.print(Panel(table, border_style="green", title="SUCCESS"))
        console.print("[bold magenta]IMPORTANT: Please note down your Account Number![/bold magenta]\n")
    else:
        console.print(f"[bold red]Registration Failed: {msg}[/bold red]")

def _get_credentials():
    print_header("AUTHENTICATION & PIN VERIFICATION", style="bold yellow")
    acc_no = Prompt.ask("[bold blue]Enter your Account Number or Email[/bold blue]").strip()
    pin = Prompt.ask("[bold blue]Please enter your secure 4-digit PIN[/bold blue]", password=True).strip()
    return acc_no, pin

def deposit_money():
    acc_no, pin = _get_credentials()
    if not acc_no: return

    amount = IntPrompt.ask("[bold blue]Enter deposit amount (₹)[/bold blue]")

    loader("Verifying and depositing funds...")
    success, msg = Bank.deposit(acc_no, pin, amount)
    
    if success:
        console.print(f"[bold green]✔ {msg}[/bold green]\n")
    else:
        console.print(f"[bold red]✖ {msg}[/bold red]\n")

def withdraw_money():
    acc_no, pin = _get_credentials()
    if not acc_no: return

    amount = IntPrompt.ask("[bold blue]Enter withdrawal amount (₹)[/bold blue]")

    loader("Verifying and processing withdrawal...")
    success, msg = Bank.withdraw(acc_no, pin, amount)
    
    if success:
        console.print(f"[bold green]✔ {msg}[/bold green]\n")
    else:
        console.print(f"[bold red]✖ {msg}[/bold red]\n")

def show_details():
    acc_no, pin = _get_credentials()
    if not acc_no: return

    loader("Fetching Ledger Status...")
    user = Bank.find_user(acc_no, pin)
    if not user:
        console.print("[bold red]✖ Authentication Failed. Invalid account number or PIN.[/bold red]\n")
        return

    table = Table(title="LIVE LEDGER STATUS", title_style="bold cyan", border_style="cyan")
    table.add_column("Information", style="bold magenta")
    table.add_column("Details", style="bold white")

    for k, v in user.items():
        if k == 'transactions': continue
        if k == 'balance':
            table.add_row(k.capitalize(), f"[bold green]₹{v}[/bold green]")
        else:
            table.add_row(k.capitalize(), str(v))
            
    console.print(table)
    console.print("\n")

def update_details():
    acc_no, pin = _get_credentials()
    if not acc_no: return

    user = Bank.find_user(acc_no, pin)
    if not user:
        console.print("[bold red]✖ Authentication Failed. Invalid account number or PIN.[/bold red]\n")
        return

    print_header("ACCOUNT MODIFICATION UTILITY", style="bold cyan")
    console.print("[italic yellow]Leave a field blank to keep current information.[/italic yellow]")
    name = Prompt.ask("[bold blue]New full name[/bold blue]", default="").strip()
    email = Prompt.ask("[bold blue]New email address[/bold blue]", default="").strip()
    phone = Prompt.ask("[bold blue]New phone number[/bold blue]", default="").strip()
    address = Prompt.ask("[bold blue]New residential address[/bold blue]", default="").strip()
    new_pin = Prompt.ask("[bold blue]New 4-digit PIN[/bold blue]", password=True, default="").strip()

    loader("Updating Account Records...")
    success, msg = Bank.update_user(acc_no, pin, name, email, new_pin, phone, address)
    
    if success:
        console.print(f"[bold green]✔ {msg}[/bold green]\n")
    else:
        console.print(f"[bold red]✖ {msg}[/bold red]\n")

def delete_account():
    acc_no, pin = _get_credentials()
    if not acc_no: return

    user = Bank.find_user(acc_no, pin)
    if not user:
        console.print("[bold red]✖ Authentication Failed. Invalid account number or PIN.[/bold red]\n")
        return

    print_header("ACCOUNT TERMINATION UTILITY", style="bold red")
    check = Confirm.ask("[bold red]Are you sure you want to delete your account? This action is irreversible![/bold red]")
    
    if not check:
        console.print("[bold yellow]Operation cancelled. Account was NOT deleted.[/bold yellow]\n")
        return

    loader("Erasing Account Data...")
    success, msg = Bank.delete_user(acc_no, pin)
    
    if success:
        console.print(f"[bold green]✔ {msg}[/bold green]\n")
    else:
        console.print(f"[bold red]✖ {msg}[/bold red]\n")

def transfer_money():
    acc_no, pin = _get_credentials()
    if not acc_no: return

    target = Prompt.ask("[bold blue]Enter recipient's Account Number or Email[/bold blue]").strip()
    amount = IntPrompt.ask("[bold blue]Enter transfer amount (₹)[/bold blue]")

    loader("Processing transfer...")
    success, msg = Bank.transfer(acc_no, pin, target, amount)
    
    if success:
        console.print(f"[bold green]✔ {msg}[/bold green]\n")
    else:
        console.print(f"[bold red]✖ {msg}[/bold red]\n")

def show_history():
    acc_no, pin = _get_credentials()
    if not acc_no: return

    loader("Fetching Transaction Records...")
    user = Bank.find_user(acc_no, pin)
    if not user:
        console.print("[bold red]✖ Authentication Failed. Invalid account number or PIN.[/bold red]\n")
        return

    txs = user.get("transactions", [])
    if not txs:
        console.print("[bold yellow]No transaction records found.[/bold yellow]\n")
        return
        
    table = Table(title="TRANSACTION HISTORY", title_style="bold cyan", border_style="cyan")
    table.add_column("Date", style="dim")
    table.add_column("Type", style="bold magenta")
    table.add_column("Amount", style="bold green", justify="right")
    table.add_column("Balance", style="bold yellow", justify="right")
    table.add_column("Details", style="italic")

    for t in txs:
        amt_str = f"₹{t['amount']}"
        if t['type'] in ['WITHDRAWAL', 'TRANSFER OUT']:
            amt_str = f"[red]-{amt_str}[/red]"
        elif t['type'] in ['DEPOSIT', 'TRANSFER IN']:
            amt_str = f"[green]+{amt_str}[/green]"
            
        table.add_row(
            t['date'],
            t['type'],
            amt_str,
            f"₹{t['balance']}",
            t.get('detail', '')
        )
            
    console.print(table)
    console.print("\n")

MENU = {
    "1": ("Register New Account", create_account),
    "2": ("Deposit Funds", deposit_money),
    "3": ("Withdraw Funds", withdraw_money),
    "4": ("Transfer Funds", transfer_money),
    "5": ("Balance Inquiry & Details", show_details),
    "6": ("Transaction History", show_history),
    "7": ("Modify Account Information", update_details),
    "8": ("Terminate Account", delete_account),
    "9": ("Exit System", None),
}

def display_main_menu():
    title = Text("VAULTX BANK MANAGER", justify="center", style="bold blue")
    subtitle = Text("Your Complete Console Banking Solution", justify="center", style="italic cyan")
    
    menu_table = Table(show_header=False, box=None, padding=(0, 2))
    menu_table.add_column("Key", style="bold magenta", justify="right")
    menu_table.add_column("Action", style="bold white")
    
    for key, (label, _) in MENU.items():
        if key == "9":
            menu_table.add_row(f"[{key}]", f"[red]{label}[/red]")
        else:
            menu_table.add_row(f"[{key}]", label)
            
    panel = Panel(
        Align.center(menu_table), 
        title=title, 
        subtitle=subtitle,
        border_style="blue", 
        padding=(1, 2)
    )
    console.print(panel)

def main():
    console.clear()
    while True:
        display_main_menu()

        choice = Prompt.ask("[bold cyan]Select an operation[/bold cyan]").strip()
        if choice == "9":
            console.print("\n[bold blue]Thank you for using VaultX Bank Manager.[/bold blue]")
            console.print("[italic green]Secure Logic. Clean Code. Reliable Banking.[/italic green]\n")
            sys.exit(0)

        entry = MENU.get(choice)
        if not entry:
            console.print("[bold red]Invalid operation. Please try again.[/bold red]\n")
            continue

        _, action = entry
        action()
        Prompt.ask("[italic dim]Press Enter to return to Main Menu...[/italic dim]")
        console.clear()

if __name__ == "__main__":
    main()
