import argparse
import requests


class FilesScrapper:
    """

    """
    def __init__(self):
        parser = argparse.ArgumentParser(description="Recursive copy static files by extension from site")
        parser.add_argument('link',
                            help='path to the page')
        parser.add_argument('--allow', '-a', default='jpg', help='Allow extensions of files')

        parser.add_argument('--limit', '-l', default='10', help='Limit of the files')

        args = parser.parse_args()

        self.main_link = args.link

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

        self.files_list =  self.get_files_links(self.main_link)

        self.parse_files()


    def parse_files(self):
        i = 1

        while True:
            print('Итерация № %d...' % i)
            new_files = self.files_list - self.finished_files

            if new_files and len(new_files):
                self.get_files(new_files)
            else:
                break


    """
    Get files links from current page
    """
    def get_files_links(self, page):
        pass

    def get_files(self, files_list):
        file_link = str()
        self.finished_files.add(file_link)
