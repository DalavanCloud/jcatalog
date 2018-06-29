# coding: utf-8
import os
import sys
from tools.sender import sender_config
from tools.sender import sender_msg_atualizacao
import models

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/sender.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

# Credenciais
remetente = sender_config.remetente
senha = sender_config.senha

# prepara a lista de editores com base na filtragem 2016 e envia
# Somente periódicos que entraram antes de 2016
#query = models.Scielo.objects.filter(fapesp_evaluation__2018__evaluated=1)
query = models.Scielo.objects.filter(issn_list='0074-0276')

for journal in query:

    issn = None
    file = None
    form = None
    title = None
    texto = None
    destinatario = None

    assunto = 'atualização - FAPESP - Avaliação dos periódicos SciELO Brasil'
    issn = journal['issn_scielo']
    file = "Fapesp-avaliacao-SciELO-"+issn+"-20180627.xlsx"
    form = "Formulario-avaliacao-Fapesp-SciELO-"+issn+"-20180627.pdf"
    title = journal['title']

    # carrega o texto e renderiza com str.format()
    texto = (sender_msg_atualizacao.body_msg % (title, file, form, file, file))

    # lista de emails destinatario
    if 'avaliacao' in journal:
        if 'contatos' in journal['avaliacao']:

            destinatario = [e['email_address'] for e in journal['avaliacao']['contatos']]
            if destinatario:
                msg = [('ok: ' + dest) for dest in destinatario]
                logger.info(msg)
                print(msg)

                # ativar para TESTES - adicionar o email manualmente
                destinatario = []
                destinatario = ['@gmail.com']
            else:
                msg = 'sem destinatario:' + issn
                logger.info(msg)
                print(msg)
        else:
            msg = 'sem contatos:' + issn
            logger.info(msg)
            print(msg)
    else:
        msg = 'sem avaliacao:' + issn
        logger.info(msg)
        print(msg)

    if issn and file and title and texto and destinatario:
        # Preparando a mensagem
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = COMMASPACE.join(destinatario)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = assunto
        msg.attach(MIMEText(texto, 'html', 'utf-8'))

        # Enviando o email
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
    else:
        msg = 'falta campo' + issn
        logger.info(msg)
        print(msg)
