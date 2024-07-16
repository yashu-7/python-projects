import cv2
import pickle
import numpy as np

with open('features-based-classification/descriptors_data/images_and_data.pkl', 'rb') as f:
    data = pickle.load(f)

dataset_descriptors = data['descriptors']
dataset_labels = data['labels']
class_labels = data['class_labels']

label_to_class = {label: class_name for class_name, label in class_labels.items()}

print(label_to_class)

orb = cv2.ORB_create()

def extract_features(images_path):
    img = cv2.imread(images_path)
    kp, des = orb.detectAndCompute(img, None)
    return des

def classify_image(new_image_path, dataset_descriptors, dataset_labels, k=2, ratio_thresh=0.75):
    new_descriptors = extract_features(new_image_path)
    
    if new_descriptors is None:
        return None
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    
    match_counts = np.zeros(len(set(dataset_labels)))
    
    for i, descriptors in enumerate(dataset_descriptors):
        matches = bf.knnMatch(new_descriptors, descriptors, k=k)
        
        good_matches = []
        for m, n in matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
        
        match_counts[dataset_labels[i]] += len(good_matches)
    
    best_class_index = np.argmax(match_counts)
    return best_class_index

new_image_path = 'features-based-classification/dataset/Rottweiler/Rottweiler_1.jpg'
label = classify_image(new_image_path, dataset_descriptors, dataset_labels)

if label is not None:
    predicted = label_to_class[label]
    print(f"Predicted class: {predicted}")
else:
    print("Could not classify the image.")