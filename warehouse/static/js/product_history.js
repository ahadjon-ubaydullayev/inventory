  $(document).ready(function() {
        $('#customer-history-table').DataTable({
            "lengthMenu": [10, 25, 50, 100], // Items per page options
            "pageLength": 10, // Initial page length
            "order": [], // Disable initial sorting
            "searching": true, // Enable search functionality
            "pagingType": "full_numbers", // Pagination type
            "language": {
                "lengthMenu": "Show _MENU_ entries",
                "search": "_INPUT_",
                "searchPlaceholder": "Search...",
                "paginate": {
                    "first": '<i class="fas fa-angle-double-left"></i>',
                    "last": '<i class="fas fa-angle-double-right"></i>',
                    "next": '<i class="fas fa-angle-right"></i>',
                    "previous": '<i class="fas fa-angle-left"></i>'
                }
            }
        });


   
// Handle double-click on table rows to show product details
$('#mahsulot-table tbody').on('dblclick', 'tr', function() {
    // Retrieve data from the clicked row
    var rowData = $(this).children('td').map(function() {
        return $(this).text();
    }).get();

    // Populate the modal with the details
    // $('#product-detail-id').text(rowData[0]);
    // $('#product-detail-name').text(rowData[1]);
    // $('#product-detail-category').text(rowData[2]);
    // $('#product-detail-price').text(rowData[3]);
    // $('#product-detail-stock').text(rowData[4]);
    // $('#product-detail-description').text(rowData[5]);
    
    $('#product-detail-id').text(rowData[0]);
    $('#product-detail-name').text(rowData[1]);
    $('#product-detail-category').text(rowData[2]);
    $('#product-detail-package').text(rowData[3]);
    $('#product-detail-box').text(rowData[4]);
    $('#product-detail-weight').text(rowData[5]);
    $('#product-detail-quantity').text(rowData[6]);
    $('#product-detail-added-date').text(rowData[7]);
    $('#product-detail-description').text(rowData[8]);

    // Show the modal
    $('#productDetailsModal').modal('show');
});

});