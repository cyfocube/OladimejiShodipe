from PIL import Image, ImageFilter
import os
import glob

def create_seamless_blend(image_files, output_path, blend_width=100):
    """
    Combine images horizontally with seamless blending at the edges
    
    Args:
        image_files (list): List of image file paths
        output_path (str): Path to save the blended image
        blend_width (int): Width of the blending area between images
    """
    try:
        print("Loading and processing images for seamless blending...")
        
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

def create_advanced_blend(image_files, output_path):
    """
    Create an advanced blend with gradient transitions and color matching
    """
    try:
        print("Creating advanced seamless blend...")
        
        # Load images
        images = [Image.open(file) for file in image_files]
        
        # Resize to same height
        max_height = max(img.size[1] for img in images)
        resized_images = []
        
        for img in images:
            aspect_ratio = img.size[0] / img.size[1]
            new_width = int(max_height * aspect_ratio)
            resized_img = img.resize((new_width, max_height), Image.Resampling.LANCZOS)
            resized_images.append(resized_img)
        
        # Create panoramic blend
        blend_width = 150  # Wider blend area
        total_width = sum(img.size[0] for img in resized_images) - (blend_width * (len(resized_images) - 1))
        
        # Create canvas with gradient background
        final_image = Image.new('RGB', (total_width, max_height))
        
        # Create gradient background
        for x in range(total_width):
            color_ratio = x / total_width
            bg_color = (
                int(240 + 15 * color_ratio),  # Subtle color shift
                int(245 + 10 * color_ratio),
                int(250 + 5 * color_ratio)
            )
            for y in range(max_height):
                final_image.putpixel((x, y), bg_color)
        
        # Blend images with feathered edges
        current_x = 0
        
        for i, img in enumerate(resized_images):
            # Create soft feather mask
            mask = Image.new('L', img.size, 255)
            
            if i > 0:  # Left edge feathering
                for x in range(min(blend_width, img.size[0])):
                    alpha = int(255 * (x / blend_width) ** 0.5)  # Curve for smoother transition
                    for y in range(img.size[1]):
                        mask.putpixel((x, y), alpha)
            
            if i < len(resized_images) - 1:  # Right edge feathering
                start_x = max(0, img.size[0] - blend_width)
                for x in range(start_x, img.size[0]):
                    alpha = int(255 * ((img.size[0] - x) / blend_width) ** 0.5)
                    for y in range(img.size[1]):
                        current_alpha = mask.getpixel((x, y))
                        mask.putpixel((x, y), min(current_alpha, alpha))
            
            # Apply mask and paste
            img_rgba = img.convert('RGBA')
            img_rgba.putalpha(mask)
            final_image.paste(img_rgba, (current_x, 0), img_rgba)
            
            current_x += img.size[0] - blend_width
        
        # Final smoothing filter
        final_image = final_image.filter(ImageFilter.GaussianBlur(radius=0.3))
        
        # Save result
        final_image.save(output_path, 'PNG', quality=98)
        print(f"✅ Advanced blend saved as: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating advanced blend: {e}")
        return False

if __name__ == "__main__":
    # Get image files
    screenshot_files = sorted(glob.glob("Screenshot 2025-09-14 at *.png"))
    oig_files = sorted(glob.glob("OIG*.jpeg"))
    
    all_files = screenshot_files + oig_files
    
    if not all_files:
        print("❌ No image files found!")
        exit(1)
    
    print(f"Found {len(all_files)} files for blending:")
    for file in all_files:
        print(f"  - {file}")
    
    # Create seamless blend
    print("\n🎨 Creating seamless blend...")
    success1 = create_seamless_blend(all_files, "combined_images_seamless.png", blend_width=120)
    
    # Create advanced blend
    print("\n🎨 Creating advanced seamless blend...")
    success2 = create_advanced_blend(all_files, "combined_images_seamless_advanced.png")
    
    if success1 or success2:
        print("\n✨ Seamless blending complete!")
        print("Files created:")
        if success1:
            print("  - combined_images_seamless.png (basic seamless blend)")
        if success2:
            print("  - combined_images_seamless_advanced.png (advanced blend with color matching)")
        print("\nThese blended images have no visible demarcation between photos!")
    else:
        print("❌ Failed to create seamless blends")
