$(function(){
    $('.js-subscription').ajaxForm({
        beforeSend: function(){
            $('.js-subscription-fail').hide();
        },
        success: function(response){
            if (response == 'OK') {
                $('.js-subscription').hide();
                $('.js-subscription-ok').show();
            } else {
                $('.js-subscription-fail').show();
            }
        }
    });
});
