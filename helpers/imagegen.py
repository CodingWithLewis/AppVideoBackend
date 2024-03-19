from diffusers import DiffusionPipeline
from PIL import Image

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0").to(
    "cuda"
)

pipe.load_lora_weights("images/checkpoint-500")

image = pipe(
    "A profile picture of a man who is an astronaut in a cyberpunk style, high contrast",
    num_inference_steps=50,
).images[0]

image.save("aiphoto.png")
