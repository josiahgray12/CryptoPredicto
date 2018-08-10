import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class cryptoPredicto(QWidget):

    # Initialize the window

    def __init__(self):

        super(cryptoPredicto, self).__init__()

        self.setWindowTitle("Crypto Predicto")
        self.setGeometry(50, 50, 600, 400)

        layout = QVBoxLayout(self)

        self.inputLabel = QLabel()
        self.inputLabel.setText("Enter Address: ")
        self.inputLabel.move(100, 180)

        self.inputLine = QLineEdit()
        self.inputLine.move(310, 180)

        self.tagLabel = QLabel()
        self.tagLabel.setText("Would you like to tag this address to a cluster now?")
        self.tagLabel.move(120, 250)

        self.yesButton = QPushButton()
        self.yesButton.setText("Yes")

        self.noButton = QPushButton()
        self.noButton.setText("No, find the cluster it belongs to!")

        self.yesButton.move(120, 290)
        self.noButton.move(300, 290)

        # Connect signals of button clicks to slots of functions

        self.yesButton.clicked.connect(self.tagWindow)
        self.noButton.clicked.connect(self.clusterFind)

        # Make sure to keep the parent reference inside the QDialog constructors

        self.new = QDialog(self)
        self.clusterDisplay = QDialog(self)
        self.clusterSearch = QDialog(self)

        layout.addWidget(self.inputLabel)
        layout.addWidget(self.inputLine)
        layout.addWidget(self.tagLabel)
        layout.addWidget(self.yesButton)
        layout.addWidget(self.noButton)

    # This function creates a dialog box and prompts user for a cluster name

    def tagWindow(self):
        self.new.layout = QHBoxLayout(self.new)

        self.new.setWindowTitle("Tag Address to Cluster")
        self.new.setGeometry(50, 50, 600, 400)

        self.new.exLabel = QLabel()
        self.new.exLabel.setText("Enter Cluster:")
        self.new.exLabel.setGeometry(50, 50, 200, 100)

        self.new.exLine = QLineEdit()
        self.new.exLine.setGeometry(220, 80, 150, 40)

        self.new.doneButton = QPushButton()
        self.new.doneButton.setText("Done, view cluster details")
        self.new.doneButton.resize(150, 40)

        self.new.doneButton.clicked.connect(self.tagAddress)

        self.new.layout.addWidget(self.new.exLabel)
        self.new.layout.addWidget(self.new.exLine)
        self.new.layout.addWidget(self.new.doneButton)

        self.new.show()

    # This function displays cluster details

    def tagAddress(self):
        clusterName = "Cluster this address belongs to: "
        clusterBalance = "Balance of this cluster: "
        clusterMovement = "Recent movement in/out of this cluster: "

        self.clusterDisplay.layout = QVBoxLayout(self.clusterDisplay)

        self.clusterDisplay.setWindowTitle("Cluster Display")
        self.clusterDisplay.setGeometry(50, 50, 600, 400)

        self.clusterDisplay.nameLabel = QLabel()
        self.clusterDisplay.balanceLabel = QLabel()
        self.clusterDisplay.movementLabel = QLabel()

        # Populate this table view with recent transactions data from a database

        self.clusterDisplay.movementTable = QTableView()

        # Can have a backend function here that tags the address to a cluster
        # Address is the first argument, exchange is the second

        print("Tagged the address {} to the cluster {}".format(self.inputLine.text(), self.new.exLine.text()))

        # After calling the function that generates cluster data
        # You can just add the returned string to the variable: clusterName
        # like this, clusterName = clusterName + returnedString
        # same for the other variables (balance and movement)

        clusterName += self.new.exLine.text()
        clusterBalance += str(4566)

        self.clusterDisplay.nameLabel.setText(clusterName)
        self.clusterDisplay.nameLabel.setGeometry(50, 50, 200, 100)

        self.clusterDisplay.balanceLabel.setText(clusterBalance)
        self.clusterDisplay.balanceLabel.setGeometry(100, 100, 200, 100)

        self.clusterDisplay.movementLabel.setText(clusterMovement)
        self.clusterDisplay.movementLabel.setGeometry(150, 150, 200, 100)

        self.clusterDisplay.cButton = QPushButton()
        self.clusterDisplay.cButton.setText("Close")
        self.clusterDisplay.cButton.setGeometry(300, 300, 150, 40)

        self.clusterDisplay.cButton.clicked.connect(exit)

        self.clusterDisplay.layout.addWidget(self.clusterDisplay.nameLabel)
        self.clusterDisplay.layout.addWidget(self.clusterDisplay.balanceLabel)
        self.clusterDisplay.layout.addWidget(self.clusterDisplay.movementLabel)
        self.clusterDisplay.layout.addWidget(self.clusterDisplay.movementTable)
        self.clusterDisplay.layout.addWidget(self.clusterDisplay.cButton)

        self.clusterDisplay.show()

    def clusterFind(self):

        # Can have a backend function here that starts clustering on the address
        print("Starting the clustering process for {}...".format(self.inputLine.text()))

        clustName = "Cluster this address belongs to: "
        clustBalance = "Balance of this cluster: "
        clustMovement = "Recent movement in/out of this cluster: "

        self.clusterSearch.layout = QVBoxLayout(self.clusterSearch)

        self.clusterSearch.setWindowTitle("Cluster found, details below")
        self.clusterSearch.setGeometry(50, 50, 600, 400)

        self.clusterSearch.nameLabel = QLabel()
        self.clusterSearch.balanceLabel = QLabel()
        self.clusterSearch.movementLabel = QLabel()
        self.clusterSearch.movementTable = QTableView()

        # Once your functions return you could just populate the data inside
        # the widget below (as done above in tagAddress)

        clustName += 'Gemini'
        clustBalance += str(9021)

        self.clusterSearch.nameLabel.setText(clustName)
        self.clusterSearch.nameLabel.setGeometry(50, 50, 200, 100)

        self.clusterSearch.balanceLabel.setText(clustBalance)
        self.clusterSearch.balanceLabel.setGeometry(100, 100, 200, 100)

        self.clusterSearch.movementLabel.setText(clustMovement)
        self.clusterSearch.movementLabel.setGeometry(150, 150, 200, 100)

        self.clusterSearch.cButton = QPushButton()
        self.clusterSearch.cButton.setText("Close")
        self.clusterSearch.cButton.setGeometry(300, 300, 150, 40)

        self.clusterSearch.cButton.clicked.connect(exit)

        self.clusterSearch.layout.addWidget(self.clusterSearch.nameLabel)
        self.clusterSearch.layout.addWidget(self.clusterSearch.balanceLabel)
        self.clusterSearch.layout.addWidget(self.clusterSearch.movementLabel)
        self.clusterSearch.layout.addWidget(self.clusterSearch.movementTable)
        self.clusterSearch.layout.addWidget(self.clusterSearch.cButton)

        self.clusterSearch.show()

def main():
    app = QApplication(sys.argv)
    window = cryptoPredicto()
    window.show()
    ret = app.exec_()
    sys.exit(ret)

if __name__ == '__main__':
    main()