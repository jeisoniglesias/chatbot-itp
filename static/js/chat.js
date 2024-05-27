document.addEventListener("DOMContentLoaded", (event) => {
    const toastTrigger = document.getElementById("liveToastBtn");
    const toastLiveExample = document.getElementById("liveToast");

    //const geocode = JSON.parse(document.getElementById("chat-data").dataset.geocode);
    const chatData = document.querySelector('.card-body').dataset.chat;

    console.log(chatData);
    console.log(chatData.length);

    showClearBTN(chatData);
    const showToast = () => {
        const toastBootstrap =
            bootstrap.Toast.getOrCreateInstance(toastLiveExample);
        toastBootstrap.show();
        toastTrigger.style.display = "none";
    };
    
    if (toastTrigger) {

        if (chatData.length > 2) {
            showToast();
        }
        toastTrigger.addEventListener("click", () => {
            showToast();
        });

        toastLiveExample.addEventListener("hidden.bs.toast", () => {
            toastTrigger.style.display = "block";
        });
    }
});

function adjustTextarea(textarea) {
    if (textarea.value.length > 0) {
        textarea.rows = 3;
    } else {
        textarea.rows = 1;
    }
}
function showClearBTN(chatData) {
    const clearButton = document.getElementById('clearChatButton');

    if (chatData.length > 2) {
        clearButton.style.display = 'block';
    } else {
        clearButton.style.display = 'none';
    }
}
function clearSession() {
    fetch('/clear_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Failed to clear session');
        }
    });
}