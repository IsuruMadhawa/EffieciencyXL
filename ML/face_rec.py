import os
import dlib
import numpy as np

def compute_face_descriptors(training_dataset_path):
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
    facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

    face_descriptors = []
    face_labels = []

    for filename in os.listdir(training_dataset_path):
        if filename.endswith(".jpg"):
            img_path = os.path.join(training_dataset_path, filename)
            img = dlib.load_rgb_image(img_path)

            detections = detector(img, 1)
            if len(detections) > 0:
                shape = sp(img, detections[0])
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                face_descriptors.append(np.array(face_descriptor))
                face_labels.append(filename)  # Use filename as label

    return face_descriptors, face_labels
