const feed = document.getElementById('ai-feed');
const status = document.getElementById('status');
const wrapper = document.getElementById('video-wrapper');


document.getElementById('start-btn').onclick = function() {
    fetch('/reset_webcam', {method: 'POST'}).then(() => {
        wrapper.style.display = 'block';
        feed.src = "/video_feed";
        status.innerText = 'Status: Webcam Streaming...';
    });
};


function uploadVideo(input) {
    if (input.files[0]) {
        let formData = new FormData();
        formData.append('video', input.files[0]);
        status.innerText = 'Status: Uploading...';
        
        fetch('/upload_video', {method: 'POST', body: formData})
        .then(res => res.json())
        .then(data => {
            if(data.success) {
                wrapper.style.display = 'block';
                feed.src = "/video_feed";
                status.innerText = 'Status: Processing Video...';
            }
        });
    }
}

document.getElementById('stop-btn').onclick = function() {
    location.reload(); 
};