let $ = window.jQuery
$(function(){
    $('#next').click(function(){
        let img = $('#pageImage img')
        let src = img.attr('src').split('page_')
        let current_page = src[1].split('.')[0]
        let next_page = parseInt(current_page)+1
        let next_url = src[0] + "page_" + next_page + '.' + src[1].split('.')[1]
        let alt = img.attr('alt', img.attr('alt').replace(current_page, next_page))
        img.attr('src', next_url)
    })
    $('#previous').click(function(){
        let img = $('#pageImage img')
        let src = img.attr('src').split('page_')
        let current_page = src[1].split('.')[0]
        let next_page = parseInt(current_page)-1
        let next_url = src[0] + "page_" + next_page + '.' + src[1].split('.')[1]
        let alt = img.attr('alt', img.attr('alt').replace(current_page, next_page))
        img.attr('src', next_url)
    })
})