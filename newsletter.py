#-------------------------------------------------------------------------------
# Name:        modulo1
# Purpose: newsletter a una lista in formato html con un template senza un massmail in ccn
#
# Author:      nibbio, e-mail:cservice@simail.it
#
# Created:     26/04/2015
# Copyright:   (c) nibbio 2015
# Licence:     gpl.v2  ver.0.02
#-------------------------------------------------------------------------------
# import librerie
import os
import csv
import io
import string
import datetime
import time
import yaml
#import mailem
from base64 import encodestring
from mailem import Message, Postman, Attachment, ImageAttachment
from mailem.connection import SMTPConnection
def cls():
    os.system("cls")
    print("")

def configurazionesmtp ():
#configurazione programma smtp, cartelle, tempo di attesa.
    try:
        stream =open ('c:\\newsletter\\config\\configurazione.yaml','r')
    except IOError :
       inserimentoparametri()
       datiserver_smtp, directory_lavoro = configurazionesmtp()
       return datiserver_smtp, directory_lavoro
    datiserver_smtp , directory_lavoro = yaml.load (stream)
    stream.close()
    return datiserver_smtp, directory_lavoro
def elencofile(percorso):
#elenco file delle cartelle
    nomifile=os.listdir (percorso)
    return nomifile

def letturamaillist (percorso):
#funzione di lettura della mail list.
    listafile= elencofile (percorso)
    print "ho trovato n." , len(listafile) ,"file .csv ; seleziona inserendo il numero corrispondente alla mail list a cui ti interessa inviare la mail:"
    solo_csv=[n for n in listafile if string.find(n,'.csv')!=-1 ]
    print solo_csv ,"\n"
    indice= int(raw_input("inserisci il numero corrispondente al nome file 1 per il primo file 2 per il secondo e cosi' via:"))
    nomefile= solo_csv [indice-1]
    print "'La lista selezionata e'",nomefile
    maillist=open( percorso+'\\'+nomefile)
    maillista=[]
    listamail = csv.reader(maillist, delimiter=';')
    for riga in listamail :
        maillista.append(riga)
    maillist.close ()
    return maillista

def inserimentoparametri ():
    conferma='n'
    while conferma == 'n' or conferma == 'N':
        print "inserire i dati di prima configurazione"
        datiserver_smtp=dict()
        datiserver_smtp ['nomeserver'] = raw_input ("inserisci il nome del server smtp(es.:smtp.gmail.com:)")
        datiserver_smtp ['mailaddress'] = raw_input ("inserisci il tuo indirizzo di posta elettronica (es.pallino@gmail.com):")
        datiserver_smtp ['login']= raw_input ('inserisci user login:')
        datiserver_smtp ['password'] = raw_input ("inserisci la password:")
        datiserver_smtp ['porta'] = int(raw_input ("inserisci il numero della porta del server di solito 25 per l'smtp:"))
        datiserver_smtp ['metodosicurezza']= False
        conferma= raw_input ("Confermi i dati inseriti? (s/n):")
    directory_lavoro= dict()
    directory_lavoro ['principale']= 'c:\\newsletter'
    directory_lavoro ['configurazione']= 'c:\\newsletter\\config'
    directory_lavoro ['mailist']= 'c:\\newsletter\\liste_mail'
    directory_lavoro ['log'] = 'c:\\newsletter\\log'
    directory_lavoro ['messaggio'] = 'c:\\newsletter\\messaggio_html'
    stream= open ('c:\\newsletter\\config\\configurazione.yaml','w') #preparazione file yaml scrittura
    yaml.dump ((datiserver_smtp, directory_lavoro), stream) #scrittura dizionari file yaml.
    stream.close()
    return
def tempoattesa (tempo):
    #funzione ti attesa t ? in minuti.
    tempo1=time.time() + tempo *60
    while int (tempo1) > int (time.time()):
        tempo2 =  int (tempo1) - int (time.time())
def caricamentopagina (percorso):
    #caricamento file html gi? preparato e personalizzato a cui va aggiunto il messaggio e la descrizione
    listafile= elencofile (percorso)
    solo_html= [n for n in listafile if string.find(n,'.html')!=-1 ]
    print solo_html,"\n"
    indice= int(raw_input ("scegli il template html in inserendo il numero:"))
    nomefile= solo_html [indice-1]
    #pagina=''''''
    html_file= open (percorso+"\\"+nomefile,'r')
    pagina= html_file.read ()
    html_file.close()
    return pagina

