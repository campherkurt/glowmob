$(document).ready(function () {
        console.log("sdfsdf");
       
        
       $("#nav li a").hover(function(){
            console.log("on hover");
            $(this).css({backgroundColor: '#FF5C00'});
        });

       
        
       $("#nav li a" ).mouseout(function(){
            console.log("on hover");
            $(this).css({backgroundColor: '#A63C00'});
        });

    
});


