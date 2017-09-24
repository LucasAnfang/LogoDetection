import argparse
import os
import pickle
import textwrap

from PIL import Image

from instagram_scraper import InstagramScraper
from instagram_scraper.constants import *
from instagram_scraper.dictConstants import *

#class IGScrapper(object):

'''
	In seperate file:
	handling pickling and compressing and stingsPicDicts to jpgs (both)

'''

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
    #print(args.max_images+ " picutres from #"+ args.train + " saved in ./" + args.train)
    #print("Please ensure all pictutes in ./" + args.train + " dir contain the "+args.train+ "logo")


def pickledTrainPicsTo_(byteString):
    '''
        Takes pickled string of training pictures
        depickles
        converts to PIL images
        Right now it just shows it
    '''
    unpickledByteString = depickle(byteString)
    for picString in unpickledByteString:
        im = stringDictToPic(picString)
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
        #compress
        picDictList.append(picToStringDict(picture));
    #if dropping pickle,
    #send picDictList to Lucas in json 
    #pickle list to serialize
    byteString = toPickle(picDictList)

    #uncomment to test unpickling
    pickledTrainPicsTo_(byteString)
    #call Lucas's function here
    
def unserialize_operate(pickledByteString):
    '''
        Take in pickled byte string that was created qith IG_operate
        unpickle
        loops through pic dict
        see dictConstants.py for constants
    '''
    byteString = depickle(pickledByteString)
    for picDict in byteString:
        print(picDict[LOGO_NAME])
        print(picDict[OWNER_ID])
        im = stringDictToPic(picDict[PICTURE])
        im.show()



def IG_operate(logo_brand, hashtagList, maxImages):
    '''
        scrapes maxImages number of images from each hashtag in hastaglist
        Includes relevant metadata
        makes a dictionary with constants defined at top of file
        DOES NOT save on harddrive
        compreses and serializes
        Calls Lucas's functions
    '''
    #saves it to director

    picList = [] # list of dictionaries of metadata + string version of list
    destinationFolder = './'
    for tag in hashtagList:
    	print "tag " + tag
        args = {
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
            'destination': destinationFolder,
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
        listScraperReturned = scraper.scrape_hashtag_operate()
        if listScraperReturned is not None:
        	picList.extend(listScraperReturned)
        pickledPicList = toPickle(picList)
        #for testing, call this to unserialize
    #unserialize_operate(pickledPicList)
    #call luca's function here
    print "Operate complete"
    

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
    parser.add_argument('--train-upload', '--train_upload', '-tu', default=None, help='logo brand name to upload directory into networed file system')
    parser.add_argument('--dir', '-d', default=None, help='Directory pictures are stored in on local machine')
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
        	print args.operate
        	IG_operate(args.logo, args.operate, args.max_images)
        	return

        
   


if __name__ == '__main__':
    main()
