(() => {
    const handleCopy = (event) => {
        const button = event.target.closest(".sc-copy");
        if (!button) return;

        const message = button.dataset.message;
        if (!message) return;

        navigator.clipboard?.writeText(message).then(() => {
            const original = button.textContent;
            button.textContent = "Copied!";
            button.disabled = true;
            setTimeout(() => {
                button.textContent = original;
                button.disabled = false;
            }, 1400);
        });
    };

    document.addEventListener("click", handleCopy);
})();
