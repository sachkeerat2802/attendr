const startBtn = document.getElementById("startWebCam");
const closeBtn = document.getElementById("closeWebCam");
let intervalId;

const showMsg = (message, type) => {
    const text = document.querySelector(".alert");
    if (text == null) {
        const msg = document.createElement("p");
        msg.classList.add("alert");
        if (type == "info") {
            msg.classList.add("alert-info");
        } else {
            msg.classList.add("alert-success");
        }
        document.body.appendChild(msg);
        msg.innerText = message;
        setTimeout(() => {
            msg.remove();
        }, 5000);
    }
};

const displayVideo = () => {
    closeBtn.style.display = "";
    startBtn.style.display = "none";
    navigator.mediaDevices
        .getUserMedia({ video: true, audio: false })
        .then(function (stream) {
            const video = document.querySelector("video");
            video.style.display = "";
            video.srcObject = stream;
            video.onloadedmetadata = function (e) {
                video.play();
            };
        })
        .catch(function (err) {
            console.log("An error occurred: " + err);
        });

    intervalId = setInterval(encodeVideo, 1000 / 30);
};

const stopVideo = () => {
    clearInterval(intervalId);
    startBtn.style.display = "";
    closeBtn.style.display = "none";
    const video = document.getElementById("video");
    video.srcObject.getTracks().forEach(function (track) {
        track.stop();
    });
    video.style.display = "none";
};

const encodeVideo = () => {
    const video = document.querySelector(".video");
    const canvas = document.createElement("canvas");
    canvas.width = video.dataset.width;
    canvas.height = video.dataset.height;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL("image/png");

    fetch(window.location.href, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ video: dataURL }),
    })
        .then((response) => response.text())
        .then((text) => {
            try {
                const data = JSON.parse(text);
                if ("info" in data) {
                    showMsg(data.info, "info");
                } else if ("success" in data) {
                    showMsg(data.success, "success");
                }
            } catch (err) {}
        })
        .catch(function (error) {
            console.log("An error occurred: " + error);
        });
};

startBtn.addEventListener("click", () => {
    displayVideo();
});

closeBtn.addEventListener("click", () => {
    stopVideo();
});