def main():
    cls ()
    datiserver, cartellelavoro = configurazionesmtp ()
    listamail= letturamaillist (cartellelavoro['mailist'])
    print "inserimento dati preparatori"
    t= int(raw_input ("inserisci l'intervallo dell'attesa tra l'invio di una mail e l'altra, in minuti(es. 3 o 4 o 5 minuti):" ))
    ora=0
    minuti=t* len (listamail)
    #calcolo tempo necessario per l'invio della mail.
    if (len(listamail)*t)>=60 :
        ora= int((len(listamail)*t)/60)
        minuti= ((len(listamail)*t/60) - ora)*60
    print "tempo necessario per completare l'invio di ", len(listamail),"mail:" ,ora,"ora/e:",minuti," minuto/i circa."
    spegnimento_macchina=raw_input("vuoi che spegnere il pc finito l'invio?(S/N or s/n):")

   #caricamento dati gia' inseriti
    cls()
    print 'inserimento o caricamento dati messaggio'
    scelta_messaggio= raw_input ("ci sono dei dati gia' predisposti li vuoi caricare e usare quei dati? (S/N o s/n):")
    if scelta_messaggio == "s" or scelta_messaggio =="S":
        stream =open ('c:\\newsletter\\messaggio_html\\datimessaggio.yaml','r')
        descrizione_foto= yaml.load (stream)
        stream.close()
    elif scelta_messaggio == "n" or scelta_messaggio== "N" :
#caricamentopaginahtml da inviare nel messaggio di posta.
        messaggiohtml= caricamentopagina (cartellelavoro['messaggio'])
        descrizione_foto= dict ()
        #inserimento oggetto messaggio
#scelta foto
        foto= elencofile (cartellelavoro['messaggio'])
        solo_foto= [n for n in foto if string.find(n,'jpg')!=-1 ]
        descrizione_foto['oggetto']= raw_input ("inserisci l'oggetto della email/newsletter:")
        print solo_foto; '\n'
        descrizione_foto['foto']= solo_foto[int(raw_input ("inserisci il numero della foto corrispondente:"))-1]
        descrizione_foto['titolo']= raw_input ("inserisci il titolo della descrizione dell'immobile (es.:'singola, appartamento, villetta ecc.): ")
        descrizione_foto['zona'] = raw_input ("inserisci dove si trova l'immobile (es. lido Nazioni, Lido Pomposa, Comacchio ecc.):")
        descrizione_foto['descrizione_breve'] = raw_input("inserisci una descrizione breve dell'immobile:")
        descrizione_foto['descrizione']= raw_input ("inserisci una descrizione piu' completa dell'immobile:")
        descrizione_foto['link']= raw_input ('inserisci il link per il bottone dettaglio:')
        descrizione_foto['paginahtml'] = messaggiohtml
        descrizione_foto['percentuale']= '%'
        dati_messaggio= open (cartellelavoro['messaggio']+'\\'+'datimessaggio.yaml','w')
        yaml.dump (descrizione_foto,dati_messaggio)
        dati_messaggio.close()
    messaggiodefinitivo = descrizione_foto ['paginahtml'] % descrizione_foto
    cls()
    #['foto'], descrizione_foto['titolo'],descrizione_foto['zona'],descrizione_foto['descrizione_breve'],descrizione_foto['descrizione']
#preparazionesmtp server
    smtp_host=datiserver['nomeserver']
    smtp_port=datiserver['porta']
    smtp_mode=datiserver['metodosicurezza']
    smtp_login=datiserver['login']
    smtp_password=datiserver ['password']
    mittente = datiserver ['mailaddress']
#caricamento elenco dei nomi dei file immagini per la pagina html.
    foto= elencofile (cartellelavoro['messaggio'])
    solo_foto= [n for n in foto if string.find(n,'gif')!=-1 ]
    solo_foto.extend ([n for n in foto if string.find(n,'jpg')!=-1])
    solo_foto.extend([n for n in foto if string.find(n,'png')!=-1])
    integrazione=[]

    for nomefile in solo_foto:
        #ImageAttachment(nomefile, open(cartellelavoro['messaggio']+'\\'+nomefile,'rb').read(), 'inline')
        integrazione.append(ImageAttachment(nomefile, open(cartellelavoro['messaggio']+'\\'+nomefile,'rb').read(), 'inline'))
    # Initialize a postman with SMTP connection to GMail
    postman = Postman(mittente,
                SMTPConnection(smtp_host, smtp_port,smtp_login,smtp_password,tls=True))
    cls()
    print 'invio mail alla mail list.'
    print "tempo necessario per completare l'invio di ", len(listamail),"mail:" ,ora,"ora/e:",minuti," minuto/i circa escluso il tempo per l'invio di ogni singola e-mail."
    if spegnimento_macchina == "S" or spegnimento_macchina == "s":
        print "la Macchina verra' spenta a fine lavoro"
    for destinatari in listamail:
        destinatario = destinatari [1]
#Composizione messaggio
        print "invio a:", destinatario
        messaggio = Message([destinatario],descrizione_foto['oggetto'],
          messaggiodefinitivo,attachments = integrazione)
# Send everything we have
        with postman.connect() as c:
            c.sendmail(messaggio)
            print "inviato con Successo"
        tempoattesa(t)

    #preparazione mail messaggio e scelta delle immagini.
    if spegnimento_macchina == "S" or spegnimento_macchina == "s":
        os.system ("c:\\windows\\system32\\shutdown.exe /s")
    exit

if __name__ == '__main__':
    main()
