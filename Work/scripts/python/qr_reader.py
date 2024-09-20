import cv2
import numpy as np

def decode_qr_code(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded correctly
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize the QR code detector
    qr_detector = cv2.QRCodeDetector()

    # Detect and decode the QR code
    data, points, _ = qr_detector.detectAndDecode(gray_image)

    if data:
        print("QR Code detected and decoded:")
        print("Data:", data)
    else:
        print("No QR code found")

if __name__ == "__main__":
    image_path = r"C:\Users\beckett.mcfarland\Pictures\qr.png"  # Replace with your image file path
    decode_qr_code(image_path)
