from skimage.filters import threshold_local
import numpy as np
import cv2
import math
from PIL import Image
import io

mu = 200
lookup = [int(255 * math.log(1 + mu * x / 255) // math.log(1 + mu)) for x in range(256)]


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def transform_four_points(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def f(x):
    return lookup[x]


def process(image_stream):
    image = cv2.imdecode(np.frombuffer(image_stream.getbuffer(), np.uint8), -1)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    screen_cnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screen_cnt = approx
            break

    reshaped = (
        image
        if screen_cnt is None
        else transform_four_points(image, screen_cnt.reshape(4, 2))
    )
    if screen_cnt is not None:
        image = transform_four_points(image, screen_cnt.reshape(4, 2))
    warped = cv2.cvtColor(reshaped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 15, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255

    product = image.copy()
    for i in range(3):
        copy = warped // 255
        product[:, :, i] *= copy

    final = np.vectorize(f)(product).astype(np.uint8)

    _, buffer = cv2.imencode(".jpg", final)
    return io.BytesIO(buffer)
