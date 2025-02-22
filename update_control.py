import tkinter as tk
from tkinter import messagebox, ttk
import winreg
import subprocess
import ctypes
import sys
import os
import time
import threading

class WindowsUpdateControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Update Control")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (400/2)
        y = (screen_height/2) - (300/2)
        self.root.geometry(f'400x300+{int(x)}+{int(y)}')
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Windows Update Control", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=20)
        
        # Buttons
        self.disable_button = ttk.Button(
            self.main_frame,
            text="Disable Windows Update",
            command=self.disable_updates_thread
        )
        self.disable_button.pack(pady=10, fill=tk.X)
        
        self.enable_button = ttk.Button(
            self.main_frame,
            text="Restore Windows Update",
            command=self.restore_updates_thread
        )
        self.enable_button.pack(pady=10, fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.main_frame,
            mode='indeterminate',
            length=300
        )
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="",
            wraplength=350
        )
        self.status_label.pack(pady=20)

    def disable_update_orchestrator(self):
        """Disable Update Orchestrator Service"""
        try:
            services_to_disable = [
                'UsoSvc',  # Update Orchestrator Service
                'WaaSMedicSvc',  # Windows Update Medic Service
                'wuauserv',  # Windows Update Service
                'BITS',  # Background Intelligent Transfer Service
                'DoSvc'   # Delivery Optimization
            ]
            
            for service in services_to_disable:
                subprocess.run(['sc', 'config', service, 'start=disabled'], capture_output=True)
                subprocess.run(['sc', 'stop', service], capture_output=True)
                
        except Exception as e:
            raise Exception(f"Error disabling services: {str(e)}")

    def modify_group_policy(self):
        """Modify Group Policy to disable Windows Update"""
        try:
            # Windows Update Policy
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, 
                                   r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', 
                                   0, 
                                   winreg.KEY_ALL_ACCESS)
            
            # Disable Windows Update completely
            winreg.SetValueEx(key, 'DisableWindowsUpdateAccess', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'DoNotConnectToWindowsUpdateInternetLocations', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'SetDisableUXWUAccess', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            # Automatic Update Policy
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, 
                                   r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU', 
                                   0, 
                                   winreg.KEY_ALL_ACCESS)
            
            # Never check for updates
            winreg.SetValueEx(key, 'NoAutoUpdate', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'AUOptions', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
        except Exception as e:
            raise Exception(f"Error modifying group policy: {str(e)}")

    def disable_tasks(self):
        """Disable Windows Update related scheduled tasks"""
        try:
            tasks_to_disable = [
                r'\Microsoft\Windows\WindowsUpdate\Scheduled Start',
                r'\Microsoft\Windows\UpdateOrchestrator\Schedule Scan',
                r'\Microsoft\Windows\UpdateOrchestrator\USO_UxBroker_Display',
                r'\Microsoft\Windows\UpdateOrchestrator\USO_UxBroker_ReadyToReboot',
                r'\Microsoft\Windows\UpdateOrchestrator\Start Oobe Expedite Work',
                r'\Microsoft\Windows\UpdateOrchestrator\Schedule Work',
                r'\Microsoft\Windows\UpdateOrchestrator\Schedule Scan Static Task',
                r'\Microsoft\Windows\UpdateOrchestrator\Report policies',
                r'\Microsoft\Windows\UpdateOrchestrator\Reboot_AC',
                r'\Microsoft\Windows\UpdateOrchestrator\Reboot',
                r'\Microsoft\Windows\UpdateOrchestrator\Policy Update',
                r'\Microsoft\Windows\UpdateOrchestrator\Maintenance Install',
                r'\Microsoft\Windows\UpdateOrchestrator\Initialize Oobe Expedite Work',
                r'\Microsoft\Windows\WaaSMedic\PerformRemediation'
            ]
            
            for task in tasks_to_disable:
                subprocess.run(['schtasks', '/Change', '/TN', task, '/DISABLE'], capture_output=True)
            
        except Exception as e:
            raise Exception(f"Error disabling scheduled tasks: {str(e)}")

    def block_update_domains(self):
        """Block Windows Update domains in hosts file"""
        try:
            hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
            update_domains = [
                'update.microsoft.com',
                'windowsupdate.microsoft.com',
                'windowsupdate.com',
                'download.microsoft.com',
                'download.windowsupdate.com',
                'wustat.windows.com',
                'ntservicepack.microsoft.com',
                'stats.microsoft.com',
                'au.download.windowsupdate.com'
            ]
            
            # Backup hosts file
            backup_path = hosts_path + '.backup'
            if not os.path.exists(backup_path):
                with open(hosts_path, 'r') as original:
                    with open(backup_path, 'w') as backup:
                        backup.write(original.read())
            
            # Add domains to hosts file
            with open(hosts_path, 'a') as hosts_file:
                hosts_file.write('\n# Windows Update Blocks\n')
                for domain in update_domains:
                    hosts_file.write(f'127.0.0.1 {domain}\n')
                    hosts_file.write(f'127.0.0.1 www.{domain}\n')
            
        except Exception as e:
            raise Exception(f"Error modifying hosts file: {str(e)}")

    def set_status(self, message):
        self.status_label.config(text=message)
        self.root.update()

    def disable_updates_thread(self):
        thread = threading.Thread(target=self.disable_updates)
        thread.start()

    def restore_updates_thread(self):
        thread = threading.Thread(target=self.restore_updates)
        thread.start()

    def disable_updates(self):
        self.disable_button.state(['disabled'])
        self.enable_button.state(['disabled'])
        self.progress.pack(pady=10)
        self.progress.start()
        
        try:
            self.set_status("Disabling Update Services...")
            self.disable_update_orchestrator()
            
            self.set_status("Modifying Group Policy...")
            self.modify_group_policy()
            
            self.set_status("Disabling Scheduled Tasks...")
            self.disable_tasks()
            
            self.set_status("Blocking Update Domains...")
            self.block_update_domains()
            
            self.set_status("Windows Update has been completely disabled!")
            messagebox.showinfo("Success", "Windows Update has been disabled successfully!")
        except Exception as e:
            self.set_status(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.disable_button.state(['!disabled'])
            self.enable_button.state(['!disabled'])

    def restore_updates(self):
        self.disable_button.state(['disabled'])
        self.enable_button.state(['disabled'])
        self.progress.pack(pady=10)
        self.progress.start()
        
        try:
            self.set_status("Restoring Windows Update...")
            
            # Enable services
            services_to_enable = ['UsoSvc', 'WaaSMedicSvc', 'wuauserv', 'BITS', 'DoSvc']
            for service in services_to_enable:
                subprocess.run(['sc', 'config', service, 'start=auto'], capture_output=True)
                subprocess.run(['sc', 'start', service], capture_output=True)
            
            # Remove registry modifications
            key_paths = [
                r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate',
                r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU'
            ]
            for path in key_paths:
                try:
                    winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, path)
                except:
                    pass
            
            # Enable tasks
            tasks_to_enable = [
                r'\Microsoft\Windows\WindowsUpdate\Scheduled Start',
                r'\Microsoft\Windows\UpdateOrchestrator\Schedule Scan'
            ]
            for task in tasks_to_enable:
                subprocess.run(['schtasks', '/Change', '/TN', task, '/ENABLE'], capture_output=True)
            
            # Restore hosts file from backup
            hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
            backup_path = hosts_path + '.backup'
            if os.path.exists(backup_path):
                with open(backup_path, 'r') as backup:
                    with open(hosts_path, 'w') as hosts_file:
                        hosts_file.write(backup.read())
            
            self.set_status("Windows Update has been restored!")
            messagebox.showinfo("Success", "Windows Update has been restored successfully!")
        except Exception as e:
            self.set_status(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.disable_button.state(['!disabled'])
            self.enable_button.state(['!disabled'])

def main():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    root = tk.Tk()
    app = WindowsUpdateControl(root)
    root.mainloop()

if __name__ == "__main__":
    main()
