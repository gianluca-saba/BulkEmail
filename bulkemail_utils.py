"""
Modulo di supporto per il programma BulkEmail. Definisce la classe BulkEmailSender che si occupa di 
aprire una connessione, preparere le email e inviarle a tutti i destinatari.
"""

import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class BulkEmailSender():
    """
    Classe per l'invio di mail a una lista di destinatari.
    
    La classe va inizializzata con i seguenti parametri:
        settings (PyQt5.QtCore.Qsettings): i valori che l'oggetto settings deve definire sono:
            'Sender Name' -> Il nome del mittente
            'Sender Email' -> Indirizzo e-mail del mittente
            'SMTP Server' -> Server SMTP per l'invio della e-mail.
            'SMTP Port' -> Porta TCP del server
            'SMTP User' -> Utente per l'autenticazione al server
            'SMTP Password' -> Password per l'autenticazione
            'SMTP Security' -> Tipo di sicurezza. Nessuna, SSL o TLS
        recipients (list): nel formato [ ['nome del destinatario', 'e-mail del destinatario'], [...] ]
        subject (string): Oggetto della e-mail. Le ricorrenze di {nome} e {email} vengono sostituite, rispettivamente, dal nome e dall'indirizzo del destinatario.
        htmlContent (string): Contenuto HTML della email. Le ricorrenze di {nome} e {email} vengono sostituite, rispettivamente, dal nome e dall'indirizzo del destinatario.
        textContent (string): Contenuto della E-mail in formato testo. Le ricorrenze di {nome} e {email} vengono sostituite, rispettivamente, dal nome e dall'indirizzo del destinatario.
        attachments(list): Lista di percorsi di file da allegare alla e-mail. ['/percorso/del/file', 'percorso/di/un/altro', ... ]
        messageCallback (function): funzione che accetta un parametro stringa che viene chiamata durante le operazioni di invio per notificare lo stato della spedizione.
        """
    def __init__(self, settings, recipients, subject, htmlContent='', textContent='', attachments=[], messageCallback=None):
        '''
        Funzione di inizializzaione della classe.
        
        Parametri:
            settings (PyQt5.QtCore.Qsettings)
            recipients (list)
            subject (string)
            htmlContent (string)
            textContent (string)
            attachments(list)
            messageCallback (function)        
        '''
        self.settings = settings
        self.recipients = recipients
        self.subject = subject
        self.htmlContent = htmlContent
        self.textContent = textContent
        self.attachments = attachments
        if messageCallback:
            self.messageCallback = messageCallback
        else:
            self.messageCallback = lambda msg: print(msg)
            
    def send(self, callback=None):
        '''
        Invia l'e-mail a tutti i destinatari. 
        Parametri:
            callback (function): Ulteriore funzione di callback per notificare lo stato di spedizione dell'email.
        '''
        self.messageCallback('Sto iniziando l\invio')
        for counter, recipient in enumerate(self.recipients, start=1):
            connection = self.open_connection()
            message = self.prepare_message(recipient)
            self.send_mail(connection, recipient, message)
            self.close_connection(connection)
            if callback:
                callback(counter)
        self.messageCallback('Invio terminato')
    
    def open_connection(self):
        '''
        Apre e restituisce la connessione al server SMTP.
        '''
        self.messageCallback('Apro la connessione a {}'.format(self.settings.value('SMTP Server')))
        if self.settings.value('SMTP Security') == 'SSL':
            connection = smtplib.SMTP_SSL(
                self.settings.value('SMTP Server'),
                self.settings.value('SMTP Port')
            )
        else:
            connection = smtplib.SMTP(
                self.settings.value('SMTP Server'),
                self.settings.value('SMTP Port')
            )
        connection.ehlo()
        
        if self.settings.value('SMTP Security') == 'TLS':
            connection.starttls()
        
        self.messageCallback('Effettuo il login come {}'.format(self.settings.value('SMTP User')))

        if self.settings.value('SMTP User'):
            connection.login(
                self.settings.value('SMTP User'),
                self.settings.value('SMTP Password') 
            )

        self.messageCallback('Connesso')
        return connection
    
    def send_mail(self, connection, recipient, message):
        '''
        Invia una mail.
        
        Parametri:
            connection (object): Oggetto connection restituito dal metodo open_connection()
            recipient (iterable): iterable di due elementi di modo che recipient[0] -> nome del destinatario, recipient[1] -> e-mail del destinatario
            message (string): messaggio e-mail secondo lo standard MIME restutuito dal metodo prepare_message()
        '''
        self.messageCallback('Spedisco la mail a {}'.format(recipient[0]))
        connection.sendmail(
            self.settings.value('Sender Email'),
            recipient[1],
            message
        )
        self.messageCallback('Mail a {} spedita con successo'.format(recipient[0]))
    
    def close_connection(self, connection):
        '''
        Chiude la connessione al server SMTP.
        Parametri:
            connection (object): Oggetto connection restituito dal metodo open_connection()
        '''
        self.messageCallback('Chiudo la connessione')
        connection.close()
        
    def prepare_message(self, recipient):
        '''
        Prepara e restituisce il messaggio secondo lo standard MIME.
        Parametri:
            recipient (iterable): iterable di due elementi di modo che recipient[0] -> nome del destinatario, recipient[1] -> e-mail del destinatario
        '''
        self.messageCallback('Preparo la mail per {}'.format(recipient[0]))
        message = MIMEMultipart()
        message.preamble = u'This is a multi-part message in MIME format.\n'
        message.epilogue = u''
        
        body = MIMEMultipart('alternative')
        
        if self.htmlContent:
            html = self.htmlContent.format(nome=recipient[0], email=recipient[1])
            body.attach(MIMEText(html.encode('utf-8'), 'html', 'UTF-8'))
        
        if self.textContent:
            text = self.textContent.format(nome=recipient[0], email=recipient[1])
            body.attach(MIMEText(text.encode('utf-8'), 'plain', 'UTF-8'))
        
        message.attach(body)
        
        for attachment in self.attachments:
            with open(attachment) as att_file:
                content = att_file.read()
                part = MIMEBase('application', "octet-stream")
                part.set_payload(content)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
                message.attach(part)

        message.add_header(
            'From',   '{} <{}>'.format(
                self.settings.value('Sender Name'),
                self.settings.value('Sender Email')
            )
        )
        message.add_header(
            'To', '{} <{}>'.format(
                recipient[0],
                recipient[1]
            )
        )
        message.add_header('Subject', self.subject.format(nome=recipient[0], email=recipient[1]))
        self.messageCallback('La mail per {} è stata preparata'.format(recipient[0]))
        return message.as_string()

