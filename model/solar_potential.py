# import sys
# import os
# import numpy as np
# import cv2
# from tensorflow.keras.models import load_model
# from .area_calculator import calculate_total_area
# from PIL import Image

# # Add the path to the cloned repo
# repo_path = os.path.join(os.path.dirname(__file__), 'Rooftop-Solar-Energy-Potential-Map')
# sys.path.append(repo_path)

# # Load the model
# model = load_model('model/Rooftop-Solar-Energy-Potential-Map/model_resnet.py', compile=False)

# def preprocess_image(image_path, target_size=(256, 256)):
#     img = Image.open(image_path)
#     img = img.resize(target_size)
#     img_array = np.array(img)
#     if img_array.shape[-1] == 4:
#         img_array = img_array[..., :3]
#     img_array = img_array / 255.0
#     img_array = np.expand_dims(img_array, axis=0)
#     return img_array

# def post_process_mask(mask):
#     kernel = np.ones((5, 5), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.GaussianBlur(mask, (5, 5), 0)
#     return mask

# def calculate_solar_irradiance(latitude):
#     """
#     Estimate average daily solar irradiance (kWh/m²/day) based on latitude.
#     This is a simplified model and should be replaced with more accurate data if available.
#     """
#     max_irradiance = 6.0  # kWh/m²/day at the equator
#     min_irradiance = 2.5  # kWh/m²/day at the poles
    
#     irradiance = max_irradiance - (abs(latitude) / 90) * (max_irradiance - min_irradiance)
#     return irradiance

# def calculate_solar_potential(image_path, latitude, longitude):
#     # Preprocess the image
#     preprocessed_image = preprocess_image(image_path)
    
#     # Predict using the model
#     predictions = model.predict(preprocessed_image)
#     binary_mask = (predictions[0, :, :, 0] > 0.45).astype(np.uint8)
    
#     # Post-process the mask
#     post_processed_mask = post_process_mask(binary_mask)
    
#     # Calculate building and image areas
#     total_building_area, image_area = calculate_total_area(image_path, post_processed_mask)
    
#     # Solar panel parameters
#     panel_efficiency = 0.20  # 20% efficiency for a typical solar panel
#     performance_ratio = 0.75  # Account for various system losses
    
#     # Calculate average daily solar irradiance
#     daily_irradiance = calculate_solar_irradiance(latitude)
    
#     # Calculate annual solar irradiance (kWh/m²/year)
#     annual_irradiance = daily_irradiance * 365
    
#     # Calculate potential annual energy production (kWh/year)
#     solar_potential = (
#         total_building_area *  # Total available area (m²)
#         annual_irradiance *    # Annual solar irradiance (kWh/m²/year)
#         panel_efficiency *     # Solar panel efficiency
#         performance_ratio      # Performance ratio (accounting for system losses)
#     )
    
#     # Convert to MWh for easier representation
#     solar_potential_mwh = solar_potential / 1000
    
#     return total_building_area, image_area, solar_potential_mwh

# # Example usage
# if __name__ == "__main__":
#     image_path = "path/to/your/image.tif"
#     latitude = 40.7128  # Example: New York City latitude
#     longitude = -74.0060  # Example: New York City longitude
    
#     building_area, image_area, potential = calculate_solar_potential(image_path, latitude, longitude)
    
#     print(f"Total Building Area: {building_area:.2f} m²")
#     print(f"Total Image Area: {image_area:.2f} m²")
#     print(f"Annual Solar Energy Potential: {potential:.2f} MWh")







# *********this is the currently worrking code *******
# import sys
# import os
# import numpy as np
# import cv2
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate
# from tensorflow.keras.applications import ResNet50
# from .area_calculator import calculate_total_area
# from PIL import Image

# # Get the absolute path of the current file (solar_potential.py)
# current_file_path = os.path.abspath(__file__)
# current_dir = os.path.dirname(current_file_path)

# def unet_resnet50(input_size=(256, 256, 3)):
#     inputs = Input(input_size)
    
#     # ResNet50 as encoder
#     resnet = ResNet50(include_top=False, weights='imagenet', input_tensor=inputs)
    
