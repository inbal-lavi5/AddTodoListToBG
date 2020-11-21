from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QDialog, QAbstractItemView
from PyQt5.QtGui import QIcon, QFont
from AddTodoListToBGFuncs_2_0 import *

ICON = os.path.join(sys.path[0], "resources\\icon.png")
FONT = QFont('Arial', 15)
DIALOG_FONT = QFont('Arial', 10)


class Window(QDialog):

    def setupUi(self, Dialog):
        Dialog.resize(900, 700)

        self.allLayout = QtWidgets.QVBoxLayout(Dialog)
        self.allLayout.setContentsMargins(30, 40, 30, 30)
        self.allLayout.setSpacing(6)

        self.topLayout = QtWidgets.QHBoxLayout(Dialog)
        self.topLayout.setContentsMargins(0, 0, 0, 20)
        self.topLayout.setSpacing(6)

        self.buildTopLayout(Dialog)

        self.bottomButtonsLayout = QtWidgets.QHBoxLayout()
        self.bottomButtonsLayout.setContentsMargins(500, 0, 0, 0)
        self.bottomButtonsLayout.setSpacing(20)

        self.buildBottomLayout(Dialog)

        self.allLayout.addLayout(self.topLayout)
        self.allLayout.addLayout(self.bottomButtonsLayout)

        self.retranslateUi(Dialog)
        self.connect_buttons(Dialog)

        self.set_clause()

    def buildTopLayout(self, Dialog):
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setFont(FONT)
        self.topLayout.addWidget(self.listWidget)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # check how to delete all selected

        self.buttonsLayout = QtWidgets.QVBoxLayout()
        self.buttonsLayout.setContentsMargins(20, 0, 0, 50)
        self.buttonsLayout.setSpacing(20)
        self.buildButtonsLayout(Dialog)

        self.topLayout.addLayout(self.buttonsLayout)

    def buildButtonsLayout(self, Dialog):
        self.pushButton_new = QtWidgets.QPushButton(Dialog)
        self.create_button(self.pushButton_new, self.buttonsLayout)

        self.pushButton_edit = QtWidgets.QPushButton(Dialog)
        self.create_button(self.pushButton_edit, self.buttonsLayout)

        self.pushButton_delete = QtWidgets.QPushButton(Dialog)
        self.create_button(self.pushButton_delete, self.buttonsLayout)

        self.pushButton_clear = QtWidgets.QPushButton(Dialog)
        self.create_button(self.pushButton_clear, self.buttonsLayout)

        spacerItem = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.buttonsLayout.addItem(spacerItem)

        self.pushButton_up = QtWidgets.QPushButton(Dialog)
        self.create_button(self.pushButton_up, self.buttonsLayout)

        self.pushButton_down = QtWidgets.QPushButton(Dialog)
        self.create_button(self.pushButton_down, self.buttonsLayout)

    def buildBottomLayout(self, Dialog):
        self.pushButton_update = QtWidgets.QPushButton(Dialog)
        self.create_button(self.pushButton_update, self.bottomButtonsLayout)

        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.create_button(self.pushButton_close, self.bottomButtonsLayout)

    def create_button(self, button, layout):
        button.setStyleSheet("font-size: 23px; height: 45px; width: 160px")
        layout.addWidget(button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BG TODO list"))
        Dialog.setWindowIcon(QIcon(ICON))
        self.pushButton_new.setText(_translate("Dialog", "New"))
        self.pushButton_edit.setText(_translate("Dialog", "Edit"))
        self.pushButton_delete.setText(_translate("Dialog", "Delete"))
        self.pushButton_clear.setText(_translate("Dialog", "Clear"))
        self.pushButton_up.setText(_translate("Dialog", "Up"))
        self.pushButton_down.setText(_translate("Dialog", "Down"))
        self.pushButton_update.setText(_translate("Dialog", "Update"))
        self.pushButton_close.setText(_translate("Dialog", "Cancel"))

    def connect_buttons(self, Dialog):
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton_new.clicked.connect(self.new)
        self.pushButton_edit.clicked.connect(self.edit)
        self.pushButton_delete.clicked.connect(self.delete)
        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_up.clicked.connect(self.up)
        self.pushButton_down.clicked.connect(self.down)
        self.pushButton_update.clicked.connect(self.update_bg)
        self.pushButton_close.clicked.connect(self.close)

    def set_clause(self):
        self.listWidget.addItems(read_txt_from_list())
        self.listWidget.setCurrentRow(0)

    def new(self):
        row = self.listWidget.currentRow()

        inputDialog = QInputDialog()
        inputDialog.setWindowIcon(QIcon(ICON))
        inputDialog.setWindowTitle("New Clause"), inputDialog.setLabelText("Enter a new clause")
        inputDialog.setInputMode(QInputDialog.TextInput)
        inputDialog.setFont(DIALOG_FONT)
        inputDialog.resize(500, 0)

        ok = inputDialog.exec_()
        text = inputDialog.textValue()

        if ok and text is not None:
            self.listWidget.insertItem(row + 1, text)
            self.listWidget.setCurrentRow(row + 1)

    def edit(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)

        if item is not None:
            inputDialog = QInputDialog()
            inputDialog.setWindowIcon(QIcon(ICON))
            inputDialog.setWindowTitle("Edit Clause"), inputDialog.setLabelText("Edit clause")
            inputDialog.setInputMode(QInputDialog.TextInput)
            inputDialog.setTextValue(item.text())
            inputDialog.setFont(DIALOG_FONT)
            inputDialog.resize(500, 0)

            ok = inputDialog.exec_()
            string = inputDialog.textValue()

            if ok and string is not None:
                item.setText(string)

    def delete(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.takeItem(row)
        del item

    def clear(self):
        self.listWidget.clear()

    def up(self):
        row = self.listWidget.currentRow()
        if row >= 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, item)
            self.listWidget.setCurrentItem(item)

    def down(self):
        row = self.listWidget.currentRow()
        if row < self.listWidget.count() - 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row + 1, item)
            self.listWidget.setCurrentItem(item)

    def update_bg(self):
        itemsTextList = [str(self.listWidget.item(i).text()) + '\n' for i in range(self.listWidget.count())]
        itemsTextList[-1] = itemsTextList[-1][:-1]  # remove '\n' from last line
        update_list(itemsTextList)
        draw_txt()
        set_bg()
        # print(itemsTextList)

    def close(self):
        quit()

# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle('Fusion')
#     Dialog = QtWidgets.QDialog()
#     ui = Window()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())
