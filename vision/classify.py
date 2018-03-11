import numpy as np
import cv2
import time


class Classifier:
    # class labels MobileNet SSD was trained to detect
    '''
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    '''

    def __init__(self, prototxt, model, min_confidence=0, debug=False):
        self.min_confidence = min_confidence
        self.debug = debug
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

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]
            # extract the index of the class label from the `detections`,
            idx = int(detections[0, 0, i, 1])

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            # index for cat is 8
            if idx == 8:
                return (confidence > self.min_confidence, confidence)
        return (False, 0)
