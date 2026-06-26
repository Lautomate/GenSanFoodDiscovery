// ─────────────────────────────────────────────
// login.js — Login page only scripts
// ─────────────────────────────────────────────

// Toggle password field visibility
// Called by the eye button next to the password field
function togglePassword(buttonElement) {
    const wrapper = buttonElement.closest('.input-wrapper');
    const field = wrapper.querySelector('input');
    field.type = field.type === 'password' ? 'text' : 'password';
}
