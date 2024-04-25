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


          // Add event listener for double click on table rows
    $('#mahsulot-table tbody').on('dblclick', 'tr', function() {
        // Retrieve data from the clicked row
        var rowData = $(this).children('td').map(function() {
            return $(this).text();
        }).get();
        
        // Populate the modal with the retrieved data
        $('#productDetailsModal').find('.modal-body').html(
            '<p><strong>Nomi:</strong> ' + rowData[0] + '</p>' +
            '<p><strong>Kategoriya:</strong> ' + rowData[1] + '</p>' +
            '<p><strong>Qadoq:</strong> ' + rowData[2] + '</p>' +
            '<p><strong>Quti:</strong> ' + rowData[3] + '</p>' +
            '<p><strong>Massa:</strong> ' + rowData[4] + '</p>' +
            '<p><strong>Miqdori:</strong> ' + rowData[5] + '</p>' +
            '<p><strong>Kelgan sana:</strong> ' + rowData[6] + '</p>' +
            '<p><strong>Tavsifi:</strong> ' + rowData[7] + '</p>'
        );
        
        // Show the modal
        $('#productDetailsModal').modal('show');
    });
});