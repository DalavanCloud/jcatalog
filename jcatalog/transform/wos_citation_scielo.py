from accent_remover import *
from cleaner import *

import models

for rec in models.WosCitations.objects().batch_size(5):

    # Title

    rec['title_lower'] = accent_remover(rec['title'].lower().replace(
        ' & ', ' ').replace('&', ''))

    rec['title_clean'] = cleaner(rec['title_lower'])

    query = models.Scielo.objects.filter(title_clean_wos=rec['title_clean'])

    if query:
        print('match: ' + rec['title'])
        rec['issns'] = query[0]['issns']
        rec['issn_scielo'] = query[0]['issn_scielo']
        rec.save()
    else:
        print('NONOT: ' + rec['title_lower'])

correction = [
    ("AISTHESIS REVISTA CHILENA DE INVESTIGACIONES ESTETICAS", "0718-7181"),
    ("ARQUIVOS DE NEUROHAFKADHFKAJN PSIQUIATRIA", "0004-282X"),
    ("CIENCIA E TECNOLOGIA DE ALIMENTOS", "0101-2061"),
    ("BRAZILIAN JOURNAL OF PSYCHIATRY", "0047-2085"),
    ("BULLETIN OF THE WORLD HEALTH ORGANIZATION INTERNATIONAL JOURNAL OF PUBLIC HEALTH", "0042-9686"),
    ("IATREIA REVISTA MEDICA UNIVERSIDAD DE ANTIOQUIA", "0121-0793"),
    ("GEN REVISTA DE LA SOCIEDAD VENEZOLANA DE GASTROENTEROLOGIA", "0016-3503"),
    ("FOOD SCIENCE AND TECHNOLOGY CAMPINAS", "0101-2061"),
    ("PAPEIS AVULSOS DE ZOOLOGIA SAO PAULO", "0031-1049"),
    ("JORNAL BRASILEIRO DE NEFROLOGIA", "0101-2800"),
    ("PHARMACY PRACTICE INTERNET", "1885-642X"),
    ("REVISTA DE DERECHO UCUDAL", "2393-6193"),
    ("REVISTA DE DERECHO UNIVERSIDAD CATOLICA DAMASO A LARRANAGA FACULTAD DE DERECHO", "2393-6193"),
    ("REVISTA DE ECONOMIA POLITICA", "0101-3157"),
    ("POLIMEROS CIENCIA E TECNOLOGIA", "0104-1428"),
    ("RELACIONES ZAMORA", "0185-3929"),
    ("PRODUCAO", "0103-6513"),
    ("PROFILE ISSUES IN TEACHERS PROFESSIONAL DEVELOPMENT", "1657-0790"),
    ("PROYECCIONES ANTOFAGASTA REVISTA DE MATEMATICA", "0716-0917"),
    ("REVISTA BRASILEIRA DE CIENCIA AVICOLA", "1516-635X"),
    ("REVISTA DE PSIQUIATRIA CLINICA", "0101-6083"),
    ("REVISTA BRASILEIRA DE CIRURGIA CARDIOVASCULAR", "0102-7638"),
    ("REVISTA FACULTAD DE MEDICINA DE LA UNIVERSIDAD NACIONAL DE COLOMBIA", "0120-0011"),
    ("REVISTA HISTORIA Y SOCIEDAD", "0121-8417")]


for journal in correction:
    print(journal[0])

    wos = models.WosCitations.objects.filter(title=journal[0])

    if wos:

        for rec in wos:
            # Title
            rec['title_lower'] = accent_remover(rec['title'].lower().replace(
                ' & ', ' ').replace('&', ''))

            rec['title_clean'] = cleaner(rec['title_lower'])

            rec['issn_scielo'] = journal[1]

            print("  " + rec.issn_scielo + " " + rec.title_lower)

            rec.save()
