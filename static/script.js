// Handle image capture and preview
$('#capture-form').on('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('imageCapture');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onloadend = function() {
            const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');

            $.ajax({
                url: "/capture",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ image_data: base64String }),
                success: function(response) {
                    alert('Image captured and saved successfully!');
                    previewImages();
                },
                error: function(error) {
                    alert('Error capturing image');
                }
            });
        };
        reader.readAsDataURL(file);
    }
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