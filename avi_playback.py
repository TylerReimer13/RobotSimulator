import re
import cv2
import os


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


def generate_avi(image_folder, video_name):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    sorted_images = sorted(set(images), key=natural_keys)
    frame = cv2.imread(os.path.join(image_folder, sorted_images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 5, (width, height))

    for image in sorted_images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
