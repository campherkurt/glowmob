$(document).ready(function() {
  $("textarea").wymeditor({ // "FIELDNAME" is the name of the field you want to give the wysiwyg features
    updateSelector: "input:submit",
    updateEvent: "click",
    postInit: function(wym) {
        
//        wym.hovertools();
//        wym.resizable();
//        word_count(wym)
//
        var doc = wym._doc;

        $(doc.body).children(WYMeditor.BR).remove();
//
//        $(doc).bind("keyup", function(){
//            var w_c = 0;
//            word_count(wym)
//            $.each($("textarea"), function(key, value) {
//                var name = $(value).attr("name");
//                if (name.match("chapter_set-") && name.match("-body") && !name.match("__prefix__")) {
//                    console.log($(value).attr("word_count"))
//                    w_c = w_c + parseInt($(value).attr("word_count"))
//                }
//            });
//            console.log(w_c)
//            $("#id_word_count").val(w_c);
//        });
//
//        $(doc).bind("click", function(e){
//            if (e.button == 2) {
//                var w_c = 0;
//                word_count(wym)
//                $.each($("textarea"), function(key, value) {
//                    var name = $(value).attr("name");
//                    if (name.match("chapter_set-") && name.match("-body") && !name.match("__prefix__")) {
//                        console.log($(value).attr("word_count"))
//                        w_c = w_c + parseInt($(value).attr("word_count"))
//                    }
//                });
//                $("#id_word_count").val(w_c);
//            }
//        });
//
//        function word_count(wym) {
//            var text = wym.html().replace(/(<([^>]+)>)/g,"").replace(/\s+/g," ");
//            text = $.trim(text);
//            wym._element.attr("word_count", text.split(" ").length);
//        }
//
//        var w_c = 0;
//        $.each($("textarea"), function(key, value) {
//            var name = $(value).attr("name");
//            if (name.match("chapter_set-") && name.match("-body") && !name.match("__prefix__")) {
//                w_c = w_c + parseInt($(value).attr("word_count"))
//            }
//        });
//        $("#id_word_count").val(w_c);
//     }
    }
  });

//  $("textarea[name$=body]").wymeditor({
//    updateSelector: "input:submit",
//    updateEvent: "click",
//    postInit: function(wym) {
//        $(wym._doc.body).children(WYMeditor.BR).remove();
//        console.log(wym.html())
////      wym.hovertools();
////      wym.resizable();
//    }
//  });
//
//  $("textarea[name$=-description]").wymeditor({
//    updateSelector: "input:submit",
//    updateEvent: "click",
//    postInit: function(wym) {
////      wym.hovertools();
////      wym.resizable();
//    }
//  });
//});

//$(document).ready(function() {
//  $(".vLargeTextField").wymeditor({ // "FIELDNAME" is the name of the field you want to give the wysiwyg features
//    updateSelector: "input:submit",
//    updateEvent: "click",
//    postInit: function(wym) {
//
//        wym.hovertools();
//        wym.resizable();
//    }
//  });
});