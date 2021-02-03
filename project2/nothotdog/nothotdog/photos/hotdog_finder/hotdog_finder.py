import glob
import os
import pathlib

import numpy as np
import tensorflow
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten,
                                     MaxPooling2D)
from tensorflow.keras.models import Sequential

import data_augmentation

# Configuration.
class_size = 20000
size = 32
input_shape = (size, size, 1)  # 1 for grayscale.
batch_size = 32
no_epochs = 100
no_classes = 2  # hotdog/!hotdog.
validation_split = 0.2  # 20% of data used for validation.
verbosity = 1  # 1 for printing all results to screen.


# Gets file path and sets working directory.
script_path = str(pathlib.Path(__file__).parent.absolute())
os.chdir(script_path)

hotdogs = glob.glob('hotdog/train/hot_dog/**/*.jpg', recursive=True) + \
    glob.glob('hotdog/test/hot_dog/**/*.jpg', recursive=True)

not_hotdogs = glob.glob('hotdog/train/not_hot_dog/**/*.jpg', recursive=True) + \
    glob.glob('hotdog/test/not_hot_dog/**/*.jpg', recursive=True)


scaled_X, y = data_augmentation.load_data(size, class_size, hotdogs, not_hotdogs)
scaled_X = data_augmentation.preprocess_data(scaled_X)
y = to_categorical(y)


rand_state = 42
tensorflow.random.set_seed(rand_state)
np.random.seed(rand_state)
X_train, X_test, y_train, y_test = train_test_split(
                                    scaled_X,
                                    y,
                                    test_size=0.2,
                                    random_state=rand_state
                                    )

print("Train shape X: ", X_train.shape)
print("Train shape y: ", y_train.shape)
print("Test shape X: ", X_test.shape)
print("Test shape y: ", y_test.shape)


# Model creation.
def create_model():
    model = Sequential()
    model.add(Conv2D(
        32,
        kernel_size=(3, 3),
        activation='relu',
        kernel_initializer='he_normal',
        input_shape=input_shape)
    )
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(Dropout(0.4))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(2, activation='softmax'))

    return model


# Model compilation.
def compile_model(model):
    model.compile(
        loss=tensorflow.keras.losses.binary_crossentropy,
        optimizer=tensorflow.keras.optimizers.Adam(lr=1e-4),
        metrics=['accuracy'],
    )
    return model


# Model training.
def train_model(model, X_train, y_train, X_test, y_test):
    model.fit(
        X_train,
        y_train,
        batch_size=batch_size,
        epochs=no_epochs,
        verbose=verbosity,
        shuffle=True,
        validation_data=(X_test, y_test),
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
    # Create and train the model.
    model = create_model()
    model = compile_model(model)
    model = train_model(model, X_train, y_train, X_test, y_test)
    model = test_model(model, X_test, y_test)
    model.save("hotdog_CNN_model")
