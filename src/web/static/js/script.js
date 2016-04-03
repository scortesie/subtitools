function render_subtitles(subtitles_html)
{
    $.ajax({
        url: 'subtitles/',
        type: 'GET',
        success: function(data){$('#subtitles').html(data)},
        error: function(data){$('#subtitles').html('Error')},
    });
}
function to_file_button(btn_file, btn_target)
{
    btn_file.hide()
    btn_file.click(function()
    {
        btn_file.val('')
    })
    btn_file.change(function()
    {
        if (btn_file.val() !== '')
        {
            var formData = new FormData($('#form_upload')[0]);
            $.ajax({
                url: 'upload/',
                type: 'POST',
                success: render_subtitles,
                error: function(data, status){$('#subtitles').html('Error')},
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
            });
        }
    })
    btn_target.click(function(){btn_file.trigger('click'); return false})
}
