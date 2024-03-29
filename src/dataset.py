import tensorflow as tf

import constants


class Dataset:
    def __init__(self, make_label_file=False):
        self.path = "data"
        self.datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1. / 255,
            validation_split=0.2)

        self.train_generator = self.datagen.flow_from_directory(
            self.path,
            target_size=(constants.IMAGE_SIZE, constants.IMAGE_SIZE),
            batch_size=constants.BATCH_SIZE,
            subset='training')

        self.val_generator = self.datagen.flow_from_directory(
            self.path,
            target_size=(constants.IMAGE_SIZE, constants.IMAGE_SIZE),
            batch_size=constants.BATCH_SIZE,
            subset='validation')

        if make_label_file:
            labels = '\n'.join(sorted(self.train_generator.class_indices.keys()))
            with open('data/labels.txt', 'w') as f:
                f.write(labels)

    def representative_data_gen(self):
        dataset_list = tf.data.Dataset.list_files(self.path + '/*/*')
        for i in range(100):
            image = next(iter(dataset_list))
            print(image)
            image = tf.io.read_file(image)
            image = tf.io.decode_jpeg(image, channels=3)
            image = tf.image.resize(image, [constants.IMAGE_SIZE, constants.IMAGE_SIZE])
            image = tf.cast(image / 255., tf.float32)
            image = tf.expand_dims(image, 0)
            yield [image]
