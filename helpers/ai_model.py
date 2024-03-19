import accelerate
import subprocess


async def train_ai_images(user_id: str):
    file_path = f"images/aiimages/{user_id}/training"
    MODEL_NAME = "CompVis/stable-diffusion-v1-4"
    INSTANCE_DIR = file_path
    OUTPUT_DIR = f"images/aiimages/{user_id}/output"
    command = [
        "accelerate",
        "launch",
        "helpers/train_dreambooth.py",
        "--pretrained_model_name_or_path",
        MODEL_NAME,
        "--instance_data_dir",
        INSTANCE_DIR,
        "--output_dir",
        OUTPUT_DIR,
        "--prior_loss_weight",
        "1.0",
        "--instance_prompt",
        "a profile picture of a person",
        "--resolution",
        "512",
        "--train_batch_size",
        "1",
        "--gradient_accumulation_steps",
        "1",
        "--learning_rate",
        "5e-6",
        "--lr_scheduler",
        "constant",
        "--lr_warmup_steps",
        "0",
        "--400",
        "800",
    ]
    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was executed successfully
    if result.returncode == 0:
        print("Command executed successfully.")
        print(result.stdout)
    else:
        print("Error in executing command.")
        print(result.stderr)
