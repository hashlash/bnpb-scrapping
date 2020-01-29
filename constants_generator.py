import requests
from autopep8 import fix_code
from bs4 import BeautifulSoup
from pprint import pformat

data_url = 'http://bnpb.cloud/dibi/tabel1b'

r = requests.get(data_url)
soup = BeautifulSoup(r.content, 'html.parser')

district_data = {}
vpr_names = {}
vkb_names = {}

for vpr_tag in soup.find(id='vpr').find_all('option')[1:]:
    print('Getting data from {}'.format(vpr_tag.text))

    vpr_id = vpr_tag['value']

    r1 = requests.post(data_url,
                       data={
                           'vth': 2020,
                           'vpr': int(vpr_id),
                           'vjn': 1,
                       })

    soup1 = BeautifulSoup(r1.content, 'html.parser')
    vkb_tags = soup1.find(id='vkb').find_all('option')[1:]

    district_data[vpr_id] = [vkb_tag['value'] for vkb_tag in vkb_tags]
    vpr_names.update({vpr_id:vpr_tag.text})
    vkb_names.update({vkb['value']: vkb.text for vkb in vkb_tags})

constant_file_name = 'constants.py'

with open(constant_file_name, 'w') as f:
    output = '''
        districts = {}
        vpr_names = {}
        vkb_names = {}
    '''.format(pformat(district_data),
               pformat(vpr_names),
               pformat(vkb_names))

    print('Generating constants.py')
    print(fix_code(output), file=f)
