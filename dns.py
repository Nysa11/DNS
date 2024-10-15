import sys
import json
import paramiko
from PyQt5 import QtWidgets, QtGui, QtCore

# File to store router data
ROUTERS_FILE = "routers.json"

# List to store router details (Loaded from file)
routers_list = []

# Load routers from JSON file
def load_routers():
    global routers_list
    try:
        with open(ROUTERS_FILE, 'r') as file:
            routers_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        routers_list = []

# Save routers to JSON file
def save_routers():
    with open(ROUTERS_FILE, 'w') as file:
        json.dump(routers_list, file, indent=4)

class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MikroTik Router Management")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.new_router_btn = QtWidgets.QPushButton("New Router")
        self.change_dns_btn = QtWidgets.QPushButton("Change DNS")

        self.layout.addWidget(self.new_router_btn)
        self.layout.addWidget(self.change_dns_btn)

        self.new_router_btn.clicked.connect(self.open_new_router_window)
        self.change_dns_btn.clicked.connect(self.open_change_dns_window)

        self.setLayout(self.layout)

    def open_new_router_window(self):
        print("Opening New Router Window")  # Debugging statement
        self.new_router_window = NewRouterWindow()
        self.new_router_window.show()

    def open_change_dns_window(self):
        print("Opening Change DNS Window")  # Debugging statement
        self.change_dns_window = ChangeDNSWindow()
        self.change_dns_window.show()

class NewRouterWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add/Delete Router")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.new_router_layout = QtWidgets.QFormLayout()
        self.new_router_name = QtWidgets.QLineEdit()
        self.new_router_ip = QtWidgets.QLineEdit()
        self.new_router_username = QtWidgets.QLineEdit()
        self.new_router_password = QtWidgets.QLineEdit()
        self.new_router_port = QtWidgets.QLineEdit()
        self.add_router_btn = QtWidgets.QPushButton("Add Router")
        self.delete_router_btn = QtWidgets.QPushButton("Delete Selected Router")

        self.new_router_layout.addRow("Name:", self.new_router_name)
        self.new_router_layout.addRow("IP Address:", self.new_router_ip)
        self.new_router_layout.addRow("Username:", self.new_router_username)
        self.new_router_layout.addRow("Password (leave blank if none):", self.new_router_password)
        self.new_router_layout.addRow("Port:", self.new_router_port)
        self.new_router_layout.addRow(self.add_router_btn, self.delete_router_btn)

        self.router_table = QtWidgets.QTableWidget()
        self.router_table.setColumnCount(5)
        self.router_table.setHorizontalHeaderLabels(["Name", "IP", "Username", "Password", "Port"])
        self.router_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.router_table.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        self.router_table.horizontalHeader().setStretchLastSection(True)

        self.populate_router_table()

        self.layout.addLayout(self.new_router_layout)
        self.layout.addWidget(self.router_table)
        self.setLayout(self.layout)

        self.add_router_btn.clicked.connect(self.add_router)
        self.delete_router_btn.clicked.connect(self.delete_router)

    def populate_router_table(self):
        self.router_table.setRowCount(0)
        for router in routers_list:
            row_position = self.router_table.rowCount()
            self.router_table.insertRow(row_position)
            self.router_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(router['name']))
            self.router_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(router['ip']))
            self.router_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(router['username']))
            self.router_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(router['password'] or ""))
            self.router_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(router['port']))

    def add_router(self):
        name = self.new_router_name.text()
        ip = self.new_router_ip.text()
        username = self.new_router_username.text()
        password = self.new_router_password.text()  # Allow empty password
        port = self.new_router_port.text()

        if name and ip and username and port:
            routers_list.append({
                'name': name,
                'ip': ip,
                'username': username,
                'password': password,  # Store even if password is empty
                'port': port
            })
            save_routers()
            QtWidgets.QMessageBox.information(self, "Success", f"Router {name} added!")

            self.new_router_name.clear()
            self.new_router_ip.clear()
            self.new_router_username.clear()
            self.new_router_password.clear()
            self.new_router_port.clear()
            self.populate_router_table()

        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields except password!")

    def delete_router(self):
        selected_row = self.router_table.currentRow()
        if selected_row >= 0:
            router = routers_list[selected_row]
            routers_list.pop(selected_row)
            save_routers()
            QtWidgets.QMessageBox.information(self, "Success", f"Router {router['name']} deleted!")
            self.populate_router_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a router to delete!")

class ChangeDNSWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change DNS on Routers")
        self.setGeometry(100, 100, 800, 400)  # Increased size

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # First and second DNS inputs
        self.change_dns_layout = QtWidgets.QFormLayout()
        self.change_dns_ip_1 = QtWidgets.QLineEdit()
        self.change_dns_ip_2 = QtWidgets.QLineEdit()
        self.save_dns_btn = QtWidgets.QPushButton("Save DNS")

        # Labels for the DNS inputs
        self.change_dns_layout.addRow("New DNS IP 1:", self.change_dns_ip_1)
        self.change_dns_layout.addRow("New DNS IP 2:", self.change_dns_ip_2)
        self.change_dns_layout.addRow(self.save_dns_btn)

        self.layout.addLayout(self.change_dns_layout)
        self.setLayout(self.layout)

        # Button click handler
        self.save_dns_btn.clicked.connect(self.change_dns)
        print("Change DNS Window initialized, button connected")  # Debugging statement

    def change_dns(self):
        dns_ip_1 = self.change_dns_ip_1.text()
        dns_ip_2 = self.change_dns_ip_2.text()

        if not routers_list:
            QtWidgets.QMessageBox.warning(self, "Error", "No routers to update DNS!")
            return

        if not dns_ip_1 or not dns_ip_2:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter both DNS IPs!")
            return

        success_count = 0
        failed_count = 0

        for router in routers_list:
            try:
                # Debugging: Print router details before connecting
                print(f"Attempting to connect to router {router['name']} at {router['ip']} with user {router['username']} and password: '{router['password']}'")

                # SSH connection to the router using Paramiko
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown host keys
                ssh.connect(router['ip'], port=int(router['port']), username=router['username'], password=router['password'])

                # Command to change the DNS settings on the router
                change_dns_command = f'/ip dns set servers={dns_ip_1},{dns_ip_2}'
                stdin, stdout, stderr = ssh.exec_command(change_dns_command)

                # Check for errors
                error = stderr.read().decode()
                if error:
                    print(f"Error: {error}")
                    failed_count += 1
                else:
                    print(f"DNS servers changed successfully for {router['name']}")
                    success_count += 1

                ssh.close()

            except Exception as e:
                print(f"Failed to update router {router['name']} at {router['ip']}: {e}")
                failed_count += 1

        # Inform user of the result
        QtWidgets.QMessageBox.information(self, "DNS Update", 
            f"DNS Update Complete!\nSuccess: {success_count}, Failed: {failed_count}")

def main():
    load_routers()
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
