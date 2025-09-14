from PIL import Image, ImageChops
import numpy as np
import os

def auto_crop_whitespace(input_path, output_path=None, padding=20):
    """
    Automatically crop white space from an image while keeping some padding.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the cropped image
        padding (int): Pixels of white space to keep around the content
    
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
            output_path = f"{name}_cropped.png"
        
        print(f"Opening {input_path}...")
        
        # Open the image
        img = Image.open(input_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        print("Detecting content boundaries...")
        
        # Create a white image of the same size
        white_bg = Image.new('RGB', img.size, (255, 255, 255))
        
        # Find difference between image and white background
        diff = ImageChops.difference(img, white_bg)
        
        # Convert to grayscale and get bounding box
        diff = diff.convert('L')
        
        # Get bounding box of non-white content
        bbox = diff.getbbox()
        
        if bbox is None:
            print("No content found - image appears to be all white")
            return None
        
        # Expand bounding box by padding
        left, top, right, bottom = bbox
        
        # Add padding but don't go outside image bounds
        left = max(0, left - padding)
        top = max(0, top - padding)
        right = min(img.width, right + padding)
        bottom = min(img.height, bottom + padding)
        
        print(f"Original size: {img.width}x{img.height}")
        print(f"Content found at: {bbox}")
        print(f"Cropping to: {left}, {top}, {right}, {bottom}")
        print(f"New size: {right-left}x{bottom-top}")
        
        # Crop the image
        cropped_img = img.crop((left, top, right, bottom))
        
        # Save the result
        print(f"Saving cropped image to {output_path}...")
        cropped_img.save(output_path, 'PNG')
        
        print(f"Successfully cropped image: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def smart_crop_edges(input_path, output_path=None, margin_percent=5):
    """
    Smart crop that removes excess white space but keeps natural margins.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the cropped image
        margin_percent (int): Percentage of content size to keep as margin
    
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
            output_path = f"{name}_smart_crop.png"
        
        print(f"Opening {input_path}...")
        
        # Open the image and convert to numpy array
        img = Image.open(input_path).convert('RGB')
        img_array = np.array(img)
        
        print("Analyzing image content...")
        
        # Define white threshold (allow for slight variations)
        white_threshold = 250
        
        # Find non-white pixels
        non_white = (img_array[:, :, 0] < white_threshold) | \
                   (img_array[:, :, 1] < white_threshold) | \
                   (img_array[:, :, 2] < white_threshold)
        
        # Find bounding box of content
        rows = np.any(non_white, axis=1)
        cols = np.any(non_white, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            print("No content found")
            return None
        
        # Get content boundaries
        top, bottom = np.where(rows)[0][[0, -1]]
        left, right = np.where(cols)[0][[0, -1]]
        
        # Calculate content dimensions
        content_width = right - left
        content_height = bottom - top
        
        # Calculate margins based on content size
        margin_w = int(content_width * margin_percent / 100)
        margin_h = int(content_height * margin_percent / 100)
        
        # Apply margins but stay within image bounds
        crop_left = max(0, left - margin_w)
        crop_top = max(0, top - margin_h)
        crop_right = min(img.width, right + margin_w)
        crop_bottom = min(img.height, bottom + margin_h)
        
        print(f"Original size: {img.width}x{img.height}")
        print(f"Content area: {left}-{right}, {top}-{bottom}")
        print(f"Cropping to: {crop_left}-{crop_right}, {crop_top}-{crop_bottom}")
        print(f"New size: {crop_right-crop_left}x{crop_bottom-crop_top}")
        
        # Crop the image
        cropped_img = img.crop((crop_left, crop_top, crop_right, crop_bottom))
        
        # Save the result
        print(f"Saving smart-cropped image to {output_path}...")
        cropped_img.save(output_path, 'PNG')
        
        print(f"Successfully created smart-cropped image: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

if __name__ == "__main__":
    # Crop the natural photo versions to remove excess white space
    
    # Try both natural versions
    input_files = ["IMG_9089_natural.png", "IMG_9089_photo_style.png"]
    
    for input_file in input_files:
        if os.path.exists(input_file):
            print(f"\n{'='*50}")
            print(f"Processing: {input_file}")
            print(f"{'='*50}")
            
            # Create output filename
            name, ext = os.path.splitext(input_file)
            
            # Auto crop with minimal padding
            print("\n1. Auto-cropping with minimal padding...")
            auto_result = auto_crop_whitespace(input_file, f"{name}_auto_crop.png", padding=30)
            
            # Smart crop with proportional margins
            print("\n2. Smart cropping with proportional margins...")
            smart_result = smart_crop_edges(input_file, f"{name}_smart_crop.png", margin_percent=8)
            
            if auto_result and smart_result:
                print(f"\n✅ Success for {input_file}!")
                print(f"   Auto crop: {auto_result}")
                print(f"   Smart crop: {smart_result}")
            else:
                print(f"\n❌ Failed to process {input_file}")
        else:
            print(f"File not found: {input_file}")
    
    print(f"\n{'='*50}")
    print("Cropping complete! You now have multiple options to choose from.")
