import pandas as pd
import re
from tabulate import tabulate
import textwrap
from IPython.core.display import display, HTML

def search_index(search_term, index_dict, display_format='text'):
    filtered_dict = {}
    for k in index_dict:
        found = False
        if search_term in k:
            filtered_dict[k] = index_dict[k]
            continue
        
        for p in index_dict[k]['package_tags']:
            if search_term in p:
                filtered_dict[k] = index_dict[k]
                found = True
                break
        
        if found: continue
            
        for d in index_dict[k]['datasets']:
            if search_term in d['dataset_id']:
                filtered_dict[k] = index_dict[k]
                found = True
         
            if found: break
                
            if search_term in d['title']:
                filtered_dict[k] = index_dict[k]
                found = True
            
            if found: break
                   
    print_index(filtered_dict, display_format)


def print_index(index_dict, display_format='text'):
    df_dict = {'File': [], 'Packages': [], 'Dataset': []}
    for k in index_dict:
        df_dict['File'].append(k)
        df_dict['Packages'].append('\n'.join(index_dict[k]['package_tags']))
        datasets = []
        for dset in index_dict[k]['datasets']:
            datasets.append((dset['title'], dset['dataset_id']))
        
        if display_format == 'text':
            datasets = '\n'.join([f'{textwrap.fill(t, width=60)}\nhttps://catalogue.ceda.ac.uk/{i}' for (t, i) in datasets])
        elif display_format == 'html':
            datasets = '\n'.join([f'<a href="https://catalogue.ceda.ac.uk/{i}" title="Catalogue record">{textwrap.fill(t, width=120)}</a>' for (t, i) in datasets])
        
        df_dict['Dataset'].append(datasets)
        
    pd.set_option('display.max_colwidth', -1)
    df = pd.DataFrame(data=df_dict)
    
    if display_format == 'text':
        print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
    elif display_format == 'html':
        display(HTML(df.to_html(escape=False, index=False).replace("\\n","<br>")))
    
