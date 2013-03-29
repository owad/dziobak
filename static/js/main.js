function createAutoClosingAlert(selector, delay) {
   var alert = $(selector).alert();
   window.setTimeout(function() { alert.alert('close') }, delay);
}

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

    createAutoClosingAlert(".alert", 5000);
});

