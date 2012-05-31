$(document).ready(function () {
       $("#nav li a").hover(function(){
                $(this).css({backgroundColor: 'pink'});
        });
       $("#nav li a" ).mouseout(function(){
            $(this).css({backgroundColor: '#FFFFFF'});
        });

       //Insert the sharing icons where necessary
       $(".share_box").html('<table>' + 
                '<tr>' +
                    '<td class="FB_td"></td>' +
                    '<td class="twitter_td"></td>' +
                    '<td class="mail_td"></td>' +
                '</tr>' +
            '</table>')
        $(".FB_td").html('<a title="Facebook" class="facebook_icon" rel="nofollow" target="_blank" href="http://www.facebook.com/share.php?u=' + window.document.URL + '">' +
                            '<img src="/site_media/static/img/mobile/facebook2.jpg" /></a>');

        $(".twitter_td").append('<a title="Twitter" class="" id="" rel="nofollow" target="_blank" href="http://twitter.com/share?text=glowmob+stories+to+light+up+our+lives&url=' + window.document.URL + '">' +
                            '<img src="/site_media/static/img/mobile/twitter2.jpg" /></a>');

        $(".mail_td").append('<a title="Email" class="mail_icon" rel="nofollow" href="mailto:campherkurt2@gmail.com">' +
                            '<img src="/site_media/static/img/mobile/mail_pic.jpg" /></a>');
});



