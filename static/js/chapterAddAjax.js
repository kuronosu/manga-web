$(function() {
    let submitObj = $("#fileuploader").uploadFile({
        url: "",
        dynamicFormData: function(){
            var data = $($('#chapterAddForm').get(0)).serialize()
            return data;        
        },
        multiple: false,
        fileName: "content",
        dragDrop: true,
        maxFileCount: 1,
        acceptFiles: "application/pdf",
        autoSubmit: false,
        sequential: false,
        showProgress: true,
        showFileSize: true,
        showQueueDiv: "output",
        onSuccess:function(files,data,xhr,pd){
            console.log(data['ajax_status'] == '0')
            if (data['ajax_status'] == '0') {
                let error = ""
                if ( data['content'] ) {
                    error += "<li>" + data['content'] + "</li>"
                }
                if ( data['user_chapter_number'] ) {
                    error += "<li>" + data['user_chapter_number'] + "</li>"
                }
                $("#eventsmessage").html("<br/>Error: "+ error);
            } else {
                window.location.replace(data['redirect_url'])
            }
        },
        onError: function(files,status,errMsg,pd){
            $("#eventsmessage").html($("#eventsmessage").html()+"<br/>Error " + status + " for: "+JSON.stringify(files));
        },
        extraHTML: function(){
            let html = "<div><label for='id_user_chapter_number'>Chapter number:</label><input type='number' name='user_chapter_number' required id='id_user_chapter_number'></div>"
            html += "</br>"
            html += "<div><label for='id_name'>Name:</label><input type='text' name='name' maxlength='100' id='id_name'></div>"
            return html;            
        }
    })
    $("#chapterAddForm").submit(function(e){
        submitObj.startUpload();
        return false
    });
})
