function render_preview(data)
{
    $("#section-workspace").html(data);
    $("#section-toolbar").show();
}

function render_error(data)
{
    $("#section-workspace").html("Error");
}

function get_preview()
{
    $.ajax({
        url: 'preview/',
        type: 'GET',
        success: render_preview,
        error: render_error,
    });
}
