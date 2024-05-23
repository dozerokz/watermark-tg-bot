import logging
import os
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def clear_folder(folder_path: str) -> None:
    """Clear the contents of a folder."""
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    await clear_folder(file_path)  # Recursively clear subdirectories
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

        os.rmdir(folder_path)
    except Exception as e:
        logging.error(f"Error clearing folder: {e}")


def add_text_watermark(folder: str, image_name: str, text="SAMPLE WATERMARK", position=1, color=(255, 255, 255),
                       opacity=128,
                       size=1) -> Optional[str]:
    """Opens image by path, adding watermark and saves it. Returns path to image with watermark
    SIZE 1 - Small, 2 - Mid, 3 - Large, 4 - XLarge (XLarge quite unstable)
    POSITION 1 - Center, 2 - Up Left, 3 - Up Right, 4 - Bottom Left, 5 - Bottom Right, 6 - Whole Image"""
    try:
        size_map = {4: 0.2, 3: 0.1, 2: 0.05, 1: 0.03}
        # Open the original image
        image = Image.open(f"{folder}/{image_name}").convert("RGBA")

        # Make the image editable
        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

        font_size = int(image.width * size_map.get(size, 0.03))

        # Choose a font and size
        font = ImageFont.truetype("utils/Impact.ttf", font_size)
        # Initialize ImageDraw
        draw = ImageDraw.Draw(txt)

        text_width, text_height = draw.textsize(text, font=font)
        if position == 1:
            position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
        elif position == 2:
            position = (int(image.width * 0.025), int(image.height * 0.025))
        elif position == 3:
            position = (int((image.width - text_width) - image.width * 0.025), int(image.height * 0.025))
        elif position == 4:
            position = (int(image.width * 0.025), int((image.height - text_height) - image.height * 0.025))
        elif position == 5:
            position = (
                int((image.width - text_width) - image.width * 0.025),
                int((image.height - text_height) - image.height * 0.025))
        elif position == 6:
            space_size = draw.textsize("  ", font=font)[0]
            line_height = draw.textsize(" \n", font=font)[1] - draw.textsize(" ", font=font)[1]
            num_x = int(image.width // (text_width + space_size))
            num_y = int(image.height // line_height)
            text = '\n'.join(['  '.join([text] * num_x)] * num_y)
            text_width, text_height = draw.textsize(text, font=font)
            position = (int((image.width - text_width) / 2), int((image.height - text_height) / 2))

        # Add text to image
        draw.text(position, text, fill=(*color, opacity), font=font)

        # Combine original image with text
        watermarked = Image.alpha_composite(image, txt)

        if not os.path.exists(folder):
            os.makedirs(folder)
        watermarked.save(f"{folder}/watermarked.png")
        return f"{folder}/watermarked.png"
    except Exception as e:
        logging.error(f"Error generating watermarked image: {e}")
        return None
