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
    let voto_anterior = $('.vote_selected')
    let data = {
      csrfmiddlewaretoken: $('#votes input:hidden').val(),
      vote_value: parseInt($(i.originalEvent.toElement).text())
    }
    if (!$('#username')[0]){
      alert("Necesita iniciar sesión para votar.")
    } else {
      $.ajax({
        type: "POST",
        url: $('#votes').attr('action-url') ,
        data: data,
        error: function(xhr,status,error){
          alert('Error')
        },
        success: function(data) {
          if (data.state == true){
            voto_anterior.removeClass('vote_selected')
            $('#vote_' + data.vote_value).addClass('vote_selected')
            $('#puntaje').html(data.puntaje.toFixed(2))
          }
        }
      })
    }
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
        let resultado = $('<h4>')
        data.chapters.forEach(element => {
          resultado.append($('<a>', {
            text: 'Capitulo: ' + element.number,
            href: element.url
          }))
          resultado.append($('<span>').html(' | '+element.name))
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
