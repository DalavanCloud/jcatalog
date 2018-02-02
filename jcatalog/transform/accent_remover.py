# coding: utf-8

import unicodedata


def accent_remover(text):

    norm = unicodedata.normalize('NFKD', text)

    text_norm = u''.join([c for c in norm if not unicodedata.combining(c)])

    return text_norm
