import fitz
from PIL import Image
import os

def extract_images(pdf_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the PDF file
    pdf_file = fitz.open(pdf_path)
    
    # Iterate through each page
    for page_index in range(len(pdf_file)):
        # Get the page itself
        page = pdf_file[page_index]
        
        # Extract images from the page's display list
        image_list = page.get_images(full=True)
        
        # Iterate through each image
        for image_index, img in enumerate(image_list):
            # Get the XREF of the image
            xref = img[0]
            
            # Get the image data
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Convert image bytes to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGBA mode to ensure transparency
            pil_image = pil_image.convert("RGBA")
            
            # Resize the image to 600x600
            pil_image = pil_image.resize((600, 600))
            
            # Construct output folder path
            page_folder = os.path.join(output_folder, f"page_{page_index + 1}")
            
            # Create page folder if it doesn't exist
            if not os.path.exists(page_folder):
                os.makedirs(page_folder)
            
            # Construct output image file path
            image_path = os.path.join(page_folder, f"image_{image_index + 1}.png")
            
            # Save the image to file
            pil_image.save(image_path)
    
    print("Images extracted and saved successfully!")
