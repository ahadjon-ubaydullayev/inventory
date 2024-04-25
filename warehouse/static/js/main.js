// for base html
 document.querySelectorAll('.extendable-link').forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default behavior of the link
            var submenu = this.nextElementSibling; // Get the submenu element
            if (submenu.classList.contains('show')) {
                submenu.classList.remove('show'); // Hide the submenu if it's already visible
            } else {
                submenu.classList.add('show'); // Show the submenu
            }
        });
    });

      function addOrUpdateProduct(data) {
            $.ajax({
                url: '/mahsulot_crud/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for Django
                },
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function (response) {
                    console.log(response);
                    // Handle response data as needed
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        }



// for mahsulotlar html
$(document).ready(function () {
    $('#addMahsulotForm').submit(function (event) {
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            url: '/mahsulot_crud/',
            method: 'POST',
            data: formData,
            success: function (response) {
                location.reload();
            },
            error: function (xhr, status, error) {
                var errorMessage = xhr.responseJSON.error || 'An error occurred';
                alert(errorMessage);
            }
        });
    });

    $('#mahsulot-table').DataTable({
        "lengthMenu": [10, 25, 50, 100],
        "pageLength": 10, // Initial page length
        "order": [[0, "asc"]], // Sort by the first column (Name) by default
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

// add existing product
    $('.add-existing-product').click(function () {
        var productId = $(this).data('id');
        $.ajax({
            url: '/get_product_data/', 
            method: 'GET',
            data: { id: productId },
            success: function (response) {

                $('#existingProductId').val(response.id);
                $('#existingProductName').val(response.nomi);
                $('#existingProductCategory').val(response.kategoriya);
                $('#existingProductQadoq').val(response.qadoq);
                $('#existingProductQuti').val(response.quti);
                $('#existingProductMassa').val(response.massa);
                $('#existingProductDescription').val(response.tavsifi);
                $('#existingProductQuantity').val(response.miqdori);
                $('#addExistingProductModal').modal('show');
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });


// SAVE THE MODIFIED PRODUCT
$('#addExistingProductForm').submit(function (event) {

    
    var formData = {
        id: $('#existingProductId').val(),  // Assuming you have an input field with ID 'productId'
        nomi: $('#existingProductName').val(),
        kategoriya: $('#existingProductCategory').val(),
        qadoq: $('#existingProductQadoq').val(),
        quti: $('#existingProductQuti').val(),
        massa: $('#existingProductMassa').val(),
        miqdori: $('#existingProductQuantity').val(),
        // kelgan_sana: $('#productKelganSana').val(),
        tavsifi: $('#existingProductDescription').val()
    };

    $.ajax({
        url: '/mahsulot_crud/',
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function (response) {
            $('#addExistingProductModal').modal('hide');
            location.reload();
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.responseJSON.error || 'An error occurred';
            alert(errorMessage);
        }
    });
});

// delete product
$('.delete-product-icon').on('click', function() {
    var productId = $(this).closest('.btn').data('product-id');
    $('#confirmDeleteButton').data('product-id', productId);
});

$('#confirmDeleteButton').on('click', function() {
    var productId = $(this).closest('.btn').data('product-id');
    $.ajax({
        url: '/mahsulot_crud/',
        method: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify({ id: productId }),
        success: function (response) {
            // alert('Mahsulot deleted successfully');
            $('#confirmDeleteModal').modal('hide');
            location.reload(); 
            $('.toast').toast('show');
            setTimeout(function() {
                $('.toast').toast('hide'); // Hide the toast after 3 seconds
                }, 3000);
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.responseJSON.error || 'An error occurred';
            alert(errorMessage);
        }
    });
      });


});



