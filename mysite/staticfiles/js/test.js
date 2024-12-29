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

// Chart
document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("spendingChart").getContext("2d");
    const chartData = JSON.parse('{{ chart_data|escapejs }}');

    new Chart(ctx, {
        type: "line", // Set chart type to line
        data: {
            labels: chartData.labels, // Pass the labels from Django
            datasets: [{
                label: '',
                //pointRadius: 10,
                borderColor: "rgba(0,0,255,1.0)", // Line color
                data: chartData.totals, // Totals from Django
                fill: false // Disable fill for pure line graph
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        display: false //this will remove only the label
                    }
                }],
                yAxes: [{
                    ticks: {
                        min: Math.min.apply(this, chartData.totals) - Math.min.apply(this, chartData.totals)*.1,
                        max: Math.max.apply(this, chartData.totals) + Math.min.apply(this, chartData.totals)*.1
                     }
                    }]

            },
            legend: {
                display: false
             },
             tooltips: {
                enabled: true,
             },
             elements: {
                point: {
                  backgroundColor: "rgba(0,0,255,1.0)",
                  radius: 5,
                  hoverRadius: 10,
                }
              },
              plugins: {
                legend: {
                    labels: {
                        // This more specific font property overrides the global property
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("spendingChart").getContext("2d");
    const chartData = JSON.parse('{{ chart_data|escapejs }}');

    new Chart(ctx, {
        type: "line", // Set chart type to line
        data: {
            labels: chartData.labels, // Pass the labels from Django
            datasets: [{
                label: '',
                //pointRadius: 10,
                borderColor: "rgba(0,0,255,1.0)", // Line color
                data: chartData.totals, // Totals from Django
                fill: false // Disable fill for pure line graph
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        display: false //this will remove only the label
                    }
                }],
                yAxes: [{
                    ticks: {
                        min: Math.min.apply(this, chartData.totals) - Math.min.apply(this, chartData.totals)*.1,
                        max: Math.max.apply(this, chartData.totals) + Math.min.apply(this, chartData.totals)*.1
                        }
                    }]

            },
            legend: {
                display: false
                },
                tooltips: {
                enabled: true,
                },
                elements: {
                point: {
                    backgroundColor: "rgba(0,0,255,1.0)",
                    radius: 5,
                    hoverRadius: 10,
                }
                },
                plugins: {
                legend: {
                    labels: {
                        // This more specific font property overrides the global property
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });
});
