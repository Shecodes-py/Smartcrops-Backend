SmartCrop Backend API
Django REST API for SmartCrop crop disease detection system.

Features
✅ Health check endpoint for deployment verification
✅ Crop image analysis endpoint with mock disease detection
✅ Image validation (JPG/PNG, size limits)
✅ Swagger/OpenAPI documentation
✅ CORS support for frontend integration
✅ Comprehensive error handling
✅ Unit tests included

Installation
1. Create virtual environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2. Install dependencies
bash
pip install -r requirements.txt
3. Configure Django project
Create a new Django app if you haven't:

bash
django-admin startproject smartcrop_project .
python manage.py startapp smartcrop

4. Update settings
Add the configuration from settings.py additions to your settings.py file.

5. Update URLs
Add the app URLs configuration to your app's urls.py
Add the Swagger configuration to your project's main urls.py

6. Run migrations
bash
python manage.py migrate

7. Start the server
bash
python manage.py runserver
The server will start at http://localhost:8000

API Endpoints
1. Health Check
Endpoint: GET /health

Purpose: Verify server is running

Response:

json
{
  "status": "OK"
}
Test:

bash
curl http://localhost:8000/health

2. Analyze Crop
Endpoint: POST /analyze

Purpose: Analyze crop image for diseases

Request:

Method: POST
Content-Type: multipart/form-data
Body: image file (JPG or PNG, max 10MB)
Response:

json
{
  "issue": "Leaf blight",
  "confidence": 0.85,
  "recommendation": [
    "Reduce watering frequency",
    "Apply organic fungicide",
    "Remove affected leaves"
  ]
}
Test with curl:

bash
curl -X POST http://localhost:8000/analyze \
  -F "image=@/path/to/crop_image.jpg"
Test with Python:

python
import requests

url = "http://localhost:8000/analyze"
files = {'image': open('crop_image.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
Error Responses
Missing Image
json
{
  "error": "No image file provided. Please upload an image."
}
Invalid File Type
json
{
  "error": "Invalid file type. Only JPG and PNG images are allowed."
}
File Too Large
json
{
  "error": "File size too large. Maximum size is 10MB."
}
Processing Error
json
{
  "error": "Failed to process image: [error details]"
}

Documentation
Swagger UI
Visit http://localhost:8000/docs/ for interactive API documentation

ReDoc
Visit http://localhost:8000/redoc/ for alternative documentation view

Testing
Run the test suite:

bash
python manage.py test
Run specific test class:

bash
python manage.py test smartcrop.tests.HealthCheckTestCase
python manage.py test smartcrop.tests.AnalyzeCropTestCase

Project Structure
smartcrop_project/
├── smartcrop/
│   ├── __init__.py
│   ├── views.py          # API endpoint implementations
│   ├── urls.py           # URL routing
│   ├── tests.py          # Unit tests
│   └── ...
├── smartcrop_project/
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── ...
├── requirements.txt      # Python dependencies
└── manage.py

Frontend Integration
The API supports CORS for frontend integration. Update CORS_ALLOWED_ORIGINS in settings.py with your frontend URL:

python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Your frontend URL
]

Mock Analysis Logic
The current implementation uses mock disease detection for MVP purposes. The mock_crop_analysis() function returns randomized results from a predefined disease database.

To integrate a real AI model:
Replace the mock_crop_analysis() function in views.py
Load your trained model (TensorFlow, PyTorch, etc.)
Process the image through the model
Return predictions with confidence scores

Deployment Checklist
 Set DEBUG = False in production
 Configure proper ALLOWED_HOSTS
 Set CORS_ALLOW_ALL_ORIGINS = False
 Configure specific CORS_ALLOWED_ORIGINS
 Set up proper static file serving
 Configure production database
 Set up environment variables for secrets
 Enable HTTPS
 Configure proper logging

Deliverables Status
✅ /health endpoint implemented and tested
✅ /analyze endpoint implemented and tested
✅ Image validation (file type and size)
✅ Error handling for all scenarios
✅ Swagger documentation available at /docs
✅ CORS enabled for frontend integration
✅ Unit tests included
✅ Ready for frontend integration

Support
For issues or questions, please contact the development team.

License
MIT License

