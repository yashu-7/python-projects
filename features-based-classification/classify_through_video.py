import cv2
import pickle
import numpy as np

cam = cv2.VideoCapture(0)

with open('features-based-classification/descriptors_data/images_and_data.pkl', 'rb') as f:
    data = pickle.load(f)

dataset_descriptors = data['descriptors']
dataset_labels = data['labels']
class_labels = data['class_labels']

label_to_class = {label: class_name for class_name, label in class_labels.items()}

print(label_to_class)

orb = cv2.ORB_create()

def extract_features(image):
    kp, des = orb.detectAndCompute(image, None)
    return des

def classify_image(image, dataset_descriptors, dataset_labels, k=2, ratio_thresh=0.75):
    new_descriptors = extract_features(image)
    
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

while 1:
    ret,frame = cam.read()
    if not ret:
        break
    
    label = classify_image(frame, dataset_descriptors, dataset_labels)

    if label is not None:
        predicted = label_to_class[label]
    else:
        predicted = "Unknown"
    
    cv2.putText(frame, predicted, (5,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('win', frame)
    
    if cv2.waitKey(1) & 0xff==ord("q"):
        break
cam.release()
cv2.destroyAllWindows()