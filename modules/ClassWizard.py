import classwizard_rc
import sip
from PyQt4 import QtCore, QtGui

sip.setapi('QString', 2)
sip.setapi('QVariant', 2)


class ClassWizard(QtGui.QWizard):

    def __init__(self, parent=None):
        super(ClassWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(ClassInfoPage())
        # self.addPage(CodeStylePage())
        # self.addPage(OutputFilesPage())
        self.addPage(ConclusionPage())

        self.setPixmap(QtGui.QWizard.BannerPixmap,
                       QtGui.QPixmap(':/images/banner.png'))
        self.setPixmap(QtGui.QWizard.BackgroundPixmap,
                       QtGui.QPixmap(':/images/background.png'))

        self.setWindowTitle("Class Wizard")


class IntroPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Introduction")
        self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                       QtGui.QPixmap(':/images/watermark1.png'))

        label = QtGui.QLabel("This wizard will be used to raise your website SEO")
        label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class ClassInfoPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(ClassInfoPage, self).__init__(parent)

        self.setTitle("Website Information")
        self.setSubTitle("Specify informations about the website that you want to check ")
        self.setPixmap(QtGui.QWizard.LogoPixmap, QtGui.QPixmap(':/images/logo1.png'))

        classNameLabel = QtGui.QLabel("&Url Address:")
        classNameLineEdit = QtGui.QLineEdit()
        classNameLabel.setBuddy(classNameLineEdit)

        baseClassLabel = QtGui.QLabel("&Number of Times:")
        baseClassLineEdit = QtGui.QLineEdit()
        baseClassLabel.setBuddy(baseClassLineEdit)

        qobjectMacroCheckBox = QtGui.QCheckBox("use &Tor")

        self.registerField('className*', classNameLineEdit)
        self.registerField('baseClass', baseClassLineEdit)
        self.registerField('qobjectMacro', qobjectMacroCheckBox)

        layout = QtGui.QGridLayout()
        layout.addWidget(classNameLabel, 0, 0)
        layout.addWidget(classNameLineEdit, 0, 1)
        layout.addWidget(baseClassLabel, 1, 0)
        layout.addWidget(baseClassLineEdit, 1, 1)
        layout.addWidget(qobjectMacroCheckBox, 2, 0, 1, 2)
        self.setLayout(layout)

    def initializePage(self):
        className = self.field('className')
        self.macroNameLineEdit.setText(className.upper() + "_H")

        baseClass = self.field('baseClass')
        is_baseClass = bool(baseClass)

        self.includeBaseCheckBox.setChecked(is_baseClass)
        self.includeBaseCheckBox.setEnabled(is_baseClass)
        self.baseIncludeLabel.setEnabled(is_baseClass)
        self.baseIncludeLineEdit.setEnabled(is_baseClass)

        if not is_baseClass:
            self.baseIncludeLineEdit.clear()
        elif QtCore.QRegExp('Q[A-Z].*').exactMatch(baseClass):
            self.baseIncludeLineEdit.setText('<' + baseClass + '>')
        else:
            self.baseIncludeLineEdit.setText('"' + baseClass.lower() + '.h"')


class ConclusionPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle("Conclusion")
        self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                       QtGui.QPixmap(':/images/watermark2.png'))

        self.label = QtGui.QLabel()
        self.label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        finishText = self.wizard().buttonText(QtGui.QWizard.FinishButton)
        finishText.replace('&', '')
        self.label.setText("Click %s to generate the class skeleton." % finishText)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = ClassWizard()
    wizard.show()
    sys.exit(app.exec_())
