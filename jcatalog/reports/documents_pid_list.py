import csv
import requests

with open('output/scielo_brasil_documents_2018.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile)
    filewriter.writerow(
        [
            'pid',
            'publicaton date',
            'title',
            'url'
        ])

    with open('data/scielo/docs_pub_2018.csv', 'r') as f:
        reader = csv.reader(f)
        for pid in reader:
            print(pid[0])
            r = requests.get(
                "http://articlemeta.scielo.org/api/v1/article/?code=" + pid[0])
            d = r.json()

            if d:
                # title
                title = None
                if 'article' in d:
                    if 'v12' in d['article']:
                        title = d['article']['v12'][0]['_']
                # url
                if 'fulltexts' in d:
                    if 'html' in d['fulltexts']:
                        url = [v for k, v in d['fulltexts']['html'].items()][0]
                    else:
                        if 'pdf' in d['fulltexts']:
                            ulr = [v for k, v in d['fulltexts']['pdf'].items()][
                                0]

                # publication date
                if 'publication_date' in d:
                    pubdate = d['publication_date']

                content = [
                    pid[0] or u'',
                    pubdate or u'',
                    title or u'',
                    url or u'']

                filewriter.writerow([l for l in content])
