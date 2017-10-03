from PIL import Image
import base64
import zlib
import StringIO
import io

# Run:		python compressionTest.py
# Creates 6 files for file size comparison: 
#	1. The byte array obtained via io
#	2. The byte array as a base64 encoded string 
#	3. The compressed byte array
#	4. The compressed base64 string byte array
#	5. The decompressed byte array
#	6. The decompressed base64 string byte array

try:
	# THIS IS HOW WE GET THE BYTE ARRAY WE SHOULD SAVE... 100-300 KB
	picture = Image.open("./patagonia/21911159_1940465642891993_2672871879034798080_n.jpg")

	imgByteArr = io.BytesIO()
	picture.save(imgByteArr, format='jpeg')
	imgByteArr = imgByteArr.getvalue()	
	# COPY ABOVE		
	
	
	#TESTING OTHER METHODS + COMPRESSION
	#Compression does not decrease file size
	picBase64 = base64.encodestring(imgByteArr)

	picBytesCompressed = zlib.compress(imgByteArr)
	picBase64Compressed = zlib.compress(picBase64)

	picBytesDecompressed = zlib.decompress(picBytesCompressed)
	picBase64Decompressed = zlib.decompress(picBase64Compressed)

	with open('file1.jpg', 'wb') as file:
		file.write(imgByteArr)
	with open('file2.jpg', 'wb') as file:
		file.write(picBase64)

	with open('file1.jpg.gz', 'wb') as file:
		file.write(picBytesCompressed)
	with open('file2.jpg.gz', 'wb') as file:
		file.write(picBase64Compressed)


	with open('file1Decom.jpg', 'wb') as file:
		file.write(picBytesDecompressed)
	with open('file2Decom.jpg', 'wb') as file:
		file.write(picBase64Decompressed)

	'''stream = StringIO.StringIO(picBytes)
	stream.write(picBytes)
	with open('file1pic.jpg', 'wb') as file:
		file.write(stream.getvalue())'''

except IOError:
	print("error")