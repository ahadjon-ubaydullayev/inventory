 $(document).ready(function() {
        var mostProductsData = {
        labels: ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        datasets: [{
            label: 'Quantity',
            data: [50, 30, 20, 10, 5], // Example data, replace with actual data from backend
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1
        }]
    };

    // Render bar chart using Chart.js
    var mostProductsChart = new Chart(document.getElementById('mostProductsChart'), {
        type: 'bar',
        data: mostProductsData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    // AJAX request to fetch data for the most products in storage
    
// Fetch data for most received products from backend (replace this with your actual AJAX call)
    var mostReceivedData = {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [{
            label: 'Quantity Received',
            data: [100, 150, 200, 250, 300], // Example data, replace with actual data from backend
            fill: true,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };

    // Render area chart for most received products using Chart.js
    var mostReceivedChart = new Chart(document.getElementById('mostReceivedChart'), {
        type: 'line',
        data: mostReceivedData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    // Fetch data for most sent products from backend (replace this with your actual AJAX call)
    var mostSentData = {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [{
            label: 'Quantity Sent',
            data: [80, 120, 180, 200, 220], // Example data, replace with actual data from backend
            fill: true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    };

    // Render area chart for most sent products using Chart.js
    var mostSentChart = new Chart(document.getElementById('mostSentChart'), {
        type: 'line',
        data: mostSentData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });


    // function fetchChartData() {
    //     $.ajax({
    //         url: '/dashboard_charts_data/',
    //         type: 'GET',
    //         success: function(response) {
    //             var mostProductsData = response.most_products;
    //             var chartLabels = mostProductsData.map(function(product) {
    //                 return product.name;
    //             });
    //             var chartData = mostProductsData.map(function(product) {
    //                 return product.quantity;
    //             });
    //             updateBarChart(chartLabels, chartData);
    //         },
    //         error: function(error) {
    //             console.error('Error fetching chart data:', error);
    //         }
    //     });
    // }

    // // Call the fetch function when the page loads
    // fetchChartData();

    // // Sample function to update bar chart using Chart.js (you'll need to replace it with your actual chart library)
    // function updateBarChart(labels, data) {
    //     // Sample code to update the chart (you'll need to replace it with your actual chart update logic)
    //     var ctx = document.getElementById('bar-chart').getContext('2d');
    //     var myChart = new Chart(ctx, {
    //         type: 'bar',
    //         data: {
    //             labels: labels,
    //             datasets: [{
    //                 label: 'Most Products in Storage',
    //                 data: data,
    //                 backgroundColor: 'rgba(54, 162, 235, 0.5)',
    //                 borderColor: 'rgba(54, 162, 235, 1)',
    //                 borderWidth: 1
    //             }]
    //         },
    //         options: {
    //             scales: {
    //                 yAxes: [{
    //                     ticks: {
    //                         beginAtZero: true
    //                     }
    //                 }]
    //             }
    //         }
    //     });
    // }



});