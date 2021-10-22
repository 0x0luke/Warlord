from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCharts import QtCharts
import sys
import os.path
from virustotal_python import Virustotal
from pprint import pprint
import hashlib
import json
import re
import requests

class WebAppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web App Testing")
        self.resize(640,480)
        self.layout = QtWidgets.QVBoxLayout()

        self.UrlBox = QtWidgets.QTextEdit(self)
        self.UrlBox.setGeometry(QtCore.QRect(270, 90, 30, 31))
        self.UrlBox.setObjectName("UrlBox")
        self.UrlBox.setText("Place the URL here!")

        # file selector code
        self.filebtn = QtWidgets.QPushButton("Select a payload file to test")
        self.filebtn.setGeometry(QtCore.QRect(30, 90, 80, 23))
        self.filebtn.clicked.connect(self.getExploits)
        self.filePathBox = QtWidgets.QTextEdit(self)
        self.filePathBox.setGeometry(QtCore.QRect(10, 90, 30, 31))
        self.filePathBox.setObjectName("filePathBox")
        self.layout.addWidget(self.filebtn)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 280, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.accept)

        self.layout.addWidget(self.filebtn)
        self.layout.addWidget(self.filePathBox)
        self.layout.addWidget(self.buttonBox)
        self.layout.addWidget(self.UrlBox)

        self.errMsg = QtWidgets.QMessageBox(self)
        self.setLayout(self.layout)

    def accept(self):
        WebAppWindow.webRequest(self)

    def getExploits(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
        "c:\\")[0]
        self.filePathBox.setText(fname)
        return fname

    def webRequest(self):
        filename = self.filePathBox.toPlainText()
        url = self.UrlBox.toPlainText()
        with open(filename, encoding="utf-8") as file:
            payloads = file.readlines()
            for line in payloads:
                request = requests.get(url + line.strip())
                if request.status_code != 200:
                    self.errMsg.setWindowTitle("Error!")
                    self.errMsg.setText("The website gave us response code " + str(request.status_code) + "!\nScanning won't work correctly!")
                    self.errMsg.setIcon(QtWidgets.QMessageBox.Critical)
                    box = self.errMsg.exec_()
                
                #Vuln detection logic
                XSSRegex = len(re.findall("<[^\w<>]*(?:[^<>\"'\s]*:)?[^\w<>]*(?:\W*s\W*c\W*r\W*i\W*p\W*t|\W*f\W*o\W*r\W*m|\W*s\W*t\W*y\W*l\W*e|\W*s\W*v\W*g|\W*m\W*a\W*r\W*q\W*u\W*e\W*e|(?:\W*l\W*i\W*n\W*k|\W*o\W*b\W*j\W*e\W*c\W*t|\W*e\W*m\W*b\W*e\W*d|\W*a\W*p\W*p\W*l\W*e\W*t|\W*p\W*a\W*r\W*a\W*m|\W*i?\W*f\W*r\W*a\W*m\W*e|\W*b\W*a\W*s\W*e|\W*b\W*o\W*d\W*y|\W*m\W*e\W*t\W*a|\W*i\W*m\W*a?\W*g\W*e?|\W*v\W*i\W*d\W*e\W*o|\W*a\W*u\W*d\W*i\W*o|\W*b\W*i\W*n\W*d\W*i\W*n\W*g\W*s|\W*s\W*e\W*t|\W*i\W*s\W*i\W*n\W*d\W*e\W*x|\W*a\W*n\W*i\W*m\W*a\W*t\W*e)[^>\w])|(?:<\w[\s\S]*[\s\0\/]|['\"])(?:formaction|style|background|src|lowsrc|ping|on(?:d(?:e(?:vice(?:(?:orienta|mo)tion|proximity|found|light)|livery(?:success|error)|activate)|r(?:ag(?:e(?:n(?:ter|d)|xit)|(?:gestur|leav)e|start|drop|over)?|op)|i(?:s(?:c(?:hargingtimechange|onnect(?:ing|ed))|abled)|aling)|ata(?:setc(?:omplete|hanged)|(?:availabl|chang)e|error)|urationchange|ownloading|blclick)|Moz(?:M(?:agnifyGesture(?:Update|Start)?|ouse(?:PixelScroll|Hittest))|S(?:wipeGesture(?:Update|Start|End)?|crolledAreaChanged)|(?:(?:Press)?TapGestur|BeforeResiz)e|EdgeUI(?:C(?:omplet|ancel)|Start)ed|RotateGesture(?:Update|Start)?|A(?:udioAvailable|fterPaint))|c(?:o(?:m(?:p(?:osition(?:update|start|end)|lete)|mand(?:update)?)|n(?:t(?:rolselect|extmenu)|nect(?:ing|ed))|py)|a(?:(?:llschang|ch)ed|nplay(?:through)?|rdstatechange)|h(?:(?:arging(?:time)?ch)?ange|ecking)|(?:fstate|ell)change|u(?:echange|t)|l(?:ick|ose))|m(?:o(?:z(?:pointerlock(?:change|error)|(?:orientation|time)change|fullscreen(?:change|error)|network(?:down|up)load)|use(?:(?:lea|mo)ve|o(?:ver|ut)|enter|wheel|down|up)|ve(?:start|end)?)|essage|ark)|s(?:t(?:a(?:t(?:uschanged|echange)|lled|rt)|k(?:sessione|comma)nd|op)|e(?:ek(?:complete|ing|ed)|(?:lec(?:tstar)?)?t|n(?:ding|t))|u(?:ccess|spend|bmit)|peech(?:start|end)|ound(?:start|end)|croll|how)|b(?:e(?:for(?:e(?:(?:scriptexecu|activa)te|u(?:nload|pdate)|p(?:aste|rint)|c(?:opy|ut)|editfocus)|deactivate)|gin(?:Event)?)|oun(?:dary|ce)|l(?:ocked|ur)|roadcast|usy)|a(?:n(?:imation(?:iteration|start|end)|tennastatechange)|fter(?:(?:scriptexecu|upda)te|print)|udio(?:process|start|end)|d(?:apteradded|dtrack)|ctivate|lerting|bort)|DOM(?:Node(?:Inserted(?:IntoDocument)?|Removed(?:FromDocument)?)|(?:CharacterData|Subtree)Modified|A(?:ttrModified|ctivate)|Focus(?:Out|In)|MouseScroll)|r(?:e(?:s(?:u(?:m(?:ing|e)|lt)|ize|et)|adystatechange|pea(?:tEven)?t|movetrack|trieving|ceived)|ow(?:s(?:inserted|delete)|e(?:nter|xit))|atechange)|p(?:op(?:up(?:hid(?:den|ing)|show(?:ing|n))|state)|a(?:ge(?:hide|show)|(?:st|us)e|int)|ro(?:pertychange|gress)|lay(?:ing)?)|t(?:ouch(?:(?:lea|mo)ve|en(?:ter|d)|cancel|start)|ime(?:update|out)|ransitionend|ext)|u(?:s(?:erproximity|sdreceived)|p(?:gradeneeded|dateready)|n(?:derflow|load))|f(?:o(?:rm(?:change|input)|cus(?:out|in)?)|i(?:lterchange|nish)|ailed)|l(?:o(?:ad(?:e(?:d(?:meta)?data|nd)|start)?|secapture)|evelchange|y)|g(?:amepad(?:(?:dis)?connected|button(?:down|up)|axismove)|et)|e(?:n(?:d(?:Event|ed)?|abled|ter)|rror(?:update)?|mptied|xit)|i(?:cc(?:cardlockerror|infochange)|n(?:coming|valid|put))|o(?:(?:(?:ff|n)lin|bsolet)e|verflow(?:changed)?|pen)|SVG(?:(?:Unl|L)oad|Resize|Scroll|Abort|Error|Zoom)|h(?:e(?:adphoneschange|l[dp])|ashchange|olding)|v(?:o(?:lum|ic)e|ersion)change|w(?:a(?:it|rn)ing|heel)|key(?:press|down|up)|(?:AppComman|Loa)d|no(?:update|match)|Request|zoom))[\s\0]*=", request.text))
                if XSSRegex != 0:
                    self.errMsg.setWindowTitle("Vulnerabilities Found!")
                    self.errMsg.setText("We discovered "+ str(XSSRegex) +" vulnerabilities with the provided list!\nPlease call 074030495982 for support!")
                    self.errMsg.setIcon(QtWidgets.QMessageBox.Critical)
                    box = self.errMsg.exec_()
        return 0


class BinaryWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binary Testing")
        self.resize(1280,480)
        self.layout = QtWidgets.QVBoxLayout()

        # file selector code
        self.filebtn = QtWidgets.QPushButton("Select file to test")
        self.filebtn.setGeometry(QtCore.QRect(270, 90, 80, 23))
        self.filebtn.clicked.connect(self.getFile)
        self.filePathBox = QtWidgets.QTextEdit(self)
        self.filePathBox.setGeometry(QtCore.QRect(160, 50, 311, 31))
        self.filePathBox.setObjectName("filePathBox")
        self.layout.addWidget(self.filebtn)

        self.series = QtCharts.QPieSeries()
        self.chart = QtCharts.QChart()
        self.chartView = QtCharts.QChartView()

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 280, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.accept)

        self.layout.addWidget(self.filebtn)
        self.layout.addWidget(self.filePathBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        BinaryWindow.malwareScan(self)

    def malwareScan(self):
        filename = self.filePathBox.toPlainText()
        with Virustotal(API_KEY="bd213c4441156be78093d19411413f256090c00905f6bdeaa73f7e6387804a41", API_VERSION="v3") as vtotal:
            with open(filename, "rb") as f:
                bytes = f.read()
                shaHash = hashlib.sha256(bytes).hexdigest()
                resp = vtotal.request(f"files/{shaHash}")
                pprint(resp.data)
                pprint(resp.data["attributes"]["last_analysis_stats"])
                self.filePathBox.setText("\nMalicious Ratings: " +str(resp.data["attributes"]["last_analysis_stats"]["malicious"]) + "\nSHA256: "+str(resp.data["attributes"]["sha256"]))
                self.series.append("Malicious",int(resp.data["attributes"]["last_analysis_stats"]["malicious"]))
                self.series.append("Suspicious",int(resp.data["attributes"]["last_analysis_stats"]["suspicious"]))
                self.series.append("Harmless",int(resp.data["attributes"]["last_analysis_stats"]["harmless"]))
                self.series.append("Undetected",int(resp.data["attributes"]["last_analysis_stats"]["undetected"]))
                self.chartView.chart().addSeries(self.series)
                self.chartView.chart().createDefaultAxes()
                self.chartView.show()
                

                return 0

    def getFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
        "c:\\")[0]
        self.filePathBox.setText(fname)
        return fname


class CreditWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Credits")
        self.resize(800,800)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("Welcome")
        self.resize(270,110)
        self.WebButton = QtWidgets.QPushButton("Web App Testing")
        self.BinaryButton = QtWidgets.QPushButton("Binary Testing")
        self.CreditButton = QtWidgets.QPushButton("Credits")
        self.UpdateButton = QtWidgets.QPushButton("Update")
               
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.WebButton)
        self.layout.addWidget(self.BinaryButton)
        self.layout.addWidget(self.CreditButton)
        self.layout.addWidget(self.UpdateButton)
        self.setLayout(self.layout)

        self.WebButton.clicked.connect(self.web)
        self.BinaryButton.clicked.connect(self.binary)
        self.CreditButton.clicked.connect(self.credit)
        self.UpdateButton.clicked.connect(self.update)

    def binary(self):
        self.w = BinaryWindow()
        self.w.show()
        self.hide()

    def web(self):
        self.w = WebAppWindow()
        self.w.show()
        self.hide()

    def credit(self):
        self.w = CreditWindow()
        self.w.show()
        self.hide()
    
    def update(self):
        return 0


def setupUI():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())