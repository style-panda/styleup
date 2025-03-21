import logging
import base64

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
    logger.info(f"load_images called with uploaded_images: {uploaded_images is not None}")
    image_parts = []
    
    # If client uploaded images, use those
    if uploaded_images:
        try:
            logger.info(f"Processing {len(uploaded_images)} uploaded images")
            for i, img in enumerate(uploaded_images):
                logger.info(f"Processing image {i+1}/{len(uploaded_images)}")
                
                if 'data' not in img or 'mime_type' not in img:
                    logger.error(f"Invalid image format for image {i+1}: missing data or mime_type")
                    return None, "Invalid image format: missing data or mime_type"
                
                logger.info(f"Image {i+1} mime_type: {img['mime_type']}")
                
                # If data is base64 encoded, decode it
                if isinstance(img['data'], str):
                    try:
                        logger.info(f"Decoding base64 data for image {i+1} (first 20 chars: {img['data'][:20]}...)")
                        binary_data = base64.b64decode(img['data'])
                        logger.info(f"Successfully decoded base64 data for image {i+1}, size: {len(binary_data)} bytes")
                    except Exception as e:
                        logger.error(f"Base64 decoding error for image {i+1}: {str(e)}")
                        return None, f"Invalid image encoding: {str(e)}"
                else:
                    logger.info(f"Image {i+1} data is already binary, size: {len(img['data'])} bytes")
                    binary_data = img['data']
                
                image_parts.append({
                    "mime_type": img['mime_type'],
                    "data": binary_data
                })
            
            logger.info(f"Successfully processed {len(image_parts)} uploaded images")
            return image_parts, None
            
        except Exception as e:
            logger.error(f"Error processing uploaded images: {str(e)}", exc_info=True)
            return None, f"Error processing uploaded images: {str(e)}"
    
    # Fall back to local images if no uploads provided
    try:
        logger.info("No uploaded images provided, falling back to local images")
        from local_constants import image_paths  # Import here to avoid circular imports
        
        logger.info(f"Attempting to load {len(image_paths)} local images")
        for i, path in enumerate(image_paths):
            logger.info(f"Loading local image {i+1}/{len(image_paths)}: {path}")
            try:
                with open(path, "rb") as image_file:
                    image_data = image_file.read()
                    logger.info(f"Successfully loaded local image {path}, size: {len(image_data)} bytes")
                    image_parts.append({"mime_type": "image/jpeg", "data": image_data})
            except Exception as e:
                logger.error(f"Error loading local image {path}: {str(e)}")
                
        if not image_parts:
            logger.error("No local images could be loaded")
            return None, "No images could be loaded"
            
        logger.info(f"Successfully loaded {len(image_parts)} local images")
        return image_parts, None
    except Exception as e:
        logger.error(f"Error loading local images: {str(e)}", exc_info=True)
        return None, f"Error loading images: {str(e)}"