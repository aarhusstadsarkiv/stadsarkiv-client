function setUploadSuccessMessage(data) {
    const filesList = document.getElementById('upload_message');
    filesList.innerHTML = '';
    for (let i = 0; i < data.files.length; i++) {
        const file = data.files[i];
        const p = document.createElement('p');
        p.textContent = `Uploaded file: ${file}`;
        filesList.appendChild(p);
    }
}

function setUploadErrorMessage(data) {
    const errorMessage = data.message;
    const filesList = document.getElementById('upload_message');
    filesList.innerHTML = '';
    const p = document.createElement('p');
    p.textContent = errorMessage;
    filesList.appendChild(p);
}

document.getElementById('upload').addEventListener('click', async function (e) {
    e.preventDefault();
    const files = document.getElementById('files').files;
    if (files.length === 0) {
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    try {
        const res = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            if (!data.error) {
                setUploadSuccessMessage(data);
            } else {
                setUploadErrorMessage(data);
            }
        } else {
            console.log('Upload failed');
        }
    } catch (e) {
        console.log(e);
    } finally {
        document.getElementById('files').value = '';
    }
});
