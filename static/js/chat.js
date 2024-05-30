document.addEventListener("DOMContentLoaded", (event) => {
    const toastTrigger = document.getElementById("liveToastBtn");
    const toastLiveExample = document.getElementById("liveToast");

    //const geocode = JSON.parse(document.getElementById("chat-data").dataset.geocode);
    const chatData = document.querySelector('.card-body').dataset.chat;
    // Obtener el contenedor
    const container = document.querySelector('.card-body');

    // Agregar un observador de mutaciones para detectar cambios en el contenedor
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(container, { childList: true });

    // Función para desplazar el scroll hasta el final
    function scrollToBottom() {
        container.scrollTop = container.scrollHeight;
    }

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
    ;
});


document.addEventListener("DOMContentLoaded", function () {
    const chatContainer = document.getElementById('chat-data');

    // Función para desplazar el contenedor hasta el final
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Desplazar al final cuando se cargue el contenido
    scrollToBottom();

    // Observador de mutaciones para detectar cambios en el contenido
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(chatContainer, { childList: true, subtree: true });
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

document.querySelectorAll('.follow_up').forEach(item => {
    item.addEventListener('click', function () {
        const value = this.getAttribute('data-value');
        const form = document.getElementById('answerForm');
        const textarea = document.getElementById('payload');

        textarea.value = value;
        setTimeout(() => {
            form.submit();
        }, 200);
        this.classList.add('hidden');

    });
});