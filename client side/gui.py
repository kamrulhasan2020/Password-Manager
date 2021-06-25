import sys
import requests
import json
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QDialog,
                             QPushButton)
import login
import no_internet_connection
import invalid_credentials
import new_entry
import update_entry
import create_or_update_or_delete


# defining urls/global vars
LOGIN_URL = "http://127.0.0.1:8000/api-token-auth/"
URL = "http://127.0.0.1:8000/data/"


# init data/global vars
TOKEN = None
DATA = None
PASSWORD = None
HEADER = None
TARGET = None


def get_header():
    """Header = token + password."""
    global HEADER
    global PASSWORD
    global TOKEN
    HEADER = {'Authorization': 'Token ' + str(TOKEN), 'password': PASSWORD}


def get_data():
    """Retrieve data and assign to DATA."""
    global HEADER
    global DATA
    header = HEADER
    with requests.session() as s:
        try:
            r = s.get(url=URL, headers=header)
            response = r.json()
            DATA = response
        except requests.exceptions.RequestException:
            win = ConnectionErrorDialog()
            win.show()


############################
# Classes For GUI starts here
############################

class LoginDialog(QDialog):
    """
    GUI.

    This class is for Login Dialog GUI
    """

    def __init__(self):

        super(LoginDialog, self).__init__()
        # Set up the user interface from Designer.
        self.ui = login.Ui_Dialog()
        self.ui.setupUi(self)
        # Connect up the buttons.
        self.ui.login_button.clicked.connect(self.login)

    @pyqtSlot()
    def login(self):
        """
        Login and receieves token.

        Stores token and password to gloabal vars.
        """
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        if(len(username) == 0 or password == 0):
            print("All field must be populated")
        payload = {
                    'username': username,
                    'password': password
                   }

        with requests.session() as s:
            global TOKEN
            global PASSWORD
            global DATA
            global LOGIN_URL
            try:
                p = s.post(LOGIN_URL, data=payload)
                response = p.json()
                try:
                    TOKEN = response['token']
                    PASSWORD = password
                    get_header()
                    get_data()
                    if (len(DATA) == 0):
                        self.close()
                        self.win = CreateNewEntryDialog()
                        self.win.show()
                    else:
                        self.win = App()
                        self.win.show()
                        self.close()
                except Exception as e:
                    print(e)
                    self.win = InvalidCredentialsDialog()
                    self.win.show()
            except requests.exceptions.RequestException:
                self.win = ConnectionErrorDialog()
                self.win.show()


class CreateNewEntryDialog(QDialog):
    """
    GUI.

    create new entry in database
    """

    def __init__(self):
        super(CreateNewEntryDialog, self).__init__()
        self.ui = new_entry.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.create_button.clicked.connect(self.create)

    @pyqtSlot()
    def create(self):
        """Send request to the server to create new entry."""
        global URL
        global HEADER
        title = self.ui.title_input.text()
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        if(len(title) == 0 or len(login) == 0 or len(password) == 0):
            print("All fields must be populated!")
        payload = {
            'title': title,
            'login': login,
            'password': password
        }

        with requests.session() as s:
            try:
                s.post(URL, data=payload, headers=HEADER)
                self.close()
                get_data()
                self.win = App()
                self.win.show()
            except requests.exceptions.RequestException:
                win = ConnectionErrorDialog()
                win.show()


class ConnectionErrorDialog(QDialog):
    """
    GUI.

    show connection realated error
    """

    def __init__(self):
        super(ConnectionErrorDialog, self).__init__()
        # Set up the user interface from Designer.
        self.ui = no_internet_connection.Ui_Dialog()
        self.ui.setupUi(self)
        # Connect up the buttons.
        self.ui.ok_button.clicked.connect(self.ok)

    @pyqtSlot()
    def ok(self):
        """Close win."""
        self.close()


class InvalidCredentialsDialog(QDialog):
    """
    GUI.

    displays if given credentials are invalid
    """

    def __init__(self):
        super(InvalidCredentialsDialog, self).__init__()
        # Set up the user interface from Designer.
        self.ui = invalid_credentials.Ui_Dialog()
        self.ui.setupUi(self)
        # Connect up the buttons.
        self.ui.ok_button.clicked.connect(self.ok)

    @pyqtSlot()
    def ok(self):
        """Close win."""
        self.close()


