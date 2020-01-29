import os
import requests
from constants import (
    districts, vpr_names, vkb_names,
)

years = range(2010,2021)

def download(years=[2018]):
    download_url = 'http://bnpb.cloud/dibi/tabel1b/excel'

    for y in years:
        print('Year: {}'.format(y))

        for vpr_id, vkb_ids in districts.items():
            print('  Province: {}'.format(vpr_names[vpr_id]))

            for vkb_id in vkb_ids:
                print('    City: {}'.format(vkb_names[vkb_id]))

                download_params = {'vth': y,
                                   'vpr': vpr_id,
                                   'vkb': vkb_id,
                                   'vjn': 1}

                with requests.get(download_url, params=download_params) as r:
                    r.raise_for_status()

                    filepath_format = {'year': y,
                                       'vpr_name': vpr_names[vpr_id],
                                       'vkb_name': vkb_names[vkb_id]}

                    filepath = 'data/{year}/{vpr_name}/{vkb_name}.xlsx'.format(**filepath_format)

                    os.makedirs(os.path.dirname(filepath), exist_ok=True)

                    with open(filepath, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

download()
