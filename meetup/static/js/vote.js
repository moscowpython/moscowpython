$(function(){
    $(document).on('click', '.js-vote', function(){
        var $link = $(this);
        var $error = $link.find('.vote__error');

        $error.text('');
        $.ajax({
            url: $link.data('href'),
            type: 'POST',
            success: function(response){
                try {
                    location.href = response;
                } catch (e) {
                    $link.find('.vote__success').text('Голос принят');
                }
            },
            error: function(xhr){
                $error.text(xhr.responseText);
            }
        });
    });
});
