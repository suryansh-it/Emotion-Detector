# # capture_image.py
# import cv2
# import base64

# def capture_image():
#     # Initialize the camera (ID 0 is usually the default webcam)
#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         raise Exception("Could not open the camera")

#     # Capture a frame
#     ret, frame = cap.read()

#     if not ret:
#         cap.release()
#         raise Exception("Failed to capture image")

#     # Encode the frame to base64 for storage in the database
#     _, buffer = cv2.imencode('.jpg', frame)
#     image_data = base64.b64encode(buffer).decode('utf-8')

#     # Release the camera
#     cap.release()

#     return buffer.tobytes()  # Return the raw bytes for storage



import cv2
import base64

def capture_image():
    # Initialize the camera (ID 0 is usually the default webcam)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise Exception("Could not open the camera")

    # Capture a frame
    ret, frame = cap.read()

    if not ret:
        cap.release()
        raise Exception("Failed to capture image")

    # Encode the frame to base64 for storage in the database
    _, buffer = cv2.imencode('.jpg', frame)
    image_data = base64.b64encode(buffer).decode('utf-8')  # Convert to Base64 string

    # Release the camera
    cap.release()

    return image_data  # Return the Base64 string for storage
