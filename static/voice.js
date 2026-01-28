
let step = 0; 

function speak(text) {
    const msg = new SpeechSynthesisUtterance(text);
    msg.rate = 0.9; // slow voice a little
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(msg);
}

function startVoiceCompose() {
    step = 0;  // reset every time
    askNextQuestion();
}


function listen() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        document.getElementById("status").innerText = "You said: " + text;

        fetch("/voice_compose", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ text: text })
        })
        .then(res => res.json())
        .then(data => {
            speak(data.reply);
            setTimeout(listen, 1200);
        });
    };
    recognition.start();
}

function startCompose() {
    fetch("/voice_compose", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text: "" })
    })
    .then(res => res.json())
    .then(data => {
        speak(data.reply);
        setTimeout(listen, 1200);
    });
}

function loadInbox() {
    fetch("/inbox")
    .then(res => res.json())
    .then(data => {
        let html = "";
        data.forEach((mail, i) => {
            html += `<p><b>${i+1}. ${mail.subject}</b><br>${mail.from}<br>${mail.snippet}</p>`;
        });
        document.getElementById("emails").innerHTML = html;
    });
}
