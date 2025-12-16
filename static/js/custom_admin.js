
document.addEventListener("DOMContentLoaded", function () {
    // Select all table rows in the results table, excluding the header
    const rows = document.querySelectorAll('#result_list tbody tr');

    rows.forEach(row => {
        // Add click event listener to the row
        row.addEventListener('click', function (e) {
            // Avoid conflict if the user clicks a checkbox or a link directly
            // Avoid conflict if the user clicks a checkbox, link, input, select, or label directly
            const tagName = e.target.tagName;
            if (
                e.target.type === 'checkbox' ||
                tagName === 'A' ||
                tagName === 'INPUT' ||
                tagName === 'SELECT' ||
                tagName === 'TEXTAREA' ||
                tagName === 'OPTION' ||
                tagName === 'LABEL' ||
                e.target.closest('a') ||
                e.target.closest('select') ||
                e.target.closest('input')
            ) {
                return;
            }

            // Find the first anchor tag (link) in the row (usually the ID or first column)
            const firstLink = row.querySelector('th a') || row.querySelector('td a');

            if (firstLink) {
                // Redirect to the link's URL
                window.location.href = firstLink.href;
            }
        });

        if (row) {
            row.style.cursor = 'pointer';
        }
    });



    // -------------------------------------------------------
    // FILTER HEADINGS & CLEANUP
    // -------------------------------------------------------



    // -------------------------------------------------------
    // AJAX FILTERING (No Page Reload)
    // -------------------------------------------------------

    // Function to re-initialize everything after AJAX reload
    const reInitUI = () => {
        // 1. Re-apply clickable rows
        const rows = document.querySelectorAll('#result_list tbody tr');
        rows.forEach(row => {
            row.addEventListener('click', function (e) {
                const tagName = e.target.tagName;
                if (
                    e.target.type === 'checkbox' ||
                    tagName === 'A' ||
                    tagName === 'INPUT' ||
                    tagName === 'SELECT' ||
                    tagName === 'TEXTAREA' ||
                    tagName === 'OPTION' ||
                    tagName === 'LABEL' ||
                    e.target.closest('a') ||
                    e.target.closest('select') ||
                    e.target.closest('input')
                ) {
                    return;
                }
                const firstLink = row.querySelector('th a') || row.querySelector('td a');
                if (firstLink) {
                    window.location.href = firstLink.href;
                }
            });
            row.style.cursor = 'pointer';
        });


    };

    // Initial Run
    // (Note: The observers above handle dynamic Select2, but we need to re-run row clicks)
    // The previous row-click code at top of file runs on DOMContentLoaded.
    // We will now hook into the filter form.

    const filterForm = document.querySelector('#changelist-search') || document.querySelector('#changelist-form');
    // Jazzmin usually puts filters in #changelist-search or a separate bar. 
    // We need to look for the select inputs that control filtering.

    // Try to find the filter inputs (Jazzmin top filters)
    const filterSelects = document.querySelectorAll('#changelist-search select, #toolbar form select, .actions select');

    filterSelects.forEach(select => {
        // Remove old listeners to be safe (though cloning or fresh selection handles this)
        select.addEventListener('change', function (e) {
            // Only hijacking if it's a filter, not an "Action" (delete selected)
            if (this.name === 'action') return;

            // Trigger AJAX update
            updateChangeList(this.closest('form'));
        });
    });

    // Handle Search Submit
    const searchForm = document.querySelector('#changelist-search');
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();
            updateChangeList(this);
        });
    }

    async function updateChangeList(form) {
        if (!form) return;

        // Visual Feedback (Opacity)
        const contentDiv = document.querySelector('#changelist');
        if (contentDiv) contentDiv.style.opacity = '0.5';

        try {
            // Construct URL
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            const url = `${window.location.pathname}?${params.toString()}`;

            // Fetch new HTML
            const response = await fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const html = await response.text();

            // Parse HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // Swap #changelist content
            const newContent = doc.querySelector('#changelist');
            if (newContent && contentDiv) {
                contentDiv.innerHTML = newContent.innerHTML;

                // Update Browser URL
                window.history.pushState({}, '', url);

                // Re-init UI features
                reInitUI();
            }
        } catch (error) {
            console.error('AJAX Filter Error:', error);
            // Fallback: reload page
            // form.submit(); 
        } finally {
            if (contentDiv) contentDiv.style.opacity = '1';
        }
    }

});