#     # Decoder
#     x = Conv2D(256, 3, activation='relu', padding='same')(resnet.output)
#     x = UpSampling2D()(x)
#     x = concatenate([x, resnet.get_layer('conv4_block6_out').output])
#     x = Conv2D(128, 3, activation='relu', padding='same')(x)
    
#     x = UpSampling2D()(x)
#     x = concatenate([x, resnet.get_layer('conv3_block4_out').output])
#     x = Conv2D(64, 3, activation='relu', padding='same')(x)
    
#     x = UpSampling2D()(x)
#     x = concatenate([x, resnet.get_layer('conv2_block3_out').output])
#     x = Conv2D(32, 3, activation='relu', padding='same')(x)
    
#     x = UpSampling2D()(x)
#     x = concatenate([x, resnet.get_layer('conv1_relu').output])
#     x = Conv2D(16, 3, activation='relu', padding='same')(x)
    
#     outputs = Conv2D(1, 1, activation='sigmoid')(x)
    
#     model = Model(inputs=inputs, outputs=outputs)
#     return model

# # Create the model
# input_shape = (256, 256, 3)
# model = unet_resnet50(input_shape)

# # Load the weights
# weights_path = os.path.join(current_dir, "Rooftop_Solar_Energy_Potential_Map", "prev_trained_model", "model_weights_resnet.h5")
# if os.path.exists(weights_path):
#      try:
#         model.load_weights(weights_path)
#         print("Weights loaded successfully")
#      except Exception as e:
#         print(f"Error loading weights: {str(e)}")
#     # model.load_weights(weights_path)
# else:
#     raise FileNotFoundError(f"Weights file not found at {weights_path}")

# def preprocess_image(image_path, target_size=(256, 256)):
#     img = Image.open(image_path)
#     img = img.resize(target_size)
#     img_array = np.array(img)
#     if img_array.shape[-1] == 4:
#         img_array = img_array[..., :3]
#     img_array = img_array / 255.0
#     img_array = np.expand_dims(img_array, axis=0)
#     return img_array

# def post_process_mask(mask):
#     kernel = np.ones((5, 5), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.GaussianBlur(mask, (5, 5), 0)
#     return mask

# def calculate_solar_irradiance(latitude):
#     max_irradiance = 6.0
#     min_irradiance = 2.5
#     irradiance = max_irradiance - (abs(latitude) / 90) * (max_irradiance - min_irradiance)
#     return irradiance

# def calculate_solar_potential(latitude, longitude, area=None, image_path=None):
#     if image_path:
#         # If image path is provided, use image processing
#         preprocessed_image = preprocess_image(image_path)
#         predictions = model.predict(preprocessed_image)
#         binary_mask = (predictions[0, :, :, 0] > 0.45).astype(np.uint8)
#         post_processed_mask = post_process_mask(binary_mask)
#         total_building_area, image_area = calculate_total_area(image_path, post_processed_mask)
#     else:
#         # If no image path, use the provided area
#         total_building_area = area
#         image_area = area  # Assuming the provided area is both total and building area

#     panel_efficiency = 0.20
#     performance_ratio = 0.75
#     daily_irradiance = calculate_solar_irradiance(latitude)
#     annual_irradiance = daily_irradiance * 365
#     solar_potential = (
#         total_building_area *
#         annual_irradiance *
#         panel_efficiency *
#         performance_ratio
#     )
#     solar_potential_mwh = solar_potential / 1000
    
#     return {
#         'solar_potential': solar_potential_mwh,
#         'avg_radiance': daily_irradiance,
#         'total_building_area': total_building_area,
#         'image_area': image_area
#     }


# if __name__ == "__main__":
#     image_path = "path/to/your/image.tif"
#     latitude = 40.7128
#     longitude = -74.0060
#     building_area, image_area, potential = calculate_solar_potential(image_path, latitude, longitude)
#     print(f"Total Building Area: {building_area:.2f} m²")
#     print(f"Total Image Area: {image_area:.2f} m²")
#     print(f"Annual Solar Energy Potential: {potential:.2f} MWh")










import os
import sys

