#!/usr/bin/env python3
"""
Real-Time Keylogger Detection System
Team: The Cyber Avengers
"""

import psutil
import os
import sys
import re
import time
from datetime import datetime

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

SUSPICIOUS_FILES = ['keystrokes.log', 'key_log.txt', 'keylog.txt']
SUSPICIOUS_KEYWORDS = ['keylog', 'pynput', 'keyboard.Listener']

def print_banner():
    """Display detection system banner"""
    print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ██████╗ ███████╗████████╗███████╗ ██████╗████████╗         ║
║    ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝         ║
║    ██║  ██║█████╗     ██║   █████╗  ██║        ██║            ║
║    ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║            ║
║    ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║            ║
║    ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝            ║
║                                                               ║
║            {Colors.GREEN}🛡  DEFENSIVE SECURITY TOOL  🛡{Colors.RED}                      ║
║                                                               ║
║           {Colors.MAGENTA}━━━━  THE CYBER AVENGERS  ━━━━{Colors.RED}                      ║
║          {Colors.CYAN}Auto-Termination Protection Active{Colors.RED}                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def print_team_credits():
    """Display team member credits"""
    print(f"{Colors.MAGENTA}┌─────────────────────────────────────────────────────────────┐")
    print(f"│  {Colors.BOLD}Defensive Team Members{Colors.RESET}{Colors.MAGENTA}                                     │")
    print(f"├─────────────────────────────────────────────────────────────┤")
    print(f"│  {Colors.CYAN}• Ajay Pratap Singh{Colors.MAGENTA}                                       │")
    print(f"│  {Colors.CYAN}• Kaushal Kumar{Colors.MAGENTA}                                                 │")
    print(f"└─────────────────────────────────────────────────────────────┘{Colors.RESET}\n")

def print_monitor_info():
    """Display monitoring information"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗")
    print(f"║  {Colors.WHITE}{Colors.BOLD}REAL-TIME MONITORING ACTIVE{Colors.RESET}{Colors.CYAN}                                  ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.GREEN}[✓] Started:         {Colors.WHITE}{timestamp}{Colors.CYAN}                     ║")
    print(f"║  {Colors.GREEN}[✓] Mode:            {Colors.WHITE}Real-time + Auto-Termination{Colors.CYAN}            ║")
    print(f"║  {Colors.GREEN}[✓] Scan Interval:   {Colors.WHITE}Every 2 seconds{Colors.CYAN}                         ║")
    print(f"║  {Colors.RED}[!] Auto-Kill:       {Colors.WHITE}Enabled for suspicious activity{Colors.CYAN}         ║")
    print(f"║  {Colors.YELLOW}[!] Press Ctrl+C to stop monitoring{Colors.CYAN}                          ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

def analyze_latest_entry(filename):
    """Analyze the most recent entry in log file"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        entries = content.split('─' * 60)
        
        if len(entries) < 2:
            return None
        
        last_entry = entries[-2]
        
        username_match = re.search(r'Username: (.+)', last_entry)
        user_status_match = re.search(r'Username_Status: (.+)', last_entry)
        password_match = re.search(r'Password: (.+)', last_entry)
        pass_status_match = re.search(r'Password_Status: (.+)', last_entry)
        status_match = re.search(r'Overall_Status: (.+)', last_entry)
        timestamp_match = re.search(r'\[(\d{2}:\d{2}:\d{2})\]', last_entry)
        
        if username_match and status_match:
            return {
                'timestamp': timestamp_match.group(1) if timestamp_match else 'Unknown',
                'username': username_match.group(1).strip(),
                'user_status': user_status_match.group(1).strip() if user_status_match else 'Unknown',
                'password': password_match.group(1).strip() if password_match else '',
                'pass_status': pass_status_match.group(1).strip() if pass_status_match else 'Unknown',
                'overall_status': status_match.group(1).strip()
            }
        
        return None
        
    except:
        return None

