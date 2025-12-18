# SmartCrop Backend API – Django REST API

A backend API for the **SmartCrop Crop Disease Detection System**, built with Django REST Framework. It supports image-based crop disease detection (mocked for MVP) and includes robust error handling, Swagger documentation, and CORS support.

---

## Features ✅

- Health check endpoint for deployment verification  
- Crop image analysis endpoint (mock disease detection)  
- Image validation (JPG/PNG, max 10MB)  
- Swagger/OpenAPI documentation  
- CORS support for frontend integration  
- Comprehensive error handling  
- Unit tests included  

---

## Installation

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Django project

Create a Django project and app if not already done:

```bash
django-admin startproject smartcrop_project .
python manage.py startapp smartcrop
```

### 4. Update settings

- Add the necessary app configuration to `settings.py`  
- Add `CORS_ALLOWED_ORIGINS` for frontend integration:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # frontend URL
]
```

### 5. Configure URLs

- Add `smartcrop/urls.py` for the app  
- Add Swagger/OpenAPI URLs in `smartcrop_project/urls.py`

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start the server

```bash
python manage.py runserver
```

Access the API at: `http://localhost:8000`

---

## API Endpoints

### 1. Health Check

- **Endpoint:** `GET /health`  
- **Purpose:** Verify the server is running  
- **Response:**

```json
{ "status": "OK" }
```

- **Test with curl:**

```bash
curl http://localhost:8000/health
```

---

### 2. Analyze Crop Image

- **Endpoint:** `POST /analyze`  
- **Purpose:** Analyze crop image for diseases  
- **Request:** `multipart/form-data`

```http
image: JPG/PNG file (max 10MB)
```

- **Response Example:**

```json
{
  "issue": "Leaf blight",
  "confidence": 0.85,
  "recommendation": [
    "Reduce watering frequency",
    "Apply organic fungicide",
    "Remove affected leaves"
  ]
}
```

- **Test with curl:**

```bash
curl -X POST http://localhost:8000/analyze \
-F "image=@/path/to/crop_image.jpg"
```

- **Test with Python:**

```python
import requests

url = "http://localhost:8000/analyze"
files = {'image': open('crop_image.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

---

### Error Responses

| Error Type          | Response |
|--------------------|----------|
| Missing Image       | `{ "error": "No image file provided. Please upload an image." }` |
| Invalid File Type   | `{ "error": "Invalid file type. Only JPG and PNG images are allowed." }` |
| File Too Large      | `{ "error": "File size too large. Maximum size is 10MB." }` |
| Processing Error    | `{ "error": "Failed to process image: [error details]" }` |

---

## Documentation

- **Swagger UI:** `http://localhost:8000/docs/`  
- **ReDoc:** `http://localhost:8000/redoc/`

---

## Testing

- Run all tests:

```bash
python manage.py test
```

- Run specific tests:

```bash
python manage.py test smartcrop.tests.HealthCheckTestCase
python manage.py test smartcrop.tests.AnalyzeCropTestCase
```

---

## Project Structure

```
smartcrop_project/
├── smartcrop/
│   ├── __init__.py
│   ├── views.py       # API endpoint implementations
│   ├── urls.py        # URL routing
│   ├── tests.py       # Unit tests
│   └── ...
├── smartcrop_project/
│   ├── settings.py    # Django settings
│   ├── urls.py        # Main URL configuration
│   └── ...
├── requirements.txt   # Python dependencies
└── manage.py
```

---

## Mock Analysis Logic

- The current `mock_crop_analysis()` function returns randomized disease results for MVP.  
- To integrate a real AI model:
  1. Replace `mock_crop_analysis()` in `views.py`  
  2. Load your trained model (TensorFlow, PyTorch, etc.)  
  3. Process the uploaded image  
  4. Return predictions with confidence scores  

---

## Deployment Checklist

- Set `DEBUG = False` in production  
- Configure proper `ALLOWED_HOSTS`  
- Set `CORS_ALLOW_ALL_ORIGINS = False` and specify `CORS_ALLOWED_ORIGINS`  
- Serve static files properly  
- Configure production database  
- Set environment variables for secrets  
- Enable HTTPS  
- Configure proper logging  

---

## Frontend Integration

- CORS is enabled. Update `CORS_ALLOWED_ORIGINS` with frontend URL.  

---

## Deliverables Status ✅

- `/health` endpoint implemented and tested  
- `/analyze` endpoint implemented and tested  
- Image validation (type & size) ✅  
- Comprehensive error handling ✅  
- Swagger documentation at `/docs` ✅  
- CORS enabled ✅  
- Unit tests included ✅  
- Ready for frontend integration ✅  

---

## License

- **MIT License**

