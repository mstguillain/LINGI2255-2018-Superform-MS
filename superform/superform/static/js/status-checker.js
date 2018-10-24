/*
* CUSTOM BY GROUP 10
*/


    $( "#descriptionpost" ).on('input', function() {

    if ($(this).val().length> 280) {
        document.getElementById("status-content").innerHTML = "If you publish this on Twitter, the tweet will be splited !";
    }
    else
    {
        document.getElementById("status-content").innerHTML = "Content";
    }
});

