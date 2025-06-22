# Deployment Guide

## 🚀 Vercel Deployment

### Prerequisites
- Vercel account
- Git repository with your code

### Steps

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Set Environment Variables** (in Vercel dashboard)
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: false

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DEBUG=false
```

## 🔧 Manual Deployment

### 1. Build Static Files
```bash
python manage.py collectstatic
```

### 2. Set Production Settings
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Set proper `SECRET_KEY`

### 3. Deploy Files
Upload all files to your hosting provider

## 📝 Notes

- The app uses SQLite database (suitable for serverless)
- EasyOCR models are downloaded on first run
- Static files are served via WhiteNoise
- No external dependencies required

## 🐛 Troubleshooting

### Common Issues
1. **Build fails**: Check Python version compatibility
2. **OCR not working**: Ensure all dependencies are installed
3. **Static files not loading**: Run `collectstatic` command

### Logs
Check Vercel function logs for detailed error information. 