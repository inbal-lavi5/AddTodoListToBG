from AddTodoListToBGFuncs_1_0 import *
from bg_todo import Ui_MainWindow
from settings_dialog import Ui_Dialog

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


class BG_Todo(qtw.QWidget):

    def __init__(self, MainWindow):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        self.ui.actionSettings.triggered.connect(self.edit)

        self.ui.listWidget.itemPressed.connect(lambda item: item.setCheckState(
            qtc.Qt.Checked if item.checkState() == qtc.Qt.Unchecked else qtc.Qt.Unchecked))

        self.ui.listWidget.itemDoubleClicked.connect(lambda item: item.setCheckState(
            qtc.Qt.Unchecked if item.checkState() == qtc.Qt.Checked else qtc.Qt.Checked))

        self.ui.listWidget.itemEntered.connect(lambda item: item.setCheckState(
            qtc.Qt.Checked if item.checkState() == qtc.Qt.Unchecked else qtc.Qt.Unchecked))

        self.init_items()

        self.ui.clear_button.clicked.connect(self.clear)
        self.ui.update_button.clicked.connect(self.update)
        self.ui.close_button.clicked.connect(self.close)

    def keyPressEvent(self, event):
        print("yo")

    def edit(self):
        self.dialog = SettingsDialog()
        self.dialog.show()

    def init_items(self):
        lst = self.ui.listWidget

        for line in read_txt_from_list():
            item = qtw.QListWidgetItem()
            item.setFlags(
                qtc.Qt.ItemIsSelectable |
                qtc.Qt.ItemIsEditable |
                qtc.Qt.ItemIsDragEnabled |
                qtc.Qt.ItemIsUserCheckable |
                qtc.Qt.ItemIsEnabled)
            item.setCheckState(qtc.Qt.Unchecked)
            item.setText(line)
            lst.addItem(item)

        lst.setCurrentRow(0)

    def clear(self):
        lst = self.ui.listWidget

        for index in range(lst.count()):
            if lst.item(index).checkState() == qtc.Qt.Checked:
                lst.item(index).setText("")
                lst.item(index).setCheckState(qtc.Qt.Unchecked)

    def update(self):
        lst = self.ui.listWidget

        itemsTextList = [str(lst.item(i).text()) + '\n' for i in range(lst.count())]
        itemsTextList[-1] = itemsTextList[-1][:-1]  # remove '\n' from last line
        update_list(itemsTextList)
        draw_txt()
        set_bg()

    def close(self):
        quit()


class SettingsDialog(qtw.QWidget):

    def __init__(self):
        super().__init__()

        self.Dialog = qtw.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.Dialog)

        self.set_location()
        self.set_font()

        self.ui.okButton.clicked.connect(self.submit)
        self.ui.cancelButton.clicked.connect(self.close)

    def show(self):
        self.Dialog.show()

    def set_location(self):
        self.ui.xValue.setMinimum(0)
        self.ui.xValue.setMaximum(3000)
        self.ui.xValue.setValue(LOCATION[0])

        self.ui.yValue.setMinimum(0)
        self.ui.yValue.setMaximum(2000)
        self.ui.yValue.setValue(LOCATION[1])

    def set_font(self):
        self.ui.fontComboBox.setCurrentFont(qtg.QFont('Arial'))
        self.ui.fontSize.setMinimum(0)
        self.ui.fontSize.setValue(FONT_SIZE)

    def submit(self):

        self.Dialog.close()

    def close(self):
        self.Dialog.close()


if __name__ == '__main__':
    import sys

    app = qtw.QApplication(sys.argv)
    MainWindow = qtw.QMainWindow()
    mw = BG_Todo(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
