import os
import sys
import requests
import pandas as pd
from tqdm import tqdm


def fetch_raw_data() -> pd.DataFrame:
    print('\nFetching data.')
    books = pd.read_excel('https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4')
    books['Subject Classification'] = books['Subject Classification'].str.upper()
    return books


def generate_url(url: requests.__url__, epub: bool = False) -> requests.__url__:
    new_url = url
    new_url = new_url.replace('/book/', '/download/epub/' if epub else '/content/pdf/')
    new_url = new_url.replace('%2F', '/')
    return new_url + '.epub' if epub else new_url + '.pdf'


def generate_path(url: requests.__url__, title: str, author: str) -> str:
    path = url.split('/')[-1]
    return title.replace(',', '-').replace('.', '').replace('/', ' ') + ' - ' \
           + author.replace(',', '-').replace('.', '').replace('/', ' ') + ' - ' \
           + path


def start(subject: str = None, epub: bool = False):
    folder = os.getcwd() + '/springer-books/'

    if not os.path.exists(folder):
        os.mkdir(folder)

    books = fetch_raw_data()
    books.to_csv(folder + 'books-list.csv')

    if subject is not None:
        print('Hello')
        books = books.loc[books['Subject Classification'].str.contains(subject.upper())]
    print(books)
    books.head()

    print('\nDownload started.')

    for url, title, author, pk_name in tqdm(books[['OpenURL', 'Book Title', 'Author', 'English Package Name']].values):
        new_folder = folder + pk_name + '/'
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)

        r = requests.get(url)

        new_url = generate_url(r.url)
        path = generate_path(new_url, title, author)

        new_file = requests.get(new_url, allow_redirects=True)
        open(new_folder + path, 'wb').write(new_file.content)

        if epub:
            new_url = generate_url(r.url, epub=True)
            path = generate_path(new_url, title, author)

            request = requests.get(new_url)
            if request.status_code == 200:
                new_file = requests.get(new_url, allow_redirects=True)
                open(new_folder + path, 'wb').write(new_file.content)

    print('\nDownload finished.')


def print_help():
    import textwrap as tw
    print('About:')
    print(
        tw.indent(tw.fill('Downloads free books offered by Springer. It will automatically create a \'springer-books\' '
                          'sub-folder in the directory where the scripts run at. '
                          'The script will categorize the books according the subject.'), '\t\t'))
    print('\nUsage:')
    print(tw.indent('python3 download.py'
                    '\npython3 download.py -s <subject-classification>'
                    '\npython3 download.py <option> -s <subject-classification>', '\t\t'))

    print('\nOptions:')
    print(tw.indent('--epub\t\tDownload ePub versions.', '\t\t'))


def get_arg():
    if sys.argv.__len__() > 4:
        print_help()
        exit(0)

    subject = None
    ePub = False
    for i, arg in enumerate(sys.argv):
        if arg == '-s' or arg == '--subject':
            subject = sys.argv[i + 1]
        if arg == '--epub':
            ePub = True
    return subject, ePub


def main():
    subject, ePub = get_arg()
    start(subject, ePub)


if __name__ == '__main__':
    main()
