﻿#!/usr/bin/env python
"""Facepager was made for fetching public available data from Facebook, Twitter and other JSON-based API. All data is stored in a SQLite database and may be exported to csv. """

# MIT License

# Copyright (c) 2019 Jakob Jünger and Till Keyling

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import argparse
import html

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget, QStyleFactory


from icons import *
from widgets.datatree import DataTree
from widgets.dictionarytree import DictionaryTree
from actions import *
from apimodules import *
from dialogs.help import *
from widgets.progressbar import ProgressBar
from dialogs.presets import *
from dialogs.timer import *
from dialogs.apiviewer import *
from dialogs.dataviewer import *
from dialogs.selectnodes import *
import logging
import threading
from server import Server, RequestHandler
from dialogs.export import ExportFileDialog
import time
import random

# Some hackery required for pyInstaller
# See https://justcode.nimbco.com/PyInstaller-with-Qt5-WebEngineView-using-PySide2/#could-not-find-qtwebengineprocessexe-on-windows
# if getattr(sys, 'frozen', False) and sys.platform == 'darwin':
#     os.environ['QTWEBENGINEPROCESS_PATH'] = os.path.normpath(os.path.join(
#         sys._MEIPASS, 'PySide2', 'Qt', 'lib',
#         'QtWebEngineCore.framework', 'Helpers', 'QtWebEngineProcess.app',
#         'Contents', 'MacOS', 'QtWebEngineProcess'
#     ))

# Fix BigSur not showing windows
if getattr(sys,'frozen', False) and sys.platform == 'darwin':
    os.environ['QT_MAC_WANTS_LAYER']='1'

