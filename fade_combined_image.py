from PIL import Image, ImageEnhance
import os

def fade_image(input_path, output_path, opacity=0.7):
    """
    Apply a fade effect to an image by reducing its opacity
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the faded image
        opacity (float): Opacity level (0.0 = transparent, 1.0 = fully opaque)
    """
    try:
        # Open the combined image
        print(f"Loading image: {input_path}")
        image = Image.open(input_path)
        
        # Convert to RGBA if not already (to support transparency)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Create a transparent overlay
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        
        # Apply opacity to the original image
        faded_image = Image.blend(overlay, image, opacity)
        
        # Save the faded image
        faded_image.save(output_path, 'PNG')
        print(f"✅ Faded image saved as: {output_path}")
        print(f"Applied opacity: {opacity} (0.0 = transparent, 1.0 = opaque)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return False

if __name__ == "__main__":
    # Input and output file paths
    input_file = "combined_images_horizontal.png"
    output_file = "combined_images_horizontal_faded.png"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        exit(1)
    
    print("Creating faded version of combined image...")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    
    # Apply fade effect (0.6 = 60% opacity for a nice subtle fade)
    success = fade_image(input_file, output_file, opacity=0.6)
    
    if success:
        print("\n🎨 Fade effect applied successfully!")
        print("You can adjust the opacity by changing the value in the script:")
        print("  - 0.3 = Very faded (30% opacity)")
        print("  - 0.5 = Medium fade (50% opacity)")
        print("  - 0.6 = Light fade (60% opacity)")
        print("  - 0.8 = Subtle fade (80% opacity)")
    else:
        print("❌ Failed to apply fade effect")
