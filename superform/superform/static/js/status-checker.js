/*
* CUSTOM BY GROUP 10
*/

MAX_LENGTH_TWEET = 280;
COUNT_TWEET = 1;

statusChecker = {
    lenTitle : 0, // Length of a post title
    lenContent : 0, //Length of a post content
    lenUrl : 0, // Length of a post's link url
    JSONTwitterContent : 'undefined', //The JSON passes for Twitter
    twitterChecked : false,  //Boolean to verify if the post will be published on Twitter
    wikiChecked : false, // Boolean to verify if the post will be published on Wiki
    canPublishing : false, // To disable or not the publish button
    statusCheckerValue : 'hey',
    checking : function() {}, // General listener method ( declaration)
    twitter : function() {},  // Add statusChecker if a twitter plugin is checked (declaration)
    wiki : function() {},  // Add statusChecker if a wiki plugin is checked (declaration)

    // Getters
    get lengthTitle() {
        return this.lenTitle;
    },
    get lengthContent() {
        return this.lenContent;
    },
    get lengthUrl() {
        return this.lenUrl;
    },
    get JSONTwitter() {
        return this.JSONTwitterContent;
    },
    get twitterCheck() {
        return this.twitterChecked;
    },
    get wikiCheck() {
        return this.wikiChecked;
    },
    get canPublish() {
        return this.canPublishing;
    },

    // Setters
    set lengthTitle(val) {
        this.lenTitle = val;
        this.checking();
    },
    set lengthUrl(val) {
        this.lenUrl = val;
        this.checking();
    },
    set lengthContent(val) {
        this.lenContent = val;
        this.checking();
    },
    set JSONTwitter(val) {
        this.JSONTwitterContent = val;
    },
    set twitterCheck(val) {
        this.twitterChecked = val;
        this.checking();
    },
    set wikiCheck(val) {
        this.wikiChecked = val;
        this.checking();
    },
    set canPublish(val) {
        this.canPublishing = val;
        this.checking();
    },
    checking : function(listener) {
        this.checking = listener;
    },
    twitter : function(listener) {
        this.twitter = listener;
    }
}

// General listener implementation
statusChecker.checking(function() {

    // For Twitter
    if (statusChecker.twitterCheck) {
       if($("#status-twitter").length == 0)  // If it doesn't exist, create it
        $("#status-content").append("<ul class=\"list-group\" id=\"status-twitter\"><li class=\"list-group-item active\">Twitter</li> </ul>");
       this.twitter();
    }
    else  {
       $("#status-twitter").remove();
    }

    // For wiki
    if (statusChecker.wikiCheck) {
        statusChecker.wiki();
    }
    else {
         //console.log("Add here hidden statusChecker");
    }
});


// Update front-end statusChecker for Twitter
statusChecker.twitter(function() {
    if (this.lenTitle > 0) {
        if ($("#tweet-title").length == 0)
            $("#status-twitter").append("<li class=\"list-group-item\" id=\"tweet-title\"></li>");

        $("#tweet-title").html("The title will be not displayed on Twitter");
    }
    else {
        $("#tweet-title").remove();
    }

    if (this.lenContent > 280)
    {
        if ($("#tweet-too-long").length == 0)
            $("#status-twitter").append("<li class=\"list-group-item\" id=\"tweet-too-long\"></li>");

        $("#tweet-too-long").html("If you hit publish, this post will be split in multiple tweets");
        renderTweet(true);
    }
    else
    {
       $("#tweet-too-long").remove();
       //renderTweet(false);
    }
});

function renderTweet(isActive) {
    if (isActive) {
        var lengthText=  $('#descriptionpost').val().length;
        //console.log(lengthText);
        while (lengthText > 280) {
           COUNT_TWEET = COUNT_TWEET + 1;
           var text1 = $("#descriptionpost").val().substring(0,280);
           var text2 =  $("#descriptionpost").val().substring(280, $("#descriptionpost").val().length);
           lengthText = lengthText - 280;
           $("#descriptionpost").val(text2);
           $('<div class="content-split"><br/><textarea class="form-control tweet-'+COUNT_TWEET+'" rows="5" name="descriptionpost" maxlength="'+MAX_LENGTH_TWEET+'">'+text1+'</textarea><br/><br/></div>').insertBefore('#descriptionpost');
        }
    }
    else {
        console.log("HERE");
        var tweet = 1;
        var text = '';
        while (COUNT_TWEET != tweet) {
            text = text + $("#tweet-"+tweet).val();
            tweet = tweet + 1;
        }
       //console.log(text);
       text = text + $("#description").val();
       $("#description").val(text);
    }
}



// Update front end statusChecker for Wiki
statusChecker.wiki(function() {
    console.log("Wiki here");
});



/*
*   Theses function manages to update the statusChecker states
*   every time a user changes the post
*/

// Every checkbox for each plugin implemented by Group 10 ( you can add here )

$('input.checkbox').change(function () {

    if ($(this).is(":checked")){
        if ($(this).hasClass('superform.plugins.twitter')) {
           statusChecker.twitterCheck = true;
        }
        if ($(this).hasClass('superform.plugins.wiki')) {
            statusChecker.wikiCheck = true;
        }
    }
    else {
        if ($(this).hasClass('superform.plugins.twitter')) {
           statusChecker.twitterCheck = false;
        }
        if ($(this).hasClass('superform.plugins.wiki')) {
           statusChecker.wikiCheck = false;
        }
    }
});

// Title
$( "#titlepost" ).on('input', function() {
    statusChecker.lengthTitle = $(this).val().length;
});

// Content
$( "#descriptionpost" ).on('input', function() {
    statusChecker.lengthContent = $(this).val().length;
});

// Link URL
$( "#linkurlpost" ).on('input', function() {
    statusChecker.lengthUrl = $(this).val().length;
});




/*
statusChecker = {
    lengthDescription : 0,
    lengthUrl : 0,
    twitterChecked : false,
    wikiChecked : false,
    lengthListener : function(val, isTwitterChecked) {},
    set lengthContent(val) {
        this.lengthDescription = val;
        this.lengthListener(val + 1 + this.lengthUrl, this.checked);
    },
    get lengthContent() {
        return this.lengthDescription;
    },
    set lengthLinkUrl(val) {
        this.lengthUrl = val;
        this.lengthListener(this.lengthDescription + 1 + val, this.checked);
    },
     get lengthLinkUrl() {
        return this.lengthUrl;
    },
    set isTwitterChecked(val) {
        this.checked = val;
        this.lengthListener(this.lengthDescription + 1 + this.lengthUrl, this.checked);
    },
    get isTwitterChecked() {
        return this.checked;
    },
    lengthListener : function(listener) {
        this.lengthListener = listener;
    }
}

tweetChecker.lengthListener(function (val, isTwitterChecked) {
    if (val > 280 && isTwitterChecked)
    {
        document.getElementById("statusChecker-content").innerHTML = "If you hit publish, this post will be split in multiple tweets";
    }
    else
    {
        document.getElementById("statusChecker-content").innerHTML = "Content";
    }

});





*/