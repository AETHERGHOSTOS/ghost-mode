#!/usr/bin/env python3
import os
import sys

def print_fallback():
    # Glowing color ASCII art
    print("       \033[1;32m      .-''''''-.       ")
    print("       \033[1;32m    .'  \033[1;36m👻  👻\033[1;32m  '.     ")
    print("       \033[1;32m   /   \033[1;36mO      O\033[1;32m   \\    ")
    print("       \033[1;32m  :                :   ")
    print("       \033[1;32m  |    \033[1;31mG H O S T\033[1;32m   |   ")
    print("       \033[1;32m  :    \033[1;33m'.____.'\033[1;32m    :   ")
    print("       \033[1;32m   \\              /    ")
    print("       \033[1;32m    '.          .'     ")
    print("       \033[1;32m      '-......-'       \033[0m")

def render_image_logo(img_path, width=44):
    try:
        from PIL import Image
    except ImportError:
        print_fallback()
        return

    if not os.path.exists(img_path):
        print_fallback()
        return

    try:
        img = Image.open(img_path)
        # Convert to RGB
        img = img.convert('RGB')
        
        # Calculate height based on aspect ratio (ANSI half-block is 1:2 aspect ratio)
        aspect = img.height / img.width
        height = int(width * aspect * 0.5)
        
        # Resize image
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Print ANSI blocks
        for y in range(0, height, 2):
            for x in range(width):
                r1, g1, b1 = img.getpixel((x, y))
                if y + 1 < height:
                    r2, g2, b2 = img.getpixel((x, y + 1))
                else:
                    r2, g2, b2 = 0, 0, 0
                
                # 24-bit TrueColor ANSI escape sequences: ▀ is upper block
                # Foreground: upper block color, Background: lower block color
                sys.stdout.write(f"\033[38;2;{r1};{g1};{b1}m\033[48;2;{r2};{g2};{b2}m▀")
            sys.stdout.write("\033[0m\n")
    except Exception:
        print_fallback()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    
    # Try finding aether_emoji.png in ghost_tools or parent directory
    paths = [
        os.path.join(base_dir, "aether_emoji.png"),
        os.path.join(parent_dir, "assets/aether_emoji.png"),
        os.path.expanduser("~/ghost_tools/aether_emoji.png")
    ]
    
    logo_path = None
    for p in paths:
        if os.path.exists(p):
            logo_path = p
            break
            
    if logo_path:
        render_image_logo(logo_path)
    else:
        print_fallback()

if __name__ == "__main__":
    main()
