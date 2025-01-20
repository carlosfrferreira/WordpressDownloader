# This is the starting point of the program
from network.wordpress_crawler import WordpressDownloader

if __name__ == '__main__':
    wordpress_downloader = WordpressDownloader()
    wordpress_downloader.download_plugins(100_000, 5, False)