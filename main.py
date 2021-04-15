import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from multiprocessing.pool import ThreadPool
class Downloader():

    VIDEO_EXTENSIONS=['mp4', 'flv', 'mov']

    def __init__(self, url):
        """:argument url Url of the page video content to be downloaded"""
        self.url = url
        res = requests.get(url)
        self.content = res.content
        filePath = os.path.dirname(os.path.abspath(__file__))
        try:
            print(os.mkdir(os.path.join(filePath,'downloads')))
        except FileExistsError:
            print('download directory already exists')
        self.downloads_dir = os.path.join(filePath,'downloads')

    @staticmethod
    def fabric(url):
        return Downloader(url)

    def _get_links(self):
        """Parsing the page and :return list of hrefs to video"""
        soup = BeautifulSoup(self.content,'html.parser')
        a_tags = soup.find_all('a',recursive=True)
        urls_to_download = []
        for a in a_tags:
            if a.has_attr('href'):
                if urlparse(a["href"]).path.lower()[-3:] in self.VIDEO_EXTENSIONS:
                    urls_to_download.append(self.url+urlparse(a['href']).path)
        return urls_to_download

    def _download_url(self, entry):
        """download the file"""
        filename = urlparse(entry).path.split('/')[-1]
        path=os.path.join(self.downloads_dir,filename)
        if not os.path.exists(path):
            r = requests.get(entry, stream=True)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
        return path

    def run(self):
        """run the main method"""
        urls_to_download = self._get_links()
        results = ThreadPool(8).imap_unordered(self._download_url, urls_to_download)
        for path in results:
            print(path)

"""usage of Downloader class"""
a = Downloader('http://task.manager')
a.run()


b = Downloader.fabric('http://task.manager')
b.run()

