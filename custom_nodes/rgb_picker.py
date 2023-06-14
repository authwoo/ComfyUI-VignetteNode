import numpy as np
import torch

class RGBColorPicker:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "red": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1
                }),
                "use_hex_instead": (["no", "yes"],
                ),
            },
            "optional": {
                "hex": ("STRING", {
                    "default": "#FFFFFF"
                }),
            },
        }

    RETURN_TYPES = ("RGB",)
    FUNCTION = "get_rgb"

    CATEGORY = "input/Color"

    def get_rgb(self, red: int, green: int, blue: int, use_hex_instead, hex: str = None):
        if use_hex_instead == "yes":
            try:
                hex = hex.lstrip('#')
                red, green, blue = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))  # Convert hex to RGB
            except ValueError:
                print("Invalid hex color. Using RGB inputs instead.")
                hex = "Invalid hex color. Using RGB inputs instead."
        
        red = max(min(red, 255), 0)
        green = max(min(green, 255), 0)
        blue = max(min(blue, 255), 0)

        return ((red / 255, green / 255, blue / 255),)  # Normalize RGB values to [0, 1]


NODE_CLASS_MAPPINGS = {
    "RGBColorPicker": RGBColorPicker,
}
