$(function() {
    $('#menu ul').each(function(i){
        if (i != 0) {$(this).hide()}
    })
    $('#menu a').each(function(){
        $(this).click(function(){
            submenu = $('ul', this.parentNode)
            submenu.fadeToggle().css('display', 'block')
        })
    })
    let checkboxs = $('input[type=checkbox]', '.form_control')
    if (checkboxs.length <= 0) {
        checkboxs = checkboxs.prevObject
    }
    checkboxs.change(function(){
        let elemento=this;
        let contador=0
        checkboxs.each(function(){
            if($(this).is(":checked"))
                contador++
        })
        let cantidadMaxima=7
        if(contador>cantidadMaxima){
            $(elemento).prop('checked', false) // para desactivar el limite poner true
            contador--
        }
    })
})