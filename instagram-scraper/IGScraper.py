from instagram_scraper import InstagramScraper
from instagram_scraper.constants import *


#class IGScrapper(object):


def serialize():
    '''
        TODO
    '''
def deserialize():
    '''
        TODO
    '''
def compress():
    '''
        TODO
    '''
def IG_train(logo_brand, maxImages):
    '''
        Scrapes max Images from logo_brand name and saves it to a directory named
        <logo_brand>
        This only needs to scrape for pictures
    '''
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

def IG_train_upload(logo_brand):
    '''
        ***ASSUMES HUMAN HAS INSURED THAT ALL PICS CONTAIN <logo_brand>***
        takes the directory './<logo_brand>' and compresses and serializes
        and calls Lucas's functions
    '''

def IG_operate(logo_brand, hashtagList, maxImages):
    '''
        scrapes maxImages number of images from each hashtag in hastaglist
        Includes relevant metadata
        makes a dictionary with constants defined at top of file
        DOES NOT save on harddrive
        compreses and serializes
        Calls Lucas's functions
    '''



def main():
    


if __name__ == '__main__':
    main()
