
document.addEventListener('DOMContentLoaded', (event) => {
    
    const uploadForm = document.getElementById('convertForm');
    const fileInput = document.getElementById('pptx_input');
    const resolution_select = document.getElementById('resolution_select');
    const submitBtn = document.getElementById('submitBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const effectSelect = document.getElementById('effectSelect');
    uploadForm.onsubmit = async (event) => {
        event.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            alert("No file selected!");
            return;
        }

        // socket.emit("upload_file", {
        //             file_name: file.name,
        //             file_data: file
        //         }, (status) => {
        //     console.log(status);
        //   });
        submitBtn.innerHTML = `<span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>
        <span role="status">Converting...</span>` ;
        downloadBtn.classList.add('d-none')
        submitBtn.disabled = true;
        const reader = new FileReader();
                reader.onload = () => {
                    const base64FileData = reader.result;

                    socket.emit('upload_file', {
                        file_name: file.name,
                        file_data: base64FileData,
                        quality: resolution_select.value,
                        effect: effectSelect.value,
                    },(status)=>{
                        submitBtn.enabled =true;
                        if (status && status == 400){
                            submitBtn.innerText = 'Convert'
                        }
                    });

                    showToast('Uploading...', 'info', 3000);
                };
                reader.readAsDataURL(file);
    };
    
    socket.on('file_uploaded', (data) => {
        submitBtn.innerText = 'Converting'
        showToast(data.message, 'success',3000);
    },);

    socket.on('file_upload_error', (data) => {
        submitBtn.disabled =true;
        submitBtn.innerText = 'Convert'
        showToast(data.message, 'danger',3000);
    },);

    socket.on('convert_success',(data)=>{
        submitBtn.disabled =false;
        submitBtn.innerHTML = 'Convert'
        const file_link = data.file_link;
        if (file_link){
            const frontUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ":" + window.location.port : ""}`;
            downloadBtn.href = '/get-file/' + file_link;
        }
        downloadBtn.classList.remove('d-none');
        showToast(data.message,'success',3000);
    })
})