# Meter Reading Price Calculator

## Overview
The **Meter Reading Price Calculator** is a **Streamlit-based application** that utilizes **Google Generative AI** to extract numeric readings from uploaded meter images. It calculates the total consumption and cost based on user-provided unit prices.

## Features
- **AI-Powered Meter Reading Extraction**: Uses Google Gemini AI to detect and extract numerical meter readings from images.
- **Automatic Consumption Calculation**: Computes the difference between previous and current readings.
- **User-Friendly Interface**: Built with Streamlit for seamless interaction.

## Installation

### Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/harshadwarokar/Meter-Reading-Price-Calculator.git
   cd Meter-Reading-Price-Calculator
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   - Create a `.env` file in the root directory and add your **Google Generative AI API key**:
     ```plaintext
     api_key = "YOUR_GOOGLE_GENERATIVE_AI_KEY"
     ```

## Usage
Run the Streamlit app:
```bash
streamlit run meterprice.py
```

### Uploading Files
- **Meter Reading Image**: Upload an image containing the current meter reading.
- **Input Values**:
  - Enter the previous meter reading.
  - Specify the cost per unit in AED.

## Dependencies
- **Streamlit** (UI framework)
- **OpenCV** (Image processing)
- **Google Generative AI** (AI-powered meter reading extraction)
- **Pillow** (Image handling)
- **NumPy** (Array operations)

## Contributing
Pull requests are welcome! If you have suggestions or improvements, please open an issue or submit a PR.



