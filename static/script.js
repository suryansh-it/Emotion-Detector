// Access the webcam video stream
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const capturedImage = document.getElementById('captured-image');
const captureBtn = document.getElementById('capture-btn');

// Start video stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        video.srcObject = stream;
    })
    .catch(function(err) {
        console.log("Error accessing webcam: " + err);
    });

// Capture the image when the button is clicked
captureBtn.addEventListener('click', function() {
    // Draw the video frame on the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas to a data URL (base64)
    const imageData = canvas.toDataURL('image/jpeg');

    // Display the captured image in the img tag
    capturedImage.src = imageData;
    capturedImage.style.display = 'block';

    // Send the captured image to the server
    fetch('/capture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_data: imageData.split(',')[1] })  // Send base64 without the data URI prefix
    })
    .then(response => response.json())
    .then(data => {
        if (data.image_id) {
            alert('Image captured and saved successfully!');
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Preview last 3 images
function previewImages() {
    $.ajax({
        url: "/preview_images",
        type: "GET",
        success: function(response) {
            const imagePreview = $('#imagePreview');
            imagePreview.empty();
            response.forEach(image => {
                const imageHtml = `
                    <div class="col-md-4">
                        <div class="card mb-4">
                            <img src="data:image/jpeg;base64,${image.image_data}" class="card-img-top" alt="Captured Image">
                            <div class="card-body text-center">
                                <button class="btn btn-success" onclick="detectEmotion(${image.id})">Detect Emotion</button>
                            </div>
                        </div>
                    </div>
                `;
                imagePreview.append(imageHtml);
            });
        },
        error: function(error) {
            alert('Error loading images');
        }
    });
}

// Detect emotion for selected image
function detectEmotion(imageId) {
    $.ajax({
        url: `/detect_emotion/${imageId}`,
        type: "GET",
        success: function(response) {
            alert('Emotion Detected: ' + JSON.stringify(response));
        },
        error: function(error) {
            alert('Error detecting emotion');
        }
    });
}

// Call previewImages on page load
$(document).ready(function() {
    previewImages();
});