function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function setupLiveSearch(inputSelector, tableSelector, columnIndices) {
    const searchInput = document.querySelector(inputSelector);
    const table = document.querySelector(tableSelector);
    const rows = table.querySelectorAll('tbody tr');

    const filterRows = debounce(() => {
        const searchText = searchInput.value.toLowerCase();

        rows.forEach(row => {
            let textToSearch = '';
            columnIndices.forEach(index => {
                const cell = row.cells[index];
                if (cell) {
                    textToSearch += cell.textContent.toLowerCase() + ' ';
                }
            });

            if (textToSearch.includes(searchText)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }, 300);

    searchInput.addEventListener('input', filterRows);
} 