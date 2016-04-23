function render_preview(data)
{
    $("#section-toolbar").fadeIn("slow");
    $("#btn-apply_filter").fadeTo("fast", 1);
    $("#btn-apply_filter").prop('disabled', false);
    $("#btn-download").fadeTo("fast", 1);
    $("#btn-download").prop('disabled', false);

    $("#section-workspace").hide();
    $("#section-workspace").html(data);
    $("#section-workspace").fadeIn("slow");
}

function render_error(error_class, error_message, error_message_default)
{
    $("#section-toolbar").show();
    $("#btn-apply_filter").fadeTo('fast', 0.3);
    $("#btn-apply_filter").prop('disabled', true);
    $("#btn-download").fadeTo('fast', 0.3);
    $("#btn-download").prop('disabled', true);

    error_message = error_message == '' ? error_message_default : error_message;
    $("#section-workspace").html(
        '<div class="' + error_class + '">' + error_message + '</div>');
}

function get_preview()
{
    $.ajax({
        url: 'preview/',
        type: 'GET',
        success: render_preview,
        error: function(xhr, status, text){
            render_error("error", xhr.responseText, "Unexpected error")}
    });
}
