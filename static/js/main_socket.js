let socket;
function initSocketIO() {
    socket = io({maxHttpBufferSize: 1e8}).connect("http://" + location.hostname + ":" + location.port, {
      reconnection: true,
      reconnectionAttempts: 2,
      reconnectionDelay: 2000,
    });
  
  
    socket.on("connect", function (params) {
      console.log("connected");
      showToast('connected','success',3000);
    });
  
    socket.on("error", function (message) {
      setTimeout(() => {
        showToast(message,'danger',3000);
      }, 3000);
    });
  
    socket.on("disconnect", (reason, details) => {
      console.log("disconnected By Server");
      console.log(reason);
      console.log(details);
  
      // Swal.fire({
      //   title: "Disconnected",
      //   text: "The connection to the server is lost,\n please check internet connection!",
      //   icon: "error",
      //   confirmButtonText: "OK",
      // }).then((result) => {
      //   // Redirect to the homepage when the modal is closed
      //   if (
      //     result.isConfirmed ||
      //     result.dismiss === Swal.DismissReason.backdrop
      //   ) {
      //     // window.location.href = "/"; // Replace with your homepage URL
      //     window.location.reload();
      //   }
      // });
    });
  
    socket.on("retry", function (msg) {
      console.error("Error Received data: " + JSON.stringify(msg));
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Something went wrong!",
        footer: '<a href="/">Click to refresh page</a>',
      });
      socket.disconnect();
    });

    socket.on("alert", function (data) {
      showToast(data.message,data.type||"info",3000)
    })

    return socket;
  }

function initializeSocketIO(testing) {
    socket = initSocketIO();
  
    if (!testing) {
      console.log("Live Mode");
  
      socket.on("connect", function (params) {
        socket.emit(
          "join_room",
          { sid: socket.id },
          (response) => {}
        );
      });
    }
}

function showToast(message, type, duration) {
  const toast = document.createElement('div');
  toast.className = `toast align-items-center text-bg-${type} border-0`;
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.setAttribute('aria-atomic', 'true');

  const toastBody = document.createElement('div');
  toastBody.className = 'd-flex';
  toastBody.innerHTML = `
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
  `;

  const progressBar = document.createElement('div');
  progressBar.className = 'toast-progress text-bg-dark';
  progressBar.style.width = '100%';

  toast.appendChild(toastBody);
  toast.appendChild(progressBar);
  toastContainer.appendChild(toast);

  const bootstrapToast = new bootstrap.Toast(toast, { delay: duration });
  bootstrapToast.show();

  // Update progress bar
  let progressWidth = 100;
  const interval = 30;  // Interval for progress update in milliseconds
  const step = interval / duration * 100;

  const progressInterval = setInterval(() => {
      progressWidth -= step;
      progressBar.style.width = progressWidth + '%';
      if (progressWidth <= 0) {
          clearInterval(progressInterval);
      }
  }, interval);

  // Remove the toast element after it hides
  toast.addEventListener('hidden.bs.toast', () => {
      toast.remove();
      clearInterval(progressInterval);
  });
}

initializeSocketIO(false);
window.addEventListener('DOMContentLoaded', () => {
});