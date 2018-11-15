/*
* CUSTOM BY GROUP 10
*/
LIMIT_CHAR_TWEET = 280;

statusListener = {
    twitter :
    [
        {
            type : "description",
            compare : "GT",
            value : LIMIT_CHAR_TWEET,
            text : "If you hit publish, this post will be split in multiple tweets",
            forbidPublish : false,
            func : "renderTweet",
            args : ""
        },
        {
            type : "title",
            compare : "EQ",
            value : "0",
            text : "The title will be not displayed",
            forbidPublish : false
        }
    ],
    mail :
    [
        {
            type : "title",
            compare : "EQ",
            value : "0",
            text : "You need a title for a mail",
            forbidPublish : true
        }
    ],
    LinkedIn :
    [
        {
            type : "title",
            compare : "EQ",
            value : "0",
            text : "The LinkedIn title will be not displayed",
            forbidPublish : false
        }
    ],
    wiki :
    [
        {
            type : "title",
            compare : "EQ",
            value : "0",
            text : "You need a title for the publication",
            forbidPublish : true
        }
    ]
}

statusChecker = {
    _lengthTitle : 0,
    _lengthContent : 0,
    _lengthURL : 0,
    _forbidPublish : true,
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
    get forbidPublish() {
        return this._forbidPublish;
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
    set forbidPublish(val) {
        this._forbidPublish = val;
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
    Object.keys(statusListener).forEach(function(item, index) {
        removeStatusBox(item);
    });

    this._forbidPublish = false;

    this._pluginChecked.forEach(function(plugin, index){
        addStatusBox(plugin);
        statusListener[plugin].forEach(function (item, index2) {
            checkStatus(plugin, item);
            if (typeof item["func"] != "undefined") {
                 window[item["func"]](item["args"]);
            }
        });
    });

    $("#publish-button").prop("disabled",this._forbidPublish);
});


function checkStatus(plugin, status) {
    value = getValueType(status["type"]);

    if (value < 0) {
        console.log("ERROR : failed to check input "+status["type"]);
        return;
    }

    if (comparingValue(value, status["compare"], status["value"])) {
        addStatusText(plugin, status["text"], status["type"]+"-"+status["compare"]+"-"+status["value"]);
        if (status["forbidPublish"])
            statusChecker.forbidPublish = true;
        console.log(statusChecker.forbidPublish);
    }

}


function comparingValue(arg1, compare, arg2) {
    var value
    switch (compare) {
        case 'LT' :
            value = (arg1 < arg2); break;
        case 'GT' :
            value = (arg1 > arg2); break;
        case 'EQ' :
            value = (arg1 == arg2); break;
        case 'LEQ' :
            value = (arg1 <= arg2); break;
        case 'GEQ' :
            value = (arg1 >= arg2); break;
        default :
            value = false;
    }
    return value;
}

function getValueType(type) {
    var value;
    switch (type) {
        case 'description' :
            value = statusChecker.lengthContent; break;
        case 'title' :
            value = statusChecker.lengthTitle; break;
        case 'link' :
            value = statusChecker.lengthUrl; break;
        default :
            value = -1;
    }
    return value;
}

/*
*   Theses function manages to update the statusChecker states
*   every time a user changes the post
*/

// Every checkbox for each plugin implemented by Group 10 ( you can add here )

$('input.checkbox').change(function () {
    var hisClass = $(this).attr("class").split(" ");
    var plugin = hisClass[2].split(".")[2];
    if (isInArray(Object.keys(statusListener), plugin)) {
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

function rearrangeArray(tb) {
    tb2 = new Array();
    tb.forEach(function(item, index) {
        if (item.length != 0)
            tb2.push(item);
    });

    return tb2;
}

/*
*  Render tweet part
*/

tweets = new Array();

function createInputTextForTweet(text, nbTweet) {
    if (nbTweet == tweets.length - 1) {
        $("#descriptionpost").val(text);
    }
    else {
        var inputToAdd = '<textarea class="form-control tweet-'+nbTweet+'" rows="5" maxlength="'+LIMIT_CHAR_TWEET+'">'
        inputToAdd += text
        inputToAdd += '</textarea>';
        $(inputToAdd).insertBefore('.tweet-'+(nbTweet+1));


        $( ".tweet-"+nbTweet).on('input', function() { //Add listener
            tweets[nbTweet] = $(this).val();

            if ($(this).val().length == 0) {
                tweets = rearrangeArray(tweets);
                tweets.push(" ");
                for (i = 0; i < tweets.length - 1; i ++) {
                    $(".tweet-"+i).remove();
                }
                tweets.pop();
                renderTweet();
            }
        });
    }
}

function renderTweet() {

    if (tweets.length > 0) // If the render is not new, suppress the last tweet
        tweets.pop();

    for (var i = 0, charsLength = $("#descriptionpost").val().length; i < charsLength; i += 280) {
        tweets.push($("#descriptionpost").val().substring(i, i + 280));
    }
    nbTweet = tweets.length - 1;
    $("#descriptionpost").attr("class","form-control tweet-"+nbTweet);
    for (i = 0; i < tweets.length - 1; i ++) {
        $(".tweet-"+i).remove();
    }

    for (i = tweets.length; i > 0; i -- ){
        createInputTextForTweet(tweets[i-1], nbTweet);
        nbTweet = nbTweet - 1;
    };
}


function unifyTweet() {
    text = "";
    if (tweets.length > 0) {
        for (i = 0; i < tweets.length; i ++) {
            text += $(".form-control tweet-"+i).val();
            $(".form-control tweet-"+i).remove();
        }
        tweets = new Array();

        $("#descriptionpost").val(text);
    }
}

function RENDER_FOR_TWEET(plugin, text, value, canPublish) {
    if ($("#descriptionpost").val().length > value) {
        renderTweet();
    }
    else {
        unifyTweet();
    }
}