class MainWindow(QMainWindow):

    def __init__(self,central=None):
        super(MainWindow,self).__init__()

        self.setWindowTitle("Facepager 4.3")
        self.setWindowIcon(QIcon(":/icons/icon_facepager.png"))
        QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)


        # This is needed to display the app icon on the taskbar on Windows 7
        if os.name == 'nt':
            import ctypes
            myappid = 'Facepager.4.3' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.setMinimumSize(1100,680)
        #self.setMinimumSize(1400,710)
        #self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center()-QPoint(0,100))
        #self.setStyleSheet("* {font-size:21px;}")
        #self.deleteSettings()
        self.lock_logging = threading.Lock()
        self.readSettings()
        self.createActions()

        self.createUI()
        self.createDB()
        self.updateUI()
        self.updateResources()
        self.startServer()
        print("Automation starts here")

        print("Clearing existing nodes")
        self.guiActions.deleteAllNodes()

        #getting id
        with open("input.txt", "r") as file:
            lines = file.readlines()
            print('lines: ', end='')
            print(lines)
        fbid = lines[0].strip('\n')
        num = lines[1].strip('\n')
        num =eval(num)//100
        print('fbid: '+fbid)
        print('num: '+str(num))
        self.apiActions.addNodes(newnodes=[fbid])
        print('Facebook ID '+fbid+' added')

        print('Fetching posts')
        for i in range(num):
            self.apiActions.fetchData()
            curr = datetime.now().strftime("%H:%M:%S")
            print("\nTime: "+curr)
            #1 minute
            sleeptime=60
            print("sleeping for "+str(sleeptime)+'second(s)')
           time.sleep(sleeptime)

        print('\nFetching comments')
        self.levelEdit.setMinimum(2)
        #########
        for i in range(10):
            self.apiActions.fetchData()
            curr = datetime.now().strftime("%H:%M:%S")
            print("\nTime: "+curr)
            #30 minutes to 1 hour
            sleeptime=random.randint(1800, 3600)
            print("sleeping for "+str(sleeptime)+'second(s)')
            time.sleep(sleeptime)

        print('\nFetching replies')
        self.levelEdit.setMinimum(3)
        self.apiActions.fetchData()
        curr = datetime.now().strftime("%H:%M:%S")
        print("\nTime: "+curr)
        
        self.levelEdit.setMinimum(1)

        self.guiActions.addAllColumns() 
        
        #export to csv
        d1 = datetime.now().strftime("%d%m%Y_%H%M%S")
        csvpath = r'../csv/fb_'+d1+'.csv'
        output = open(csvpath, 'w', newline='', encoding='utf8')
        ExportFileDialog(self).exportAllNodes(output) 
        print('fb_'+d1+'.csv')
        print("Automation ends here")
        
        #close window
        sys.exit()

    def createDB(self):
        self.database = Database(self)

        dbname= cmd_args.database #sys.argv[1] if len(sys.argv) > 1 else None
        #lastpath = self.settings.value("lastpath")
        #lastpath = 'C:\\Users\\huayq\\Desktop\\processor\\Facepager\\db1.db'
        lastpath = r'Facepager\db1.db'
        if dbname and os.path.isfile(dbname):
            self.database.connect(dbname)
        elif lastpath and os.path.isfile(lastpath):
            self.database.connect(self.settings.value("lastpath"))

        self.tree.loadData(self.database)
        self.guiActions.actionShowColumns.trigger()

    def createActions(self):
        self.apiActions = ApiActions(self)
        self.guiActions = GuiActions(self, self.apiActions)
        self.serverActions = ServerActions(self, self.apiActions)
    def createUI(self):
        #
        #  Windows
        #

        self.progressWindow = None
        self.helpwindow=HelpWindow(self)
        self.presetWindow=PresetWindow(self)
        self.presetWindow.logmessage.connect(self.logmessage)
        self.apiWindow = ApiViewer(self)
        self.apiWindow.logmessage.connect(self.logmessage)
        self.dataWindow = DataViewer(self)
        self.timerWindow=TimerWindow(self)
        self.selectNodesWindow=SelectNodesWindow(self)

        self.timerWindow.timerstarted.connect(self.guiActions.timerStarted)
        self.timerWindow.timerstopped.connect(self.guiActions.timerStopped)
        self.timerWindow.timercountdown.connect(self.guiActions.timerCountdown)
        self.timerWindow.timerfired.connect(self.guiActions.timerFired)

        #
        #  Statusbar and toolbar
        #

        self.statusbar = self.statusBar()
        self.toolbar=Toolbar(parent=self,mainWindow=self)
        self.addToolBar(Qt.TopToolBarArea,self.toolbar)

        self.timerStatus = QLabel("Timer stopped ")
        self.statusbar.addPermanentWidget(self.timerStatus)

        self.databaseLabel = QPushButton("No database connection ")
        self.statusbar.addWidget(self.databaseLabel)

        self.selectionStatus = QLabel("0 node(s) selected ")
        self.statusbar.addPermanentWidget(self.selectionStatus)
        #self.statusBar.showMessage('No database connection')
        self.statusbar.setSizeGripEnabled(False)

        self.databaseLabel.setFlat(True)
        self.databaseLabel.clicked.connect(self.databaseLabelClicked)


        #
        #  Layout
        #

        #dummy widget to contain the layout manager
        self.mainWidget=QSplitter(self)
        self.mainWidget.setOrientation(Qt.Vertical)
        self.setCentralWidget(self.mainWidget)

        #top
        topWidget=QWidget(self)
        self.mainWidget.addWidget(topWidget)
        dataLayout=QHBoxLayout()
        topWidget.setLayout(dataLayout)
        dataSplitter = QSplitter(self)
        dataLayout.addWidget(dataSplitter)

        #top left
        dataWidget=QWidget()
        dataLayout=QVBoxLayout()
        dataLayout.setContentsMargins(0,0,0,0)
        dataWidget.setLayout(dataLayout)
        dataSplitter.addWidget(dataWidget)
        dataSplitter.setStretchFactor(0, 1)

        #top right
        detailSplitter=QSplitter(self)
        detailSplitter.setOrientation(Qt.Vertical)

        #top right top
        detailWidget=QWidget(self)
        detailLayout=QVBoxLayout()
        detailLayout.setContentsMargins(11,0,0,0)
        detailWidget.setLayout(detailLayout)
        detailSplitter.addWidget(detailWidget)

        dataSplitter.addWidget(detailSplitter)
        dataSplitter.setStretchFactor(1, 0);

        #bottom
        bottomSplitter=QSplitter(self)
        self.mainWidget.addWidget(bottomSplitter)
        self.mainWidget.setStretchFactor(0, 1);

        #requestLayout=QHBoxLayout()
        #bottomWidget.setLayout(requestLayout)

        #bottom left
        modulesWidget = QWidget(self)
        moduleslayout=QVBoxLayout()
        modulesWidget.setLayout(moduleslayout)
        bottomSplitter.addWidget(modulesWidget)

        #bottom middle
        fetchWidget = QWidget(self)
        fetchLayout=QVBoxLayout()
        fetchWidget.setLayout(fetchLayout)
        bottomSplitter.addWidget(fetchWidget)

        settingsGroup=QGroupBox("Settings")
        fetchLayout.addWidget(settingsGroup)

        fetchsettings = QFormLayout()
        fetchsettings.setRowWrapPolicy(QFormLayout.DontWrapRows)
        fetchsettings.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        fetchsettings.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        fetchsettings.setLabelAlignment(Qt.AlignLeft)
        settingsGroup.setLayout(fetchsettings)
        #fetchLayout.addLayout(fetchsettings)

        fetchdata=QHBoxLayout()
        fetchdata.setContentsMargins(10,0,10,0)
        fetchLayout.addLayout(fetchdata)

        #bottom right
        statusWidget = QWidget(self)
        statusLayout=QVBoxLayout()
        statusWidget.setLayout(statusLayout)
        bottomSplitter.addWidget(statusWidget)

        #
        # Settings widget
        #

        self.settingsWidget = QWidget()
        self.settingsLayout = QFormLayout()
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsWidget.setLayout(self.settingsLayout)

        # Add headers
        self.headersCheckbox = QCheckBox("Create header nodes",self)
        self.headersCheckbox.setChecked(str(self.settings.value('saveheaders', 'false')) == 'true')
        self.headersCheckbox.setToolTip(
            wraptip("Check if you want to create nodes containing headers of the response."))
        self.settingsLayout.addRow(self.headersCheckbox)

        # Timeout
        self.timeoutEdit = QSpinBox(self)
        self.timeoutEdit.setMinimum(1)
        self.timeoutEdit.setMaximum(300)
        self.timeoutEdit.setToolTip(
            wraptip("How many seconds will you wait for a response?"))
        self.timeoutEdit.setValue(self.settings.value('timeout',15))
        self.settingsLayout.addRow('Request timeout',self.timeoutEdit)

        # Expand Box
        self.autoexpandCheckbox = QCheckBox("Expand new nodes",self)
        self.autoexpandCheckbox.setToolTip(wraptip(
            "Check to automatically expand new nodes when fetching data. Disable for big queries to speed up the process."))
        self.settingsLayout.addRow(self.autoexpandCheckbox)
        self.autoexpandCheckbox.setChecked(str(self.settings.value('expand', 'true')) == 'true')

        # Log Settings
        self.logCheckbox = QCheckBox("Log all requests",self)
        self.logCheckbox.setToolTip(
            wraptip("Check to see every request in the status log; uncheck to hide request messages."))
        self.settingsLayout.addRow( self.logCheckbox)
        self.logCheckbox.setChecked(str(self.settings.value('logrequests', 'true')) == 'true')

        # Clear setttings
        self.clearCheckbox = QCheckBox("Clear settings when closing.",self)
        self.settings.beginGroup("GlobalSettings")
        self.clearCheckbox.setChecked(str(self.settings.value('clearsettings', 'false')) == 'true')
        self.settings.endGroup()

        self.clearCheckbox.setToolTip(wraptip(
            "Check to clear all settings and access tokens when closing Facepager. You should check this on public machines to clear credentials."))
        self.settingsLayout.addRow(self.clearCheckbox)

        # Style
        self.styleEdit = QComboBox(self)
        self.styleEdit.setToolTip(wraptip("Choose the styling of Facepager."))

        styles = [x for x in QStyleFactory.keys() if x != "Windows"]
        styles = ['<default>'] + styles

        self.styleEdit.insertItems(0, styles)
        self.styleEdit.setCurrentText(self.settings.value('style', '<default>'))

        self.styleEdit.currentIndexChanged.connect(self.setStyle)
        self.settingsLayout.addRow('Style', self.styleEdit)

        #
        #  Components
        #

        #main tree
        treetoolbar = QToolBar(self)
        treetoolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon);
        treetoolbar.setIconSize(QSize(16,16))

        treetoolbar.addActions(self.guiActions.treeActions.actions())
        dataLayout.addWidget (treetoolbar)

        self.tree=DataTree(self.mainWidget)
        self.tree.nodeSelected.connect(self.guiActions.treeNodeSelected)
        self.tree.logmessage.connect(self.logmessage)
        self.tree.showprogress.connect(self.showprogress)
        self.tree.hideprogress.connect(self.hideprogress)
        self.tree.stepprogress.connect(self.stepprogress)
        dataLayout.addWidget(self.tree)


        #right sidebar - toolbar
        detailtoolbar = QToolBar(self)
        detailtoolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon);
        detailtoolbar.setIconSize(QSize(16,16))
        detailtoolbar.addActions(self.guiActions.detailActions.actions())
        detailLayout.addWidget(detailtoolbar)

        #right sidebar - json viewer
        self.detailTree=DictionaryTree(self.mainWidget,self.apiWindow)
        detailLayout.addWidget(self.detailTree)

        #right sidebar - column setup
        detailGroup=QGroupBox("Custom Table Columns (one key per line)")
        detailSplitter.addWidget(detailGroup)
        groupLayout=QVBoxLayout()
        detailGroup.setLayout(groupLayout)

        self.fieldList=QTextEdit()
        self.fieldList.setLineWrapMode(QTextEdit.NoWrap)
        self.fieldList.setWordWrapMode(QTextOption.NoWrap)
        self.fieldList.acceptRichText=False
        self.fieldList.clear()
        self.fieldList.append('name')
        self.fieldList.append('message')
        self.fieldList.setPlainText(self.settings.value('columns',self.fieldList.toPlainText()))
        groupLayout.addWidget(self.fieldList)

        #column setup toolbar
        columntoolbar = QToolBar(self)
        columntoolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon);
        columntoolbar.setIconSize(QSize(16,16))
        columntoolbar.addActions(self.guiActions.columnActions.actions())
        groupLayout.addWidget(columntoolbar)

        #Requests/Apimodules
        self.RequestTabs=QTabWidget()
        moduleslayout.addWidget(self.RequestTabs)
        self.RequestTabs.addTab(YoutubeTab(self),"YouTube")
        self.RequestTabs.addTab(TwitterTab(self),"Twitter")
        self.RequestTabs.addTab(TwitterStreamingTab(self),"Twitter Streaming")
        self.RequestTabs.addTab(FacebookTab(self), "Facebook")
        self.RequestTabs.addTab(AmazonTab(self),"Amazon")
        self.RequestTabs.addTab(GenericTab(self),"Generic")

        #module = self.settings.value('module',False)
        module = 'Facebook'
        tab = self.getModule(module)
        print("module")
        print(module)
        if tab is not None:
            self.RequestTabs.setCurrentWidget(tab)

        #Fetch settings
        #-Level
        self.levelEdit=QSpinBox(self.mainWidget)
        self.levelEdit.setMinimum(1)
        self.levelEdit.setToolTip(wraptip("Based on the selected nodes, only fetch data for nodes and subnodes of the specified level (base level is 1)"))
        fetchsettings.addRow("Node level",self.levelEdit)
        #-Selected nodes
        self.allnodesCheckbox = QCheckBox(self)
        ##
        self.allnodesCheckbox.setCheckState(Qt.Checked)
        self.allnodesCheckbox.setToolTip(wraptip("Check if you want to fetch data for all nodes. This helps with large datasets because manually selecting all nodes slows down Facepager."))
        fetchsettings.addRow("Select all nodes", self.allnodesCheckbox)

        #-Empty nodes
        self.emptyCheckbox = QCheckBox(self)
        self.emptyCheckbox.setCheckState(Qt.Unchecked)
        self.emptyCheckbox.setToolTip(wraptip("Check if you want process only empty nodes."))
        fetchsettings.addRow("Only empty nodes", self.emptyCheckbox)

        #Object types
        self.typesEdit = QLineEdit('offcut, headers')
        self.typesEdit.setToolTip(wraptip("Skip nodes with these object types, comma separated list. Normally this should not be changed."))
        fetchsettings.addRow("Exclude object types",self.typesEdit)

        #-Continue pagination
        self.resumeCheckbox = QCheckBox(self)
        self.resumeCheckbox.setCheckState(Qt.Checked)
        self.resumeCheckbox.setToolTip(wraptip("Check if you want to continue collection after fetching was cancelled or nodes were skipped. The last fetched offcut or data node is used to determine the pagination value. Nodes are skipped if no pagination value can be found. Nodes without children having status fetched(200) are processed anyway."))
        fetchsettings.addRow("Resume collection", self.resumeCheckbox)

        # Thread Box
        self.threadsEdit = QSpinBox(self)
        self.threadsEdit.setMinimum(1)
        self.threadsEdit.setMaximum(40)
        self.threadsEdit.setToolTip(wraptip("The number of concurrent threads performing the requests. Higher values increase the speed, but may result in API-Errors/blocks"))
        fetchsettings.addRow("Parallel Threads", self.threadsEdit)

        # Speed Box
        self.speedEdit = QSpinBox(self)
        self.speedEdit.setMinimum(1)
        self.speedEdit.setMaximum(60000)
        self.speedEdit.setValue(200)
        self.speedEdit.setToolTip(wraptip("Limit the total amount of requests per minute (calm down to avoid API blocking)"))
        fetchsettings.addRow("Requests per minute", self.speedEdit)

        #Error Box
        self.errorEdit = QSpinBox(self)
        self.errorEdit.setMinimum(1)
        self.errorEdit.setMaximum(100)
        self.errorEdit.setValue(10)
        self.errorEdit.setToolTip(wraptip("Set the number of consecutive errors after which fetching will be cancelled. Please handle with care! Continuing with erroneous requests places stress on the servers."))
        fetchsettings.addRow("Maximum errors", self.errorEdit)

        #More
        button=QPushButton(QIcon(":/icons/more.png"),"", self.mainWidget)
        button.setToolTip(wraptip("Can't get enough? Here you will find even more settings!"))
        # button.setMinimumSize(QSize(120,40))
        # button.setIconSize(QSize(32,32))
        button.clicked.connect(self.guiActions.actionSettings.trigger)
        fetchsettings.addRow("More settings", button)
        
        #Fetch data

        #-button
        f=QFont()
        f.setPointSize(11)
        button=QPushButton(QIcon(":/icons/fetch.png"),"Fetch Data", self.mainWidget)
        button.setToolTip(wraptip("Fetch data from the API with the current settings. If you click the button with the control key pressed, a browser window is opened instead."))
        button.setMinimumSize(QSize(120,40))
        button.setIconSize(QSize(32,32))
        button.clicked.connect(self.guiActions.actionQuery.trigger)
        button.setFont(f)
        fetchdata.addWidget(button,1)

        #-timer button
        button=QToolButton(self.mainWidget)
        button.setIcon(QIcon(":/icons/timer.png"))
        button.setMinimumSize(QSize(40,40))
        button.setIconSize(QSize(25,25))
        button.clicked.connect(self.guiActions.actionTimer.trigger)
        fetchdata.addWidget(button,1)

        #Status
        detailGroup=QGroupBox("Status Log")
        groupLayout=QVBoxLayout()
        detailGroup.setLayout(groupLayout)
        statusLayout.addWidget(detailGroup,1)


        self.loglist=QTextEdit()
        self.loglist.setLineWrapMode(QTextEdit.NoWrap)
        self.loglist.setWordWrapMode(QTextOption.NoWrap)
        self.loglist.acceptRichText=False
        self.loglist.clear()
        groupLayout.addWidget(self.loglist)

    def setStyle(self):
        style = self.styleEdit.currentText()
        try:
            if style == '<default>':
                style = self.styleEdit.itemText(1)
            QApplication.setStyle(style)
        except Exception as e:
            self.logmessage(e)

    def databaseLabelClicked(self):
        if self.database.connected:
            if platform.system() == "Windows":
                webbrowser.open(os.path.dirname(self.database.filename))
            elif platform.system() == "Darwin":
                webbrowser.open('file:///'+os.path.dirname(self.database.filename))
            else:
                webbrowser.open('file:///'+os.path.dirname(self.database.filename))


    def getModule(self,module):
        for i in range(0, self.RequestTabs.count()):
            if self.RequestTabs.widget(i).name == module:
                tab = self.RequestTabs.widget(i)
                return tab
        return None

    def updateUI(self):
        #disable buttons that do not work without an opened database
        self.guiActions.databaseActions.setEnabled(self.database.connected)
        self.guiActions.actionQuery.setEnabled(self.tree.selectedCount() > 0)

        if self.database.connected:
            #self.statusBar().showMessage(self.database.filename)
            self.databaseLabel.setText(self.database.filename)
        else:
            #self.statusBar().showMessage('No database connection')
            self.databaseLabel.setText('No database connection')

    # Downloads default presets and api definitions in the background
    def updateResources(self):

        self.apiWindow.checkDefaultFiles()
        self.presetWindow.checkDefaultFiles()

        def getter():
            self.apiWindow.downloadDefaultFiles(True)
            self.presetWindow.downloadDefaultFiles(True)

        t = threading.Thread(target=getter)
        t.start()

    def startServer(self):
        port = cmd_args.port
        if port is None:
            self.serverInstance = None
            self.serverThread = None
            return False

        self.serverInstance = Server(port, self.serverActions)
        self.serverThread = threading.Thread(target=self.serverInstance.serve_forever)
        self.serverThread.start()
        self.logmessage('Server started on http://localhost:%d.' % port)

    def stopServer(self):
        if self.serverInstance is not None:
            self.serverInstance.shutdown()
            self.logmessage("Server stopped")

    def cleanupModules(self):
        for i in range(self.RequestTabs.count()):
            self.RequestTabs.widget(i).cleanup()

    def writeSettings(self):
        QCoreApplication.setOrganizationName("Strohne")
        QCoreApplication.setApplicationName("Facepager")

        self.settings = QSettings()
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("version","4.3")
        self.settings.endGroup()


        self.settings.setValue('columns',self.fieldList.toPlainText())
        self.settings.setValue('module',self.RequestTabs.currentWidget().name)
        self.settings.setValue("lastpath", self.database.filename)

        self.settings.setValue('saveheaders', self.autoexpandCheckbox.isChecked())
        self.settings.setValue('expand', self.autoexpandCheckbox.isChecked())
        self.settings.setValue('logrequests', self.logCheckbox.isChecked())
        self.settings.setValue('style', self.styleEdit.currentText())

        self.settings.beginGroup("GlobalSettings")
        self.settings.setValue("clearsettings", self.clearCheckbox.isChecked())
        self.settings.endGroup()

        for i in range(self.RequestTabs.count()):
            self.RequestTabs.widget(i).saveSettings()

    def readSettings(self):
        QSettings.setDefaultFormat(QSettings.IniFormat)
        QCoreApplication.setOrganizationName("Strohne")
        QCoreApplication.setApplicationName("Facepager")
        self.settings = QSettings()

    def deleteSettings(self):
        QSettings.setDefaultFormat(QSettings.IniFormat)
        QCoreApplication.setOrganizationName("Strohne")
        QCoreApplication.setApplicationName("Facepager")
        self.settings = QSettings()

        self.settings.clear()
        self.settings.sync()

        self.settings.beginGroup("GlobalSettings")
        self.settings.setValue("clearsettings", self.clearCheckbox.isChecked())
        self.settings.endGroup()


    def closeEvent(self, event=QCloseEvent()):
        if self.close():
            if self.clearCheckbox.isChecked():
                self.deleteSettings()
            else:
                self.writeSettings()

            self.stopServer()
            self.cleanupModules()
            event.accept()
        else:
            event.ignore()

    @Slot(str)
    def logmessage(self, message):
        with self.lock_logging:
            if isinstance(message, Exception):
                self.loglist.append(str(datetime.now())+" Exception: "+str(message))
                logging.exception(message)

            else:
                self.loglist.append(str(datetime.now())+" "+message)
            time.sleep(0)

    def getlog(self):
        with self.lock_logging:
            return self.loglist.toPlainText().splitlines()

    @Slot(str)
    def showprogress(self, maximum=None):
        pass
        # if self.progressWindow is None:
        #     self.progressWindow = ProgressBar("Loading nodes...",self)
        #
        # self.progressWindow.setMaximum(maximum)


    @Slot(str)
    def stepprogress(self):
        pass
        # if (self.progressWindow is not None):
        #     self.progressWindow.step()

    @Slot(str)
    def hideprogress(self):
        pass
        # if self.progressWindow is not None:
        #     self.progressWindow.close()
        #     self.progressWindow = None

