from django.shortcuts import render
from django.http import JsonResponse
import logging
import cv2
import numpy as np
import easyocr
import io
import time

logger = logging.getLogger(__name__)

# Global variable for EasyOCR reader
_reader = None

def get_ocr_reader():
    """Get or initialize the EasyOCR reader"""
    global _reader
    if _reader is None:
        try:
            logger.info("Initializing EasyOCR reader...")
            _reader = easyocr.Reader(['en'], gpu=False, model_storage_directory='/tmp')
            logger.info("EasyOCR reader initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {str(e)}")
            raise
    return _reader

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'OCR API is running'
    })

def ocr_view(request):
    """Main OCR view with privacy protection"""
    # Only clear session data on GET requests (fresh page loads)
    if request.method == 'GET':
        if 'extracted_text' in request.session:
            del request.session['extracted_text']
        if 'processing_time' in request.session:
            del request.session['processing_time']
        if 'error_message' in request.session:
            del request.session['error_message']
    
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            logger.info(f"Processing image: {image_file.name}, size: {image_file.size} bytes")
            
            # Validate file type
            if not image_file.content_type.startswith('image/'):
                logger.warning(f"Invalid file type: {image_file.content_type}")
                return render(request, 'ocr_app/ocr.html', {
                    'error_message': "Please upload a valid image file."
                })
            
            # Validate file size (10MB limit)
            if image_file.size > 10 * 1024 * 1024:
                logger.warning(f"File too large: {image_file.size} bytes")
                return render(request, 'ocr_app/ocr.html', {
                    'error_message': "File size too large. Please upload an image smaller than 10MB."
                })
            
            # Read image data
            image_data = image_file.read()
            logger.info("Image data read successfully")
            
            # Process with OCR
            start_time = time.time()
            extracted_text = process_image(image_data)
            processing_time = time.time() - start_time
            
            logger.info(f"OCR processing completed in {processing_time:.2f} seconds")
            
            if extracted_text:
                logger.info(f"Text extracted successfully: {len(extracted_text)} characters")
                return render(request, 'ocr_app/ocr.html', {
                    'extracted_text': extracted_text,
                    'processing_time': f"{processing_time:.2f} seconds"
                })
            else:
                logger.warning("No text extracted from image")
                return render(request, 'ocr_app/ocr.html', {
                    'error_message': "Could not extract text from image. Please try with a clearer image."
                })
                
        except Exception as e:
            logger.error(f"Error in OCR processing: {str(e)}", exc_info=True)
            return render(request, 'ocr_app/ocr.html', {
                'error_message': f"An error occurred while processing the image: {str(e)}"
            })
    
    # For GET requests, always return clean page
    return render(request, 'ocr_app/ocr.html')

def process_image(image_data):
    """Process image with OCR"""
    try:
        # Get OCR reader
        reader = get_ocr_reader()
        
        # Convert image data to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            logger.error("Failed to decode image")
            return None
        
        logger.info(f"Image decoded successfully: {image.shape}")
        
        # Perform OCR
        logger.info("Starting OCR processing...")
        results = reader.readtext(image)
        logger.info(f"OCR found {len(results)} text regions")
        
        # Extract and clean text
        texts = []
        for i, (bbox, text, confidence) in enumerate(results):
            logger.info(f"Text {i+1}: '{text}' (confidence: {confidence:.3f})")
            if confidence > 0.3 and len(text.strip()) > 0:
                cleaned_text = text.strip()
                texts.append(cleaned_text)
        
        # Join texts with newlines
        if texts:
            final_text = '\n'.join(texts)
            logger.info(f"Final extracted text: {len(final_text)} characters")
            return final_text
        else:
            logger.warning("No text passed confidence threshold")
            return None
            
    except Exception as e:
        logger.error(f"Error in image processing: {str(e)}", exc_info=True)
        return None 