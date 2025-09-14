from PIL import Image
import numpy as np
from rembg import remove
import os

def remove_background_rembg(input_path, output_path=None):
    """
    Remove background from an image using rembg library.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the image with transparent background
    
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
            output_path = f"{name}_no_bg.png"
        
        print(f"Opening {input_path}...")
        
        # Read the input image
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
        
        print("Removing background...")
        # Remove background using rembg
        output_data = remove(input_data)
        
        # Save the result
        print(f"Saving image with transparent background to {output_path}...")
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        print(f"Successfully created image with transparent background: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        print("Make sure you have rembg installed: pip install rembg")
        return None

def remove_background_manual(input_path, output_path=None):
    """
    Remove background manually using color-based segmentation (fallback method).
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the image with transparent background
    
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
            output_path = f"{name}_no_bg_manual.png"
        
        print(f"Opening {input_path}...")
        
        # Open the image
        img = Image.open(input_path).convert("RGBA")
        
        print("Processing background removal (manual method)...")
        
        # Convert to numpy array for easier manipulation
        data = np.array(img)
        
        # Create a mask for the background (this is a simple approach)
        # We'll assume the background is relatively uniform
        # Sample the corners to get background color
        h, w = data.shape[:2]
        corner_samples = [
            data[0, 0], data[0, w-1], data[h-1, 0], data[h-1, w-1]
        ]
        
        # Use the most common corner color as background
        bg_color = corner_samples[0][:3]  # RGB only
        
        # Create mask based on color similarity
        tolerance = 30  # Adjust this value as needed
        mask = np.sqrt(np.sum((data[:, :, :3] - bg_color) ** 2, axis=2)) < tolerance
        
        # Set background pixels to transparent
        data[mask] = [0, 0, 0, 0]  # Transparent
        
        # Create new image
        result_img = Image.fromarray(data, 'RGBA')
        
        # Save the result
        print(f"Saving image with transparent background to {output_path}...")
        result_img.save(output_path, 'PNG')
        
        print(f"Successfully created image with transparent background: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

if __name__ == "__main__":
    # Remove background from the flipped image
    input_file = "IMG_9089_flipped.png"
    
    # Try rembg first (AI-based background removal)
    print("Attempting AI-based background removal...")
    result = remove_background_rembg(input_file)
    
    if not result:
        print("\nAI method failed, trying manual method...")
        result = remove_background_manual(input_file)
    
    if result:
        print(f"\n✅ Success! Image with transparent background saved as: {result}")
    else:
        print("\n❌ Failed to remove background")