import cv2
import numpy as np
from keras.applications import ResNet50
from keras.layers import Conv2D, Input, MaxPooling2D, UpSampling2D, concatenate
from keras.models import Model
from PIL import Image
from tensorflow import keras

from .area_calculator import calculate_total_area

# Get the absolute path of the current file (solar_potential.py)
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

def unet_resnet50(input_size=(256, 256, 3)):
    inputs = Input(input_size)
    
    # ResNet50 as encoder
    resnet = ResNet50(include_top=False, weights='imagenet', input_tensor=inputs)
    
    # Decoder
    x = Conv2D(256, 3, activation='relu', padding='same')(resnet.output)
    x = UpSampling2D()(x)
    x = concatenate([x, resnet.get_layer('conv4_block6_out').output])
    x = Conv2D(128, 3, activation='relu', padding='same')(x)
    
    x = UpSampling2D()(x)
    x = concatenate([x, resnet.get_layer('conv3_block4_out').output])
    x = Conv2D(64, 3, activation='relu', padding='same')(x)
    
    x = UpSampling2D()(x)
    x = concatenate([x, resnet.get_layer('conv2_block3_out').output])
    x = Conv2D(32, 3, activation='relu', padding='same')(x)
    
    x = UpSampling2D()(x)
    x = concatenate([x, resnet.get_layer('conv1_relu').output])
    x = Conv2D(16, 3, activation='relu', padding='same')(x)
    
    outputs = Conv2D(1, 1, activation='sigmoid')(x)
    
    model = Model(inputs=inputs, outputs=outputs)
    return model

# Create the model
input_shape = (256, 256, 3)
model = unet_resnet50(input_shape)

# New function to load weights partially
def load_weights_partially(model, weights_path):
    model.load_weights(weights_path, by_name=True, skip_mismatch=True)
    print("Weights loaded partially")

# Load the weights
weights_path = os.path.join(current_dir,  "model_weights_resnet.h5")
if os.path.exists(weights_path):
    try:
        load_weights_partially(model, weights_path)
    except Exception as e:
        print(f"Error loading weights: {str(e)}")
else:
    raise FileNotFoundError(f"Weights file not found at {weights_path}")

def preprocess_image(image_path, target_size=(256, 256)):
    img = Image.open(image_path)
    img = img.resize(target_size)
    img_array = np.array(img)
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def post_process_mask(mask):
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    return mask

def calculate_solar_irradiance(latitude):
    max_irradiance = 6.0
    min_irradiance = 2.5
    irradiance = max_irradiance - (abs(latitude) / 90) * (max_irradiance - min_irradiance)
    return irradiance

def calculate_solar_potential(latitude, longitude, area=None, image_path=None):
    if image_path:
        # If image path is provided, use image processing
        preprocessed_image = preprocess_image(image_path)
        predictions = model.predict(preprocessed_image)
        binary_mask = (predictions[0, :, :, 0] > 0.45).astype(np.uint8)
        post_processed_mask = post_process_mask(binary_mask)
        total_building_area, image_area = calculate_total_area(image_path, post_processed_mask)
    else:
        # If no image path, use the provided area
        total_building_area = area
        image_area = area  # Assuming the provided area is both total and building area

    panel_efficiency = 0.20
    performance_ratio = 0.75
    daily_irradiance = calculate_solar_irradiance(latitude)
    annual_irradiance = daily_irradiance * 365
    solar_potential = (
        total_building_area *
        annual_irradiance *
        panel_efficiency *
        performance_ratio
    )
    solar_potential_mwh = solar_potential / 1000
    
    return {
        'solar_potential': solar_potential_mwh,
        'avg_radiance': daily_irradiance,
        'total_building_area': total_building_area,
        'image_area': image_area
    }

if __name__ == "__main__":
    image_path = "path/to/your/image.tif"
    latitude = 40.7128
    longitude = -74.0060
    result = calculate_solar_potential(latitude, longitude, image_path=image_path)
    print(f"Total Building Area: {result['total_building_area']:.2f} m²")
    print(f"Total Image Area: {result['image_area']:.2f} m²")
    print(f"Annual Solar Energy Potential: {result['solar_potential']:.2f} MWh")