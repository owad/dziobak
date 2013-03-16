$(document).ready(function() {
    $('.search-submit').click(function() {
        var form = $('#search-form');
        if (this.id == 'client-search') {
            form.attr('action', CLIENT_LIST);
        }
        if (this.id == 'product-search') {
            form.attr('action', PRODUCT_LIST);
        }
        form.submit();
    });

    $('#search-options').removeClass('open'); 
});

