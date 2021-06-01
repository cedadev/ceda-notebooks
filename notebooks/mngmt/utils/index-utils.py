
def search_index(search_term, index_dict):
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
            for d_id in d['dataset_id']:
                if search_term in d_id:
                    filtered_dict[k] = index_dict[k]
                    found = True
                    break
            
            if found: break
                
            for t in d['title']:
                if search_term in t:
                    filtered_dict[k] = index_dict[k]
                    found = True
                    break
            
            if found: break
                     
    print_index(filtered_dict)


def print_index(index_dict):
    print('{:<30} {:<30} {:<35} {:<25}'.format('File', 'Packages', 'Dataset ID', 'Dataset Title'))
    for k in index_dict:
        print('-'*250)
        values = index_dict[k]
        packages = values['package_tags']
        dset_ids = []
        dset_titles = []

        for dset in values['datasets']:
            dset_ids.append(dset['dataset_id'])
            dset_titles.append(dset['title'])

        for n in range(0, max(1, len(packages), len(dset_ids), len(dset_titles))):
            file_name = k if n == 0 else ''
            package = packages[n] if len(packages) > n else ''
            id = dset_ids[n] if len(dset_ids) > n else ''
            title = dset_titles[n] if len(dset_titles) > n else ''

            print('{:<30} {:<30} {:<35} {:<25}'.format(file_name, package, id, title))