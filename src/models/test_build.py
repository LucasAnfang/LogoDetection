import numpy as np
import os
import tensorflow as tf
import urllib2

from datasets import my_dataset
from nets import inception
from nets import inception_utils
from preprocessing import inception_preprocessing

slim = tf.contrib.slim

def classify(checkpoints_dir, images, reuse=False):
    image_size = inception.inception_v4.default_image_size
    probabilities_list = []
    processed_image_list = []
    images_list = []
    for image in images:
        image = tf.image.decode_jpeg(image, channels=3)
        #image = tf.image.resize_image_with_crop_or_pad(image, 299, 299)
        processed_image = inception_preprocessing.preprocess_image(image,
                                                             image_size,
                                                             image_size,
                                                             is_training=False)
        #processed_images  = tf.expand_dims(processed_image, 0)
        images_list.append(image)
        processed_image_list.append(processed_image)
    print("input shape: ", np.shape(processed_image_list))
    with slim.arg_scope(inception_utils.inception_arg_scope()):
        logits, _ = inception.inception_v4(processed_image_list,
                               #num_classes=2,
                               reuse=reuse,
                               is_training=False,
                               logo_names= ['Patagonia'])
        probabilities = tf.nn.softmax(logits[-1])

        if tf.gfile.IsDirectory(checkpoints_dir):
          checkpoints_dir = tf.train.latest_checkpoint(checkpoints_dir)

        init_fn = slim.assign_from_checkpoint_fn(
        checkpoints_dir,
        slim.get_model_variables('InceptionV4'))

        with tf.Session() as sess:
            init_fn(sess)
            np_image, network_input, probabilities = sess.run([images_list,
                                                               processed_image_list,
                                                               probabilities])
            print("probabilities shape: ", np.shape(probabilities))
            probabilities_list = probabilities
    return probabilities_list
'''def main(_):
    images = []
    for filename in os.listdir('../../resources/results/Not_Patagonia'):
        image = os.path.join('../../resources/results/Not_Patagonia', filename)
        print "filename:", image
        images.append(tf.read_file(image))
    list_test = classify("../../resources/train2",images)
    names = ["Not Patagonia","Patagonia",]
    for probabilities in list_test:
        for i in range(len(names)):
            print('Probability %0.2f => [%s]' % (probabilities[i], names[i]))
main(None)'''
