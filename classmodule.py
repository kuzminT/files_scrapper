import argparse
import requests
from lxml import etree, html
import re, os.path as path


class FilesScrapper:
    """"
    Utilit for downloading files from page by allowed extension
    Save all files in directories with the same names
    """""

    def __init__(self):
        parser = argparse.ArgumentParser(description="Recursive copy static files by extension from site")
        parser.add_argument('link',
                            help='path to the page')
        parser.add_argument('--allow', '-a', default='jpg', help='Allow extensions of files')

        parser.add_argument('--limit', '-l', default='10', help='Limit of the files')

        args = parser.parse_args()

        self.main_link = args.link

        self.extension = args.allow

        self.files_limit = int(args.limit)

        self.reg = re.compile('%s.*.(%s)$' % (self.main_link, re.escape(self.extension)))
        # print(self.reg)

        if not args.link:
            print('Error! Main link not defined!')
            return
        else:
            self.main_link = args.link

        self.finished_files = set()
        self.links = set()

        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) ' +
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                        }

        self.files_list = self.get_files_links(self.main_link)
        # print(self.files_list)
        self.parse_files()

    def get_page(self, page):
        try:
            r = self.session.get(page, headers=self.headers)
        except requests.exceptions.RequestException as e:
            print('Something wrong! Was error while parsing link {}\n'.format(page))
            print(e)
            return None
        else:
            return r

    def parse_files(self):

        for file in self.files_list:
            if len(self.finished_files) < self.files_limit:
                attr, link = file[1], file[2].strip()
                print(attr, link)
                # print(re.match(r'\.(jpg|png|jpeg|svg)$', link.strip()))
                if attr is not None and re.search(self.reg, link):
                    self.get_file(link)
            else:
                return

            # print(file[2])

    """
    Get files links from current page
    """

    def get_files_links(self, page):

        response = self.get_page(page)

        if not response:
            return set()

        if response.status_code != 200:
            print('Ошибка обращения по ссылке {}. Страница вернула {} код'.format(page, response.status_code))
        else:
            try:
                parsed_body = html.fromstring(response.content)
                """
                Отлавливем исключение, если документ не содержит html 
                 """
            except etree.ParserError as e:
                print(e)
                return set()
            else:
                # Получаем все ссылки со страницы
                parsed_body.make_links_absolute(self.main_link)
                links = parsed_body.iterlinks()
                return set(links)

    def get_file(self, file_link):

        # If we downloaded this file early, then quit
        if file_link in self.finished_files:
            return None

        print('Downloading {}...'.format(file_link))
        filename = path.basename(file_link)
        response = requests.get(file_link)

        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            # Save file_link in memory
            self.finished_files.add(file_link)
