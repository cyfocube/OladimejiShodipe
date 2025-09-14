#!/usr/bin/env python3
"""
Script to join multiple images horizontally
"""

from PIL import Image
import os

def join_images_horizontally(image_paths, output_path):
    """Join multiple images horizontally"""
    
    # Check if all files exist
    for path in image_paths:
        if not os.path.exists(path):
            print(f"Error: File not found - {path}")
            return False
    
    try:
        # Open all images
        images = []
        for path in image_paths:
            img = Image.open(path)
            images.append(img)
            print(f"Loaded: {path} - Size: {img.size}")
        
        # Get the height of the tallest image
        max_height = max(img.height for img in images)
        
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
        combined_image = Image.new('RGB', (total_width, max_height), 'white')
        
        # Paste images side by side
        x_offset = 0
        for img in resized_images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # Save the combined image
        combined_image.save(output_path, 'PNG', quality=95)
        print(f"Successfully created combined image: {output_path}")
        print(f"Final size: {total_width}x{max_height}")
        
        # Close all images
        for img in images + resized_images:
            img.close()
        combined_image.close()
        
        return True
        
    except Exception as e:
        print(f"Error processing images: {str(e)}")
        return False

if __name__ == "__main__":
    # List of image files to join
    image_files = [
        "./Screenshot 2025-09-14 at 12.34.00 AM.png",
        "./Screenshot 2025-09-14 at 12.33.13 AM.png", 
        "./Screenshot 2025-09-14 at 12.32.22 AM.png",
        "./OIG2.XzWwD1jQtvXf_J.3nnd2.jpeg",
        "./OIG3.Lvr9EzPA43yHSRCiATCz.jpeg",
        "./OIG4.krim_Up00g7mdIGo8JRH.jpeg"
    ]
    
    output_file = "combined_images_horizontal.png"
    
    print("Starting image combination process...")
    print(f"Images to combine: {len(image_files)}")
    print(f"Current directory: {os.getcwd()}")
    
    success = join_images_horizontally(image_files, output_file)
    
    if success:
        print(f"\n✅ Images successfully combined into: {output_file}")
    else:
        print(f"\n❌ Failed to combine images")
