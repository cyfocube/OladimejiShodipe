#!/usr/bin/env python3
"""
Script to flip IMG_9089.HEIC horizontally so the person looks to the right
"""

from PIL import Image
import pillow_heif
import os

# Register HEIF opener with pillow
pillow_heif.register_heif_opener()

def flip_photo_horizontally(input_path, output_path=None):
    """
    Flip a photo horizontally (left to right).
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the flipped image (optional)
    
    Returns:
        str: Path to the output image
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # If no output path specified, create one
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            # Convert HEIC to PNG for web compatibility
            if ext.lower() == '.heic':
                output_path = f"{name}_flipped.png"
            else:
                output_path = f"{name}_flipped{ext}"
        
        print(f"Opening {input_path}...")
        # Open the image
        with Image.open(input_path) as img:
            # Flip horizontally using transpose
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            
            # Save the flipped image
            print(f"Saving flipped image to {output_path}...")
            flipped_img.save(output_path)
            
        print(f"Successfully created flipped image: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        print("Make sure you have Pillow and pillow-heif installed: pip install Pillow pillow-heif")
        return None

if __name__ == "__main__":
    # Flip the IMG_9089.HEIC image
    input_file = "IMG_9089.HEIC"
    result = flip_photo_horizontally(input_file)
    
    if result:
        print(f"\n✅ Success! Flipped image saved as: {result}")
    else:
        print("\n❌ Failed to flip image")
