let pdfPath = '';
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const pageContainer = document.getElementById('pageContainer');
const reorganizeBtn = document.getElementById('reorganizeBtn');


dropZone.onclick = () => fileInput.click();

dropZone.ondragover = (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#000';
};

dropZone.ondragleave = () => {
    dropZone.style.borderColor = '#ccc';
};

dropZone.ondrop = (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ccc';
    fileInput.files = e.dataTransfer.files;
    handleFile(e.dataTransfer.files[0]);
};

fileInput.onchange = () => {
    handleFile(fileInput.files[0]);
};

function handleFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        pdfPath = data.path;
        renderPDF(file);
    })
    .catch(error => console.error('Error:', error));
}

function renderPDF(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const typedarray = new Uint8Array(e.target.result);

        pdfjsLib.getDocument(typedarray).promise.then(pdf => {
            pageContainer.innerHTML = '';
            for (let i = 1; i <= pdf.numPages; i++) {
                pdf.getPage(i).then(page => {
                    const scale = 1.5;
                    const viewport = page.getViewport({ scale: scale });
                    const div = document.createElement('div');
                    div.className = 'pagePreview';
                    div.dataset.pageNum = i - 1;
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;

                    const renderContext = {
                        canvasContext: context,
                        viewport: viewport
                    };
                    page.render(renderContext);

                    div.appendChild(canvas);
                    
                    const optionsDiv = document.createElement('div');
                    optionsDiv.className = 'pageOptions';
                    optionsDiv.innerHTML = `
                        <button onclick="rotatePage(${i - 1}, 90)" id="rotatePage">Rotate 90°</button>
                        <button onclick="addBlankPage(${i - 1})" id="addBlankPage" >Add Blank Page</button>
                    `;
                    div.appendChild(optionsDiv);
                    
                    pageContainer.appendChild(div);
                });
            }
            reorganizeBtn.style.display = 'block';
        });
    };
    reader.readAsArrayBuffer(file);
}

new Sortable(pageContainer, {
    animation: 150,
    ghostClass: 'blue-background-class'
});

reorganizeBtn.onclick = () => {
    const newOrder = Array.from(pageContainer.children).map(child => parseInt(child.dataset.pageNum));
    
    fetch('/reorganize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({path: pdfPath, order: newOrder})
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = `/download/${encodeURIComponent(data.path)}`;
    })
    .catch(error => console.error('Error:', error));
};


    
function rotatePage(pageNumber, rotation) {
    fetch('/rotate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({path: pdfPath, pageNumber: pageNumber, rotation: rotation})
    })
    .then(response => response.json())
    .then(data => {
        pdfPath = data.path;
        // Re-render the PDF with the new rotated page
        fetch(pdfPath)
            .then(response => response.arrayBuffer())
            .then(arrayBuffer => {
                renderPDF(new Blob([arrayBuffer]));
            });
    })
    
    .catch(error => console.error('Error:', error));
}


function addBlankPage(afterPage) {
    fetch('/add-blank-page', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({path: pdfPath, afterPage: afterPage})
    })
    .then(response => response.json())
    .then(data => {
        pdfPath = data.path;
        // Re-render the PDF with the new blank page
        fetch(pdfPath)
            .then(response => response.arrayBuffer())
            .then(arrayBuffer => {
                renderPDF(new Blob([arrayBuffer]));
            });
    })
    .catch(error => console.error('Error:', error));
}
