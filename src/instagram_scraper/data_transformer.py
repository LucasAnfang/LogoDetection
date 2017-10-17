import pickle
from PIL import Image
from instagram_scraper.dictConstants import *


def toPickle(thingToPickle):
    '''
        pickles thingToPickle
    '''
    return pickle.dumps(thingToPickle)

def depickle(thingToDepickle):
    '''
        un-pickles thingToDepickle
    '''
    return pickle.loads(thingToDepickle)

def picToStringDict(picture):
    '''
        given a PIL picture, returns a string dictionary representation of it 
        Needed to serialize pictures
    '''
    return {
        'pixels': picture.tobytes(),
        'size': picture.size,
        'mode': picture.mode,
    }
def stringDictToPic(imageDict):
    '''
        takes a string representation of a picture and returns a PIL Image representation of it
    '''
    return Image.frombytes(imageDict['mode'], imageDict['size'], imageDict['pixels'])

def picFileToImageRepresentation(fileName):
    '''
        given fileName, a path to a jpg saved picture,
        returns: and PIL Image representation
    '''
    try:
        picture = Image.open(fileName)
        return picture
    except IOError:
        return None

def unserialize_train(byteString):
    '''
        Takes pickled string of training pictures
        depickles
        converts to PIL images
        Right now it just shows it
        TO DO: decide how to download it
    '''
    unpickledByteString = depickle(byteString)
    for picString in unpickledByteString:
        im = stringDictToPic(picString)
        im.show()



def unserialize_operate(pickledByteString):
    '''
        Take in pickled byte string that was created with IG_operate
        unpickle
        loops through pic dict
        right now it just shows, but should download them or something
        see dictConstants.py for constants
    '''
    byteString = depickle(pickledByteString)
    for picDict in byteString:
        #print(picDict[LOGO_NAME])
        #print(picDict[OWNER_ID])
        im = stringDictToPic(picDict[PICTURE])
        im.show()

def compress():
    '''
        TODO
    '''