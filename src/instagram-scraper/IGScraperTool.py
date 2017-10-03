import sys
import os
import argparse
import textwrap
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
from src.storage_controller.instagram_post_entity import InstagramPostEntities
from src.storage_controller.storage_manager import LogoStorageConnector
from instagram_scraper import InstagramScraper
#../storage_controller/

"""
TRAIN: python IGScraperTool.py -t patagonia -m 10
TRAIN UPLOAD: python IGScraperTool.py -tu patagonia
OPERATE:  python IGScraperTool.py  -o patagonia nature -l patagonia -m 2
"""

def IG_train(logo_brand, maxImages):
    '''
        Scrapes max Images from logo_brand name and saves it to a directory named
        <logo_brand>
        This only needs to scrape for pictures
    '''
    destinationFolder = './'
    args = {
        'username': [logo_brand],
        'verbose': 0,
        'login_user': None,
        'usernames': [logo_brand],
        'quiet': False,
        'tag': True,
        'retain_username': True,
        'media_types': ['image'],
        'media_metadata': False,
        'login_only': False,
        'destination': destinationFolder,
        'maximum': maxImages,
        'filename': None,
        'filter': None,
        'location': False,
        'login_pass': None,
        'latest': False,
        'logo_name': logo_brand
    }

    scraper = InstagramScraper(**args)
    scraper.scrape_hashtag()
    print(str(maxImages)+ " picutres from #"+ logo_brand + " saved in " + logo_brand +" folder")
    print("Please ensure all pictutes in " + logo_brand + " dir contain the "+logo_brand+ " logo")




def IG_train_upload(logo_brand, directory):
    '''
        ***ASSUMES HUMAN HAS INSURED THAT ALL PICS CONTAIN <logo_brand>***
        takes the directory './<logo_brand>' 
    '''

    lsc = LogoStorageConnector()
    ipe = InstagramPostEntities(isTraining=True)
    ipe.archiveImageDirectory(directory)
    lsc.upload_brand_training_input_IPE(logo_brand, ipe, isProcessed = False)

def IG_operate(logo_brand, hashtagList, maxImages):
    '''
        scrapes maxImages number of images from each hashtag in hastaglist
        Includes relevant metadata
        makes a dictionary with constants defined at top of file
        DOES NOT save on harddrive
        compreses and serializes
        Calls Lucas's functions
    '''
    lsc = LogoStorageConnector()

    #saves it to director
    ipe = InstagramPostEntities(isClassification=True)
    
    for tag in hashtagList:
        args = {
            #use a list here instead of a loop
            'username': [tag],
            'verbose': 0,
            'login_user': None,
            'usernames': [tag],
            'quiet': False,
            'tag': True,
            'retain_username': True,
            'include_location': True,
            'media_types': ['image'],
            'media_metadata': True,
            'search_location': False,
            'login_only': False,
            'destination': './',
            'maximum': maxImages,
            'comments': False,
            'filename': None,
            'filter': None,
            'location': False,
            'login_pass': None,
            'latest': False,
            'logo_name': logo_brand
        }
        scraper = InstagramScraper(**args)
        ipe.extend(scraper.scrape_hashtag_operate())
    print("Operate complete")
    #print(ipe.serialize())
    # lsc.upload_brand_operational_input_data(logo_brand, ipe.serialize(), isProcessed = False)
    lsc.upload_brand_operational_input_IPE(logo_brand, ipe, isProcessed = False)


def main():
    parser = argparse.ArgumentParser(
        description="Scrapes instagram for picutres based on a hashtag.",
        epilog=textwrap.dedent("""
        Used for logo detection

        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@')
    #train
    parser.add_argument('--train', '-t', default=None, help='Scrape for training pictures on hashtag provided')
    parser.add_argument('--max_images', '-m', type=int, default=500, help='Maximum number of images scraped for')
    #train-upload
    parser.add_argument('--train-upload', '--train_upload', '-tu', default=None, help='logo brand name to upload directory into networked file system')
    parser.add_argument('--dir', '-d', default=None, help='Directory pictures are already stored in on local machine')
    #operate
    parser.add_argument('--operate', '-o', nargs='+', default=None, help='Input list of hashtags (in ) to scrape on with -l logo.')
    parser.add_argument('--logo', '-l', default=None, help='Logo name to operate on')
    args= parser.parse_args()

    if(args.train is not None):
        IG_train(args.train, args.max_images)
        return
    if(args.train_upload is not None):
        picDir = './' + args.train_upload
        if(args.dir is not None):
            picDir = args.dir
        #check if dir is valid
        if not os.path.isdir(picDir):
            print("Error: directory invalid")
            return
        IG_train_upload(args.train_upload, picDir)
    if args.operate is not None:
        if args.logo is None:
            print("Please provide a logo name with operate")
            return
        else:
            print(args.operate)
            IG_operate(args.logo, args.operate, args.max_images)
            return

if __name__ == '__main__':
    main()
