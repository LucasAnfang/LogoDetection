import zlib
from io import BytesIO
from PIL import Image
import json



def _compress():
	picture = Image.open("dog.jpg")
	picDict = {
        'pixels': picture.tobytes(),
        'size': picture.size,
        'mode': picture.mode,
    }
	with open('file1.txt', 'w') as file:
		file.write(json.dumps(str(picDict)))
	c = zlib.compress(picture.tobytes())
	newPicDict = {
        'pixels': c,
        'size': picture.size,
        'mode': picture.mode,
    }
	with open('file2.txt', 'w') as file:
		file.write(json.dumps(str(newPicDict)))
	u = zlib.decompress(c)
	newPic = Image.frombytes( picture.mode, picture.size, u)
	newPic.show()
	#print c


def main():
	_compress()


if __name__ == '__main__':
    main()