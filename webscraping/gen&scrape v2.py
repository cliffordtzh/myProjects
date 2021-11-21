from tqdm import trange
import os
import pandas as pd
from functions import selenium_scrape

in_source = r'C:\Users\Clifford\Documents\Shortcuts\Clifford\Me\Coding\Appiloque\Gen&Scrape v2\input'
in_folder = os.listdir(in_source)
out_folder = r'C:\Users\Clifford\Documents\Shortcuts\Clifford\Me\Coding\Appiloque\Gen&Scrape v2\output'

for file in in_folder:
    data = pd.read_csv(f'{in_source}\\{file}')
    with trange(len(data['url'])) as pbar:
        for count, link in enumerate(data['url']):
            if link != 'No website':
                email, number = selenium_scrape(link)
                data.loc[count, 'email'] = email
                data.loc[count, 'number'] = number
                pbar.update(1)

    data.to_csv(f'{out_folder}\\output.csv')
    os.rename(f'{out_folder}\\output.csv', f'{out_folder}\\{file[0:-4]}.csv')
