import os

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


def validate_image(image):
    # Image is required when creating a blog post.
    if not image:
        return False, "Please upload an image."

    # Check file size.
    if image.size > MAX_IMAGE_SIZE:
        return False, "Image size must be 2 MB or less."

    # Check file extension.
    extension = os.path.splitext(image.name)[1].lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return False, "Only JPG, JPEG, and PNG images are allowed."

    return True, ""
