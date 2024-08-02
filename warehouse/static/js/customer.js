$(document).ready(function() {
    // Initialize DataTable
    $('#customer-table').DataTable({
            "lengthMenu": [10, 25, 50, 100], 
            "pageLength": 10,                
            "order": [[0, "asc"]],          
            "responsive": true,              
            "searching": true,               
            "pagingType": "full_numbers",    
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

$('#addCustomerForm').submit(function(event) {
    event.preventDefault(); 
    var formData = $(this).serialize();

    $.ajax({
        url: '/customer_crud/',
        method: 'POST',
        data: formData,
        success: function(response) {
            
            console.log('Customer added successfully:', response);
            $('#addCustomerModal').modal('hide');
            location.reload();
        },
        error: function(xhr, status, error) {
            console.error('Error adding customer:', error); 
        }
    });

});

// Edit customer button click event handler
$('.edit-customer').on('click', function() {
    var customerId = $(this).data('id');
    $.ajax({
        url: '/customer_crud/',
        method: 'GET',
        data: { id: customerId },
        success: function (response) {
            $('#editCustomerId').val(response.customer.id);
            $('#editCustomerName').val(response.customer.name);
            $('#editCustomerLocation').val(response.customer.location);
            $('#editCustomerPhoneNumber').val(response.customer.phone_number);
            
            // Show the edit customer modal
            $('#editCustomerModal').modal('show');
        },
        error: function (xhr, status, error) {
            // Handle errors
            alert('An error occurred while fetching customer data.');
        }
    });
});


$('#editCustomerForm').submit(function(event) {
    event.preventDefault();

    var formData = {
        id: $('#editCustomerId').val(), // Assuming you have an input field with ID 'editCustomerId'
        name: $('#editCustomerName').val(),
        location: $('#editCustomerLocation').val(),
        phone_number: $('#editCustomerPhoneNumber').val()
    };
    $.ajax({
        url: '/customer_crud/', // Adjust the URL as needed
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            $('#editCustomerModal').modal('hide');
            location.reload(); // Refresh the page
        },
        error: function(xhr, status, error) {
            var errorMessage = xhr.responseJSON.error || 'An error occurred';
            alert(errorMessage);
        }
    });
});


$('.delete-customer').on('click', function() {
    var customerId = $(this).data('customer-id'); // Access the data attribute
    // alert("this is id when clicked: " + customerId); // Alert to verify the ID
    $('#confirmCustomerDeleteButton').data('customer-id', customerId); // Set the data attribute on the confirm button
});


$(document).on('click', '#confirmCustomerDeleteButton', function() {
    var customerId = $(this).data('customer-id');

    $.ajax({
        url: '/customer_crud/',
        method: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify({ id: customerId }),
        success: function(response) {
            console.log("Customer deleted successfully");
            $('#confirmDeleteModal').modal('hide');
            location.reload();  // Refresh the page to reflect the changes
        },
        error: function(xhr, status, error) {
            var errorMessage = xhr.responseJSON ? xhr.responseJSON.error : 'An unknown error occurred';
            console.error("Deletion error:", errorMessage);
            alert(errorMessage);
        }
    });
});


 // Add event listener for double click on table rows
    $('#customer-table tbody').on('dblclick', 'tr', function() {
        // Retrieve data from the clicked row
        var rowData = $(this).children('td').map(function() {
            return $(this).text();
        }).get();
        
        // Populate the modal with the retrieved data
        $('#customerDetailsModal').find('.modal-body').html(
            '<p><strong>Name:</strong> ' + rowData[0] + '</p>' +
            '<p><strong>Location:</strong> ' + rowData[1] + '</p>' +
            '<p><strong>Phone Number:</strong> ' + rowData[2] + '</p>'
        );
        
        // Show the modal
        $('#customerDetailsModal').modal('show');
    });

       $(document).ready(function () {
        // Initialize tooltips
        $('[data-tooltip]').each(function () {
            $(this).tooltip({
                title: $(this).data('tooltip')
            });
        });
    });

});
