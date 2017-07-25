# coding: utf-8
'''
This script remove the first line of JCR CSV files.
'''
import os
import shutil

work_dir = 'extractors/wos/'

filelist = [f for f in os.listdir(work_dir) if os.path.isfile(work_dir + f)]

filelist.sort()

# Remove first line and rename
for f in filelist:
    print('\n'+f)

    data = ''
    with open(work_dir + f, 'r') as fin:
        l1 = fin.readlines()[0]
        print(l1)

        year = l1.split()[7]
        print(year)

        key = l1.split(':')[4]
        name = key.split(' ')[1].replace('"', '')[1:4]
        print(name)

        fin.seek(0)

        data = fin.read().splitlines(True)

        fin.close()

        if not os.path.exists(work_dir + name):
            os.makedirs(work_dir + name)

        shutil.move(work_dir + f, work_dir + name)

    with open('data/wos/jcr_' + name + '_' + year + '.csv', 'w') as fout:
        fout.writelines(data[1:])
        print('jcr_' + name + '_' + year + '.csv')
