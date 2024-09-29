//     const video = document.getElementById('video');
//     const captureBtn = document.getElementById('capture-btn');
//     const previewContainer = document.getElementById('preview-container');

//     // Start video stream
//     navigator.mediaDevices.getUserMedia({ video: true })
//         .then(function (stream) {
//             video.srcObject = stream;
//         })
//         .catch(function (err) {
//             console.log("Error accessing webcam: " + err);
//         });

//     // Capture the image when the button is clicked
// captureBtn.addEventListener('click', function () {
//     const canvas = document.createElement('canvas');
//     const context = canvas.getContext('2d');
//     canvas.width = video.videoWidth;
//     canvas.height = video.videoHeight;

//     // Draw the video frame on the canvas
//     context.drawImage(video, 0, 0, canvas.width, canvas.height);

//     // Convert the canvas to a data URL (base64)
//     const image_data = canvas.toDataURL('image/jpeg').split(',')[1];  // Send base64 without the data URI prefix

//     // Send the captured image to the server
//     fetch('http://127.0.0.1:5000/capture', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ image_data: image_data})
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.message) {
//             alert('Image captured and saved successfully!');
//             // After capturing the image, update the preview with the last 3 images
//             fetchPreviewImages();
//         } else {
//             alert('Error: ' + data.error);
//         }
//     })
//     .catch(error => console.error('Error:', error));
// });


//     // Fetch and update the preview with the last 3 images
//     function fetchPreviewImages() {
//         fetch('/preview', {
//             method: 'GET'
//         })
//             .then(response => response.json())
//             .then(data => {
//                 console.log("Preview Data:", data);
//                 updatePreview(data);
//             })
//             .catch(error => console.error('Error fetching preview images:', error));
//     }

//     // Function to update the preview with the fetched images
//     function updatePreview(images) {
//         // Clear the existing preview
//         for (let i = 1; i <= 3; i++) {
//             const previewImage = document.getElementById(`preview-${i}`);
//             previewImage.src = '';  // Clear existing image
//             previewImage.style.display = 'none';  // Hide if no image available
//         }
    
//         // Add the new images to the preview (up to 3)
//         images.forEach((image, index) => {
//             if (index < 3 && image.image_data) {  // Ensure image_data exists
//                 const previewImage = document.getElementById(`preview-${index + 1}`);
//                 previewImage.src = `data:image/jpeg;base64,${image.image_data}?${new Date().getTime()}`;
//                   // Assuming image data is returned as base64
//                 previewImage.style.display = 'block';  // Show the image
//             }
//         });
//     }
    
    





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
    const image_data = canvas.toDataURL('image/png').split(',')[1];  // Send base64 without the data URI prefix

    // Send the captured image to the server
    fetch('http://127.0.0.1:5000/capture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_data: image_data })
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


// function fetchPreviewImages() {
//     fetch('/preview', {
//         method: 'GET'
//     })
//         .then(response => response.json())
//         .then(data => {
//             console.log("Preview Data:", data);
//             updatePreview(data);
//         })
//         .catch(error => console.error('Error fetching preview images:', error));
// }

// // Function to update the preview with the fetched images
// function updatePreview(images) {
//     // Clear the existing preview
//     for (let i = 1; i <= 3; i++) {
//         const previewImage = document.getElementById(`preview-${i}`);
//         previewImage.src = '';  // Clear existing image
//         previewImage.style.display = 'none';  // Hide if no image available
//     }

//     // Add the new images to the preview (up to 3)
//     images.forEach((image, index) => {
//         if (index < 3 && image.image_data) {
//             const previewImage = document.getElementById(`preview-${index + 1}`);
            
//             // Directly set the src to the Base64 string
//             previewImage.src = `data:image/jpeg;base64,${image.image_data}`;
//             previewImage.style.display = 'block';  // Show the image
//         }
//     });
// }


let selectedImageId = null;  // Track the selected image

// Fetch preview images on page load
window.onload = function() {
    fetchPreviewImages();
};

function fetchPreviewImages() {
    fetch('/preview', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Preview Data:", data);
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
        previewImage.classList.remove("selected"); // Remove selected class
    }

    // Add the new images to the preview (up to 3)
    images.forEach((image, index) => {
        if (index < 3 && image.image_data) {
            const previewImage = document.getElementById(`preview-${index + 1}`);
            previewImage.src = `data:image/jpeg;base64,${image.image_data}`;
            previewImage.style.display = 'block';  // Show the image
            previewImage.setAttribute('data-image-id', image.id);  // Set the image ID for selection
        }
    });
}

// Function to select an image
function selectImage(previewIndex) {
    // Clear previously selected image
    for (let i = 1; i <= 3; i++) {
        document.getElementById(`preview-${i}`).classList.remove("selected");
    }

    // Mark the selected image
    const previewImage = document.getElementById(`preview-${previewIndex}`);
    previewImage.classList.add("selected");

    // Store the selected image ID
    selectedImageId = previewImage.getAttribute('data-image-id');

    // Show the detect emotion button
    document.getElementById('detect-emotion-btn').style.display = 'block';
}

// Function to detect emotion for the selected image
function detectEmotion() {
    if (!selectedImageId) {
        alert('Please select an image first!');
        return;
    }

    fetch(`/detect_emotion/${selectedImageId}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Emotion Data:', data);
        displayEmotion(data);
    })
    .catch(error => console.error('Error detecting emotion:', error));
}

// Function to display the detected emotion
function displayEmotion(emotionData) {
    const emotionResult = document.getElementById('emotion-data');
    emotionResult.textContent = JSON.stringify(emotionData);
}
