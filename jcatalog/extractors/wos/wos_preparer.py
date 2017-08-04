# coding: utf-8
'''
This script remove the first line of CSV files of the JCR
and saves as name 'year'_'edition'
'''
import os

work_dir = 'extractors/wos/download_all/'
dest_dir = 'data/wos/jcr_all/'

filelist = [f for f in os.listdir(work_dir) if os.path.isfile(work_dir + f)]

filelist.sort()

# Remove first line and save as
for f in filelist:
    print('\n'+f)

    data = ''
    with open(work_dir + f, 'r') as fin:
        l1 = fin.readlines()[0]
        print(l1)

        year = l1.split()[7]
        print(year)

        edition = l1.split()[10]
        print(edition)

        fin.seek(0)

        data = fin.read().splitlines(True)

        fin.close()

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

    with open(dest_dir + 'jcr_' + edition + '_' + year + '.csv', 'w') as fout:

        fout.writelines(data[1:])

        print('jcr_' + edition + '_' + year + '.csv')

        fout.close()
