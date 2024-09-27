    const video = document.getElementById('video');
    const captureBtn = document.getElementById('capture-btn');
    const previewContainer = document.getElementById('preview-container');

    // Start video stream
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err) {
            console.log("Error accessing webcam: " + err);
        });

    // Capture the image when the button is clicked
captureBtn.addEventListener('click', function () {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the video frame on the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas to a data URL (base64)
    const imageData = canvas.toDataURL('image/jpeg').split(',')[1];  // Send base64 without the data URI prefix

    // Send the captured image to the server
    fetch('/capture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_data: imageData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Image captured and saved successfully!');
            // After capturing the image, update the preview with the last 3 images
            fetchPreviewImages();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});


    // Fetch and update the preview with the last 3 images
    function fetchPreviewImages() {
        fetch('/preview_images', {
            method: 'GET'
        })
            .then(response => response.json())
            .then(data => {
                updatePreview(data);
            })
            .catch(error => console.error('Error fetching preview images:', error));
    }

    // Function to update the preview with the fetched images
    function updatePreview(images) {
        // Clear the existing preview
        for (let i = 1; i <= 3; i++) {
            const previewImage = document.getElementById(`preview-${i}`);
            previewImage.src = '';  // Clear existing image
            previewImage.style.display = 'none';  // Hide if no image available
        }
    
        // Add the new images to the preview (up to 3)
        images.forEach((image, index) => {
            if (index < 3) {
                const previewImage = document.getElementById(`preview-${index + 1}`);
                previewImage.src = `data:image/jpeg;base64,${image.image_data}`;  // Assuming image data is returned as base64
                previewImage.style.display = 'block';  // Show the image
            }
        });
    }
    