// ─────────────────────────────────────────────
// index.js — Home page only scripts
// ─────────────────────────────────────────────

// Search on Enter key press
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            document.getElementById('searchForm').submit();
        }
    });
}
