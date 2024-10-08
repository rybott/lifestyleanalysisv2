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
        data.forEach(item => {
            const p = document.createElement('p');
            p.innerHTML = `<strong>${item.Category} </strong>: $${item.Amount} [ ${item.Percent}% ]`;
            container.appendChild(p);
        });
    })

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