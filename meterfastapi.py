from fastapi import FastAPI, HTTPException, Path
import requests
from io import BytesIO
from PIL import Image
import cv2
import google.generativeai as genai
import numpy as np
import time

# Initialize FastAPI app
app = FastAPI()

# Configure Google Generative AI API key (replace with your actual API key)
API_KEY = "AIzaSyD_sZRCvGI3P7aPVyCtznPAuqtcBdiQYvo"
genai.configure(api_key=API_KEY)

def analyze_meter_reading(frame):
    """
    Analyzes the meter reading from the provided image frame using the Gemini vision model.
    Returns the meter reading as a float if successful.
    Raises an Exception if there is an error.
    """
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Convert the frame (BGR) to a PIL Image (RGB)
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Prompt to instruct the model to extract only the numeric meter reading.
        prompt = (
            "Extract the meter reading from the image. "
            "Provide only the numeric reading value, with no additional text. "
            "For example, if the reading is 12345, simply return 12345."
        )
        
        # Generate content using the Gemini model
        response = model.generate_content([prompt, image])
        
        if response and response.text:
            reading_str = response.text.strip()
            # Filter out only digits and dots (in case of a decimal reading)
            filtered_str = ''.join(filter(lambda c: c.isdigit() or c == '.', reading_str))
            try:
                reading_value = float(filtered_str)
                return reading_value
            except ValueError:
                raise ValueError("Unable to parse a numeric meter reading from the model's response.")
        else:
            raise ValueError("No response received from the vision model.")
    except Exception as e:
        raise Exception(f"Error during meter reading analysis: {e}")

@app.get("/upload-analyze/{file_url:path}/{previous_reading}/{unit_cost}")
def upload_analyze(
    file_url: str = Path(..., description="URL of the image file. URL-encoded if it contains special characters."),
    previous_reading: float = Path(..., description="Previous meter reading"),
    unit_cost: float = Path(..., description="Price rate per unit in AED")
):
    """
    Endpoint to download an image from a given URL, extract the current meter reading,
    calculate consumption (current - previous) and then compute the total price.
    """
    try:
        # Remove a potential "file_url=" prefix if present in the path parameter.
        if file_url.startswith("file_url="):
            file_url = file_url[len("file_url="):]
        
        # Download the image from the provided URL
        response = requests.get(file_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Unable to download image from provided URL.")
        
        try:
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error opening the image: {e}")
        
        # Convert the image to a format suitable for OpenCV (BGR)
        try:
            frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing the image: {e}")
        
        # Analyze the current meter reading from the image
        current_reading = analyze_meter_reading(frame)
        time.sleep(1)  # Optional delay to simulate processing time
        
        if current_reading is None:
            raise HTTPException(status_code=400, detail="Could not extract a meter reading from the image.")
        
        # Calculate consumption ensuring no negative consumption
        consumption = current_reading - previous_reading
        if consumption < 0:
            raise HTTPException(status_code=400, detail="Current meter reading is less than previous reading.")
        
        total_price = consumption * unit_cost
        
        return {
            "current_reading": current_reading,
            "previous_reading": previous_reading,
            "consumption": consumption,
            "unit_cost": unit_cost,
            "total_price": total_price,
            "currency": "AED"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
