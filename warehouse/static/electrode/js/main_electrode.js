$(document).ready(function () {
    $('#electrode-table').DataTable({
    "lengthMenu": [10, 25, 50, 100],
    "pageLength": 10, // Initial page length
    "order": [[0, "desc"]], // Sort by the first column (Name) by default
    "responsive": true,
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

// Function to populate labels in the form
function populateLabels() {
    $.ajax({
        url: '/elektrod/api/labels/', // Replace with your API endpoint
        type: 'GET', 
        success: function (response) {
            $('#label').empty();
            $.each(response, function (index, label) {
                $('#label').append($('<option>', {
                    value: label.id,
                    text: label.label_name
                }));
            });
        }
    });
}
populateLabels();

// Handle form submission
$('#addElectrodeForm').submit(function (event) {
    event.preventDefault();
    var formData = {
        label_id: $('#label').val(),
        category_id: $('#category').val(),
        package: $('#package').val(),
        // box: $('#box').val(),
        // weight: $('#weight').val(),
        // count_by_label: $('#count_by_label').val(),
        description: $('#description').val()
    };

    $.ajax({
        url: '/elektrod/electrode_crud/',
        type: 'POST', 
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function (response) {
            // Reload the page or update the table with the new data
            // Example: window.location.reload();
                $('#addElectrodeModal').modal('hide');
            location.reload();
            // console.log(response);
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.responseJSON.error || 'An error occurred';
            alert(errorMessage);
            // console.error(xhr.responseText);
        }
    });
});
populateCategories();
    
function populateCategories() {
        
    var labelId = $('#label').val() ? $('#label').val() : '1';
    console.log(labelId);
    $.ajax({
        url: '/elektrod/api/categories/?label_id=' + labelId, // Adjust the endpoint to accept label_id parameter
        type: 'GET',
        success: function (response) {
            $('#category').empty();
            $.each(response, function (index, category) {
                $('#category').append($('<option>', {
                    value: category.id,
                    text: category.category_name
                }));
            });
        }
    });
}

// Listen for changes in the label field and update categories accordingly
$('#label').change(function () {
    populateCategories();
});

$(document).on('click', '.add-existing-electrode', function () {
    var electrodeId = $(this).data('id');
    $.ajax({
        url: '/elektrod/get_electrode_data/',
        method: 'GET',
        data: { id: electrodeId },
        success: function (response) {
            $('#existingElectrodeId').val(response.id);
            $('#existingElectrodeLabel').val(response.label);
            $('#existingElectrodeCategory').val(response.category);
            // $('#existingElectrodePackage').val(response.package); // Populate package field
            // Add logic to populate other fields as needed
            $('#addExistingElectrodeModal').modal('show');
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
});

// SAVE THE MODIFIED ELECTRODE
$('#addExistingElectrodeForm').submit(function (event) {
    event.preventDefault(); // Prevent default form submission

    var formData = {
        id: $('#existingElectrodeId').val(),
        label: $('#existingElectrodeLabel').val(),
        category: $('#existingElectrodeCategory').val(),
        package: $('#existingElectrodePackage').val(),
        // Add other fields as needed
        description: $('#existingElectrodeDescription').val() // Example field
    };
    

    $.ajax({
        url: '/elektrod/electrode_crud/', // Adjust URL as per your Django URL pattern
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function (response) {
            $('#addExistingElectrodeModal').modal('hide');
            location.reload(); // Reload the page after successful submission
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.responseJSON.error || 'An error occurred';
            alert(errorMessage);
        }
    });
});

// Populate the modal with electrode ID when the send button is clicked
$('#sendElectrodeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var electrodeId = button.data('id');
    var modal = $(this);
    modal.find('#electrode-id').val(electrodeId);
});

// Handle form submission
$('#send-electrode-btn').on('click', function () {
    var form = $('#send-electrode-form');
    $.ajax({
        url: '/elektrod/send_electrode/',
        method: 'POST',
        data: JSON.stringify({
            electrode_id: form.find('#electrode-id').val(),
            quantity: form.find('#quantity').val(),
            customer_id: form.find('#customer-id').val()
        }),
        headers: {
            'Content-Type': 'application/json'
        },
        success: function (response) {
            $('#sendElectrodeModal').modal('hide');
            location.reload();
        },
        error: function (response) {
            alert('Error: ' + response.responseJSON.error);
        }
    });
});

$('#electrode-table tbody').on('dblclick', 'tr', function () {
    // Retrieve data from the clicked row
    var rowData = $(this).children('td').map(function () {
        return $(this).text();
    }).get();

    // Populate the modal with the details
    $('#detail-id').text(rowData[0]);
    $('#detail-label').text(rowData[1]);
    $('#detail-category').text(rowData[2]);
    $('#detail-package').text(rowData[3]);
    $('#detail-box').text(rowData[4]);
    $('#detail-weight').text(rowData[5]);
    $('#detail-count-by-label').text(rowData[6]);
    $('#detail-added-date').text(rowData[7]);
    $('#detail-description').text(rowData[8]);

    // Show the modal
    $('#electrodeDetailsModal').modal('show');
});

//Delete Electrode
$('.delete-electrode').on('click', function () {
    var electrodeId = $(this).data('id');
    $('#confirm-delete-electrode-btn').data('electrode-id', electrodeId);
});

// Handle confirm delete button click
$('#confirm-delete-electrode-btn').on('click', function () {
    var electrodeId = $(this).data('electrode-id');
    $.ajax({
        url: '/elektrod/electrode_crud/',
        method: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify({ id: electrodeId }),
        success: function (response) {
            $('#deleteElectrodeModal').modal('hide');
            location.reload(); // Reload the page to reflect changes in the table
        },
        error: function (response) {
            var errorMessage = response.responseJSON.error || 'An error occurred';
            alert(errorMessage);
        }
    });
});

// Populate the modal with electrode ID when the send button is clicked
$('#sendElectrodeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var electrodeId = button.data('id');
    var modal = $(this);
    modal.find('#electrode-id').val(electrodeId);
});


//add your code here

});