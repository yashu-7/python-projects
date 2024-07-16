import cv2
import os
import pickle

dataset_path = 'features-based-classification\\dataset'
classes = os.listdir(dataset_path)

class_labels = {class_name: idx for idx, class_name in enumerate(classes)}
print(class_labels)

orb = cv2.ORB_create()

def extract_features(images_path):
    img = cv2.imread(images_path)
    kp, des = orb.detectAndCompute(img, None)
    return des

descriptors_list = []
labels_list = []

for label, name in enumerate(classes):
    class_path = os.path.join(dataset_path, name)
    for image in os.listdir(class_path):
        images_path = os.path.join(class_path,image)
        des = extract_features(images_path)
        if des is not None:
            descriptors_list.append(des)
            labels_list.append(label)

data = {'descriptors': descriptors_list,
        'labels': labels_list,
        'class_labels':class_labels}

with open('features-based-classification\\descriptors_data\\images_and_data.pkl','wb') as f:
    pickle.dump(data,f)