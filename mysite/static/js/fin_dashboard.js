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

// Function to fetch and display the chart
function fetchChartData(type) {
    let apiUrl = `/finance/api/${type.toLowerCase()}_sums/`; // Adjust the API URL based on the type

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Ensure the dates are correctly parsed
            const labels = data.map(item => {
                const date = new Date(item.day); // Create a new date object
                return date.toLocaleDateString(); // Convert the date to a readable string (e.g., "MM/DD/YYYY")
            });

            const amounts = data.map(item => -1 * parseFloat(item.total_amount)); // Negate the amounts

            // Get the canvas element for the chart
            const ctx = document.getElementById('dailySpendingChart').getContext('2d');

            // Clear any previous chart instance
            if (window.chartInstance) {
                window.chartInstance.destroy();
            }

            // Create the chart
            window.chartInstance = new Chart(ctx, {
                type: 'line', // Line chart type
                data: {
                    labels: labels, // X-axis labels (formatted dates)
                    datasets: [{
                        label: `${type} Spending`,
                        data: amounts, // Y-axis data (negated spending amounts)
                        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light blue background
                        borderColor: 'rgba(75, 192, 192, 1)', // Darker blue border
                        borderWidth: 2,
                        fill: false, // Disable filling under the line
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Date',
                            },
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Amount Spent ($)',
                            },
                            ticks: {
                                callback: function(value) {
                                    return '$' + value; // Add dollar sign to Y-axis labels
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching spending data:', error));
}

// Function to handle filter changes
function handleFilterChange() {
    const filter = document.getElementById('Expense_Chart_Filter').value; // Get the selected value
    fetchChartData(filter); // Fetch data based on the selected filter
}

// Set up the event listener for the select dropdown
document.getElementById('Expense_Chart_Filter').addEventListener('change', handleFilterChange);

// Fetch the default chart data for "Weekly" on page load
document.addEventListener('DOMContentLoaded', function() {
    fetchChartData('Weekly'); // Fetch weekly data by default
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