class Toolbar(QToolBar):
    """
    Initialize the main toolbar for the facepager - that provides the central interface and functions.
    """
    def __init__(self,parent=None,mainWindow=None):
        super(Toolbar,self).__init__(parent)
        self.mainWindow=mainWindow
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon);
        self.setIconSize(QSize(24,24))

        self.addActions(self.mainWindow.guiActions.basicActions.actions())
        self.addSeparator()
        self.addActions(self.mainWindow.guiActions.databaseActions.actions())

        self.addSeparator()
        #self.addAction(self.mainWindow.actions.actionExpandAll)
        #self.addAction(self.mainWindow.actions.actionCollapseAll)
        #self.addAction(self.mainWindow.actions.actionSelectNodes)
        self.addAction(self.mainWindow.guiActions.actionLoadPreset)
        self.addAction(self.mainWindow.guiActions.actionLoadAPIs)
        self.addAction(self.mainWindow.guiActions.actionHelp)



# See https://stackoverflow.com/questions/4795757/is-there-a-better-way-to-wordwrap-text-in-qtooltip-than-just-using-regexp
class QAwesomeTooltipEventFilter(QObject):
    '''
    Tooltip-specific event filter dramatically improving the tooltips of all
    widgets for which this filter is installed.

    Motivation
    ----------
    **Rich text tooltips** (i.e., tooltips containing one or more HTML-like
    tags) are implicitly wrapped by Qt to the width of their parent windows and
    hence typically behave as expected.

    **Plaintext tooltips** (i.e., tooltips containing no such tags), however,
    are not. For unclear reasons, plaintext tooltips are implicitly truncated to
    the width of their parent windows. The only means of circumventing this
    obscure constraint is to manually inject newlines at the appropriate
    80-character boundaries of such tooltips -- which has the distinct
    disadvantage of failing to scale to edge-case display and device
    environments (e.g., high-DPI). Such tooltips *cannot* be guaranteed to be
    legible in the general case and hence are blatantly broken under *all* Qt
    versions to date. This is a `well-known long-standing issue <issue_>`__ for
    which no official resolution exists.

    This filter globally addresses this issue by implicitly converting *all*
    intercepted plaintext tooltips into rich text tooltips in a general-purpose
    manner, thus wrapping the former exactly like the latter. To do so, this
    filter (in order):

    #. Auto-detects whether the:

       * Current event is a :class:`QEvent.ToolTipChange` event.
       * Current widget has a **non-empty plaintext tooltip**.

    #. When these conditions are satisfied:

       #. Escapes all HTML syntax in this tooltip (e.g., converting all ``&``
          characters to ``&amp;`` substrings).
       #. Embeds this tooltip in the Qt-specific ``<qt>...</qt>`` tag, thus
          implicitly converting this plaintext tooltip into a rich text tooltip.

    .. _issue:
        https://bugreports.qt.io/browse/QTBUG-41051
    '''


    def eventFilter(self, widget: QObject, event: QEvent) -> bool:
        '''
        Tooltip-specific event filter handling the passed Qt object and event.
        '''


        # If this is a tooltip event...
        if event.type() == QEvent.ToolTipChange:
            # If the target Qt object containing this tooltip is *NOT* a widget,
            # raise a human-readable exception. While this should *NEVER* be the
            # case, edge cases are edge cases because they sometimes happen.
            if not isinstance(widget, QWidget):
                raise ValueError('QObject "{}" not a widget.'.format(widget))

            # Tooltip for this widget if any *OR* the empty string otherwise.
            tooltip = widget.toolTip()

            # If this tooltip is both non-empty and not already rich text...
            if tooltip and not tooltip.startswith('<'): #not Qt.mightBeRichText(tooltip):
                tooltip = '<qt>{}</qt>'.format(html.escape(tooltip))
                widget.setToolTip(tooltip)

                # Notify the parent event handler this event has been handled.
                return True

        # Else, defer to the default superclass handling of this event.
        return super().eventFilter(widget, event)



def startMain():
    app = QApplication(sys.argv)

    # Word wrap tooltips (does not work yet, chrashes app)
    #tooltipfilter = QAwesomeTooltipEventFilter(app)
    #app.installEventFilter(tooltipfilter)

    main=MainWindow(QMainWindow)

    # Change styling
    if cmd_args.style is not None:
        QApplication.setStyle(cmd_args.style)
    #elif sys.platform == 'darwin':
    #    QApplication.setStyle('Fusion')
    elif main.settings.value('style', '<default>') != '<default>':
        QApplication.setStyle(main.settings.value('style'))

    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Logging
    try:
        logfolder = os.path.join(os.path.expanduser("~"),'Facepager','Logs')
        if not os.path.isdir(logfolder):
            os.makedirs(logfolder)
        logging.basicConfig(filename=os.path.join(logfolder,'facepager.log'),level=logging.ERROR,format='%(asctime)s %(levelname)s:%(message)s')
    except Exception as e:
        print("Error intitializing log file: {}".format(e.message))

    # Command line options
    cmd_args = argparse.ArgumentParser(description='Run Facepager.')

    cmd_args.add_argument('database', help='Database file to open', nargs='?')
    cmd_args.add_argument('--style', dest='style', default=None, help='Select the PySide style, for example Fusion')
    cmd_args.add_argument('--server', dest='port', default=None, type=int, help='Start a local server at the given port') #8009

    cmd_args = cmd_args.parse_args()

    # Locate the SSL certificate for requests
    # todo: no longer necessary because requests uses certifi? https://requests.readthedocs.io/en/master/user/advanced/#ca-certificates
    # os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(getResourceFolder() , 'ssl', 'cacert.pem')

    startMain()
