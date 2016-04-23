(function ($)
{
    function to_file_uploader(btn_file, url, on_click, on_success, on_error)
    {
        btn_target = $('#' + btn_file.attr('id') + '-visible');
        btn_file.hide();
        btn_file.click(function()
        {
            btn_file.val('');
        });
        btn_file.change(function()
        {
            if (btn_file.val() !== '')
            {
                on_click();
                var formData = new FormData(btn_file.parent()[0]);
                $.ajax({
                    url: url,
                    type: 'POST',
                    success: on_success,
                    error: on_error,
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                });
            }
        });
        btn_target.click(function(){btn_file.trigger('click'); return false})
    }

    $.fn.file_uploader = function(options)
    {
        var settings = $.extend({
            on_click: function(){},
            on_success: function(){},
            on_error: function(){}
            }, options);
        to_file_uploader(
            this, settings.url,
            settings.on_click, settings.on_success, settings.on_error);
        return this;
    };
}(jQuery));