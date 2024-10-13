# MikroTik DNS Changer

This application allows you to easily change the DNS settings of MikroTik routers. You can update the DNS settings for multiple routers all at once, which helps to ensure your Internet connection stays reliable.

## How to Download and Run the Application

### Step 1: Download Python

1. Go to [python.org](https://www.python.org/downloads/).
2. Click on the "Download" button for your operating system.
3. Follow the instructions on the website to install Python.

### Step 2: Download the Application

1. Go to the GitHub repository link: (https://github.com/Nysa11/DNS).
2. Click on the green "Code" button and select "Download ZIP".
3. Extract (unzip) the downloaded ZIP file to a folder on your computer.

### Step 3: Install Required Libraries

1. Open the Command Prompt (Windows) or Terminal (Mac/Linux).
   - For Windows: Press `Win + R`, type `cmd`, and press Enter.
   - For Mac: Open Finder, go to Applications > Utilities, and open Terminal.
   - For Linux: Look for Terminal in your applications.

2. In the Command Prompt or Terminal, type the following command and press Enter:

   ```bash
   pip install PyQt5 python-routeros

This command will install the additional tools needed for the application.

### Step 4: Run the Application

1. Still in the Command Prompt or Terminal, navigate to the folder where you extracted the application files. For example:

   ```bash
   cd C:\Users\YourName\Downloads\DNS-main\DNS-main
   
- Note: Make sure to change YourName to your actual username on your computer. For example, if your username is John, you should type:

   ```bash
   cd C:\Users\John\Downloads\DNS-main\DNS-main

2. Once you're in the correct folder, type the following command and press Enter to start the application:

   ```bash
   python dns.py

### Step 5: Using the Application

1. Add a Router:
  - Enter the router’s name, IP address, username, password (if needed), and port number.
  - Click the "Add" button to save it to your list.

2. Delete a Router:
  - Select a router from the list and click the "Delete" button to remove it.

3. Change DNS Settings:
  - Enter the new DNS addresses in the two fields.
  - Click the "Save DNS" button to apply the changes to all routers in your list.

4. Saving Your Routers
  - The application automatically saves the router information so you don’t lose it. When you open the application again, your routers will still be there!
