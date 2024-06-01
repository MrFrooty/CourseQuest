import torch
from diffusers import StableDiffusionPipeline


def generate_image(prompt: str):
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(model_id).to(device)

    image = pipe(prompt).images[0]
    image_path = "generated_image.png"
    image.save(image_path)
    return image_path
