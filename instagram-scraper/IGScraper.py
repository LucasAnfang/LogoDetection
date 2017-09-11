from instagram_scraper import InstagramScraper
from instagram_scraper.constants import *


#class IGScrapper(object):


def main():
    tag = "pagatonia"
    maxNum = 10
    destinationFolder = './'
    args = {
        'username': [tag],
        'verbose': 0,
        'login_user': None,
        'usernames': [tag],
        'quiet': False,
        'tag': True,
        'retain_username': True,
        'include_location': True,
        'media_types': ['image', 'video', 'story'],
        'media_metadata': True,
        'search_location': False,
        'login_only': False,
        'destination': destinationFolder,
        'maximum': maxNum,
        'comments': False,
        'filename': None,
        'filter': None,
        'location': False,
        'login_pass': None,
        'latest': False,
        'logo_name': tag
    }

    scraper = InstagramScraper(**args)
    scraper.scrape_hashtag()


if __name__ == '__main__':
    main()
