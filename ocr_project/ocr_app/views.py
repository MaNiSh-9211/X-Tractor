from django.shortcuts import render
from django.http import JsonResponse
import logging
import cv2
import numpy as np
import easyocr
import io

logger = logging.getLogger(__name__)

# Global variable for EasyOCR reader
_reader = None

def get_ocr_reader():
    global _reader
    if _reader is None:
        try:
            _reader = easyocr.Reader(['en'], gpu=False, model_storage_directory='/tmp')
            logger.info("EasyOCR reader initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {str(e)}")
            raise
    return _reader

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'message': 'OCR API is running'
    })

def ocr_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            if not image_file.content_type.startswith('image/'):
                return render(request, 'ocr_app/ocr.html', {
                    'error_message': "Please upload a valid image file."
                })
            if image_file.size > 10 * 1024 * 1024:
                return render(request, 'ocr_app/ocr.html', {
                    'error_message': "File size too large. Please upload an image smaller than 10MB."
                })
            image_data = image_file.read()
            extracted_text = process_image(image_data)
            if extracted_text:
                return render(request, 'ocr_app/ocr.html', {
                    'extracted_text': extracted_text
                })
            else:
                return render(request, 'ocr_app/ocr.html', {
                    'error_message': "Could not extract text from image. Please try again."
                })
        except Exception as e:
            logger.error(f"Error in OCR processing: {str(e)}")
            return render(request, 'ocr_app/ocr.html', {
                'error_message': "An error occurred while processing the image. Please try again."
            })
    return render(request, 'ocr_app/ocr.html')

def process_image(image_data):
    try:
        reader = get_ocr_reader()
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            logger.error("Failed to decode image")
            return None
        results = reader.readtext(image)
        texts = []
        for (bbox, text, confidence) in results:
            if confidence > 0.3 and len(text.strip()) > 0:
                cleaned_text = text.strip()
                texts.append(cleaned_text)
        if texts:
            return '\n'.join(texts)
        else:
            return None
    except Exception as e:
        logger.error(f"Error in image processing: {str(e)}")
        return None 