document.addEventListener('DOMContentLoaded', function() {
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const downloadContainer = document.getElementById('download-container');
    const downloadLink = document.getElementById('download-link');

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(uploadForm);
        const xhr = new XMLHttpRequest();
        
        xhr.open('POST', '/merge_pdf', true);

        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                progressBar.value = percentComplete;
            }
        };

        xhr.onloadstart = function() {
            progressContainer.style.display = 'block';
            progressBar.value = 0;
        };

        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const downloadUrl = '/download/' + response.filename;
                downloadLink.href = downloadUrl;
                progressContainer.style.display = 'none';
                downloadContainer.style.display = 'block';
            } else {
                const response = JSON.parse(xhr.responseText);
                alert('An error occurred: ' + response.error);
            }
        };

        xhr.onerror = function() {
            alert('An error occurred while uploading the files.');
        };

        xhr.send(formData);
    });
});

