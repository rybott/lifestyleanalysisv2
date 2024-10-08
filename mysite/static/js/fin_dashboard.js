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

// Function to create the chart with given data
function createChart(labels, spendingData, incomeData, chartType) {
    const ctx = document.getElementById('spendingChart').getContext('2d');

    // Clear previous chart instance
    if (window.chartInstance) {
        window.chartInstance.destroy();
    }

    // Create the chart
    window.chartInstance = new Chart(ctx, {
        type: chartType, // 'line', 'bar', or any other chart type
        data: {
            labels: labels, // X-axis labels (formatted dates)
            datasets: [
                {
                    label: 'Spending',
                    data: spendingData, // Y-axis data for spending amounts
                    backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light blue background
                    borderColor: 'rgba(75, 192, 192, 1)', // Darker blue border
                    borderWidth: 2,
                    fill: false // Disable filling under the line
                },
                {
                    label: 'Income',
                    data: incomeData, // Y-axis data for income
                    backgroundColor: 'rgba(192, 75, 75, 0.2)', // Light red background
                    borderColor: 'rgba(192, 75, 75, 1)', // Darker red border
                    borderWidth: 2,
                    fill: false // Disable filling under the line
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Amount ($)'
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
}

// Function to get data for the selected chart type
function getChartData(type) {
    let sums;
    switch (type) {
        case 'Daily':
            sums = dailySums;
            break;
        case 'Weekly':
            sums = weeklySums;
            break;
        case 'Monthly':
            sums = monthlySums;
            break;
    }

    const labels = sums.map(item => {
        const date = new Date(item.day); // Convert the string date to Date object
        return date.toLocaleDateString('en-US'); // Convert to readable format
    });

    const spendingData = sums.map(item => parseFloat(item.total_amount));
    const incomeData = spendingData.map(() => 0); // Replace with actual income data if needed

    createChart(labels, spendingData, incomeData, 'line'); // Create the chart as a line chart
}

// Handle chart type selection
document.getElementById('Expense_Chart_Filter').addEventListener('change', function() {
    const selectedType = this.value;
    getChartData(selectedType); // Fetch the appropriate data for the selected type
});

// Initialize chart on page load with weekly data
document.addEventListener('DOMContentLoaded', function() {
    getChartData('Weekly'); // Load the weekly data by default
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