class App(QWidget):
    """
    GUI.

    show all the records and provides options for updating and deleting data
    """

    def __init__(self):
        super().__init__()
        self.title = 'All Entries'
        self.left = 100
        self.top = 200
        self.width = 1000
        self.height = 500
        self.initUI()

    def initUI(self):
        """
        GUI.

        Set window properties.

        Returns
        -------
        None.

        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable()
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        # Show widget
        self.show()

    def createTable(self):
        """
        Create table containing all entries.

        Returns
        -------
        None.

        """
        global DATA
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(DATA) + 1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Title"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Login"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Password"))
        for c in range(0, len(DATA)):
            for d in range(5):
                if d == 0:
                    self.tableWidget.setItem(
                        c+1, d, QTableWidgetItem(DATA[c]['title']))
                elif d == 1:
                    self.tableWidget.setItem(
                        c+1, d, QTableWidgetItem(DATA[c]['login']))
                elif d == 2:
                    self.tableWidget.setItem(
                        c+1, d, QTableWidgetItem(DATA[c]['password']))
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        """
        Get the the target entry to update or delete.

        Trigerred by double click.

        Returns
        -------
        None.

        """
        global TARGET
        global DATA
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            TARGET = DATA[currentQTableWidgetItem.row() - 1]['id']
            self.close()
            self.win = CreateOrUpdateOrDeleteDialog()
            self.win.show()


class CreateOrUpdateOrDeleteDialog(QDialog):
    """
    GUI.

    Chooses update / delete
    """

    def __init__(self):
        super(CreateOrUpdateOrDeleteDialog, self).__init__()
        # Set up the user interface from Designer.
        self.ui = create_or_update_or_delete.Ui_Dialog()
        self.ui.setupUi(self)
        # Connect up the buttons.
        self.ui.create_button.clicked.connect(self.create)
        self.ui.update_button.clicked.connect(self.update)
        self.ui.delete_button.clicked.connect(self.delete)
        self.ui.cancel_button.clicked.connect(self.cancel)

    @pyqtSlot()
    def cancel(self):
        """Cancel."""
        self.close()
        self.window = App()
        self.window.show()

    @pyqtSlot()
    def create(self):
        """Create new entry."""
        self.close()
        self.win = CreateNewEntryDialog()
        self.win.show()

    @pyqtSlot()
    def update(self):
        """
        Update targeted entry.

        Returns
        -------
        None.

        """
        self.close()
        self.win = UpdateEntryDialog()
        self.win.show()

    @pyqtSlot()
    def delete(self):
        """
        Delete targeted entry.

        Returns
        -------
        None.

        """
        global TARGET
        global URL
        global HEADER
        url = URL + str(TARGET)
        with requests.session() as s:
            try:
                s.delete(url=url, headers=HEADER)
                self.close()
                get_data()
                self.close()
                self.win = App()
                self.win.show()
            except requests.exceptions.RequestException:
                self.win = ConnectionErrorDialog()
                self.win.show()


class UpdateEntryDialog(QDialog):
    """
    GUI.

    Update an existing entry
    """

    def __init__(self):
        super(UpdateEntryDialog, self).__init__()
        self.ui = update_entry.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.update_button.clicked.connect(self.update)

    @pyqtSlot()
    def update(self):
        """Send request to server to update entry."""
        global TARGET
        global HEADER
        url = URL + str(TARGET)
        title = self.ui.title_input.text()
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        payload = {
            'title': title,
            'login': login,
            'password': password
        }

        with requests.session() as s:
            try:
                s.put(url=url, data=payload, headers=HEADER)
                self.close()
                get_data()
                self.win = App()
                self.win.show()
            except requests.exceptions.RequesException:
                self.win = ConnectionErrorDialog()
                self.win.show()


app = QApplication(sys.argv)
window = LoginDialog()
window.show()
sys.exit(app.exec_())
