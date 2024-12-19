# Email Generator InstAddr

**Email Generator InstAddr** is a Python application that automates the creation of multiple email addresses using Selenium. Its user-friendly Tkinter interface allows for easy account management and email generation, making it ideal for users needing temporary or disposable email addresses.

## Features

- **Account Management**: Add, view, and delete accounts with associated credentials.
- **Email Generation**: Specify the number of emails to generate for a selected account.
- **Clipboard Support**: Copy generated emails to the clipboard with a single click.
- **Domain Modification**: Add asterisks in email domains for privacy.
- **Real-Time Status Updates**: Get feedback on the email generation process.

## Requirements

To run this application, you will need:

- Python 3.x
- Required Python packages:
  - `selenium`
  - `tkinter`
  - `PIL` (Pillow)
  - `pyperclip`
  - `requests`

You can install the required packages using pip:

```bash
pip install selenium pillow pyperclip requests
```

Additional Requirements
Web Driver: Download a compatible web driver for Selenium (e.g., ChromeDriver) and ensure it's in your system's PATH.
Usage Instructions
Launch the Application: Run the script to start the application.
bash

```bash
python email_generator.py
```

Load Accounts: Existing accounts will be loaded from accounts.pkl. You can add new ones if none exist.
Add Accounts: Click "Add Account" to input a new account name, ID, and password.
Select an Account: Choose an account from the dropdown to view its details.
Generate Emails: Enter the desired number of emails and click "Generate Emails" to start the process.
View and Copy Emails: Generated emails will appear in the text area, which can be copied to the clipboard.
Modify Emails: Use the "Add Asterisk" button to modify displayed emails.
Delete Accounts: Select and remove accounts as needed.
Troubleshooting
Ensure the correct web driver version matches your browser.
Check internet connectivity for Selenium automation.
Make sure all required packages are installed.
