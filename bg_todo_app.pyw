from AddTodoListToBGFuncs_2_0 import *
from bg_todo import Ui_MainWindow
from settings import Ui_Form

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

IMAGE_SIZE = IMAGE.size


class BG_Todo(qtw.QWidget):
    pos = list(LOCATION)

    # init
    def __init__(self, verticalSlider):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        self.ui.actionSettings.triggered.connect(self.edit)

        # self.ui.listWidget.itemClicked.connect(self.un_check) # pressed? right?
        self.ui.listWidget.itemChanged.connect(self.strike)
        self.ui.listWidget.model().rowsMoved.connect(self.drag)
        # self.ui.listWidget.itemDoubleClicked.connect(self.un_check)
        # self.ui.listWidget.itemEntered.connect(self.un_check)

        self.init_items()

        self.ui.clear_button.clicked.connect(self.clear)
        self.ui.update_button.clicked.connect(self.update)
        self.ui.close_button.clicked.connect(verticalSlider.close)

    def init_items(self):
        lst = self.ui.listWidget
        # lst.setStyleSheet("QListWidget::item:selected{background-color: rgb(255,0,0);}")
        # lst.setStyleSheet("QListWidget::indicator:checked{ background:red; }")
        lst.setStyleSheet(
            "QListWidget::item {padding-left: 2px; border-left: 5px;}"
            "QListWidget::indicator {width: 30px; height: 30px;}"
            "QListWidget{ alternate-background-color: rgb(237, 248, 255);}"
            "QListWidget {selection-color: black}"
            "QListWidget::item:selected {background-color: rgb(188, 229, 255); color: black;}"
        )

        for line in read_txt_from_list():
            item = qtw.QListWidgetItem()
            item.setFlags(
                qtc.Qt.ItemIsSelectable |
                qtc.Qt.ItemIsEditable |
                qtc.Qt.ItemIsDragEnabled |
                qtc.Qt.ItemIsUserCheckable |
                qtc.Qt.ItemIsEnabled)
            item.setText(line[0])
            self.strike_completed(item, line)
            lst.addItem(item)

        lst.setCurrentRow(0)

    def strike_completed(self, item, line):
        if line[1] == COMPLETE:
            f = item.font()
            f.setStrikeOut(True)
            item.setFont(f)
            item.setCheckState(qtc.Qt.Checked)
        else:
            item.setCheckState(qtc.Qt.Unchecked)

    # not working
    def keyPressEvent(self, event):
        print("yo")

    # check/uncheck
    def strike(self, item):
        self.ui.update_button.setEnabled(True)
        if item.checkState() == qtc.Qt.Checked:
            f = item.font()
            f.setStrikeOut(True)
            item.setFont(f)
        else:
            f = item.font()
            f.setStrikeOut(False)
            item.setFont(f)

    def drag(self):
        self.ui.update_button.setEnabled(True)

    def un_check(self, item):
        if item.checkState() == qtc.Qt.Unchecked:
            item.setCheckState(qtc.Qt.Checked)
            f = item.font()
            f.setStrikeOut(True)
            item.setFont(f)
        else:
            item.setCheckState(qtc.Qt.Unchecked)
            f = item.font()
            f.setStrikeOut(False)
            item.setFont(f)

    # settings
    def edit(self):
        # updated = [False]
        self.setting = SettingsDialog(self.pos)
        self.setting.show()

        # if self.setting.closeEvent() and updated[0]:
        #     print("yas")
        #     self.ui.update_button.setEnabled(True)
        # else:
        #     print("NO")

    # buttons
    def clear(self):
        lst = self.ui.listWidget

        for index in range(lst.count()):
            if lst.item(index).checkState() == qtc.Qt.Checked:
                lst.item(index).setText("")
                lst.item(index).setCheckState(qtc.Qt.Unchecked)

    def update(self):
        self.ui.update_button.setDisabled(True)
        lst = self.ui.listWidget

        itemsTextList = []
        for i in range(lst.count()):
            checked = lst.item(i).checkState() == qtc.Qt.Checked
            itemsTextList.append(str(lst.item(i).text()) + ',' + (COMPLETE if checked else TODO) + '\n')

        # print(itemsTextList)
        # itemsTextList = [str(lst.item(i).text()) + '\n' for i in range(lst.count())]
        itemsTextList[-1] = itemsTextList[-1][:-1]  # remove '\n' from last line
        update_list(itemsTextList)
        draw_txt(tuple(self.pos))
        set_bg()


class SettingsDialog(qtw.QWidget):
    # todo: return to default

    # init
    def __init__(self, pos):
        super().__init__()

        self.pos = pos

        self.Form = qtw.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)

        self.set_sliders()

        self.ui.load_button.clicked.connect(self.load_image)
        self.ui.reset_button.clicked.connect(self.reset_default)
        self.ui.update_button.clicked.connect(self.update)
        self.ui.cancel_button.clicked.connect(self.Form.close)

    def set_sliders(self):
        # print(IMAGE_GEOMETRY)
        self.ui.horizontalSlider.setMaximum(IMAGE_SIZE[0])
        self.ui.verticalSlider.setMaximum(IMAGE_SIZE[1])
        self.ui.horizontalSlider.setPageStep(IMAGE_SIZE[0] / 50)
        self.ui.verticalSlider.setPageStep(IMAGE_SIZE[1] / 50)
        self.ui.horizontalSlider.setValue(self.pos[0])
        self.ui.verticalSlider.setValue(self.pos[1])
        self.set_x(self.ui.horizontalSlider.value())
        self.set_y(self.ui.verticalSlider.value())
        self.ui.horizontalSlider.valueChanged.connect(self.set_x)
        self.ui.verticalSlider.valueChanged.connect(self.set_y)

    def set_x(self, value):
        self.ui.reset_button.setEnabled(True)

        self.ui.x_coor.setNum(value)
        min = self.ui.bg_image.x()
        self.ui.pos.move((self.ui.bg_image.width() * value / IMAGE_SIZE[0]) + min - self.ui.pos.width() / 2,
                         int(self.ui.pos.y()))

    def set_y(self, value):
        self.ui.reset_button.setEnabled(True)

        self.ui.y_coor.setNum(value)
        min = self.ui.bg_image.y()
        self.ui.pos.move(int(self.ui.pos.x()),
                         (self.ui.bg_image.height() * value / IMAGE_SIZE[1]) + min - self.ui.pos.height() / 2)

    # show
    def show(self):
        self.Form.show()

    # def keyPressEvent(self, event):
    #     print("yo")

    # buttons
    def load_image(self):
        pass

    def update(self):
        self.pos[0] = self.ui.horizontalSlider.value()
        self.pos[1] = self.ui.verticalSlider.value()
        self.Form.close()

    def reset_default(self):
        self.pos[0] = LOCATION[0]
        self.pos[1] = LOCATION[1]
        # reset image

        self.set_sliders()

        self.ui.reset_button.setDisabled(True)


if __name__ == '__main__':
    import sys

    app = qtw.QApplication(sys.argv)
    MainWindow = qtw.QMainWindow()
    mw = BG_Todo(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
