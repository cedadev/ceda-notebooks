import pandas as pd
import re
from tabulate import tabulate
import ipywidgets as widgets

def search_index(search_term, index_dict): #Is not working for dataset content currently
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
                   
    print_index(filtered_dict)


def print_index(index_dict):
    df_dict = {'File': [], 'Packages': [], 'Dataset ID': [], 'Dataset Title': []}
    for k in index_dict:
        df_dict['File'].append(k)
        df_dict['Packages'].append('\n'.join(index_dict[k]['package_tags']))
        dset_ids = []
        dset_titles = []
        for dset in index_dict[k]['datasets']:
            dset_ids.append(dset['dataset_id'])
            dset_titles.append(dset['title'])
        
        dset_titles = '\n'.join([re.sub('(.{32})', '\\1\n', t, 0, re.DOTALL) for t in dset_titles])
        
        df_dict['Dataset ID'].append('\n'.join(dset_ids))
        df_dict['Dataset Title'].append(dset_titles)
        
    
    print(tabulate(pd.DataFrame(data=df_dict), headers='keys', tablefmt='fancy_grid'))
    