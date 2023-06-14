import numpy as np
import torch

class VignetteExtended:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "vignette_strength": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 1.0
                }),
                "center_offset": ("FLOAT", {
                    "default": 0.333,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "feathering": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1
                }),
                "shape": (["circle", "ellipse", "square"],
                ),
                "reverse_vignette": (["no", "yes"],
                ),
                "rgb_subtract": (["no", "yes"],
                ),
            },
            "optional": {
                "vignette_color": ("RGB", {
                    "default": (0.0, 0.0, 0.0)
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_vignette"

    CATEGORY = "postprocessing/Effects"

    def apply_vignette(self, image: torch.Tensor, vignette_strength: float, center_offset: float, feathering: float, shape, reverse_vignette, rgb_subtract, vignette_color: tuple = (0.0, 0.0, 0.0)):
        # Checking and adjusting parameters if they are out of bounds
        vignette_strength = max(min(vignette_strength, 10.0), 0.0)
        feathering = max(min(feathering, 2.0), 0.1)
        vignette_color = tuple(max(min(c, 1.0), 0.0) for c in vignette_color)
        center_offset = max(min(center_offset, 1.0), 0.0)

        if vignette_strength == 0:
            return (image,)

        height, width, _ = image.shape[-3:]
        x = torch.linspace(-1, 1, width, device=image.device) * feathering
        y = torch.linspace(-1, 1, height, device=image.device) * feathering
        Y, X = torch.meshgrid(y, x)

        if shape == "circle":
            radius = torch.sqrt(X ** 2 + Y ** 2)
        elif shape == "ellipse":
            radius = torch.sqrt(X ** 2 * 0.75 + Y ** 2)
        elif shape == "square":
            radius = torch.max(torch.abs(X), torch.abs(Y))

        # Subtract center offset
        radius = torch.clamp(radius - center_offset, min=0)

        # Map vignette strength from 0-10 to 1.800-0.800
        mapped_vignette_strength = 1.8 - (vignette_strength - 1) * 0.1
        vignette_strength = 1 - torch.clamp(radius / mapped_vignette_strength, 0, 1)

        if reverse_vignette == "no":
            vignette_strength = 1 - vignette_strength

        # Convert vignette color to tensor
        vignette_color = torch.tensor(vignette_color, device=image.device)

        # Reshape to match image shape
        vignette_strength = vignette_strength.unsqueeze(-1).expand_as(image)

        # Choose method based on rgb_subtract option
        if rgb_subtract == "yes":
            # Subtract image from vignette color and multiply with vignette_strength
            vignette_image = torch.clamp(image - vignette_color * vignette_strength, 0, 1)
        else:
            # Interpolate between image and vignette color based on vignette_strength
            vignette_image = torch.lerp(image, vignette_color, vignette_strength)


        return (vignette_image,)


NODE_CLASS_MAPPINGS = {
    "Vignette_Extended": VignetteExtended,
}
