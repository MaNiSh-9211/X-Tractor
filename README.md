# OCR Text Extractor

A fully local, serverless-ready OCR (Optical Character Recognition) application built with Django and EasyOCR. Extract text from images without any external APIs or internet dependencies.

## 🚀 Features

- **100% Local Processing** - No external APIs or internet required
- **EasyOCR Integration** - Powered by deep learning neural networks
- **Modern UI** - Clean, responsive design with real-time feedback
- **Serverless Ready** - Deployable on Vercel, Netlify, and similar platforms
- **Privacy Focused** - Images never leave your machine
- **Multi-format Support** - JPEG, PNG, GIF, BMP, and more
- **Real-time Processing** - Shows processing time and progress

## 🛠️ Technology Stack

- **Backend**: Django 5.2.3
- **OCR Engine**: EasyOCR (PyTorch-based)
- **Image Processing**: OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Vercel-ready with WhiteNoise

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd OCRtesrect
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
Open your browser and go to: `http://127.0.0.1:8000/`

## 📁 Project Structure

```
OCRtesrect/
├── ocr_project/          # Django project settings
│   ├── settings.py       # Main configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI application
├── ocr_app/             # Main OCR application
│   ├── views.py         # OCR processing logic
│   ├── urls.py          # App URL patterns
│   └── templates/       # HTML templates
│       └── ocr_app/
│           └── ocr.html # Main OCR interface
├── static/              # Static files (CSS, JS, images)
├── media/               # Uploaded files (development)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment config
├── build.sh             # Build script for deployment
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key (auto-generated if not set)
- `DEBUG`: Set to 'true' for development, 'false' for production

### OCR Settings
- **Language**: English (configurable in `views.py`)
- **GPU**: Disabled for serverless compatibility
- **Confidence Threshold**: 0.3 (30% minimum confidence)
- **File Size Limit**: 10MB maximum

## 🚀 Deployment

### Vercel Deployment

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Set Environment Variables** (in Vercel dashboard)
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: false

### Manual Deployment
```bash
# Build static files
python manage.py collectstatic

# Deploy using your preferred method
```

## 📊 How It Works

### 1. Image Upload
- User selects an image file (JPEG, PNG, etc.)
- File is validated for type and size
- Image data is read into memory

### 2. Image Processing
- OpenCV converts image to numpy array
- Image is prepared for OCR processing
- Format validation and error handling

### 3. OCR Processing
- EasyOCR neural network analyzes the image
- Text regions are detected and recognized
- Confidence scores are calculated for each text region

### 4. Text Extraction
- High-confidence text regions are extracted
- Text is cleaned and formatted
- Duplicate removal and ordering

### 5. Result Display
- Extracted text is displayed in formatted output
- Processing time is shown
- Error handling for failed extractions

## 🔍 Troubleshooting

### Common Issues

1. **"No text extracted"**
   - Try a clearer, higher resolution image
   - Ensure text is clearly visible and not blurry
   - Check if image contains actual text content

2. **Slow processing**
   - First run downloads models (one-time process)
   - Large images take longer to process
   - Consider resizing very large images

3. **Memory errors**
   - Reduce image file size
   - Close other applications to free memory
   - Use smaller images for testing

### Logs
Check `django.log` file for detailed error information:
```bash
tail -f django.log
```

## 🎯 Performance Tips

- **Image Quality**: Use clear, high-contrast images
- **Text Size**: Ensure text is readable (minimum 12pt equivalent)
- **File Size**: Keep images under 5MB for faster processing
- **Format**: JPEG or PNG work best

## 🔒 Security & Privacy

- **No External APIs**: All processing is local
- **No Data Storage**: Images are processed in memory only
- **No Tracking**: No analytics or user tracking
- **Open Source**: Transparent codebase

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the logs in `django.log`
- Create an issue in the repository

---

**Built with ❤️ using Django and EasyOCR** 