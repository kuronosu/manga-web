$(document).ready(function(){
       $("input[type=checkbox]").change(function(){
           let elemento=this;
           let contador=0
           $("input[type=checkbox]").each(function(){
               if($(this).is(":checked"))
                   contador++
           })
           let cantidadMaxima=3
           if(contador>cantidadMaxima)
           {
               $(elemento).prop('checked', false) // para desactivar el limite poner true
               contador--
           }
       })
   })