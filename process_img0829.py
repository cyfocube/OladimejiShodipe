from PIL import Image
import pillow_heif
import os
from rembg import remove

# Register HEIF opener with pillow
pillow_heif.register_heif_opener()

def process_heic_photo(input_path, output_prefix="processed"):
    """
    Complete processing pipeline for HEIC photos:
    1. Flip horizontally to face right
    2. Remove background
    3. Add white background
    4. Crop excess white space
    
    Args:
        input_path (str): Path to the input HEIC image
        output_prefix (str): Prefix for output filenames
    
    Returns:
        dict: Dictionary with paths to all generated versions
    """
    results = {}
    
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        print(f"Processing {input_path}...")
        print("="*60)
        
        # Step 1: Flip the image horizontally
        print("Step 1: Flipping image horizontally...")
        flipped_path = flip_image_horizontal(input_path, f"{output_prefix}_flipped.png")
        if flipped_path:
            results['flipped'] = flipped_path
            print(f"✅ Flipped image saved: {flipped_path}")
        else:
            print("❌ Failed to flip image")
            return results
        
        # Step 2: Remove background
        print("\nStep 2: Removing background...")
        no_bg_path = remove_background_ai(flipped_path, f"{output_prefix}_no_bg.png")
        if no_bg_path:
            results['no_background'] = no_bg_path
            print(f"✅ Background removed: {no_bg_path}")
        else:
            print("❌ Failed to remove background")
            return results
        
        # Step 3: Add white background
        print("\nStep 3: Adding white background...")
        white_bg_path = add_white_background(no_bg_path, f"{output_prefix}_white_bg.png")
        if white_bg_path:
            results['white_background'] = white_bg_path
            print(f"✅ White background added: {white_bg_path}")
        else:
            print("❌ Failed to add white background")
            return results
        
        # Step 4: Crop excess white space
        print("\nStep 4: Cropping excess white space...")
        cropped_path = smart_crop_photo(white_bg_path, f"{output_prefix}_final.png")
        if cropped_path:
            results['final'] = cropped_path
            print(f"✅ Final cropped image: {cropped_path}")
        else:
            print("❌ Failed to crop image")
        
        print("\n" + "="*60)
        print("✅ Processing complete!")
        return results
        
    except Exception as e:
        print(f"Error in processing pipeline: {e}")
        return results

def flip_image_horizontal(input_path, output_path):
    """Flip image horizontally."""
    try:
        with Image.open(input_path) as img:
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            flipped_img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error flipping image: {e}")
        return None

def remove_background_ai(input_path, output_path):
    """Remove background using AI."""
    try:
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
        
        output_data = remove(input_data)
        
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        return output_path
    except Exception as e:
        print(f"Error removing background: {e}")
        return None

def add_white_background(input_path, output_path):
    """Add white background to transparent image."""
    try:
        img = Image.open(input_path).convert("RGBA")
        white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        result = Image.alpha_composite(white_bg, img)
        result = result.convert("RGB")
        result.save(output_path, "PNG")
        return output_path
    except Exception as e:
        print(f"Error adding white background: {e}")
        return None

def smart_crop_photo(input_path, output_path, margin_percent=8):
    """Smart crop to remove excess white space."""
    try:
        import numpy as np
        
        img = Image.open(input_path).convert('RGB')
        img_array = np.array(img)
        
        # Find non-white pixels
        white_threshold = 250
        non_white = (img_array[:, :, 0] < white_threshold) | \
                   (img_array[:, :, 1] < white_threshold) | \
                   (img_array[:, :, 2] < white_threshold)
        
        # Find bounding box of content
        rows = np.any(non_white, axis=1)
        cols = np.any(non_white, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            print("No content found for cropping")
            return None
        
        # Get content boundaries
        top, bottom = np.where(rows)[0][[0, -1]]
        left, right = np.where(cols)[0][[0, -1]]
        
        # Calculate margins
        content_width = right - left
        content_height = bottom - top
        margin_w = int(content_width * margin_percent / 100)
        margin_h = int(content_height * margin_percent / 100)
        
        # Apply margins
        crop_left = max(0, left - margin_w)
        crop_top = max(0, top - margin_h)
        crop_right = min(img.width, right + margin_w)
        crop_bottom = min(img.height, bottom + margin_h)
        
        # Crop and save
        cropped_img = img.crop((crop_left, crop_top, crop_right, crop_bottom))
        cropped_img.save(output_path, 'PNG')
        
        print(f"Cropped from {img.width}x{img.height} to {crop_right-crop_left}x{crop_bottom-crop_top}")
        
        return output_path
    except Exception as e:
        print(f"Error cropping image: {e}")
        return None

if __name__ == "__main__":
    # Process IMG_0829.HEIC
    input_file = "IMG_0829.HEIC"
    
    if os.path.exists(input_file):
        results = process_heic_photo(input_file, "IMG_0829")
        
        if results:
            print(f"\n🎉 Successfully processed {input_file}!")
            print("\nGenerated files:")
            for step, path in results.items():
                print(f"   {step}: {path}")
            
            if 'final' in results:
                print(f"\n⭐ Recommended final image: {results['final']}")
        else:
            print(f"\n❌ Failed to process {input_file}")
    else:
        print(f"❌ File not found: {input_file}")
        print("Available HEIC files:")
        heic_files = [f for f in os.listdir('.') if f.lower().endswith('.heic')]
        for f in heic_files:
            print(f"   {f}")
