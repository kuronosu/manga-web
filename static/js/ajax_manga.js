let $ = window.jQuery
$(function(){
  let tomos = $('#tomos li a')
  tomos_ajax($(tomos[0]).attr('href'), $('#chapters'))
  // Ajax para los detalles de los tomos implementado en la pagina de Manga Detail
  tomos.click(function(e){
    let url = $(e.toElement).attr('href')
    let result_cont = $('#chapters')
    tomos_ajax(url, result_cont)
    return false
  })
  // Ajax para los votos implementado en la pagina de Manga Detail
  $('.vote').click(function(i){
    let voto_anterior = $('.text-warning')
    let data = {
      csrfmiddlewaretoken: $('#votes input:hidden').val(),
      vote_value: parseInt($(i.originalEvent.toElement).text())
    }

      $.ajax({
        type: "POST",
        url: $('#votes').attr('action-url') ,
        data: data,
        error: function(xhr,status,error){
          alert('Error')
        },
        success: function(data) {
          if (data.state == true){
            voto_anterior.addClass('text-dark')
            voto_anterior.removeClass('text-warning')
            let star = $($('#vote_' + data.vote_value).children()[0])
            star.addClass('text-warning')
            star.removeClass('text-dark')
            $('#puntaje').html(data.puntaje.toFixed(1))
          } else {
            alert(data.message)
          }
        }
      })
  })
  // Funcion para hacer un request con ajax para obtener los capitulos de un tomo
  function tomos_ajax(url, result_cont){
    $.ajax({
      type: "POST",
      url: url,
      data: {csrfmiddlewaretoken: $('#tomos input:hidden').val()},
      error: function(){
        alert('Error')
      },
      success: function(data) {
        let resultado = $('<span>')
        data.chapters.forEach(element => {
          let tmp = (element.name) ? `: ${element.name}` : ''
          resultado.append($('<a>', {
            text: `Capitulo ${element.number}${tmp}`,
            href: element.url
          }))
          resultado.append($('<br>'))
        })
        let link_add = $('#add_chapter')
        $('#add_chapter').attr("href", data.url_add)
        resultado.append(link_add)
        result_cont.html(resultado)
      }
    })
  }

})
