from PIL import Image, ImageFilter
import os
import glob

def create_seamless_blend_all(image_files, output_path, blend_width=100):
    """
    Combine all images horizontally with seamless blending at the edges
    
    Args:
        image_files (list): List of image file paths
        output_path (str): Path to save the blended image
        blend_width (int): Width of the blending area between images
    """
    try:
        print("Loading and processing ALL images for seamless blending...")
        
        # Load all images
        images = []
        for file in image_files:
            img = Image.open(file)
            print(f"Loaded: {os.path.basename(file)} - Size: {img.size}")
            images.append(img)
        
        if not images:
            print("No images found!")
            return False
        
        # Find the maximum height
        max_height = max(img.size[1] for img in images)
        print(f"Target height: {max_height}")
        
        # Resize all images to the same height while maintaining aspect ratio
        resized_images = []
        for img in images:
            aspect_ratio = img.size[0] / img.size[1]
            new_width = int(max_height * aspect_ratio)
            resized_img = img.resize((new_width, max_height), Image.Resampling.LANCZOS)
            resized_images.append(resized_img)
            print(f"Resized to: {new_width}x{max_height}")
        
        # Calculate total width accounting for blend overlap
        total_width = sum(img.size[0] for img in resized_images) - (blend_width * (len(resized_images) - 1))
        print(f"Total blended width: {total_width}x{max_height}")
        
        # Create the final canvas
        final_image = Image.new('RGB', (total_width, max_height), (255, 255, 255))
        
        # Paste images with blending
        current_x = 0
        
        for i, img in enumerate(resized_images):
            if i == 0:
                # First image - paste normally
                final_image.paste(img, (current_x, 0))
                current_x += img.size[0] - blend_width
            else:
                # Subsequent images - create blend mask
                blend_mask = Image.new('L', img.size, 255)
                
                # Create gradient for left edge blending
                for x in range(min(blend_width, img.size[0])):
                    alpha = int(255 * (x / blend_width))
                    for y in range(img.size[1]):
                        blend_mask.putpixel((x, y), alpha)
                
                # Convert image to RGBA for blending
                img_rgba = img.convert('RGBA')
                img_rgba.putalpha(blend_mask)
                
                # Paste with blend
                final_image.paste(img_rgba, (current_x, 0), img_rgba)
                current_x += img.size[0] - blend_width
        
        # Apply subtle overall smoothing
        final_image = final_image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Save the result
        final_image.save(output_path, 'PNG', quality=95)
        print(f"✅ Seamlessly blended image saved as: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating blend: {e}")
        return False

if __name__ == "__main__":
    # Get all image files including the new ones
    screenshot_files = sorted(glob.glob("Screenshot 2025-09-14 at *.png"))
    
    # Include all OIG files, including the new ones
    all_oig_files = sorted(glob.glob("OIG*.jpeg"))
    
    all_files = screenshot_files + all_oig_files
    
    if not all_files:
        print("❌ No image files found!")
        exit(1)
    
    print(f"Found {len(all_files)} files for blending:")
    for file in all_files:
        print(f"  - {file}")
    
    # Create seamless blend with all images
    print("\n🎨 Creating seamless blend with ALL images...")
    success = create_seamless_blend_all(all_files, "combined_images_seamless_all.png", blend_width=120)
    
    if success:
        print("\n✨ Complete seamless blending finished!")
        print("File created: combined_images_seamless_all.png")
        print("This includes all screenshots and ALL OIG images with seamless transitions!")
    else:
        print("❌ Failed to create complete seamless blend")
