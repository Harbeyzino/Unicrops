import cloudinary.uploader

def upload_product_image(image_file, public_id=None):
    """
    Uploads an image to Cloudinary and returns the secure URL.
    """
    try:
        response = cloudinary.uploader.upload(
            image_file,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )
        return response.get("secure_url")  # Return the Cloudinary URL
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None
