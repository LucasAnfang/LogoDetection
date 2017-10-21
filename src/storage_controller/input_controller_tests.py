from input_controller import InputController
from instagram_post_entity import InstagramPostEntities
from PIL import Image

config_name = 'nfs_test_config'

ic = InputController(config_name)
test_upload = False
test_download = False

if test_upload:
    print 'extracting images'
    image_dir = './test_images'
    image_1_path = '{}/{}'.format(image_dir,'Unknown-1.jpeg')
    image_2_path = '{}/{}'.format(image_dir,'Unknown.jpeg')
    image_1 = Image.open(image_1_path)
    image_2 = Image.open(image_2_path)

    classification_ipe = InstagramPostEntities(isClassification = True)
    classification_ipe.append({'picture' : image_1 , 'id' : image_1_path})
    classification_ipe.append({'picture' : image_1 , 'id' : image_1_path})
    print '{}:\n{}'.format('Classification', classification_ipe.posts)

    ic.upload_brand_operational_input_IPE('Audi', classification_ipe, True)
    ic.upload_brand_operational_input_IPE('Audi', classification_ipe, False)
    ic.upload_brand_operational_input_IPE('Audi', classification_ipe, False)

    training_ipe = InstagramPostEntities(isTraining = True)
    training_ipe.archiveImageDirectory(image_dir)
    print '{}:\n{}'.format('Training', training_ipe.posts)

    ic.upload_brand_training_input_IPE('Audi', training_ipe, True)
    ic.upload_brand_training_input_IPE('Audi', training_ipe, False)
    ic.upload_brand_training_input_IPE('Audi', training_ipe, False)

# if test_download:
