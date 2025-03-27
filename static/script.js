"use strict";

document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded!");

    setupMeetButton();
    setupLumaNoxAnimations();
    setupChatbot();
    setupImageUpload();
    setupCameraCapture();
    setupArrivalButton();
});

// 🟢 Setup Meet Button (Debugging & Backend Call)
function setupMeetButton() {
    const button = document.getElementById("meet-button");

    if (button) {
        console.log("Meet button found!");

        button.addEventListener("click", function () {
            console.log("Meet button clicked!");

            // Temporary UI Feedback
            button.innerText = "Luma & Nox Arrived!";
            button.style.backgroundColor = "red";

            // Backend API Call
            fetch('/analyze', {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ image: "test_image.jpg" })
            })
            .then(response => response.json())
            .then(data => {
                alert(`${data.message}\nResult: ${data.result}`);
            })
            .catch(error => console.error("Error:", error));
        });
    } else {
        console.error("Button with ID 'meet-button' not found!");
    }
}

// 🟢 Setup Animations for Luma & Nox
function setupLumaNoxAnimations() {
    console.log("Luma & Nox are Arriving!");

    let luma = document.getElementById("luma");
    let nox = document.getElementById("nox");

    if (luma) {
        luma.classList.add("luma-appear");
        luma.style.opacity = "1";
        luma.style.transform = "translateY(0)";
    }

    if (nox) {
        nox.classList.add("nox-appear");
        nox.style.opacity = "1";
        nox.style.transform = "translateY(0)";
    }
}

// 🟢 Setup Chatbot Functionality
function setupChatbot() {
    document.getElementById("sendMessage").addEventListener("click", function () {
        let userText = document.getElementById("userInput").value.trim();
        if (!userText) return;

        let chatbox = document.getElementById("chatbox");

        // Display User Message
        chatbox.innerHTML += `<p class="userText"><span>${userText}</span></p>`;

        // Send Request to Flask Backend
        fetch("/chatbot", {
            method: "POST",
            body: JSON.stringify({ message: userText }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            chatbox.innerHTML += `<p class="botText"><span>${data.response}</span></p>`;
            chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll
        })
        .catch(error => console.error("Error:", error));

        document.getElementById("userInput").value = "";
    });
}

// 🟢 Setup Image Upload & Analysis
function setupImageUpload() {
    document.querySelector("#uploadForm").addEventListener("submit", async (e) => {
        e.preventDefault();

        let formData = new FormData();
        let imageFile = document.querySelector("#imageInput").files[0];

        if (!imageFile) {
            alert("Please select an image!");
            return;
        }

        formData.append("image", imageFile);

        try {
            let response = await fetch("/analyze", { method: "POST", body: formData });
            let data = await response.json();
            console.log("API Response:", data);

            if (data.error) {
                alert("Error: " + data.error);
                return;
            }

            alert(`Pollution Level: ${data.pollution_level}\nResult: ${data.description}`);
        } catch (error) {
            console.error("Error fetching API:", error);
            alert("Something went wrong. Check console for details.");
        }
    });
}

// 🟢 Setup Camera Capture & Live Analysis
function setupCameraCapture() {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const context = canvas ? canvas.getContext("2d") : null;
    const captureButton = document.getElementById("capture");

    if (video && canvas && captureButton) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                video.srcObject = stream;
            })
            .catch((err) => {
                console.error("Camera access denied", err);
            });

        // Capture & Send Image
        captureButton.addEventListener("click", () => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL("image/png");
            sendToBackend(imageData);
        });
    } else {
        console.warn("Camera elements not found.");
    }
}

// 🟢 Send Image to Backend for Analysis
function sendToBackend(imageData) {
    fetch("/analyze-sky", {
        method: "POST",
        body: JSON.stringify({ image: imageData }),
        headers: { "Content-Type": "application/json" }
    })
    .then((response) => response.json())
    .then((data) => {
        alert(`Light Pollution Level: ${data.pollution_level}`);
    })
    .catch((error) => console.error("Error:", error));
}

// 🟢 Setup "Luma & Nox Arrived" Button
function setupArrivalButton() {
    const button = document.getElementById("arrived-btn");

    if (button) {
        button.addEventListener("click", function () {
            let luma = document.getElementById("luma-img");
            let nox = document.getElementById("nox-img");

            if (luma && nox) {
                luma.style.display = "block";
                nox.style.display = "block";

                luma.style.animation = "fadeIn 2s ease-in-out, glow 1.5s infinite alternate";
                nox.style.animation = "fadeIn 2s ease-in-out, evil-glow 1.5s infinite alternate";
            } else {
                console.error("Luma or Nox image not found!");
            }
        });
    } else {
        console.warn("Arrival button not found.");
    }
}

const video = document.createElement("video");
video.setAttribute("autoplay", "");
video.setAttribute("playsinline", "");
document.body.appendChild(video);

const captureBtn = document.createElement("button");
captureBtn.innerText = "Capture Sky";
document.body.appendChild(captureBtn);

const canvas = document.createElement("canvas");
canvas.style.display = "none";
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");

// Request Camera Access
navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((err) => console.error("Camera error:", err));

captureBtn.addEventListener("click", () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Convert Image to Blob
  canvas.toBlob((blob) => {
    let formData = new FormData();
    formData.append("image", blob);

    // Send to Flask Backend
    fetch("/analyze", { method: "POST", body: formData })
      .then((res) => res.json())
      .then((data) => {
        if (data.level.includes("High")) {
          document.getElementById("noxMessage").style.display = "block";
          document.getElementById("lumaMessage").innerText = "Luma: The sky is too bright!";
        } else {
          document.getElementById("lumaMessage").innerText = "Luma: Great! The stars are visible!";
        }
      })
      .catch((err) => console.error("Error in fetching analysis:", err));
  }, "image/jpeg");
});
document.getElementById("sendButton").addEventListener("click", function() {
    let userInput = document.getElementById("userInput");
    let chatBox = document.getElementById("chatBox");
    
    let userMessage = userInput.value.trim();
    if (userMessage === "") return; // Stop empty messages

    // Display user message
    chatBox.innerHTML += `<p><b>You:</b> ${userMessage}</p>`;
    
    // Clear input box
    userInput.value = "";

    // Send message to Flask backend
    fetch("/chatbot", {
        method: "POST",
        body: JSON.stringify({ message: userMessage }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<p><b>Luma:</b> ${data.reply}</p>`;
    })
    .catch(error => console.error("Error:", error));
});


