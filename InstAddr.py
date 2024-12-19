import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import pyperclip
import threading
import pickle
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO



class EmailGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Generator InstAddr!")
        self.root.geometry("510x620")
        self.root.resizable(False, False)  # Prevent resizing
        self.root.configure(bg="#213555")

        self.load_accounts()  # Load accounts on initialization



         # URL of the image
        image_url = 'https://play-lh.googleusercontent.com/6jRUHSniEVWXCy4buFK9WCnvhb5_QEuT9AgX18MY12QfuJbcpHn0lnxE36xgJ83P9w'  # Replace with your Imgur image URL

        # Download the image
        response = requests.get(image_url)
        img_data = response.content

        # Load the image
        self.icon_image = Image.open(BytesIO(img_data))
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)

        # Set the image as the window icon
        self.root.iconphoto(True, self.icon_photo)



        # Create main frame without borders
        main_frame = ttk.Frame(root, padding="20", relief="flat", borderwidth=0)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style="Main.TFrame")

        # Configure style
        style = ttk.Style()
        style.configure("Main.TFrame", background="#213555")
        style.configure("TLabel", background="#213555", foreground="white", font=("Helvetica", 12))
        style.configure("TButton", relief="flat", padding=10, font=("Helvetica", 10), background="#213555", foreground="#3E5879")
        style.map("TButton", background=[('active', '#213555')])
        style.configure("TCombobox", font=("Helvetica", 12), padding=5)
        style.configure("TEntry", font=("Helvetica", 12), padding=5)

        # Account selection
        ttk.Label(main_frame, text="Select Account:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.account_var = tk.StringVar(value="")
        self.account_menu = ttk.Combobox(main_frame, textvariable=self.account_var, values=list(self.accounts.keys()), state="readonly")
        self.account_menu.grid(row=0, column=1, columnspan=2, sticky=tk.W, pady=5)
        self.account_menu.bind("<<ComboboxSelected>>", self.update_account_info)

        # Account ID and Password (Display only)
        ttk.Label(main_frame, text="Account ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.account_id_display = ttk.Label(main_frame, text="", foreground="white")
        self.account_id_display.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)

        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_display = ttk.Label(main_frame, text="", foreground="white")
        self.password_display.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)

        # Email count per account
        ttk.Label(main_frame, text="Emails Created:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.emails_created_label = ttk.Label(main_frame, text="0", foreground="white")
        self.emails_created_label.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=5)

        # Number of emails to generate
        ttk.Label(main_frame, text="Number of Emails:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.email_count = ttk.Entry(main_frame, width=40)
        self.email_count.grid(row=4, column=1, columnspan=2, sticky=tk.W, pady=5)

        # Generate button
        self.generate_btn = ttk.Button(main_frame, text="Generate Emails", command=self.start_generation)
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=10)

        # Email display area
        self.email_display = scrolledtext.ScrolledText(main_frame, width=50, height=15, bg="#3E5879", font=("Helvetica", 12))
        self.email_display.grid(row=6, column=0, columnspan=3, pady=10)

        # Buttons frame without borders
        button_frame = ttk.Frame(main_frame, padding=0, relief="flat")
        button_frame.grid(row=7, column=0, columnspan=3, pady=0)

        # Copy and Add Asterisk buttons
        self.copy_btn = ttk.Button(button_frame, text="Copy Emails", command=self.copy_emails)
        self.copy_btn.grid(row=0, column=0, padx=0)

        self.asterisk_btn = ttk.Button(button_frame, text="Add Asterisk", command=self.add_asterisk)
        self.asterisk_btn.grid(row=0, column=1, padx=0)

        # Add account button
        self.add_account_btn = ttk.Button(button_frame, text="Add Account", command=self.add_account)
        self.add_account_btn.grid(row=0, column=2, padx=0)

        # Delete account button
        self.delete_account_btn = ttk.Button(button_frame, text="Delete Account", command=self.delete_account)
        self.delete_account_btn.grid(row=0, column=3, padx=0)

        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)

        self.generated_emails = []

    def load_accounts(self):
        if os.path.exists('accounts.pkl'):
            with open('accounts.pkl', 'rb') as file:
                self.accounts = pickle.load(file)
        else:
            self.accounts = {}

    def save_accounts(self):
        with open('accounts.pkl', 'wb') as file:
            pickle.dump(self.accounts, file)

    def update_account_info(self, event=None):
        account_name = self.account_var.get()
        if account_name in self.accounts:
            account = self.accounts[account_name]
            self.account_id_display.config(text=account["id"])
            self.password_display.config(text=account["password"])
            self.emails_created_label.config(text=str(account["emails_created"]))
        else:
            self.account_id_display.config(text="")
            self.password_display.config(text="")
            self.emails_created_label.config(text="0")

    def add_account(self):
        def save_account():
            name = name_entry.get()
            acc_id = id_entry.get()
            password = password_entry.get()
            if name and acc_id and password:
                self.accounts[name] = {"id": acc_id, "password": password, "emails_created": 0}
                self.account_menu['values'] = list(self.accounts.keys())
                self.account_var.set(name)
                self.save_accounts()  # Save accounts after adding
                add_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required")

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Account")
        add_window.configure(bg="#f7f9fc")
        ttk.Label(add_window, text="Account Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Account ID:").grid(row=1, column=0, padx=5, pady=5)
        id_entry = ttk.Entry(add_window)
        id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(add_window, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        save_btn = ttk.Button(add_window, text="Save", command=save_account)
        save_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def delete_account(self):
        account_name = self.account_var.get()
        if account_name and messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{account_name}'?"):
            del self.accounts[account_name]
            self.account_menu['values'] = list(self.accounts.keys())
            self.account_var.set("")
            self.update_account_info()
            self.save_accounts()  # Save accounts after deletion

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update()

    def generate_emails(self):
        try:
            account = self.accounts[self.account_var.get()]
            self.update_status("Starting browser...")
            driver = webdriver.Chrome()
            driver.get("https://m.kuku.lu/index.php")
            wait = WebDriverWait(driver, 30)

            # Login process
            self.update_status("Logging in...")
            login_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="link_loginform"]')))
            driver.execute_script("arguments[0].scrollIntoView();", login_element)
            driver.execute_script("arguments[0].click();", login_element)
            time.sleep(1)

            account_id_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="user_number"]')))
            driver.execute_script("arguments[0].scrollIntoView();", account_id_element)
            driver.execute_script("arguments[0].value = arguments[1];", account_id_element, account["id"])

            password_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="user_password"]')))
            driver.execute_script("arguments[0].scrollIntoView();", password_element)
            driver.execute_script("arguments[0].value = arguments[1];", password_element, account["password"])

            login_element2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="area_loginform"]/div/form/div[4]/a')))
            driver.execute_script("arguments[0].scrollIntoView();", login_element2)
            driver.execute_script("arguments[0].click();", login_element2)
            time.sleep(2)

            merge_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="area-confirm-dialog-button-cancel"]')))
            driver.execute_script("arguments[0].scrollIntoView();", merge_element)
            driver.execute_script("arguments[0].click();", merge_element)
            time.sleep(3)

            # Generate emails
            num_emails = int(self.email_count.get())
            terms_of_use = True
            self.generated_emails = []

            for i in range(num_emails):
                self.update_status(f"Generating email {i+1} of {num_emails}...")

                create_email_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="link_addMailAddrByAuto"]')))
                driver.execute_script("arguments[0].scrollIntoView();", create_email_element)
                driver.execute_script("arguments[0].click();", create_email_element)

                if terms_of_use:
                    yes_terms_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="area-confirm-dialog-button-ok"]')))
                    driver.execute_script("arguments[0].scrollIntoView();", yes_terms_element)
                    driver.execute_script("arguments[0].click();", yes_terms_element)
                    terms_of_use = False

                time.sleep(4)

                copy_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="link_newaddr_copyaddr"]')))
                copy_button.click()

                email_address = pyperclip.paste()
                self.generated_emails.append(email_address)
                self.email_display.insert(tk.END, email_address + '\n')

                current_url = driver.current_url
                if current_url == "https://m.kuku.lu/new.php":
                    driver.back()
                    time.sleep(2)

            # Update account email count
            account["emails_created"] += num_emails
            self.update_account_info()
            self.save_accounts()  # Save accounts after generating emails

            # Save to file
            today = datetime.now()
            date_str = today.strftime("%d-%m")
            file_name = f"{str(num_emails)} Account - {date_str}.txt"

            with open(file_name, 'w') as file:
                for email in self.generated_emails:
                    file.write(email + '\n')

            self.update_status("Email generation completed!")
            driver.quit()

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            if 'driver' in locals():
                driver.quit()

    def start_generation(self):
        self.email_display.delete(1.0, tk.END)
        self.generated_emails = []
        threading.Thread(target=self.generate_emails, daemon=True).start()

    def copy_emails(self):
        email_text = self.email_display.get(1.0, tk.END)
        pyperclip.copy(email_text)
        self.update_status("Emails copied to clipboard!")

    def add_asterisk(self):
        self.email_display.delete(1.0, tk.END)
        for email in self.generated_emails:
            domain_parts = email.split('@')
            if len(domain_parts) == 2:
                modified_email = f"{domain_parts[0]}@{domain_parts[1].replace('.', '*.', 1)}"
                self.email_display.insert(tk.END, modified_email + '\n')
        self.update_status("Asterisks added to domains!")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailGeneratorGUI(root)
    root.mainloop()