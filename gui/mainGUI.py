# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGUI.ui'
#
# Created: Wed Dec 12 14:54:07 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_StaticsRecGUI(object):
    def setupUi(self, StaticsRecGUI):
        StaticsRecGUI.setObjectName(_fromUtf8("StaticsRecGUI"))
        StaticsRecGUI.resize(1400, 800)
        self.centralwidget = QtGui.QWidget(StaticsRecGUI)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.matplot = matplotlibwidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matplot.sizePolicy().hasHeightForWidth())
        self.matplot.setSizePolicy(sizePolicy)
        self.matplot.setObjectName(_fromUtf8("matplot"))
        self.horizontalLayout.addWidget(self.matplot)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(300, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(300, 700))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.labelerTab = QtGui.QWidget()
        self.labelerTab.setObjectName(_fromUtf8("labelerTab"))
        self.gridLayoutWidget = QtGui.QWidget(self.labelerTab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 651))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnLabelTest = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnLabelTest.setObjectName(_fromUtf8("btnLabelTest"))
        self.gridLayout.addWidget(self.btnLabelTest, 1, 1, 1, 1)
        self.labelLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.labelLineEdit.setObjectName(_fromUtf8("labelLineEdit"))
        self.gridLayout.addWidget(self.labelLineEdit, 3, 1, 1, 1)
        self.btnLabelLoad = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnLabelLoad.setObjectName(_fromUtf8("btnLabelLoad"))
        self.gridLayout.addWidget(self.btnLabelLoad, 1, 0, 1, 1)
        self.btnLabel = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnLabel.setObjectName(_fromUtf8("btnLabel"))
        self.gridLayout.addWidget(self.btnLabel, 3, 0, 1, 1)
        self.rdbSingleStroke = QtGui.QRadioButton(self.gridLayoutWidget)
        self.rdbSingleStroke.setChecked(True)
        self.rdbSingleStroke.setObjectName(_fromUtf8("rdbSingleStroke"))
        self.gridLayout.addWidget(self.rdbSingleStroke, 5, 0, 1, 1)
        self.rdbMultiStroke = QtGui.QRadioButton(self.gridLayoutWidget)
        self.rdbMultiStroke.setChecked(False)
        self.rdbMultiStroke.setObjectName(_fromUtf8("rdbMultiStroke"))
        self.gridLayout.addWidget(self.rdbMultiStroke, 5, 1, 1, 1)
        self.labelList = QtGui.QListWidget(self.gridLayoutWidget)
        self.labelList.setObjectName(_fromUtf8("labelList"))
        self.gridLayout.addWidget(self.labelList, 6, 0, 1, 2)
        self.labelText = QtGui.QLabel(self.gridLayoutWidget)
        self.labelText.setLineWidth(1)
        self.labelText.setObjectName(_fromUtf8("labelText"))
        self.gridLayout.addWidget(self.labelText, 0, 0, 1, 2)
        self.btnLabelSave = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnLabelSave.setObjectName(_fromUtf8("btnLabelSave"))
        self.gridLayout.addWidget(self.btnLabelSave, 2, 0, 1, 1)
        self.lblCheckIncremental = QtGui.QCheckBox(self.gridLayoutWidget)
        self.lblCheckIncremental.setObjectName(_fromUtf8("lblCheckIncremental"))
        self.gridLayout.addWidget(self.lblCheckIncremental, 4, 0, 1, 1)
        self.lblCheckIncFollow = QtGui.QCheckBox(self.gridLayoutWidget)
        self.lblCheckIncFollow.setObjectName(_fromUtf8("lblCheckIncFollow"))
        self.gridLayout.addWidget(self.lblCheckIncFollow, 4, 1, 1, 1)
        self.tabWidget.addTab(self.labelerTab, _fromUtf8(""))
        self.dataTab = QtGui.QWidget()
        self.dataTab.setObjectName(_fromUtf8("dataTab"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.dataTab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(9, 9, 281, 651))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.dataLabelLocation = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.dataLabelLocation.setObjectName(_fromUtf8("dataLabelLocation"))
        self.gridLayout_2.addWidget(self.dataLabelLocation, 3, 0, 1, 2)
        self.label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.dataRawLocation = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.dataRawLocation.setObjectName(_fromUtf8("dataRawLocation"))
        self.gridLayout_2.addWidget(self.dataRawLocation, 1, 0, 1, 2)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.dataBtnLabelBrowse = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.dataBtnLabelBrowse.setObjectName(_fromUtf8("dataBtnLabelBrowse"))
        self.gridLayout_2.addWidget(self.dataBtnLabelBrowse, 2, 1, 1, 1)
        self.dataBtnRawBrowse = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.dataBtnRawBrowse.setObjectName(_fromUtf8("dataBtnRawBrowse"))
        self.gridLayout_2.addWidget(self.dataBtnRawBrowse, 0, 1, 1, 1)
        self.dataComboSelector = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.dataComboSelector.setObjectName(_fromUtf8("dataComboSelector"))
        self.gridLayout_2.addWidget(self.dataComboSelector, 5, 0, 1, 2)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)
        self.labelTree = QtGui.QTreeWidget(self.gridLayoutWidget_2)
        self.labelTree.setColumnCount(1)
        self.labelTree.setObjectName(_fromUtf8("labelTree"))
        item_0 = QtGui.QTreeWidgetItem(self.labelTree)
        self.labelTree.header().setVisible(False)
        self.gridLayout_2.addWidget(self.labelTree, 6, 0, 1, 2)
        self.dataBtnRefreshFiles = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.dataBtnRefreshFiles.setObjectName(_fromUtf8("dataBtnRefreshFiles"))
        self.gridLayout_2.addWidget(self.dataBtnRefreshFiles, 4, 1, 1, 1)
        self.tabWidget.addTab(self.dataTab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        StaticsRecGUI.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(StaticsRecGUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        StaticsRecGUI.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(StaticsRecGUI)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        StaticsRecGUI.setStatusBar(self.statusbar)
        self.actionLoad_Unlabeled = QtGui.QAction(StaticsRecGUI)
        self.actionLoad_Unlabeled.setObjectName(_fromUtf8("actionLoad_Unlabeled"))
        self.btnLoadLabel = QtGui.QAction(StaticsRecGUI)
        self.btnLoadLabel.setObjectName(_fromUtf8("btnLoadLabel"))
        self.actionSave_Unlabeled = QtGui.QAction(StaticsRecGUI)
        self.actionSave_Unlabeled.setObjectName(_fromUtf8("actionSave_Unlabeled"))

        self.retranslateUi(StaticsRecGUI)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StaticsRecGUI)

    def retranslateUi(self, StaticsRecGUI):
        StaticsRecGUI.setWindowTitle(QtGui.QApplication.translate("StaticsRecGUI", "Statics Recognizer", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLabelTest.setText(QtGui.QApplication.translate("StaticsRecGUI", "TEST", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLabelLoad.setText(QtGui.QApplication.translate("StaticsRecGUI", "Load File...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLabel.setText(QtGui.QApplication.translate("StaticsRecGUI", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.rdbSingleStroke.setText(QtGui.QApplication.translate("StaticsRecGUI", "Single Strokes", None, QtGui.QApplication.UnicodeUTF8))
        self.rdbMultiStroke.setText(QtGui.QApplication.translate("StaticsRecGUI", "Multi-Stroke", None, QtGui.QApplication.UnicodeUTF8))
        self.labelText.setText(QtGui.QApplication.translate("StaticsRecGUI", "Selected:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLabelSave.setText(QtGui.QApplication.translate("StaticsRecGUI", "Save...", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCheckIncremental.setText(QtGui.QApplication.translate("StaticsRecGUI", "Incremental", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCheckIncFollow.setText(QtGui.QApplication.translate("StaticsRecGUI", "Incr. Follow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.labelerTab), QtGui.QApplication.translate("StaticsRecGUI", "Labeler", None, QtGui.QApplication.UnicodeUTF8))
        self.dataLabelLocation.setText(QtGui.QApplication.translate("StaticsRecGUI", "/home/david/Dropbox/Research/Data/PenCaseLabels/", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StaticsRecGUI", "Raw Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.dataRawLocation.setText(QtGui.QApplication.translate("StaticsRecGUI", "/home/david/Dropbox/Research/Data/PencaseDataFix/", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("StaticsRecGUI", "Labels Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.dataBtnLabelBrowse.setText(QtGui.QApplication.translate("StaticsRecGUI", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.dataBtnRawBrowse.setText(QtGui.QApplication.translate("StaticsRecGUI", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("StaticsRecGUI", "Current File:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTree.headerItem().setText(0, QtGui.QApplication.translate("StaticsRecGUI", "Colored Labels", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.labelTree.isSortingEnabled()
        self.labelTree.setSortingEnabled(False)
        self.labelTree.topLevelItem(0).setText(0, QtGui.QApplication.translate("StaticsRecGUI", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTree.setSortingEnabled(__sortingEnabled)
        self.dataBtnRefreshFiles.setText(QtGui.QApplication.translate("StaticsRecGUI", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dataTab), QtGui.QApplication.translate("StaticsRecGUI", "Data Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Unlabeled.setText(QtGui.QApplication.translate("StaticsRecGUI", "Load Unlabeled", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadLabel.setText(QtGui.QApplication.translate("StaticsRecGUI", "Load Labeled", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Unlabeled.setText(QtGui.QApplication.translate("StaticsRecGUI", "Save Unlabeled", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidget import matplotlibwidget
