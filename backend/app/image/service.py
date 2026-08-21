import easyocr
from PIL import Image
import numpy as np

# Load OCR model only once
reader = easyocr.Reader(["en"], gpu=False)


def extract_text_from_image(file):

    image = Image.open(file.file)

    image = np.array(image)

    results = reader.readtext(image)

    text = "\n".join(
        [result[1] for result in results]
    )

    return text