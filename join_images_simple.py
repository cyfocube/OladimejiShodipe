#!/usr/bin/env python3
"""
Simple script to join images horizontally
"""

from PIL import Image
import glob
import os

def join_images_horizontally():
    """Join multiple images horizontally"""
    
    # Find all the specific image files
    screenshot_files = sorted(glob.glob("Screenshot*.png"))
    oig_files = sorted(glob.glob("OIG*.jpeg"))
    
    all_files = screenshot_files + oig_files
    
    print(f"Found {len(all_files)} files:")
    for f in all_files:
        print(f"  - {f}")
    
    if not all_files:
        print("No image files found!")
        return False
    
    try:
        # Open all images
        images = []
        for path in all_files:
            img = Image.open(path)
            images.append(img)
            print(f"Loaded: {path} - Size: {img.size}")
        
        # Get the height of the tallest image
        max_height = max(img.height for img in images)
        print(f"Max height: {max_height}")
        
        # Resize all images to have the same height while maintaining aspect ratio
        resized_images = []
        total_width = 0
        
        for img in images:
            # Calculate new width to maintain aspect ratio
            aspect_ratio = img.width / img.height
            new_width = int(max_height * aspect_ratio)
            
            # Resize image
            resized_img = img.resize((new_width, max_height), Image.Resampling.LANCZOS)
            resized_images.append(resized_img)
            total_width += new_width
            print(f"Resized to: {new_width}x{max_height}")
        
        # Create new image with combined width
        print(f"Creating combined image: {total_width}x{max_height}")
        combined_image = Image.new('RGB', (total_width, max_height), 'white')
        
        # Paste images side by side
        x_offset = 0
        for img in resized_images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # Save the combined image
        output_file = "combined_images_horizontal.png"
        combined_image.save(output_file, 'PNG', quality=95)
        print(f"Successfully created combined image: {output_file}")
        
        # Close all images
        for img in images + resized_images:
            img.close()
        combined_image.close()
        
        return True
        
    except Exception as e:
        print(f"Error processing images: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting image combination process...")
    print(f"Current directory: {os.getcwd()}")
    
    success = join_images_horizontally()
    
    if success:
        print(f"\n✅ Images successfully combined!")
    else:
        print(f"\n❌ Failed to combine images")
