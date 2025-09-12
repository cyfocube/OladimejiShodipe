#!/usr/bin/env python3
"""
Script to create faded versions of images
Creates light, medium, and heavy fade versions of specified images
"""

from PIL import Image, ImageEnhance
import os

def create_faded_image(input_path, output_path, opacity=0.6, brightness=1.1):
    """
    Create a faded version of an image
    
    Args:
        input_path: Path to the original image
        output_path: Path where faded image will be saved
        opacity: Opacity level (0.0 to 1.0)
        brightness: Brightness adjustment (1.0 = original)
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Adjust brightness
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
            
            # Create a white overlay for fade effect
            overlay = Image.new('RGBA', img.size, (255, 255, 255, int(255 * (1 - opacity))))
            
            # Composite the images
            faded_img = Image.alpha_composite(img, overlay)
            
            # Save the result
            faded_img.save(output_path, 'PNG')
            print(f"Created faded image: {output_path}")
            
    except FileNotFoundError:
        print(f"Error: Could not find image file {input_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def main():
    """Main function to create faded versions of specified images"""
    
    # List of images to process
    images = [
        'climate1.png',
        'photo_graph.png', 
        'photo_graph2.png'
    ]
    
    # Fade configurations: (suffix, opacity, brightness)
    fade_configs = [
        ('_faded_light', 0.8, 1.1),
        ('_faded_medium', 0.6, 1.05),
        ('_faded_heavy', 0.4, 1.1)
    ]
    
    for image_file in images:
        if os.path.exists(image_file):
            print(f"\nProcessing {image_file}...")
            
            # Get the base name without extension
            base_name = os.path.splitext(image_file)[0]
            
            # Create different fade versions
            for suffix, opacity, brightness in fade_configs:
                output_file = f"{base_name}{suffix}.png"
                create_faded_image(image_file, output_file, opacity, brightness)
        else:
            print(f"Warning: {image_file} not found in current directory")
    
    print("\nFaded image creation completed!")
    print("\nCSS classes have been added to styles.css:")
    print("- .faded-light (80% opacity)")
    print("- .faded-medium (60% opacity)")  
    print("- .faded-heavy (40% opacity)")
    print("- .faded-image (60% opacity with hover effect)")
    print("- .fade-overlay (gradient overlay effect)")

if __name__ == "__main__":
    main()
