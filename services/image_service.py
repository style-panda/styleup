import logging
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def load_images(uploaded_images=None):
    """
    Load images from URLs.
    
    Args:
        uploaded_images (list, optional): List of image URLs from the client.
            Each item should be a dict with 'url' and optional 'mime_type'.
    
    Returns:
        tuple: (image_parts, error_message)
    """
    logger.info(f"load_images called with uploaded_images: {uploaded_images is not None}")
    image_parts = []
    
    # If client provided image URLs, use those
    if uploaded_images:
        try:
            logger.info(f"Processing {len(uploaded_images)} image URLs")
            for i, img in enumerate(uploaded_images):
                logger.info(f"Processing image {i+1}/{len(uploaded_images)}")
                
                # Check if URL is provided
                if 'url' not in img:
                    logger.error(f"Invalid image format for image {i+1}: missing url")
                    return None, "Invalid image format: missing url"
                
                try:
                    logger.info(f"Processing image URL: {img['url']}")
                    response = requests.get(img['url'], timeout=10)
                    response.raise_for_status()  # Raise exception for 4XX/5XX responses
                    
                    binary_data = response.content
                    
                    # Try to determine mime_type if not provided
                    mime_type = img.get('mime_type')
                    if not mime_type:
                        # Try to guess from content-type header
                        mime_type = response.headers.get('Content-Type')
                        # If still not available, try to guess from URL extension
                        if not mime_type:
                            path = urlparse(img['url']).path
                            ext = path.split('.')[-1].lower() if '.' in path else ''
                            if ext in ['jpg', 'jpeg']:
                                mime_type = 'image/jpeg'
                            elif ext in ['png']:
                                mime_type = 'image/png'
                            elif ext in ['gif']:
                                mime_type = 'image/gif'
                            elif ext in ['webp']:
                                mime_type = 'image/webp'
                            else:
                                mime_type = 'application/octet-stream'
                    
                    logger.info(f"Image {i+1} from URL, size: {len(binary_data)} bytes, mime_type: {mime_type}")
                    
                    image_parts.append({
                        "mime_type": mime_type,
                        "data": binary_data
                    })
                except Exception as e:
                    logger.error(f"Error fetching image URL for image {i+1}: {str(e)}")
                    return None, f"Error fetching image URL: {str(e)}"
            
            logger.info(f"Successfully processed {len(image_parts)} image URLs")
            return image_parts, None
            
        except Exception as e:
            logger.error(f"Error processing image URLs: {str(e)}", exc_info=True)
            return None, f"Error processing image URLs: {str(e)}"
    else:
        logger.info("No image URLs provided")
        return None, "No image URLs provided"
