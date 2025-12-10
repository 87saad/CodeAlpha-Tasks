const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBody = document.getElementById("chat-body");

window.onload = () => {
    const startupMessage = "Hello! I am the **CodeAlpha AI Assistant**! I will provide you with all internship details, submission methods, task details, and general help. How can I assist you today? 🚀";
    addMessage(startupMessage, "bot");
    
    
    setTimeout(() => {
        addMessage("You can start by asking about: **Tasks, Perks, Certificates, or Contact Info.**", "bot");
    }, 1500); 
};


async function askBot(message) {
    try {
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ msg: message })
        });
        const data = await response.json();
        return data.answer;
    } catch (error) {
        
        return "Backend is not running. Please start the Python Flask app (Chatbot.py) first.";
    }
}

sendBtn.addEventListener("click", async () => {
    let msg = userInput.value;
    if(!msg) return;

    addMessage(msg, "user");
    userInput.value = "";

    const botAnswer = await askBot(msg);
    addMessage(botAnswer, "bot");
});

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `msg ${sender}-msg`;
    div.innerText = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
}
