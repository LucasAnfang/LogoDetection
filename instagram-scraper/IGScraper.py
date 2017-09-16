import argparse
import os
import pickle
import textwrap

from PIL import Image

from instagram_scraper import InstagramScraper
from instagram_scraper.constants import *


#class IGScrapper(object):


def toPickle(thingToPickle):
    return pickle.dumps(thingToPickle)

def depickle(thingToDepickle):
    return pickle.loads(thingToDepickle)

def picToStringDict(picture):
    return {
        'pixels': picture.tobytes(),
        'size': picture.size,
        'mode': picture.mode,
    }

def stringDictToPic(imageDict):
    return Image.frombytes(imageDict['mode'], imageDict['size'], imageDict['pixels'])

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
    print("here")
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
    print(args.max_images+ " picutres from #"+ args.train + " saved in ./" + args.train)
    print("Please ensure all pictutes in ./" + args.train + " dir contain the "+args.train+ "logo")


def pickledTrainPicsTo_(byteString):
    '''
        Takes pickled string of training pictures
        depickles
        converts to PIL images
        Right now it just shows it
    '''
    unpickledByteString = depickle(byteString)
    for picString in unpickledByteString:
        im = stringDictToPic(pic)
        im.show()

def IG_train_upload(logo_brand, directory):
    '''
        ***ASSUMES HUMAN HAS INSURED THAT ALL PICS CONTAIN <logo_brand>***
        takes the directory './<logo_brand>' and compresses and serializes
        and calls Lucas's functions
    '''
    picDictList = []
    for pictureName in os.listdir(directory):
        try:
            picture = Image.open(directory + '/'+ pictureName)
        except IOError:
            continue
        picDictList.append(picToStringDict(picture));
    #pickle list to serialize
    byteString = toPickle(picDictList)

    #uncomment to test unpickling
    #pickledTrainPicsTo_(byteString)
    #call Lucas's function here
    

def IG_operate(logo_brand, hashtagList, maxImages):
    '''
        scrapes maxImages number of images from each hashtag in hastaglist
        Includes relevant metadata
        makes a dictionary with constants defined at top of file
        DOES NOT save on harddrive
        compreses and serializes
        Calls Lucas's functions
    '''
    '''
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
    '''



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
    parser.add_argument('--train-upload', '--train_upload' '-tu', default=None, help='logo brand name to upload directory into networed file system')
    parser.add_argument('--dir', '-d', default=None, help='Directory pictures are stored in on local machine')
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
            print "Error: directory invalid"
            return
        IG_train_upload(args.train_upload, picDir)
        
   


if __name__ == '__main__':
    main()
