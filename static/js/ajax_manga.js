let $ = window.jQuery
$(function(){
    // Ajax para los votos implementado en la pagina de Manga Detail
    $('.vote').click(function(i){
      let voto_anterior = $('.vote_selected')
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
            voto_anterior.removeClass('vote_selected')
            $('#vote_' + data.vote_value).addClass('vote_selected')
            $('#puntaje').html(data.puntaje)
          }
        }
      })
    })
  })