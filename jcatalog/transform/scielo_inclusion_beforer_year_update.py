# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import logging
import models

logging.basicConfig(
    filename='logs/activethisyear_inclusion_before.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def activethisyear_inclusion_before():
    query = models.Scielo.objects.filter(
        title_current_status='current',
        collection='scl')
    counter = 0

    for j in query:
        docs16 = 0
        entrada = 0
        ativo_y = 0

        if 'docs' in j:
            if j['docs']['docs_2016'] == '':
                pass
            elif j['docs']['docs_2016'] > 0:
                docs16 = 1

            for year in range(2007, 2019):
                y = str(year)
                if 'docs_'+y in j['docs']:
                    if j['docs']['docs_'+y] == '':
                        pass
                    elif int(j['docs']['docs_'+y]) > 0:
                        ativo_y = 1
                        break

        if j['inclusion_year_at_scielo'] < 2016:
            entrada = 1

        if docs16 == 1 and entrada == 1 and ativo_y == 1:
            counter += 1
            data = {}
            data = {'activethisyear_inclusion_before': 2016}

            if data:
                j.modify(**data)

            print(counter)


def main():
    activethisyear_inclusion_before()


if __name__ == "__main__":
    main()
