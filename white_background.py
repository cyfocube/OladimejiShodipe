from PIL import Image
import numpy as np
import os

def make_background_white(input_path, output_path=None):
    """
    Replace the background of an image with white.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the image with white background
    
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
            output_path = f"{name}_white_bg.png"
        
        print(f"Opening {input_path}...")
        
        # Open the image
        img = Image.open(input_path).convert("RGBA")
        
        print("Creating white background...")
        
        # Create a white background
        white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        
        # Composite the image on the white background
        # This will replace transparent areas with white
        result = Image.alpha_composite(white_bg, img)
        
        # Convert to RGB (removes alpha channel)
        result = result.convert("RGB")
        
        # Save the result
        print(f"Saving image with white background to {output_path}...")
        result.save(output_path, "PNG")
        
        print(f"Successfully created image with white background: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def make_background_white_simple(input_path, output_path=None):
    """
    Simple method to replace background with white using color detection.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the image with white background
    
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
            output_path = f"{name}_white_bg_simple.png"
        
        print(f"Opening {input_path}...")
        
        # Open the image
        img = Image.open(input_path).convert("RGB")
        
        print("Processing background replacement...")
        
        # Convert to numpy array for easier manipulation
        data = np.array(img)
        
        # Sample corners to detect background color
        h, w = data.shape[:2]
        corner_samples = [
            data[0, 0], data[0, w-1], data[h-1, 0], data[h-1, w-1],
            data[5, 5], data[5, w-6], data[h-6, 5], data[h-6, w-6]  # Inner corners
        ]
        
        # Use the most common corner color as background
        bg_color = corner_samples[0]  # Start with first corner
        
        # Create mask for background pixels
        tolerance = 40  # Adjust this value as needed
        mask = np.sqrt(np.sum((data - bg_color) ** 2, axis=2)) < tolerance
        
        # Replace background pixels with white
        data[mask] = [255, 255, 255]  # White
        
        # Create new image
        result_img = Image.fromarray(data, 'RGB')
        
        # Save the result
        print(f"Saving image with white background to {output_path}...")
        result_img.save(output_path, 'PNG')
        
        print(f"Successfully created image with white background: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

if __name__ == "__main__":
    # Make background white for the flipped image
    input_file = "IMG_9089_flipped.png"
    
    # First try the simple method (works well if transparent background already exists)
    if os.path.exists("IMG_9089_flipped_no_bg.png"):
        print("Using the transparent background version...")
        result = make_background_white("IMG_9089_flipped_no_bg.png", "IMG_9089_flipped_white_bg.png")
    else:
        print("Using the original flipped image...")
        result = make_background_white_simple(input_file)
    
    if result:
        print(f"\n✅ Success! Image with white background saved as: {result}")
    else:
        print("\n❌ Failed to create white background image")
