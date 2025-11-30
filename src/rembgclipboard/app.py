import subprocess
from PIL import Image
from io import BytesIO
from rembg import remove as rembg_remove


def notify_send(message: str):
    subprocess.run(
        ['notify-send', message]
    )


def get_clipboard_types():
    types_result = subprocess.run(
        ['wl-paste', '--list-types'],
        capture_output=True,
        text=True
    )
    types = [i.strip() for i in types_result.stdout.splitlines()]
    return types


def get_image_from_clipboard():

    if 'image/png' not in get_clipboard_types():
        notify_send("No image in clipboard")
        exit(1)

    result = subprocess.run(
        ['wl-paste' , '--type', 'image/png'],
        capture_output = True,
        check = True
    )

    image = Image.open(BytesIO(result.stdout))

    return image

def write_image_to_clipboard(image: Image):
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    subprocess.run(
        ['wl-copy', '--type', 'image/png'],
        input=buffer.read(),
        check=True
    )


def remove_background(image: Image):
    return rembg_remove(
        image,
        providers=['CPUExecutionProvider']
    )

if __name__ == "__main__":
    clip_image = get_image_from_clipboard()
    removed = remove_background(clip_image)
    write_image_to_clipboard(removed)
    notify_send("Background removed and copied to clipboard")
