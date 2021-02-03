import cv2
import numpy as np
from skimage import exposure


def rotate_image(img, angle):
    (rows, cols, ch) = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    return cv2.warpAffine(img, M, (cols, rows))


def load_blur_img(path, img_size):
    img = cv2.imread(path)
    angle = np.random.randint(0, 360)
    img = rotate_image(img, angle)
    img = cv2.blur(img, (5, 5))
    img = cv2.resize(img, img_size)
    return img


def load_img_class(class_path, class_label, class_size, img_size):
    x = []
    y = []

    for path in class_path:
        img = load_blur_img(path, img_size)
        x.append(img)
        y.append(class_label)

    while len(x) < class_size:
        rand_idx = np.random.randint(0, len(class_path))
        img = load_blur_img(class_path[rand_idx], img_size)
        x.append(img)
        y.append(class_label)

    return x, y


def load_data(img_size, class_size, hotdogs, not_hotdogs):
    img_size = (img_size, img_size)
    x_hotdog, y_hotdog = load_img_class(hotdogs, 0, class_size, img_size)
    x_not_hotdog, y_not_hotdog = load_img_class(not_hotdogs, 1, class_size, img_size)
    print("There are", len(x_hotdog), "hotdog images")
    print("There are", len(x_not_hotdog), "not hotdog images")

    X = np.array(x_hotdog + x_not_hotdog)
    y = np.array(y_hotdog + y_not_hotdog)

    return X, y


def to_gray(images):
    # rgb2gray converts RGB values to grayscale values by forming a weighted sum of the R, G, and B components:
    # 0.2989 * R + 0.5870 * G + 0.1140 * B
    # source: https://www.mathworks.com/help/matlab/ref/rgb2gray.html

    images = 0.2989*images[:, :, :, 0] + 0.5870*images[:, :, :, 1] + 0.1140*images[:, :, :, 2]
    return images


def normalize_images(images):
    # use Histogram equalization to get a better range
    # source http://scikit-image.org/docs/dev/api/skimage.exposure.html#skimage.exposure.equalize_hist
    images = (images / 255.).astype(np.float32)

    for i in range(images.shape[0]):
        images[i] = exposure.equalize_hist(images[i])

    images = images.reshape(images.shape + (1,))
    return images


def preprocess_data(images):
    gray_images = to_gray(images)
    return normalize_images(gray_images)
