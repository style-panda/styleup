import logging
import base64
from local_constants import image_paths

logger = logging.getLogger(__name__)

def load_images(uploaded_images=None):
    """
    Load images either from uploaded data or from specified local paths.
    
    Args:
        uploaded_images (list, optional): List of uploaded image data from the client.
            Each item should be a dict with 'data' (base64 string) and 'mime_type'.
    
    Returns:
        tuple: (image_parts, error_message)
    """
    image_parts = []
    
    # If client uploaded images, use those
    if uploaded_images:
        try:
            for img in uploaded_images:
                if 'data' not in img or 'mime_type' not in img:
                    return None, "Invalid image format: missing data or mime_type"
                
                # If data is base64 encoded, decode it
                if isinstance(img['data'], str):
                    try:
                        binary_data = base64.b64decode(img['data'])
                    except Exception as e:
                        logger.error(f"Base64 decoding error: {str(e)}")
                        return None, f"Invalid image encoding: {str(e)}"
                else:
                    binary_data = img['data']
                
                image_parts.append({
                    "mime_type": img['mime_type'],
                    "data": binary_data
                })
            
            logger.info(f"Successfully processed {len(image_parts)} uploaded images")
            return image_parts, None
            
        except Exception as e:
            logger.error(f"Error processing uploaded images: {str(e)}")
            return None, f"Error processing uploaded images: {str(e)}"
    
    # Fall back to local images if no uploads provided
    try:
        for path in image_paths:
            with open(path, "rb") as image_file:
                image_data = image_file.read()
                image_parts.append({"mime_type": "image/jpeg", "data": image_data})
        logger.info(f"Successfully loaded {len(image_parts)} local images")
        return image_parts, None
    except FileNotFoundError as e:
        logger.error(f"Image not found: {str(e)}")
        return None, f"Image not found: {str(e)}"