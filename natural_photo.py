from PIL import Image
import os

def add_natural_padding(input_path, output_path=None, padding_percent=15):
    """
    Add white padding around an image to make it look like a natural photo.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the padded image
        padding_percent (int): Percentage of image size to add as padding
    
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
            output_path = f"{name}_natural.png"
        
        print(f"Opening {input_path}...")
        
        # Open the image
        img = Image.open(input_path)
        
        # Convert to RGB if it has transparency
        if img.mode in ('RGBA', 'LA'):
            # Create white background
            white_bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                white_bg.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            else:
                white_bg.paste(img)
            img = white_bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        print("Adding natural padding...")
        
        # Calculate padding
        original_width, original_height = img.size
        padding_w = int(original_width * padding_percent / 100)
        padding_h = int(original_height * padding_percent / 100)
        
        # Create new image with white background and padding
        new_width = original_width + (padding_w * 2)
        new_height = original_height + (padding_h * 2)
        
        # Create white canvas
        padded_img = Image.new('RGB', (new_width, new_height), (255, 255, 255))
        
        # Paste the original image in the center
        paste_x = padding_w
        paste_y = padding_h
        padded_img.paste(img, (paste_x, paste_y))
        
        # Save the result
        print(f"Saving natural-looking image to {output_path}...")
        padded_img.save(output_path, 'PNG')
        
        print(f"Successfully created natural-looking image: {output_path}")
        print(f"Original size: {original_width}x{original_height}")
        print(f"New size: {new_width}x{new_height}")
        print(f"Added {padding_w}px horizontal and {padding_h}px vertical padding")
        
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def create_photo_style(input_path, output_path=None):
    """
    Create a more photo-like version with generous white space around the subject.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the photo-style image
    
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
            output_path = f"{name}_photo_style.png"
        
        print(f"Opening {input_path}...")
        
        # Open the image
        img = Image.open(input_path)
        
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA'):
            white_bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                white_bg.paste(img, mask=img.split()[-1])
            else:
                white_bg.paste(img)
            img = white_bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        print("Creating photo-style layout...")
        
        # Calculate dimensions for a more natural photo look
        original_width, original_height = img.size
        
        # Add more generous padding (25% on each side)
        padding_percent = 25
        padding_w = int(original_width * padding_percent / 100)
        padding_h = int(original_height * padding_percent / 100)
        
        # Create even more spacious canvas
        new_width = original_width + (padding_w * 2)
        new_height = original_height + (padding_h * 2)
        
        # Create white canvas
        photo_img = Image.new('RGB', (new_width, new_height), (255, 255, 255))
        
        # Center the image
        paste_x = padding_w
        paste_y = padding_h
        photo_img.paste(img, (paste_x, paste_y))
        
        # Save the result
        print(f"Saving photo-style image to {output_path}...")
        photo_img.save(output_path, 'PNG')
        
        print(f"Successfully created photo-style image: {output_path}")
        print(f"Original size: {original_width}x{original_height}")
        print(f"New size: {new_width}x{new_height}")
        
        return output_path
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

if __name__ == "__main__":
    # Create natural-looking photo from the white background version
    input_file = "IMG_9089_flipped_white_bg.png"
    
    if not os.path.exists(input_file):
        input_file = "IMG_9089_flipped.png"
        print(f"Using {input_file} as input...")
    
    # Create both versions
    print("Creating natural padding version (15% padding)...")
    result1 = add_natural_padding(input_file, "IMG_9089_natural.png", 15)
    
    print("\nCreating photo-style version (25% padding)...")
    result2 = create_photo_style(input_file, "IMG_9089_photo_style.png")
    
    if result1 and result2:
        print(f"\n✅ Success! Created two versions:")
        print(f"   Natural padding: {result1}")
        print(f"   Photo style: {result2}")
        print("\nYou can choose which one looks better!")
    else:
        print("\n❌ Failed to create natural-looking images")
