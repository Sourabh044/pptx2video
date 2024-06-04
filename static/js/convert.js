
document.addEventListener('DOMContentLoaded', (event) => {
    
    const uploadForm = document.getElementById('convertForm');
    const fileInput = document.getElementById('pptx_input');
    const audioInput = document.getElementById('audio_input');
    const resolutionSelect = document.getElementById('resolution_select');
    const submitBtn = document.getElementById('submitBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const effectSelect = document.getElementById('effectSelect');
    const progressBarDiv = document.getElementById('progressbar');
    const progressBar = document.querySelector(".progress-bar");

    uploadForm.onsubmit = async (event) => {
        event.preventDefault();
        progressBarDiv.classList.add('d-none');
        progressBar.style.width = "10%";
        const pptFile = fileInput.files[0];
        const audioFile = audioInput.files[0];

        if (!pptFile) {
            alert("No file selected!");
            return;
        }


        submitBtn.innerHTML = `<span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>
        <span role="status">Converting...</span>` ;
        downloadBtn.classList.add('d-none')
        // progressBarDiv.classList.remove('d-none');
        progressBar.style.width = "25%"
        submitBtn.disabled = true;


        const formData = new FormData();
        formData.append('ppt_file', pptFile);
        if (audioFile) {
            formData.append('audio_file', audioFile);
        }
        formData.append('quality', resolutionSelect.value);
        formData.append('effect', effectSelect.value);
        
        
        showToast('Uploading...', 'info', 3000);

        const data = {
            ppt_file: pptFile,
            ppt_name :pptFile.name,
            audio_file: audioFile ? audioFile : null,
            audio_name: audioFile?audioFile.name:null,
            quality: resolutionSelect.value,
            effect: effectSelect.value,
        };

        // Create a new FileReader to read the ppt_file
        const pptReader = new FileReader();
        pptReader.onload = function(event) {
            data.ppt_file_data = event.target.result;

            if (audioFile) {
                const audioReader = new FileReader();
                audioReader.onload = function(event) {
                    data.audio_file = event.target.result;
                    socket.emit('upload_file', data,(status)=>{
                        if (status && status == 400){
                            submitBtn.enabled =true;
                            submitBtn.innerText = 'Convert'
                        }
                    });
                };
                audioReader.readAsDataURL(audioFile);
            } else {
                socket.emit('upload_file', data,(status)=>{
                    if (status && status == 400){
                        submitBtn.enabled =true;
                        submitBtn.innerText = 'Convert'
                    }
                }); 
            }
            showToast('Uploading...', 'info', 3000);
        };
        pptReader.readAsDataURL(pptFile);
        
        // socket.emit('upload_file', formData,(status)=>{
        //     if (status && status == 400){
        //         submitBtn.enabled =true;
        //         submitBtn.innerText = 'Convert'
        //     }
        // }); 
    };
    
    socket.on('file_uploaded', (data) => {
        submitBtn.innerText = 'Converting'
        showToast(data.message, 'success',3000);
        progressBar.style.width = "45%"
    },);

    socket.on('file_upload_error', (data) => {
        submitBtn.disabled =true;
        submitBtn.innerText = 'Convert'
        showToast(data.message, 'danger',3000);
        progressBar.classList.add('d-none');
        progressBar.style.width = "10%"
    },);

    socket.on('convert_success',(data)=>{
        progressBar.style.width = "100%"
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