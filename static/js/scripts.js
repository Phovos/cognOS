document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('[data-collapse-toggle="mobile-menu"]');
    const menu = document.querySelector('#mobile-menu');
    // Ensure the mobile menu is hidden initially
    menu.style.display = 'none';
    toggleButton.addEventListener('click', () => {
        if (menu.style.display === 'none') {
            menu.style.display = 'block';
        } else {
            menu.style.display = 'none';
        }
    });

    const executeBtn = document.getElementById('execute-btn');
    const replInput = document.getElementById('repl-input');
    const replOutput = document.getElementById('repl-output');

    executeBtn.addEventListener('click', () => {
        const query = replInput.value;
        fetch('/repl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => response.json())
        .then(data => {
            replOutput.textContent = data.result;
        })
        .catch((error) => {
            console.error('Error:', error);
            replOutput.textContent = 'An error occurred while processing your request.';
        });
    });
});