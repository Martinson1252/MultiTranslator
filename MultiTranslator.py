from asyncio.windows_events import NULL
from cProfile import label
from ctypes import alignment
from fnmatch import translate
from gettext import translation
from msilib.schema import File
from operator import contains
from os import system
from stat import filemode
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
from PyQt5.QtGui import QCursor
import sys
from googletrans import Translator
import os

import googletrans


class App:
    def __init__(self):
        self.multiTranslateBool = False
        self.actLangList = ["pl = polish","en = english","de = german"]
        self.transLangList = ["en = english","pl = polish","de = german"]
        self.AllMultiLangList = []
        self.MultiLangList = []
        self.SetMultiLang()
        self.destLanguage = ""
        self.actualLanguage = ""
        self.editL = QtWidgets.QTextEdit
        self.transL = QtWidgets.QTextEdit
        self.prepareList()
        self.Window()
        

    def prepareList(self):
        date = "pl = polish,en = english,de = german\nen = english,pl = polish,de = german"
        if not os.path.exists("lang.txt") or os.path.exists("lang.txt") and os.path.getsize("lang.txt")==0:
            fs = open("lang.txt","wt")
            fs.write(date)
            fs.close()
        f = open("lang.txt","rt")
        l = f.readlines(-1)
        self.actLangList = list( str( l[0] ).replace("\n","").split(",") )
        self.actualLanguage = (self.actLangList[0])[0]+(self.actLangList[0])[1]
        self.transLangList = list( str( l[1] ).replace("\n","").split(",") )
        self.destLanguage = (self.transLangList[0])[0]+(self.transLangList[0])[1]
        f.close()

    def Translate(self):
        if self.editL.toPlainText()=="": return
        print(self.multiTranslateBool)
        self.transL.setText("")
        translator = Translator()
        print(self.actualLanguage)
        print(self.destLanguage)
        print(self.editL.toPlainText())
        translations = translator.translate(self.editL.toPlainText(),src=self.actualLanguage,dest=self.destLanguage)
        print(translations.text)
        self.transL.setText(translations.text)

    def MultiTranslate(self):
        self.transL.setText("")
        if self.editL.toPlainText()=="": return
        translator = Translator()
        for lang in list( self.multiTransL.toPlainText().split() ):
            if(len(lang)==2 or len(lang)==3 or len(lang)==5 and lang[2]=="-"):
                print(lang)
                if lang not in self.transL.toPlainText():
                    try:
                        translation = translator.translate(self.editL.toPlainText(),src=self.actualLanguage,dest=lang)
                        self.transL.append(lang+": "+translation.text)
                    except: pass

    def SetDestLang(self,var2):
            self.destLanguage = var2[0]+var2[1]
            print(str(var2[0]+var2[1]))
    def SetActLang(self,var2):
            self.actualLanguage = var2[0]+var2[1]
            print(str(var2[0]+var2[1]))

    def SetMultiLang(self):
        index = 0
        for i in googletrans.LANGUAGES:
            self.AllMultiLangList.insert(index,i+" = "+str( googletrans.LANGUAGES.get(i) ))
            index+=1
        #self.AllMultiLangList.sort()
    def Window(self):

        
        #main window
        textColor = "color: #acacac;"
        app = QApplication(sys.argv)
        win = QMainWindow()
        win.setGeometry(700,200,750,500)
        win.setStyleSheet("background: #292827;")

        #text
        label = QtWidgets.QLabel(win)
        label.setText("Text for translation: ")
        label.adjustSize()
        label.move(15,90)
        label.setStyleSheet(textColor)
        #text
        label = QtWidgets.QLabel(win)
        label.setText("Translated text: ")
        label.adjustSize()
        label.move(450,90)
        label.setStyleSheet(textColor)
        #text
        label = QtWidgets.QLabel(win)
        label.setText("Multi translate languages: ")
        label.adjustSize()
        label.move(280,90)
        label.setStyleSheet(textColor)
        #text
        label = QtWidgets.QLabel(win)
        label.setText("Add languages: ")
        label.adjustSize()
        label.move(310,330)
        label.setStyleSheet(textColor)


        #editText label
        self.editL = QtWidgets.QTextEdit(win)
        self.editL.adjustSize()
        #typeL.setMaximumWidth(55) #adjustSize()
        #self.editL.textChanged.connect(self.Translate)
        self.editL.move(15,120)
        self.editL.setStyleSheet(textColor+
        "border: 2px solid #737373;"+
        "background: #211f1f;"+
        "selection-background-color: #34626d;"
        )

        #translation label
        self.transL = QtWidgets.QTextEdit(win)
        self.transL.adjustSize()
        self.transL.setReadOnly(True)
        #typeL.setMaximumWidth(55) #adjustSize()
        self.transL.move(450,120)
        self.transL.setStyleSheet(textColor+
        "border: 2px solid #737373;"+
        "background: #211f1f;"+
        "selection-background-color: #34626d;"
        )

        #multiTranslation label
        self.multiTransL = QtWidgets.QTextEdit(win)
        self.multiTransL.adjustSize()
        #typeL.setMaximumWidth(55) #adjustSize()
        self.multiTransL.setMaximumWidth(120)
        self.multiTransL.move(300,120)
        self.multiTransL.setStyleSheet(textColor+
        "border: 2px solid #737373;"+
        "background: #211f1f;"+
        "selection-background-color: #34626d;"
        )
        #checkbox for multi translate
        MultiTranslateSetB = QtWidgets.QCheckBox(win)
        MultiTranslateSetB.clicked.connect(lambda:  self.__setattr__( "multiTranslateBool", not self.multiTranslateBool ))
        MultiTranslateSetB.move(300,50)
        MultiTranslateSetB.setMinimumWidth(118)
        MultiTranslateSetB.setText("Multi translate")
        MultiTranslateSetB.setStyleSheet(textColor+
        "border: 0px solid #737373;"+
        "indicator:"
                                "{"
                                "background-color: lightgreen;"
                                "}"
        )

        #translate button 
        translateB = QtWidgets.QPushButton(win)
        translateB.move(20,40)
        translateB.setText("Translate")
        translateB.clicked.connect(lambda: self.Translate() if self.multiTranslateBool==False else self.MultiTranslate())
        translateB.setMaximumWidth(70)
        translateB.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        #translateB.setCursor(self,QCursor)
        translateB.setStyleSheet("*{"+textColor+
        "border: 4px solid #3b3b3b;"+
        "border-radius: 15px;"+
        "background: #3b3b3b;}"+
        "*:hover{background: '#34626d';"+
        "border: 4px solid #34626d;}"
        )


        #choose languages from list
        chooseActuLang = QtWidgets.QComboBox(win)
        chooseActuLang.addItems(self.actLangList)
        chooseActuLang.activated.connect(lambda: self.SetActLang(chooseActuLang.currentText())) 
        chooseActuLang.move(150,40)
        chooseActuLang.setMinimumWidth(120)
        chooseActuLang.setStyleSheet(textColor+
        "border: 0px solid #737373;"+
        "background: #3b3b3b;"+
        "selection-background-color: #34626d;"
        )

        #choose languages from list
        chooseTransLang = QtWidgets.QComboBox(win)
        chooseTransLang.addItems(self.transLangList)
        chooseTransLang.activated.connect(lambda: self.SetDestLang(chooseTransLang.currentText())) 
        chooseTransLang.move(450,40)
        chooseTransLang.setMinimumWidth(120)
        chooseTransLang.setStyleSheet(textColor+
        "border: 0px solid #737373;"+
        "background: #3b3b3b;"+
        "selection-background-color: #34626d;"
        )

        #choose multiLanguages from list
        addTransLang = QtWidgets.QComboBox(win)
        addTransLang.addItems(self.AllMultiLangList)
        addTransLang.activated.connect(lambda: self.multiTransL.append(addTransLang.currentText()) if addTransLang.currentText() not in self.multiTransL.toPlainText() else None)
        addTransLang.move(300,350)
        addTransLang.setMinimumWidth(120)
        addTransLang.setStyleSheet(textColor+
        "border: 0px solid #737373;"+
        "background: #3b3b3b;"+
        "selection-background-color: #34626d;"
        )

        

        win.setWindowTitle("Translate")
        win.show()
        sys.exit(app.exec_())
        



App()
