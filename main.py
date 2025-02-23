from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
import io
import uvicorn

app = FastAPI()

# Load pre-trained AI model (example: MobileNetV2 for food recognition)
model = tf.keras.applications.MobileNetV2(weights="imagenet")

# Function to preprocess image
def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# API endpoint to analyze food image
@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    processed_img = preprocess_image(image)
    predictions = model.predict(processed_img)
    decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
    return {"predictions": [{"food": pred[1], "confidence": float(pred[2])} for pred in decoded_preds]}

# API endpoint for barcode scanning
@app.get("/scan-barcode/{barcode}")
def scan_barcode(barcode: str):
    response = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json")
    data = response.json()
    if "product" in data:
        product = data["product"]
        return {
            "name": product.get("product_name", "Unknown"),
            "calories": product.get("nutriments", {}).get("energy-kcal", "N/A"),
            "nutrients": product.get("nutriments", {})
        }
    return {"error": "Product not found"}

# API endpoint for manual text-based food logging
@app.post("/log-food/")
def log_food(food_name: str):
    # Example database/API integration (mocked response)
    food_data = {
        "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fats": 0.2},
        "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fats": 0.3}
    }
    if food_name.lower() in food_data:
        return {"food": food_name, "nutrition": food_data[food_name.lower()]}
    return {"error": "Food not found in database"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
