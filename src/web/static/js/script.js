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
            $('#form_tune').submit()
        }
    })
    btn_target.click(function(){btn_file.trigger('click'); return false})
}
