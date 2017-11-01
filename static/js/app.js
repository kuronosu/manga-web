$(document).ready(function(){
       $("input[type=checkbox]").change(function(){
           var elemento=this;
           var contador=0;
           $("input[type=checkbox]").each(function(){
               if($(this).is(":checked"))
                   contador++;
           });
           var cantidadMaxima=7;
           if(contador>cantidadMaxima)
           {
               $(elemento).prop('checked', false) // para desactivar el limite poner true
               contador--;
           }
       });
   });