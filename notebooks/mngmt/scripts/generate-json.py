import simplejson as json
import nbformat
import os
import re
import requests


def get_standard_lib():
    contents = os.listdir(os.path.dirname(os.__file__))
    return list(filter(lib_filter, contents))
    

def lib_filter(item):
    if item[0] == '_': 
        return False
    elif '.' in item:
        extension = item.split('.')[1]
        if extension != 'py':
            return False

    return True


def get_dataset_id(fpath):
    request_url = 'https://catalogue.ceda.ac.uk/api/v0/obs/get_info' + fpath
    resp = requests.get(request_url)
    id_url = resp.json()['url']
    title = resp.json()['title']
    return {'dataset_id': os.path.basename(id_url), 'title': title}


def generate_json(fpath):
    dataset_dirs = ['/neodc/', '/badc/']
    packages = []
    datasets = []
    standard_lib = get_standard_lib()
    filename = os.path.splitext(os.path.basename(fpath))[0]
    nb = nbformat.read(fpath, 4)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            content = cell['source']
            if 'import' in content:
                imports = re.findall(r'^(from|import).*(?:$|\n)', content, re.MULTILINE)
                #from_imports = re.findall(r'^from.*import.*(?:$|\n)', content, re.MULTILINE)
                found_packages = [imp.split(' ')[1].strip('\n').split('.')[0] for imp in imports]
                packages += [p for p in found_packages if p not in standard_lib and f'{p}.py' not in standard_lib]

            for d in dataset_dirs:
                if d in content:
                    fpaths = re.findall(fr"'{d}.*'", content)
                    new_datasets = [f.strip("'") for f in fpaths]
                    datasets += [get_dataset_id(ds) for ds in new_datasets]

    
    # remove duplicates
    packages = list(set(packages))
    datasets = [i for n, i in enumerate(datasets) if i not in datasets[n + 1:]]
    
    return (filename, {'package_tags': packages, 'datasets': datasets})


def main():
    notebooks_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    notebooks = {}

    for root, _, files in os.walk(notebooks_dir):
        for f in files:
            extension = os.path.splitext(f)[1]
            if extension == '.ipynb':
                full_path = os.path.join(notebooks_dir, root, f)
                filename, tag_dict = generate_json(full_path)
                notebooks[filename] = tag_dict

    with open('index.json', 'w') as outfile:
        json.dump(notebooks, outfile, indent='\t')


if __name__ == "__main__":
    main()
