#/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets

import Ui_MainForm, Ui_ConfigDialog

class ConfigDialog(QtWidgets.QDialog, Ui_ConfigDialog.Ui_Dialog):
    """Dialogo di configurazione"""
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        
        self.setupUi(self)
        
        self.leServer.textChanged.connect(self.validate)
        
    def validate(self):
        if self.leServer.text():
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        else:
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)

class MainForm(QtWidgets.QMainWindow, Ui_MainForm.Ui_MainWindow):
    '''Finestra di esecuzione del programma'''
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        
        self.setupUi(self)
        
        self.loadSettings() #Carica le impostazioni
        
        self.attachments = [] #Allegati alle email
        
        #Di seguito le dichiarazioni degli eventi
        self.actionConfigure.triggered.connect(self.openConfiguration)
        self.btnNewContact.clicked.connect(self.newContact)
        self.btnDelContact.clicked.connect(self.delContact)
        self.btnLoadContacts.clicked.connect(self.loadContacts)
        self.btnSaveContacts.clicked.connect(self.saveContacts)
        self.btnNewAttachment.clicked.connect(self.newAttachment)
        self.btnDelAttachment.clicked.connect(self.delAttachment)
        self.btnSend.clicked.connect(self.sendEmails)
    
    def loadSettings(self):
        '''Carica le impostazioni del programma
        https://doc.qt.io/qt-5/qsettings.html
        '''
        self.settings = settings = QtCore.QSettings('sarduz.com', 'BulkEmail')
        if not settings.value("SMTP Server"):
            self.openConfiguration()
    
    def openConfiguration(self):
        'Apre il dialogo di configurazione e ne imposta i controlli'
        dialog = ConfigDialog(self)
        dialog.leSenderName.setText(self.settings.value('Sender Name', ''))
        dialog.leSenderEmail.setText(self.settings.value('Sender Email', ''))
        dialog.leServer.setText(self.settings.value('SMTP Server', ''))
        dialog.sbPort.setValue(int(self.settings.value('SMTP Port', '25')))
        dialog.leUsername.setText(self.settings.value('SMTP User', ''))
        dialog.lePassword.setText(self.settings.value('SMTP Password', ''))
        dialog.cbSecurity.setCurrentText(self.settings.value('SMTP Security', ''))            
        
        rsp = dialog.exec()
        
        if rsp == QtWidgets.QDialog.Accepted:
            self.settings.setValue('Sender Name', dialog.leSenderName.text())
            self.settings.setValue('Sender Email', dialog.leSenderEmail.text())
            self.settings.setValue('SMTP Server', dialog.leServer.text())
            self.settings.setValue('SMTP Port', dialog.sbPort.value())
            self.settings.setValue('SMTP User', dialog.leUsername.text())
            self.settings.setValue('SMTP Password', dialog.lePassword.text())
            self.settings.setValue('SMTP Security', dialog.cbSecurity.currentText())
            
    def newContact(self):
        '''Aggiunge una riga alla QTableWidget dei contatti
        https://doc.qt.io/qt-5/qtablewidget.html
        '''
        self.tbwContacts.setRowCount(self.tbwContacts.rowCount() + 1)

    def delContact(self):
        'Rimozione di un contatto'
        rowsSet = set([idx.row() for idx in self.tbwContacts.selectedIndexes()])
        rows = list(rowsSet)
        rows.sort(reverse=True)
        for row in rows:
            self.tbwContacts.removeRow(row)
    
    def loadContacts(self):
        '''Carica file di contatti in formato CSV.
        csv è una libreria standard di python per la gestione di questo tipo di file
        https://docs.python.org/3/library/csv.html
        '''
        import csv
        fileName, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Apri Elenco di Contatti",
            "",
            "*.csv",
            "*.csv")
        
        if fileName:
            with open(fileName, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for row in reader:
                    self.newContact()
                    
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(row[0])
                    self.tbwContacts.setItem(self.tbwContacts.rowCount() -1, 0, item)
                    
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(row[1])
                    self.tbwContacts.setItem(self.tbwContacts.rowCount() -1, 1, item)

    def saveContacts(self):
        '''Salva i contatti della QTableWidget in un file csv'''
        import csv
        if self.tbwContacts.rowCount() > -1:
            fileName = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Salva l'elenco dei contatti",
                "",
                "*.csv",
                "*.csv")
            with open(fileName[0], 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in range(self.tbwContacts.rowCount()):
                    rowList = [
                        self.tbwContacts.item(row, 0) and self.tbwContacts.item(row, 0).text() or '',
                        self.tbwContacts.item(row, 1) and self.tbwContacts.item(row, 1).text() or '',
                    ]
                    writer.writerow(rowList)
            self.statusBar.showMessage('File Salvato')
    
    def newAttachment(self):
        '''Nuovo allegato alla e-mail.
        Il nome del file viene salvato nell'attributo di istanza self.attachments'''
        fileName, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Seleziona i file da allegare",
            "",
            "",
            None)
        
        if fileName:
            self.attachments.append(fileName)
            self.refreshAttachmentsWidget()
    
    def delAttachment(self):
        'Rimuove l\'allegato'
        row = self.lswAttachments.currentRow()
        if row > -1:
            self.attachments.pop(row)
            self.refreshAttachmentsWidget()

    def setProgressBar(self, value):
        '''Aggiorna la barra di avanzamento della spedizione'''
        self.prbSending.setValue(value)
    
    def sendEmails(self):
        '''Dà il via alla spedizione delle email. 
        Durante la spedizione il programma non risponde. Solo la barra di avanzamento della 
        spedizione si aggiorna dopo l'invio di ogni mail. Per evitare che si clicchi sul tasto di invio creando una coda di eventi da processare,
        dopo l'avvio della procedura, il tasto di invio viene disabilititato'''
        self.btnSend.setEnabled(False) #disabilitazione del tasto di invio
        self.prbSending.setMaximum(self.tbwContacts.rowCount())
        recipients = []
        for row in range(self.tbwContacts.rowCount()):
            name = self.tbwContacts.item(row, 0).text()
            email = self.tbwContacts.item(row, 1).text()
            recipients.append((name, email,))
        import bulkemail_utils
        sender = bulkemail_utils.BulkEmailSender(
            self.settings, 
            recipients, 
            self.leSubject.text(), 
            self.pteHtml.toPlainText(),
            self.pteText.toPlainText(),
            self.attachments,
            self.statusBar.showMessage
        )
        try:
            sender.send(self.setProgressBar)
        except Exception as exc: #In caso di errore viene visualizzato un dialogo con i dettagli dell'eccezione
            QtWidgets.QMessageBox.critical(
                self,
                "Errore nell'esecuzione del programma",
                """<h2>Durante l'invio si è verificato il seguente errore:</h2><br>
<h3>{}</h3><br>
<p>{}</p>""".format(exc.__doc__, exc),
                QtWidgets.QMessageBox.StandardButtons(
                    QtWidgets.QMessageBox.Close),
                QtWidgets.QMessageBox.Close)
        finally:
            self.btnSend.setEnabled(True)
        
        self.setProgressBar(0)
        self.statusBar.showMessage('Invio Completato')
        
    def refreshAttachmentsWidget(self):
        '''Aggiornamento della lista di allegati'''
        import os
        self.lswAttachments.clear()
        for attachment in self.attachments:
            self.lswAttachments.addItem(
              os.path.basename(attachment)
            )

if __name__ == "__main__":
    '''Avvio del programma'''
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    w = MainForm()
    w.show()
    
    sys.exit(app.exec_())
