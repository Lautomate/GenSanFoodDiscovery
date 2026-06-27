// ─────────────────────────────────────────────
// create_store.js — Create store page only scripts
// ─────────────────────────────────────────────

// Character counter for the description textarea
// Shows how many characters are left out of 500
const description = document.getElementById('description');
const counter = document.getElementById('charCounter');

if (description && counter) {
    // Update counter on every keystroke
    description.addEventListener('input', function () {
        const current = this.value.length;
        const max = 500;
        const remaining = max - current;

        counter.textContent = `${current} / ${max} characters`;

        // Warn when getting close to the limit
        if (remaining < 50) {
            counter.classList.add('near-limit');
        } else {
            counter.classList.remove('near-limit');
        }
    });
}
