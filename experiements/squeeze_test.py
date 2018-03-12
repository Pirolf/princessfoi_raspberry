import cv2
import time
import numpy as np


class SqueezeClassifier:
    # classes to match against
    CLASSES = {
        'n02123045': 'tabby, tabby cat',
        'n02123159': 'tiger cat',
        'n02123394': 'Persian cat',
        'n02123597': 'Siamese cat, Siamese',
        'n02124075': 'Egyptian cat',
        'n02125311': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'
    }

    LABELS_PATH = '../models/squeezenet_labels'

    def __init__(self, prototxt, model, min_confidence=0, debug=False):
        self.min_confidence = min_confidence
        self.debug = debug
        # Load the class labels from disk
        rows = open(self.LABELS_PATH).read().strip().split("\n")
        self.labels = [r[r.find(" ") + 1:].split(",")[0] for r in rows]

        # load our serialized model from disk
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # image: np array (h, w, 3)
    def detect(self, image):
        detect_start = 0
        if (self.debug):
            detect_start = time.perf_counter()

        ret = self._detect(image)
        if (self.debug):
            print("Detect taken: {} ms".format(
                1000*(time.perf_counter() - detect_start)))
        return ret

    def _detect(self, image):
        # load the input image and construct an input blob for the image
        # by resizing to a fixed 300x300 pixels and then normalizing it
        # (note: normalization is done via the authors of the MobileNet SSD
        # implementation)
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        print("[INFO] computing object detections...")
        self.net.setInput(blob)
        detections = self.net.forward()

        # Sort the indexes of the probabilities in descending order (higher
        # probabilitiy first) and grab the top-5 predictions
        detections = detections.reshape((1, len(self.labels)))
        idxs = np.argsort(detections[0])[::-1][:100]

        # Loop over the top-5 predictions and display them
        for (i, idx) in enumerate(idxs):
            # Display the predicted label
            # + associated probability to the console
            label = self.labels[idx]
            prob = detections[0][idx]

            print("[INFO] {}. label: {}, probability: {}".format(i, label, prob))

        return (False, 0)


classifier = SqueezeClassifier('../models/squeezenet_v1.1.prototxt',
                               '../models/squeezenet_v1.1.caffemodel',
                               debug=True)

image = cv2.imread('test_images/fluff_tilt.jpg')
classifier.detect(image)
