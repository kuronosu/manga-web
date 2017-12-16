let $ = window.jQuery
$(function(){
    $('#id_username').change(function(ev){
        let form = $(this).closest('form')
        let $input = $(this)
        let data = {}
        data[$input.attr('name')] = $input.val()
        console.log(data)
        $.ajax({
            url: form.attr('username-validate-url'),
            data: data,
            dataType: 'json',
            success: function(data){
                console.log(data)
            },
        })
    })
})

