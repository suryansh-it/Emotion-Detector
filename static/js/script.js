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


let selectedImageId = null;  // This will hold the ID of the selected image

// Function to handle image selection
function selectImage(index) {
    // Highlight the selected image (if needed, add some visual effect)
    for (let i = 1; i <= 3; i++) {
        const previewImage = document.getElementById(`preview-${i}`);
        previewImage.style.border = (i === index) ? '2px solid blue' : 'none';
    }

    // Get the selected image ID from the fetched data (you'll need to have this stored when fetching images)
    selectedImageId = previewImages[index - 1].id;  // Assuming `previewImages` contains the fetched image data

    // Show the 'Detect Emotion' button
    document.getElementById('detect-emotion-btn').style.display = 'block';
}

// Function to detect emotion for the selected image
function detectEmotion() {
    if (!selectedImageId) {
        alert("Please select an image first.");
        return;
    }

    // Send request to detect emotion for the selected image
    fetch(`/detect_emotion/${selectedImageId}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Display the detected emotions
            document.getElementById('emotion-data').textContent = JSON.stringify(data);
        }
    })
    .catch(error => {
        console.error('Error detecting emotion:', error);
        alert('Failed to detect emotion.');
    });
}

// Fetch preview images and populate the preview section
let previewImages = [];  // This will store the fetched image data
function fetchPreviewImages() {
    fetch('/preview', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Preview Data:", data);
        previewImages = data;  // Store the fetched images

        updatePreview(previewImages);
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
        if (index < 3 && image.image_data) {
            const previewImage = document.getElementById(`preview-${index + 1}`);
            
            // Convert Base64 to binary data
            const byteCharacters = atob(image.image_data);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], { type: 'image/jpeg' });

            // Create a temporary URL for the blob and set it as the image src
            const blobUrl = URL.createObjectURL(blob);
            previewImage.src = blobUrl;
            previewImage.style.display = 'block';  // Show the image
        }
    });
}

// Call this function to load preview images when the page loads
fetchPreviewImages();
