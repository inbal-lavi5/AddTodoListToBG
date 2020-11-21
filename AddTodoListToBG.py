from DialogGUI_2_0 import *

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Window()
    ui.setupUi(Dialog)

    Dialog.show()
    sys.exit(app.exec_())