addEvent(window, 'load', inicializarEventos, false)

function inicializarEventos() {
    inicializarMenu('menu')
}

function inicializarMenu(m) {
    let ob = document.getElementById(m)
    let menu = ob.getElementsByTagName('ul')
    for (let f = 1; f < menu.length; f++) {
        menu[f].style.display='none'
    }
    let enlaces=ob.getElementsByTagName('a')
    for (let f = 0; f < enlaces.length; f++) {
        addEvent(enlaces[f], 'mouseover', itemSeleccionadoShow, false)
        addEvent(enlaces[f], 'mouseout', itemSeleccionadoHidde, false)
    }
}

function itemSeleccionadoShow(e) {
    let enlace
    if (window.event) {
        enlace = window.event.srcElement
    } else {
        enlace = e.target
    }
    // console.log(enlace)
    let padre = enlace.parentNode
    console.log("padre:"+padre)
    let ul = padre.getElementsByTagName('ul')
    if (ul.length > 0) {
        if (ul[0].style.display=='none') {
            ul[0].style.display='block'
        }
    }
}
function itemSeleccionadoHidde(e) {
    let enlace
    if (window.event) {
        enlace = window.event.srcElement
    } else {
        enlace = e.target
    }
    // console.log(enlace)
    let padre = enlace.parentNode
    let ul = padre.getElementsByTagName('ul')
    if (ul.length > 0) {
        if (ul[0].style.display=='block') {
            ul[0].style.display='none'
        }
    }
}
function addEvent(elemento, nomevento, funcion, captura) {
    if (elemento.attachEvent) {
        elemento.attachEvent('on'+nomevento, funcion)
        return true
    } else if (elemento.addEventListener) {
        elemento.addEventListener(nomevento, funcion, captura)
        return true
    } else {
        return false
    }
}