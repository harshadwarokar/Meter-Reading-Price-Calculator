import streamlit as st
import cv2
import google.generativeai as genai
from PIL import Image
import numpy as np
import time

# Configure Google Generative AI API key
API_KEY = "AIzaSyD_sZRCvGI3P7aPVyCtznPAuqtcBdiQYvo"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

def analyze_meter_reading(frame):
    """
    Analyzes the meter reading from the provided image frame using the Gemini vision model.
    Returns the meter reading as a float if successful, or None otherwise.
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
        
        # Generate the content using the Gemini model
        response = model.generate_content([prompt, image])
        
        if response and response.text:
            reading_str = response.text.strip()
            # Filter out only digits and dots (in case of a decimal reading)
            filtered_str = ''.join(filter(lambda c: c.isdigit() or c == '.', reading_str))
            try:
                reading_value = float(filtered_str)
                return reading_value
            except ValueError:
                st.error("Unable to parse a numeric meter reading from the model's response.")
                return None
        else:
            st.error("No response received from the vision model.")
            return None
    except Exception as e:
        st.error(f"Error during meter reading analysis: {e}")
        return None

# Streamlit App Layout
st.title("Meter Reading Price Calculator (in Dirhams)")
st.write(
    "Upload an image of your current meter reading, enter the previous meter reading and the cost per unit (e.g., 10 AED per unit), "
    "and click **Submit** to calculate the total consumption and price in Dirhams."
)

# File uploader for the current meter reading photo
uploaded_file = st.file_uploader("Upload current meter reading photo", type=["jpg", "jpeg", "png"])

# Input field for previous meter reading
try:
    previous_reading = st.number_input("Enter previous meter reading", min_value=0.0, step=0.1, format="%.2f")
except Exception as e:
    st.error(f"Error in previous meter reading input: {e}")

# Input field for cost per unit in AED
try:
    unit_cost = st.number_input("Enter cost per unit (e.g., 10 AED per unit)", min_value=0.0, step=0.1, format="%.2f")
except Exception as e:
    st.error(f"Error in unit cost input: {e}")

# Process the image and calculate the price when the Submit button is clicked
if st.button("Submit"):
    try:
        if uploaded_file is not None:
            try:
                # Open and display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Meter Reading", use_container_width=True)
            except Exception as e:
                st.error(f"Error opening the uploaded image: {e}")
                image = None

            if image is not None:
                try:
                    # Convert the image to a format suitable for OpenCV (BGR)
                    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                except Exception as e:
                    st.error(f"Error converting image for processing: {e}")
                    frame = None

                if frame is not None:
                    with st.spinner("Extracting current meter reading..."):
                        current_reading = analyze_meter_reading(frame)
                        time.sleep(1)  # Optional pause to simulate processing time
                    
                    if current_reading is None:
                        st.error("Could not extract a meter reading from the image. Please try again with a clearer photo.")
                    else:
                        # Calculate the consumption ensuring no negative consumption
                        consumption = current_reading - previous_reading
                        if consumption < 0:
                            st.error("The current meter reading is less than the previous reading. Please verify the inputs.")
                        else:
                            total_price = consumption * unit_cost
                            st.success(f"**Current Meter Reading:** {current_reading}")
                            st.info(f"**Previous Meter Reading:** {previous_reading}")
                            st.success(f"**Consumption (Units):** {consumption}")
                            st.success(f"**Total Price:** AED {total_price:.2f}")
        else:
            st.error("Please upload a current meter reading image.")
    except Exception as e:
        st.error(f"Error processing the request: {e}")
