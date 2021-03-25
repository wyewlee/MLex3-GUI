from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QFileDialog, QCheckBox, QComboBox, QLabel, QHBoxLayout
import csv
from widgets.progressbar import ProgressBar
from database import *
##
from datetime import datetime


class ExportFileDialog(object):
    """
    Create a custom Export-File Dialog with options like BOM etc.
    """

    def __init__(self,mainWindow):
        #super(ExportFileDialog,self).__init__(*args,**kwargs)

        self.mainWindow = mainWindow
        


    def exportSelectedNodes(self,output):
        progress = ProgressBar("Exporting data...", self.mainWindow)

        #indexes = self.mainWindow.tree.selectionModel().selectedRows()
        #if child nodes should be exported as well, uncomment this line an comment the previous one
        indexes = self.mainWindow.tree.selectedIndexesAndChildren()
        indexes = list(indexes)
        progress.setMaximum(len(indexes))

        try:
            writer = csv.writer(output, quotechar='"', quoting=csv.QUOTE_ALL, doublequote=True,
                                lineterminator='\r\n')


            #headers
            row = [str(val) for val in self.mainWindow.tree.treemodel.getRowHeader()]
            row = [val.replace('\n', ' ').replace('\r',' ') for val in row]
            row = ['path'] + row
            writer.writerow(row)

            #rows
            path = []
            for index in indexes:
                if progress.wasCanceled:
                    break

                # data
                rowdata = self.mainWindow.tree.treemodel.getRowData(index)

                # path of parents (#2=level;#3=object ID)
                while rowdata[2] < len(path):
                    path.pop()
                path.append(rowdata[3])

                # values
                row = [str(val) for val in rowdata]
                row = ["/".join(path)] + row
                row = [val.replace('\n', ' ').replace('\r',' ') for val in row]

                writer.writerow(row)

                progress.step()

        finally:
            progress.close()


    def exportAllNodes(self,output):
        print("Exporting all nodes to csv file named as ", end='')
        progress = ProgressBar("Exporting data...", self.mainWindow)
        progress.setMaximum(Node.query.count())

        try:
            #delimiter = self.optionSeparator.currentText()
            #delimiter = delimiter.encode('utf-8').decode('unicode_escape')
            writer = csv.writer(output, quotechar='"',
                                quoting=csv.QUOTE_ALL, doublequote=True,
                                lineterminator='\r\n')

            # Headers
            row = ["level", "id", "parent_id", "object_id", "object_type",
                   "query_status", "query_time", "query_type"]
            for key in extractNames(self.mainWindow.tree.treemodel.customcolumns):
                row.append(key)
            row = [val.replace('\n', ' ').replace('\r',' ') for val in row]
            writer.writerow(row)

            # Rows
            page = 0
            while not progress.wasCanceled:
                allnodes = Node.query.offset(page * 5000).limit(5000)
                if allnodes.count() == 0:
                    break

                for node in allnodes:
                    if progress.wasCanceled:
                        break
                    #print(row[0])
                    row = [node.level, node.id, node.parent_id, node.objectid,
                           node.objecttype, node.querystatus, node.querytime, node.querytype]
                    for key in self.mainWindow.tree.treemodel.customcolumns:
                        row.append(node.getResponseValue(key)[1])

                    #if self.optionLinebreaks.isChecked():
                    row = [str(val).replace('\n', ' ').replace('\r',' ') for val in row]

                    writer.writerow(row)

                    # Step the bar
                    progress.step()

                page += 1

        finally:
            progress.close()
