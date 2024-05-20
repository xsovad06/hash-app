document.getElementById("hash-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    var algorithm = document.getElementsByClassName("active")[0].value;
    var message = document.getElementById("message").value;

    var response = await fetch("/hash", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ algorithm: algorithm, message: message })
    });

    var result = await response.json();

    document.getElementById("result").classList.remove('hidden');
    document.getElementById("your-message").innerText = result.message;
    document.getElementById("your-algorithm").innerText = result.algorithm;
    var hashResElem = document.getElementById("hash-result");
    // clear before writing result
    hashResElem.innerHTML = '';
    const paragraph = document.createElement('p');
    paragraph.innerText = result.hash;
    hashResElem.appendChild(paragraph);

    const button = document.createElement('button');
    button.id = 'copy-button';
    button.className = 'px-1 ml-auto';
    const icon = document.createElement('i');
    icon.className = 'fas fa-copy green-icon';
    button.appendChild(icon);

    hashResElem.appendChild(button);
});

// Add event listener to the parent element of the copy button
document.getElementById("hash-result").addEventListener("click", async function (event) {
    if (event.target.id === "copy-button") {
        const hashResult = event.target.previousElementSibling.innerText;
        try {
            await navigator.clipboard.writeText(hashResult);
            alert("Hash copied to clipboard!");
        } catch (error) {
            console.error("Failed to copy hash to clipboard: ", error);
        }
    }
});

const algorithmButtons = document.querySelectorAll('.algorithm-button');

algorithmButtons.forEach(button => {
    button.addEventListener('click', () => {
        algorithmButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
    });
});