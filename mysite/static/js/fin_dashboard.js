// Fetch category names and populate the drop-down
fetch('/finance/api/category_names')
    .then(response => response.json())
    .then(data => {
        const categorySelect = document.getElementById('category-name');

        // Populate dropdown options with category names
        data.forEach(category => {
            const option = document.createElement('option');
            option.value = category;  // Option value is the category name
            option.text = category;   // Option label is the category name
            categorySelect.add(option);
        });
    });

//Top Expenses
fetch('/finance/api/top_expenses/')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('TopExpenses');

        // Calculate the maximum length of the category and amount for alignment
        const maxCategoryLength = Math.max(...data.map(item => item.Category.length));
        const maxAmountLength = Math.max(...data.map(item => `$${item.Amount}`.length));

        data.forEach(item => {
            const p = document.createElement('p');

            // Get the lengths of the current category and amount
            const category = item.Category;
            const amount = `$${item.Amount}`;

            // Calculate the number of spaces needed for alignment between category and amount
            const categorySpaceCount = maxCategoryLength - category.length +1; // Extra 1 space for padding
            const categorySpaces = '&nbsp;'.repeat(categorySpaceCount);

            // Calculate the number of spaces needed between amount and percent
            const amountSpaceCount = maxAmountLength - amount.length + 2; // Extra 1 space for padding
            const amountSpaces = '&nbsp;'.repeat(amountSpaceCount);

            // Set the innerHTML with aligned category, amount, and percentage
            p.innerHTML = `<strong>${category}</strong>${categorySpaces}${amount}${amountSpaces}${item.Percent}%`;
            container.appendChild(p);
        });
    });



// Filter Button
document.getElementById('filter-form').addEventListener('change', () => {
    // Update display dynamically
    const category = document.getElementById('category-name').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const excludeNocount = document.getElementById('exlude-nocount').checked ? 'checked' : '';

    const categoryDisplay = category ? category : 'All Categories';

    document.querySelector('.filter-display').innerHTML = `
        <p>Category: ${categoryDisplay}</p>
        <p>From: ${startDate}</p>
        <p>Until: ${endDate}</p>
        <p>Excluded Do Not Count: ${excludeNocount}</p>
    `;
});
const toggleButton = document.getElementById('toggle-button');
const formContainer = document.getElementById('form-container');

toggleButton.addEventListener('click', () => {
formContainer.classList.toggle('active');
});
