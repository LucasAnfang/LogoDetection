import json
import os
from PIL import Image
DIMENSIONS = 'dimensions'
CAPTION = 'caption'
OWNER_ID = 'owner_id'
TAGS = 'tags'
TIME = 'time'
LOCATION = 'location'
LOGO_NAME = 'logo_name'
HAS_LOGO = 'has_logo'
PICTURE = 'picture'
PICTURE_ID = "picture_id"
""" NEW """
IMAGE_CONTEXT = "image_context"
TYPE = "processing_type"
TYPE_TRAINING = "training"
TYPE_CLASSIFICATION = "classification"

class InstagramPostEntities:
	def __init__(self, isTraining = False, isClassification = False):
		self.posts = []
		self.isTraining = isTraining
		self.isClassification = isClassification
		if(self.isTraining == self.isClassification):
			raise ValueError('InstagramPostEntities must be either for classification or training')

	def append(self, post = None, brand_name = None, serialized_image = None):
		ig_post_entity = {}
		if(isClassification == True):
			if(post == None):
				raise ValueError('No post supplied')
	        if "id" in post:
	           ig_post_entity[PICTURE_ID] = post['id']
			if "dimensions" in post:
				ig_post_entity[DIMENSIONS] = post['dimensions']
			if "edge_media_to_caption" in post:
				ig_post_entity[CAPTION] = post["edge_media_to_caption"]["edges"][0]["node"]["text"]
			if "owner" in post:
				ig_post_entity[OWNER_ID] = post["owner"]["id"]
			if "tags" in post:
				ig_post_entity[TAGS] = post["tags"]
			if "taken_at_timestamp" in post:
				ig_post_entity[TIME] = post["taken_at_timestamp"]
			if "location" in post and post['location'] is not None:
				if "name" in post["location"]:
					ig_post_entity[LOCATION] = post["location"]["name"]
			else:
				ig_post_entity[LOCATION] = None
			ig_post_entity[LOGO_NAME] = brand_name
			ig_post_entity[HAS_LOGO] = None
			ig_post_entity[IMAGE_CONTEXT] = None
			ig_post_entity[PICTURE] = post['picture']
		if(isTraining == True):
			if(serialized_image == None):
				raise ValueError('No serialized image supplied')
			ig_post_entity[PICTURE] = serialized_image
		self.posts.append(ig_post_entity)

	def extend(self, post_list):
		if post_list is not None:
			self.posts.extend(post_list)

	def archiveImageDirectory(self, directory):
		if(self.isTraining == False):
			raise ValueError('You can only archive if this class is said to be for training')
		for image_name in os.listdir(directory):
			picture = openImage('{}/{}'.format(directory,image_name))
			if picture is None:
				continue
			serialized_image = self.serializeImage(picture)
			self.append(self.serialized_image = serialized_image)

	def openImage(fileName):
	try:
		picture = Image.open(fileName)
		return picture
	except IOError:
		return None

	def serializeImage(self, picture):
	return {
		'pixels': picture.tobytes(),
		'size': picture.size,
		'mode': picture.mode,
	}

	def size(self):
		return len(self.posts)

	def getImageAtIndex(self, index):
		""" return deserialized image """
		return self.deserializeImage(self.posts[index][PICTURE])

	def setImageContextAtIndex(self, index, image_context):
		self.posts[index][IMAGE_CONTEXT] = image_context

	def setHasLogoAtIndex(self, index, has_logo):
		self.posts[index][HAS_LOGO] = has_logo

	def deserializeImage(self, serialized_image):
		return Image.frombytes(serialized_image['mode'], serialized_image['size'], serialized_image['pixels'])

	def serialize(self):
		return json.dumps(self.posts, indent=4, sort_keys=True, ensure_ascii=False)

	def deserialize(self, serialized_entity):
		self.posts = json.loads(serialized_entity)
