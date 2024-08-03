
# Rooftop-Solar-Energy-Potential-Map

The Rooftop Solar Energy Potential Map project is a comprehensive initiative aimed at identifying and visualizing the potential for solar energy generation on rooftops within a specific geographic area.

 By leveraging advanced geospatial analysis and data-driven modeling, the project creates automatic solar energy consumption for the specific geographical area helping government decide where to plant solar planels 

 


## Screenshots

![App Screenshot](https://iili.io/dR03Ux4.jpg)
![App Screenshot](https://iili.io/dR0Fmps.jpg)
![App Screenshot](https://iili.io/dR0KgFS.jpg)

## Project Overview

This project leverages advanced machine learning models and geospatial analysis to address two key objectives:
1. **Building Footprint Extraction**: Detect and delineate building footprints from satellite images using a sophisticated ResNet50-U-Net model.
2. **Solar Energy Estimation**: Calculate potential solar energy generation based on solar radiance data and user-defined parameters.

## Files and Notebooks

### 1. `README.md`
This document provides an overview of the repository, explains the purpose of each file, and outlines setup and usage instructions.

### 2. `area_finder.ipynb`
**Purpose**: This Jupyter Notebook calculates the real-world area of buildings from model predictions.
- **Process**: 
  - Extract geographic coordinates for the building’s bounding box.
  - Calculate the pixel-to-world conversion factor based on geographic coordinates and image resolution.
  - Use the conversion factor to determine the area of each building in square meters.
### Building Area Calculation Formula

To calculate the area of each building detected by the model, use the following formula:

##### Building Area (m²) = (Pixel Area (m²) / Conversion Factor) × Number of Pixels

#### Explanation:
- **Pixel Area (m²)**: The area represented by a single pixel in square meters.
- **Conversion Factor**: The ratio of real-world dimensions (latitude and longitude) to pixel dimensions, determined using geographic coordinates and image resolution.
- **Number of Pixels**: The total count of pixels within the building's footprint as predicted by the model.

### Steps for Calculation:
1. **Extract Geographic Coordinates**: Use the coordinates provided by the user to define the area covered by the image.
2. **Determine Conversion Factor**: Calculate the conversion factor by relating real-world distances (latitude and longitude) to pixel dimensions in the image.
3. **Calculate Building Area**:
   - Find the pixel area for the building using the conversion factor.
   - Multiply the pixel area by the number of pixels that represent the building footprint to get the total building area in square meters.

This method ensures accurate area calculations by integrating geographic and pixel-based information, providing a precise measurement of each building's footprint in real-world units.



### 3. `create_mask.ipynb`
**Purpose**: Generate binary masks from satellite images for model training.
- **Process**: Creates masks highlighting building footprints, which are then used to train the model.
- **Output**: Binary masks where buildings are marked in white on a black background.

### 4. `model_architecture_resnet.json`
**Purpose**: Contains the JSON file detailing the architecture of the ResNet50-U-Net model.
- **Details**: Provides specifications of layers, activations, and connections used in the model.


### 5. `model_resnet.ipynb`
**Purpose**: Train the ResNet50-U-Net model for building footprint extraction.
- **Process**: Implements and trains the model on the dataset, evaluates its performance, and saves the trained model.
- **Model**: Combines ResNet50 as the encoder with a U-Net decoder to handle segmentation tasks.

![App Screenshot](https://iili.io/dR0B4SI.png)

### 6. `prediction.ipynb`
**Purpose**: Generate predictions using the trained ResNet50-U-Net model.
- **Process**: Uses the trained model to predict building footprints on new satellite images, applies post-processing to refine results.

### 7. `split_folders.ipynb`
**Purpose**: Organize and split the dataset into training and validation sets.
- **Process**: Ensures that data is properly divided for model training and evaluation, facilitating better model performance and validation.

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Install Dependencies**:
    Ensure Python 3.x is installed. Use the following command to install required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. **Jupyter Notebooks**:
    Launch Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
    Open and execute the notebooks in the following sequence for a complete workflow:
    - `split_folders.ipynb`
    - `create_mask.ipynb`
    - `automatic_tif_converter.ipynb`
    - `model_resnet.ipynb`
    - `prediction.ipynb`
    - `area_finder.ipynb`

4. **Make Changes to Data2 folder as shown**:
   
    ![App Screenshot](https://iili.io/dR0aoCB.png)
    

## Model Overview

### ResNet50-U-Net Architecture
- **Encoder**: ResNet50 extracts hierarchical features from input images.
- **Decoder**: U-Net uses these features to reconstruct segmentation masks, capturing detailed building footprints.

### Performance
- **Validation Accuracy**: 95.21%
- **Mean IoU Before Post-Processing**: 0.85
- **Mean IoU After Post-Processing**: 0.92

## Area Calculation

1. **Extract Coordinates**: From user inputs, determine the geographic bounds of the image area.
2. **Calculate Conversion Factor**: Convert pixel dimensions to real-world measurements using the geographic bounds.
3. **Compute Area**: Multiply the number of pixels detected in each building by the conversion factor to obtain the real-world area.

## Usage

- **Data Preparation**: Use `split_folders.ipynb` to organize your dataset. Generate masks using `create_mask.ipynb`.
- **Model Training**: Train the ResNet50-U-Net model with `model_resnet.ipynb`.
- **Prediction and Post-Processing**: Predict building footprints and refine results using `prediction.ipynb`. Calculate building areas with `area_finder.ipynb`.

## Notes

- Ensure that file paths and directories are correctly configured in the notebooks.
- Review `model_architecture_resnet.json` for detailed model architecture information.

For issues or contributions, please open an issue or pull request on the repository.

---



