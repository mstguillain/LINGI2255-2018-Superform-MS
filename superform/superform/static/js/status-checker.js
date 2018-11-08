/*
* CUSTOM BY GROUP 10
*/
LIMIT_CHAR_TWEET = 280;
LIMIT_NB_TWEET = 10;

PLUGINS_TO_CHECK = ["twitter"];

statusListener = {
    twitter :
    [
        {
            func : "LIMIT_CONTENT",
            text : "If you hit publish, this post will be split in multiple tweets",
            canPublish : true,
            value : LIMIT_CHAR_TWEET
        },
        {
            func : "NO_TITLE",
            text : "The title will be not displayed",
            canPublish : true
        },
        {
            func : "RENDER_FOR_TWEET",
            canPublish : true,
            value : LIMIT_CHAR_TWEET
        }
    ]
};




statusChecker = {
    _lengthTitle : 0,
    _lengthContent : 0,
    _lengthURL : 0,
    _pluginChecked : new Array(),
    checking : function() {},
    //Getters
    get lengthContent() {
        return this._lengthContent;
    },
    get lengthTitle() {
        return this._lengthTitle;
    },
    get lengthURL() {
        return this._lengthURL;
    },
    get pluginChecked() {
        return this._pluginChecked;
    },

    //Setters
    set lengthContent(val) {
        this._lengthContent = val;
        this.checking();
    },
    set lengthTitle(val) {
        this._lengthTitle = val;
        this.checking();
    },
     set lengthURL(val) {
        this._lengthURL = val;
        this.checking();
    },
    set pluginChecked(val) {
        this._pluginChecked = val;
        this.checking();
    },
    checking : function(listener) {
        this.checking = listener;
    }
}


/*
*  Main function, checking every plugin check to update front-end status
*/
statusChecker.checking(function(){
    PLUGINS_TO_CHECK.forEach(function(item, index) {
        removeStatusBox(item);
    });

    this._pluginChecked.forEach(function(plugin, index){
        addStatusBox(plugin);
        statusListener[plugin].forEach(function (item, index2) {
            window[item["func"]]("twitter", item["text"], item["value"], item["canPublish"]);
        });
    });
});


/*
*   Theses function manages to update the statusChecker states
*   every time a user changes the post
*/

// Every checkbox for each plugin implemented by Group 10 ( you can add here )

$('input.checkbox').change(function () {
    var hisClass = $(this).attr("class").split(" ");
    var plugin = hisClass[2].split(".")[2];
    if (isInArray(PLUGINS_TO_CHECK, plugin)) {
        if (($(this).is(":checked")) && isInArray(statusChecker.pluginChecked, plugin) == false ) {
           var tb = statusChecker.pluginChecked;
           tb.push(plugin);
           statusChecker.pluginChecked = tb;
        }
        else if ($(this).is(":checked") == false && isInArray(statusChecker.pluginChecked, plugin) == true) {
            statusChecker.pluginChecked = removeFromArray(statusChecker.pluginChecked, plugin);
        }
    }
});

// Title
$( "#titlepost" ).on('input', function() {
    statusChecker.lengthTitle = $(this).val().length;
});

// Content
$( "#descriptionpost" ).on('input', function() {
    if (isInArray(statusChecker.pluginChecked, "twitter"))
        statusChecker.lengthContent = $(this).val().length + tweets.toString().length;
    else
        statusChecker.lengthContent = $(this).val().length;
    console.log((isInArray(statusChecker.pluginChecked, "twitter")));
});

// Link URL
$( "#linkurlpost" ).on('input', function() {
    statusChecker.lengthUrl = $(this).val().length;
});



/*
* Utility functions to render status
*/

function addStatusBox(name) {
    var title = name.substring(0,1).toUpperCase() + name.substring(1,name.length);
    if($("#status-"+name).length == 0)   { // If it doesn't exist, create it
        $("#status-content").append("<ul class=\"list-group\" id=\"status-"+name+"\"><li class=\"list-group-item active\">"+title+"</li> </ul>");
    }
}

function removeStatusBox(name) {
    $("#status-"+name).remove();
}

function addStatusText(plugin, text, id) {
    if ($("#"+id).length == 0) { // If it doesn't exist, create it
         $("#status-"+plugin).append("<li class=\"list-group-item\" id=\""+plugin+"-"+id+"\">"+text+"</li>");
    }
}

function removeStatusText(plugin, id) {
    if ($("#"+id).length != 0) { // If it doesn't exist, create it
         $("#status-"+plugin+"-"+id).remove();
    }
}

/*
*   Listeners function
*/

function LIMIT_CONTENT(plugin, text, value, canPublish) {
    if (statusChecker.lengthContent  > value) {
        var id = plugin + "content-too-long";
        addStatusText(plugin, text, id);
    }
    console.log(statusChecker.lengthContent + NB_TWEET * 280)
}

function LIMIT_TITLE(plugin, text, value, canPublish) {
    if (statusChecker.lengthTitle > value) {
        var id = plugin + "title-too-long";
        addStatusText(plugin, text, id);
    }
}

function LIMIT_URL(plugin, text, value, canPublish) {
    if (statusChecker.lengthURL > value) {
        var id = plugin + "url-too-long";
        addStatusText(plugin, text, id);
    }
}

function NO_CONTENT(plugin, text, value, canPublish) {
    if (statusChecker.lengthContent == 0)  {
        var id = plugin +"-no-content";
        addStatusText(plugin,text,id);
    }
}
function NO_TITLE(plugin, text, value, canPublish) {
    if (statusChecker.lengthTitle == 0)  {
        var id = plugin +"-no-title";
        addStatusText(plugin,text,id);
    }
}
function NO_URL(plugin, text, value, canPublish) {
    if (statusChecker.lengthTitle == 0)  {
        var id = plugin +"-no-url";
        addStatusText(plugin,text,id);
    }
}

function RENDER_FOR_TWEET(plugin, text, value, canPublish) {
    if (statusChecker.lengthContent > value) {
        renderTweet();
    }
}

/*
function addStatus(func, text, block, val = 0) {
    window[func](text, block, val);
}
*/

// Utily function for array
function isInArray(tb, value) {
    var isIn = false;
    tb.forEach(function(item, index) {
        if (item.localeCompare(value) == 0)
            isIn = true;
    });
    return isIn;
}

function removeFromArray(tb, value) {
    var tb2 = new Array();
    tb.forEach(function(item, index) {
        if (item != value)
            tb2.push(item);
    });
    return tb2;
}

/*
*  Render tweet part
*/
/*
tweets = new Array();
NB_TWEET = 0;

function createInputTextForTweet(text, nbTweet) {

    var inputToAdd = '<div id=tweet-"'+nbTweet+'>';
    inputToAdd += '<textarea class="form-control" rows="5" id="descriptionpost" name="descriptionpost" maxlength="'+LIMIT_CHAR_TWEET+'">'
    inputToAdd += text
    inputToAdd += '</textarea><br/><br/></div>';
    if (nbTweet == NB_TWEET - 1)
        $(inputToAdd).insertBefore('#descriptionpost');
    else
        $(inputToAdd).insertBefore('#tweet-'+nbTweet - 1);
}

function renderTweet() {
    //Create array of tweets
    var sizeArray = 0;
    for (var i = 0, charsLength = $("#descriptionpost").val().length; i < charsLength; i += 280) {
        tweets.push($("#descriptionpost").val().substring(i, i + 280));
        NB_TWEET = NB_TWEET + 1;
    }
    //Create each input based on this
    tweets.forEach(function(item, index) {
        createInputTextForTweet(text, nbTweet);
    });

}


*/