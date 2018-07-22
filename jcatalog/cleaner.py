# coding: utf-8
from accent_remover import *


def cleaner(text):

    t = accent_remover(text.replace(' & ', ' and ').
                       replace('&', ' and ').
                       replace(" ", "").
                       replace(".", "").
                       replace(":", "").
                       replace("-", "").
                       replace("_", "").
                       replace(",", "").
                       replace(";", "").
                       replace("|", "").
                       replace("/", "").
                       replace("\\", "").
                       replace("(", "").
                       replace(")", "").
                       replace("@", "").
                       replace("+", "").
                       replace("=", "").
                       replace("[", "").
                       replace("]", "").
                       replace('"', '').
                       replace("*", "").
                       replace("#", "").
                       replace("!", "").
                       replace("'", "").
                       lower().strip()
                       )
    return t