def find_keylogger_processes():
    """Find all suspicious keylogger processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info['name']
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            
            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword.lower() in name.lower() or keyword.lower() in cmdline.lower():
                    processes.append({'pid': proc.info['pid'], 'name': name, 'cmdline': cmdline})
                    break
        except:
            continue
    return processes

def terminate_process(pid):
    """Terminate process immediately"""
    try:
        process = psutil.Process(pid)
        process.terminate()
        gone, alive = psutil.wait_procs([process], timeout=3)
        
        if alive:
            for p in alive:
                p.kill()
        
        return True
    except:
        return False

def auto_terminate_threat():
    """Automatically terminate keylogger when threat detected"""
    print(f"\n{Colors.RED}{Colors.BOLD}{'═' * 63}")
    print(f"  ⚠  INITIATING AUTO-TERMINATION SEQUENCE  ⚠")
    print(f"{'═' * 63}{Colors.RESET}\n")
    
    processes = find_keylogger_processes()
    
    if processes:
        for proc in processes:
            print(f"{Colors.YELLOW}[*] Target: PID {proc['pid']} ({proc['name']}){Colors.RESET}")
            print(f"{Colors.BLUE}[*] Terminating process...{Colors.RESET} ", end='', flush=True)
            
            if terminate_process(proc['pid']):
                print(f"{Colors.GREEN}✓ TERMINATED{Colors.RESET}")
            else:
                print(f"{Colors.RED}✗ FAILED{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}[+] Threat neutralized successfully!{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Keylogger process terminated{Colors.RESET}\n")
        
        for log_file in SUSPICIOUS_FILES:
            if os.path.exists(log_file):
                try:
                    os.remove(log_file)
                    print(f"{Colors.GREEN}[+] Deleted malicious log file: {log_file}{Colors.RESET}")
                except:
                    pass
        
        print(f"\n{Colors.MAGENTA}{'─' * 63}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Resuming monitoring for new threats...{Colors.RESET}\n")
        return True
    else:
        print(f"{Colors.YELLOW}[!] No active keylogger process found{Colors.RESET}\n")
        return False

def real_time_monitor():
    """Continuously monitor log file for new entries"""
    last_size = 0
    entries_detected = []
    threat_count = 0
    total_entries = 0
    
    print(f"{Colors.BLUE}[*] Monitoring started... Waiting for activity...{Colors.RESET}\n")
    
    while True:
        try:
            for log_file in SUSPICIOUS_FILES:
                if os.path.exists(log_file):
                    current_size = os.path.getsize(log_file)
                    
                    if current_size != last_size and current_size > 0:
                        last_size = current_size
                        
                        entry = analyze_latest_entry(log_file)
                        
                        if entry:
                            entry_id = f"{entry['timestamp']}-{entry['username']}"
                            
                            if entry_id not in entries_detected:
                                entries_detected.append(entry_id)
                                total_entries += 1
                                
                                print(f"{Colors.YELLOW}{'═' * 63}{Colors.RESET}")
                                print(f"{Colors.CYAN}[{entry['timestamp']}] {Colors.BOLD}NEW ENTRY DETECTED{Colors.RESET}")
                                print(f"{Colors.YELLOW}{'─' * 63}{Colors.RESET}")
                                
                                if entry['overall_status'] == 'CLEAN':
                                    print(f"{Colors.GREEN}┌─ Status: CLEAN ───────────────────────────────────────────┐{Colors.RESET}")
                                    print(f"{Colors.GREEN}│{Colors.RESET}  {Colors.WHITE}Username: {entry['username']:<47}{Colors.GREEN}│{Colors.RESET}")
                                    print(f"{Colors.GREEN}│{Colors.RESET}  {Colors.WHITE}Password: {'*' * len(entry['password']):<47}{Colors.GREEN}│{Colors.RESET}")
                                    print(f"{Colors.GREEN}│{Colors.RESET}{Colors.BOLD}✓ No suspicious patterns detected{' ' * 26}{Colors.GREEN}│{Colors.RESET}")
                                    print(f"{Colors.GREEN}└───────────────────────────────────────────────────────────┘{Colors.RESET}\n")
                                
                                else:
                                    threat_count += 1
                                    
                                    print(f"{Colors.RED}┌─ ⚠ THREAT DETECTED ───────────────────────────────────────┐{Colors.RESET}")
                                    print(f"{Colors.RED}│{Colors.RESET}  {Colors.YELLOW}Username: {Colors.WHITE}{entry['username']:<47}{Colors.RED}│{Colors.RESET}")
                                    print(f"{Colors.RED}│{Colors.RESET}  {Colors.YELLOW}Issue:    {Colors.WHITE}{entry['user_status']:<47}{Colors.RED}│{Colors.RESET}")
                                    print(f"{Colors.RED}│{Colors.RESET}  {Colors.YELLOW}Password: {Colors.WHITE}{'*' * len(entry['password']):<47}{Colors.RED}│{Colors.RESET}")
                                    print(f"{Colors.RED}│{Colors.RESET}  {Colors.YELLOW}Issue:    {Colors.WHITE}{entry['pass_status']:<47}{Colors.RED}│{Colors.RESET}")
                                    print(f"{Colors.RED}│{Colors.RESET}{Colors.BOLD}✗ SUSPICIOUS ACTIVITY - Attack detected!{' ' * 19}{Colors.RED}│{Colors.RESET}")
                                    print(f"{Colors.RED}└───────────────────────────────────────────────────────────┘{Colors.RESET}\n")
                                    
                                    print(f"{Colors.RED}{Colors.BOLD}[!] CRITICAL ALERT: Malicious pattern detected!{Colors.RESET}")
                                    print(f"{Colors.RED}[!] Activating automatic termination protocol...{Colors.RESET}\n")
                                    
                                    auto_terminate_threat()
                                    
                                    last_size = 0
                                    entries_detected = []
                                    
                                    print(f"{Colors.GREEN}{Colors.BOLD}[✓] System secured - Ready for next threat{Colors.RESET}\n")
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}{'═' * 63}{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Monitoring stopped by user{Colors.RESET}")
            print(f"{Colors.RED}{'═' * 63}{Colors.RESET}\n")
            break
        except Exception as e:
            time.sleep(2)
            continue
    
    return total_entries, threat_count

def print_summary(entries_count, threats):
    """Print monitoring summary"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"{Colors.GREEN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗")
    print(f"║  MONITORING SESSION COMPLETED                                 ║")
    print(f"╠═══════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.WHITE}Session Ended:      {timestamp}{Colors.GREEN}                  ║")
    print(f"║  {Colors.WHITE}Entries Monitored:  {entries_count}{' ' * (40 - len(str(entries_count)))}{Colors.GREEN}║")
    print(f"║  {Colors.WHITE}Threats Detected:   {threats}{' ' * (40 - len(str(threats)))}{Colors.GREEN}║")
    print(f"║  {Colors.WHITE}Threats Eliminated: {threats}{' ' * (40 - len(str(threats)))}{Colors.GREEN}║")
    print(f"╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    print(f"{Colors.MAGENTA}{Colors.BOLD}        ★ The Cyber Avengers - System Protected ★{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Detection system terminated{Colors.RESET}\n")

def main():
    """Main detection function"""
    
    print_banner()
    print_team_credits()  # Team credits added here
    print_monitor_info()
    
    entries, threats = real_time_monitor()
    
    print_summary(entries, threats)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Interrupted{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error: {e}{Colors.RESET}\n")
        sys.exit(1)
