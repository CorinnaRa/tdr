#!/usr/bin/python

import os

from PyQt4 import QtCore, QtGui
from xml.dom.minidom import parse
import math

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MappingWindow(object):
    def setupUi(self, MappingWindow):
        MappingWindow.setObjectName(_fromUtf8("MappingWindow"))
        MappingWindow.resize(845, 598)
        MappingWindow.setWindowTitle(QtGui.QApplication.translate("MappingWindow", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout_2 = QtGui.QVBoxLayout(MappingWindow)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(MappingWindow)
        self.groupBox.setTitle(QtGui.QApplication.translate("MappingWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText(QtGui.QApplication.translate("MappingWindow", "Touch-sensitive object:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(MappingWindow)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MappingWindow", "Touch Visualization", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = VisualizationArea(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setAutoFillBackground(True)
        pal = self.widget.palette()
        pal.setColor(self.widget.backgroundRole(), QtGui.QColor(255,255,255))
        self.widget.setPalette(pal)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        
        self.retranslateUi(MappingWindow)
        QtCore.QMetaObject.connectSlotsByName(MappingWindow)

    def retranslateUi(self, MappingWindow):
        pass

class VisualizationArea(QtGui.QWidget):
    xmlFile = ""
    
    x = 100
    y = 200
    z = 200
    angleX = 0
    angleY = 0
    angleZ = 0
    
    def __init__(self, B):
        QtGui.QWidget.__init__(self, B)
        
    def setXmlFile(self, xmlFile):
        self.xmlFile = xmlFile
        self.x = 100
        self.y = 300
        self.z = 200
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
        
    def paintEvent(self, event):
        if self.xmlFile != "":
            painter = QtGui.QPainter(self)
        
            pen = QtGui.QPen(QtGui.QColor(90,90,90))
            pen.setWidth(3)
            pen.setStyle(QtCore.Qt.DotLine)
            painter.setPen(pen)
        
            dom = parse(self.xmlFile)
            for command in dom.getElementsByTagName("objectBoundary")[0].childNodes:
                if command.nodeType != command.TEXT_NODE:
                    if command.tagName == "draw":
                        newX = self.x + (math.sin(math.radians(self.angleZ))) * float(command.childNodes[0].data)
                        newY = self.y + (math.cos(math.radians(self.angleZ))) * float(command.childNodes[0].data)
                        painter.drawLine(self.x, self.y, newX, newY)
                        self.x = newX
                        self.y = newY
                    else:
                        if command.tagName == "move":
                            self.x = self.x + (math.sin(math.radians(self.angleZ))) * float(command.childNodes[0].data)
                            self.y = self.y + (math.cos(math.radians(self.angleZ))) * float(command.childNodes[0].data)
                        else:
                            if command.tagName == "turnZ":
                                self.angleZ += float(command.childNodes[0].data)
                        

class MappingWindow(QtGui.QDialog, Ui_MappingWindow):
    path = "mapping/objectDescriptions/"
    foundFiles = {}
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("MappingWindow", "No object selected", "no_object_selected", QtGui.QApplication.UnicodeUTF8))
        
        self.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.chooseObject)
        
        i = 1
        for xmlFile in os.listdir(self.path):
            self.foundFiles[i] = xmlFile
            
            dom = parse(self.path + xmlFile)
            self.comboBox.addItem(_fromUtf8(""))
            self.comboBox.setItemText(i, QtGui.QApplication.translate("MappingWindow", xmlFile + ": " + dom.getElementsByTagName("name")[0].childNodes[0].data, xmlFile, QtGui.QApplication.UnicodeUTF8))
            i = i+1
            
    def chooseObject(self):
        currentIndex = self.comboBox.currentIndex()
        
        if currentIndex != 0:
            self.widget.setXmlFile(self.path + self.foundFiles[self.comboBox.currentIndex()])
            self.widget.repaint()
        else:
            self.widget.setXmlFile("")
            self.widget.repaint()