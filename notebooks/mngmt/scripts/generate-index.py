import mdutils
import simplejson as json


def create_md(index_dict):
    mdFile = mdutils.MdUtils(file_name='index', title='Placeholder Index Heading')

    row_n = len(index_dict.keys()) + 1
    content = ['Notebook', 'Packages', 'Datasets', 'Dataset IDs']

    for notebook in index_dict:
        packages = '<br />'.join(index_dict[notebook]['package_tags'])
        datasets_titles = '<br />'.join([d['title'] for d in index_dict[notebook]['datasets']])
        datasets_ids = '<br />'.join([d['dataset_id'] for d in index_dict[notebook]['datasets']])
        content.extend([notebook, packages, datasets_titles, datasets_ids])

    mdFile.new_line()
    mdFile.new_table(columns=4, rows=row_n, text=content, text_align='left')
    mdFile.create_md_file()


def main():
    index_dict = {}
    with open('index.json', 'r') as reader:
        index_dict = json.load(reader)

    create_md(index_dict)


if __name__ == "__main__":
    main()
