#!/usr/bin/env python3
"""
Script to create horizontal scrolling background images for menu section
Combines faded versions side by side and creates multiple copies for seamless scrolling
"""

from PIL import Image
import os

def create_horizontal_strip(base_name, menu_height=70):
    """
    Create a horizontal strip combining light, medium, heavy faded versions
    
    Args:
        base_name: Base name of the image (without extension)
        menu_height: Height of the menu container in pixels
    """
    try:
        # Load the three faded versions
        light_img = Image.open(f"{base_name}_faded_light.png")
        medium_img = Image.open(f"{base_name}_faded_medium.png") 
        heavy_img = Image.open(f"{base_name}_faded_heavy.png")
        
        # Resize all images to match menu height while maintaining aspect ratio
        def resize_to_height(img, target_height):
            aspect_ratio = img.width / img.height
            new_width = int(target_height * aspect_ratio)
            return img.resize((new_width, target_height), Image.Resampling.LANCZOS)
        
        light_resized = resize_to_height(light_img, menu_height)
        medium_resized = resize_to_height(medium_img, menu_height)
        heavy_resized = resize_to_height(heavy_img, menu_height)
        
        # Calculate total width
        total_width = light_resized.width + medium_resized.width + heavy_resized.width
        
        # Create the combined horizontal strip
        strip = Image.new('RGBA', (total_width, menu_height), (255, 255, 255, 0))
        
        # Paste images side by side
        x_offset = 0
        strip.paste(light_resized, (x_offset, 0))
        x_offset += light_resized.width
        strip.paste(medium_resized, (x_offset, 0))
        x_offset += medium_resized.width
        strip.paste(heavy_resized, (x_offset, 0))
        
        # Save the single strip
        strip_filename = f"{base_name}_menu_strip.png"
        strip.save(strip_filename, 'PNG')
        print(f"Created menu strip: {strip_filename}")
        
        return strip, total_width
        
    except Exception as e:
        print(f"Error creating strip for {base_name}: {str(e)}")
        return None, 0

def create_scrolling_background(base_name, strip_img, strip_width, menu_height=70, total_copies=5):
    """
    Create a long horizontal image with multiple copies for seamless scrolling
    
    Args:
        base_name: Base name of the image
        strip_img: The single strip image
        strip_width: Width of a single strip
        menu_height: Height of the menu
        total_copies: Number of copies to create for seamless scrolling
    """
    try:
        # Create a long image with multiple copies
        scroll_width = strip_width * total_copies
        scroll_bg = Image.new('RGBA', (scroll_width, menu_height), (255, 255, 255, 0))
        
        # Paste multiple copies side by side
        for i in range(total_copies):
            x_position = i * strip_width
            scroll_bg.paste(strip_img, (x_position, 0))
        
        # Save the scrolling background
        scroll_filename = f"{base_name}_menu_scroll_bg.png"
        scroll_bg.save(scroll_filename, 'PNG')
        print(f"Created scrolling background: {scroll_filename}")
        
        return scroll_filename
        
    except Exception as e:
        print(f"Error creating scrolling background for {base_name}: {str(e)}")
        return None

def create_combined_scroll_background(menu_height=70):
    """
    Create a combined scrolling background using all three images
    """
    try:
        # Load all individual strips
        climate_strip = Image.open("climate1_menu_strip.png")
        photo1_strip = Image.open("photo_graph_menu_strip.png")
        photo2_strip = Image.open("photo_graph2_menu_strip.png")
        
        # Calculate total width for one complete cycle
        total_width = climate_strip.width + photo1_strip.width + photo2_strip.width
        
        # Create multiple copies for smooth scrolling (3 complete cycles)
        scroll_width = total_width * 3
        combined_bg = Image.new('RGBA', (scroll_width, menu_height), (255, 255, 255, 0))
        
        # Paste the pattern multiple times
        for cycle in range(3):
            x_offset = cycle * total_width
            
            # Climate strip
            combined_bg.paste(climate_strip, (x_offset, 0))
            x_offset += climate_strip.width
            
            # Photo graph 1 strip  
            combined_bg.paste(photo1_strip, (x_offset, 0))
            x_offset += photo1_strip.width
            
            # Photo graph 2 strip
            combined_bg.paste(photo2_strip, (x_offset, 0))
        
        # Save the combined scrolling background
        combined_filename = "menu_combined_scroll_bg.png"
        combined_bg.save(combined_filename, 'PNG')
        print(f"Created combined scrolling background: {combined_filename}")
        
        return combined_filename, total_width
        
    except Exception as e:
        print(f"Error creating combined background: {str(e)}")
        return None, 0

def main():
    """Main function to create all scrolling backgrounds"""
    
    print("Creating horizontal scrolling backgrounds for menu section...")
    
    # Menu height (matching your navbar height)
    menu_height = 70
    
    # Process each image
    images = ['climate1', 'photo_graph', 'photo_graph2']
    
    strips = []
    
    for base_name in images:
        print(f"\nProcessing {base_name}...")
        
        # Create horizontal strip
        strip_img, strip_width = create_horizontal_strip(base_name, menu_height)
        
        if strip_img:
            strips.append((base_name, strip_img, strip_width))
            
            # Create scrolling background for individual image
            create_scrolling_background(base_name, strip_img, strip_width, menu_height)
    
    # Create combined scrolling background
    if len(strips) == 3:
        print(f"\nCreating combined scrolling background...")
        combined_file, pattern_width = create_combined_scroll_background(menu_height)
        
        if combined_file:
            print(f"\n✅ Successfully created scrolling backgrounds!")
            print(f"Files created:")
            print(f"- Individual strips: *_menu_strip.png")
            print(f"- Individual scrolling: *_menu_scroll_bg.png") 
            print(f"- Combined scrolling: {combined_file}")
            print(f"\nPattern width for CSS animation: {pattern_width}px")
            print(f"Menu height: {menu_height}px")

if __name__ == "__main__":
    main()
