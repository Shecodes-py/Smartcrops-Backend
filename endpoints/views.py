from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view #,  parser_classes
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from PIL import Image # Pillow for image processing
import io # for in-memory file handling
import random
from django.http import HttpResponse

from huggingface_hub import InferenceClient
import io
import os 
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)
MODEL_ID = "wambugu71/crop_leaf_diseases_vit"

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the SmartCrops API", status=200)

@require_http_methods(["GET"])
def health_check(request):

    """
    Health check endpoint to verify that the server is running.

    Returns with a freaking ok as Lope Requested 
    """
    return JsonResponse({"status": "ok"}, status=200)

@api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser])
def analyze_crop(request):
    """
    Accepts an uploaded crop image. 
    - Analyzes the image for crop issues. 
    - Returns detected issue, confidence, and recommendations.
    """

    # check if image exist first
    if 'image' not in request.FILES:
        return Response({
            "error": "No image provided. PPlease upload an image file."},
            status=status.HTTP_400_BAD_REQUEST)
    
    image_file = request.FILES['image']

    # validate image type
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
    if image_file.content_type not in allowed_types:
        return Response({
            "error": "Unsupported file type. Please upload a JPEG or PNG or JPEG image."},
            status=status.HTTP_400_BAD_REQUEST)

    # check file size   max is 10mb
    max_size = 10 * 1024 * 1024  # 10 MB
    if image_file.size > max_size:
        return Response({
            "error": "File size exceeds the 10MB limit."},
            status=status.HTTP_400_BAD_REQUEST)
    
    # time to see if we can read and valdate the image
    try:
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))

        image.verify()  # Verify that it is, in fact, an image

        analysis_result = mock_crop_analysis(image_file.name)

        return Response({
            "analysis": analysis_result,
            "message": "Image uploaded and validated successfully."},
            status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "error": "Invalid image file. Please upload a valid image."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def mock_crop_analysis(image_name):
    """
    Mock function to simulate crop analysis.
    In a real implementation, this would involve ML model inference.
    """

    diseases = [
        {
            "issue": "Powdery Mildew",
            "confidence": round(random.uniform(0.7, 0.99), 2),
            "recommendation": "Apply fungicide and ensure proper air circulation."
        },
        {
            "issue": "Aphid Infestation",
            "confidence": round(random.uniform(0.6, 0.95), 2),
            "recommendation": "Use insecticidal soap or introduce natural predators."
        },
        {
            "issue": "Nutrient Deficiency",
            "confidence": round(random.uniform(0.5, 0.9), 2),
            "recommendation": "Test soil and apply appropriate fertilizers."
        },
        {
            "issue": "Leaf blight",
            "confidence": round(random.uniform(0.75, 0.95), 2),
            "recommendation": [
                "Reduce watering frequency",
                "Apply organic fungicide",
                "Remove affected leaves",
                "Improve air circulation"
            ]
        },
        {
            "issue": "Powdery mildew",
            "confidence": round(random.uniform(0.70, 0.90), 2),
            "recommendation": [
                "Apply neem oil spray",
                "Reduce humidity levels",
                "Increase sunlight exposure",
                "Remove infected plant parts"
            ]
        },
        {
            "issue": "Nutrient deficiency (Nitrogen)",
            "confidence": round(random.uniform(0.80, 0.95), 2),
            "recommendation": [
                "Apply nitrogen-rich fertilizer",
                "Use compost or manure",
                "Test soil pH levels",
                "Ensure proper drainage"
            ]
        },
        {
            "issue": "Pest infestation (Aphids)",
            "confidence": round(random.uniform(0.75, 0.92), 2),
            "recommendation": [
                "Spray with insecticidal soap",
                "Introduce beneficial insects",
                "Remove pests manually",
                "Use neem oil treatment"
            ]
        },
        {
            "issue": "Healthy crop",
            "confidence": round(random.uniform(0.85, 0.98), 2),
            "recommendation": [
                "Continue current care routine",
                "Monitor regularly for changes",
                "Maintain consistent watering",
                "Ensure adequate nutrition"
            ]
        }
    ]
    
    detected_issue = random.choice(diseases)
    return detected_issue

'''
def analyze_with_ai_model(image):
    # Load model
    model = load_model('path/to/model.h5')
    
    # Preprocess image
    img_array = preprocess_image(image)
    
    # Make prediction
    predictions = model.predict(img_array)
    
    # Format response
    return {
        "issue": get_disease_name(predictions),
        "confidence": float(predictions.max()),
        "recommendation": get_recommendations(predictions)
    }'''


@csrf_exempt
@require_http_methods(["POST"])
def diagnose_plant(request):
    """
    Django view to diagnose plant diseases from uploaded images
    """
    # Check if file was uploaded
    if 'file' not in request.FILES:
        return JsonResponse(
            {"error": "No file provided"},
            status=400
        )
    
    file = request.FILES['file']
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        return JsonResponse(
            {"error": "File provided is not an image."},
            status=400
        )
    
    try:
        # Read image data
        image_data = file.read()
        
        # Get predictions from HuggingFace model
        results = client.image_classification(image_data, model=MODEL_ID)
        
        # Return results
        return JsonResponse({
            "filename": file.name,
            "top_prediction": results[0]["label"],
            "confidence": f"{results[0]['score']:.2%}",
            "all_results": results[:3]
        })
    
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )