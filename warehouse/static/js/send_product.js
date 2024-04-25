    // Show alert when button is clicked
    $('.show-alert').click(function () {
        alert("Button clicked!");
    });


// Send product to customer
    $('.send-product-icon').click(function () {
        var productId = $(this).data('send-product-id');
        console.log(productId);
        // Open modal to enter customer ID and quantity
        // Assuming you have a modal with ID 'sendProductModal'
        

        // Store the product ID in a hidden input field within the modal
        $('#sendProductModal').find('#send-product-id').val(productId);
        console.log("value set");
    });

$('#sendProductButton').on('click', function() {
    // var productId = $(this).data('send-product-id');
    var productId = $('#send-product-id').val();
    // alert(productId)
    console.log(productId, "product id")
    var quantity = $('#sendProductQuantity').val(); // Assuming you have an input field with ID 'sendProductQuantity'
    var customerId = $('#customerSelect').val(); // Assuming you have a select element with ID 'customerSelect' containing customer IDs
    $.ajax({
        url: '/send_product/',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ product_id: productId, quantity: quantity, customer_id: customerId }),
        success: function(response) {
            $('#sendProductModal').modal('hide');
            location.reload(); // Refresh the page
            $('.toast').toast('show');
            setTimeout(function() {
                $('.toast').toast('hide'); // Hide the toast after 3 seconds
            }, 3000);
        },
        error: function(xhr, status, error) {
            var errorMessage = xhr.responseJSON.error || 'An error occurred';
            alert(errorMessage);
        }
    });
});