import os
import pathlib

import cv2
import numpy as np
import tensorflow
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Dropout, ELU, Activation
from tensorflow.keras.models import Sequential


# Configuration.
img_width, img_height = 25, 25  # 25, 25
input_shape = (img_width, img_height, 1)  # 1 for grayscale.
batch_size = 10
no_epochs = 25
no_classes = 2  # hotdog/!hotdog.
validation_split = 0.2  # 20% of data used for validation.
verbosity = 1  # 1 for printing all results to screen.

# Gets file path and sets working directory.
script_path = str(pathlib.Path(__file__).parent.absolute())
os.chdir(script_path)


# Load data.
def load_data(data_type='train', class_name='hot_dog'):
    instances = []
    classes = []

    for file_path in os.listdir(f'hotdog/{data_type}/{class_name}'):
        resized_image = cv2.imread(f'hotdog/{data_type}/{class_name}/{format(file_path)}', 0)  # 0 for grayscale.
        resized_image = cv2.resize(resized_image, (img_width, img_height))  # Resizes image.
        instances.append(resized_image)
        classes.append(0 if class_name == 'not_hot_dog' else 1)

    return (instances, classes)


# Model creation.
def create_model():
    model = Sequential()
    # model.add(Conv2D(4, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    # model.add(Conv2D(8, kernel_size=(3, 3), activation='relu'))
    # model.add(Conv2D(12, kernel_size=(3, 3), activation='relu'))
    # model.add(Flatten())  # Allows output feature maps to be input into dense layers.
    # model.add(Dense(256, activation='relu'))
    # model.add(Dense(no_classes, activation='softmax'))  # Generates probability distribution.
    # model = Sequential()
    model.add(Conv2D(16, kernel_size=(8, 8), strides=(4, 4), padding='valid', input_shape=input_shape))
    model.add(ELU())
    model.add(Conv2D(32, kernel_size=(5, 5), strides=(2, 2), padding="same"))
    model.add(ELU())
    model.add(Conv2D(64, kernel_size=(5, 5), strides=(2, 2), padding="same"))
    model.add(Flatten())
    model.add(Dropout(.2))
    model.add(ELU())
    model.add(Dense(512))
    model.add(Dropout(.5))
    model.add(ELU())
    model.add(Dense(2))
    model.add(Activation('softmax'))
    return model


# Model compilation.
def compile_model(model):
    model.compile(
        loss=tensorflow.keras.losses.sparse_categorical_crossentropy,
        optimizer=tensorflow.keras.optimizers.Adam(),
        metrics=['accuracy'],
    )
    return model


# Model training.
def train_model(model, X_train, y_train):
    model.fit(
        X_train,
        y_train,
        batch_size=batch_size,
        epochs=no_epochs,
        verbose=verbosity,
        shuffle=True,
        validation_split=validation_split,
    )
    return model


# Model testing.
def test_model(model, X_test, y_test):
    score = model.evaluate(
        X_test,
        y_test,
        verbose=1,
    )
    print(f'Test loss: {score[0]} / Test accuracy: {score[1]}')
    return model


if __name__ == '__main__':
    # Load and merge training data.
    X_train_nh, y_train_nh = load_data(data_type='train', class_name='not_hot_dog')
    X_train_h, y_train_h = load_data(data_type='train', class_name='hot_dog')
    X_train = np.array(X_train_nh + X_train_h)
    X_train = X_train.reshape((X_train.shape[0], img_width, img_height, 1))
    y_train = np.array(y_train_nh + y_train_h)

    # Load and merge testing data.
    X_test_nh, y_test_nh = load_data(data_type='test', class_name='not_hot_dog')
    X_test_h, y_test_h = load_data(data_type='test', class_name='hot_dog')
    X_test = np.array(X_test_nh + X_test_h)
    X_test = X_test.reshape((X_test.shape[0], img_width, img_height, 1))
    y_test = np.array(y_test_nh + y_test_h)

    # Create and train the model.
    model = create_model()
    model = compile_model(model)
    model = train_model(model, X_train, y_train)
    model = test_model(model, X_test, y_test)

    # model.save("/hotdog_CNN_model")

    # tested_stuff = X_test[:]
    # prediction = model.predict_classes(tested_stuff)
    # prediction_normal = model.predict(tested_stuff)
    # for i in range(len(tested_stuff)):
    #     print(f"Predicted = {prediction[i]}")
    #     print(f"Normal predict = {np.round(prediction_normal[i][1], 2)}")
    #     cv2.imwrite(script_path + "/hotdog/output/" + str(i) + "_" + str(prediction[i]) + "_" + str(np.round(prediction_normal[i][1], 2)) + ".jpg", X_test[i])
    #     cv2.imshow('image', tested_stuff[i])
    #     cv2.waitKey(0)
