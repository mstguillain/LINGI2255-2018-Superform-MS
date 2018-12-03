
LIMIT_CHAR_TWEET = 280;

statusListener = {
    twitter :
    [
        {
            type : "title",
            compare : "GT",
            value : 0,
            text : "The title will be not displayed",
            forbidPublish : false
        },
        {
            type : "description",
            compare : "GT",
            value : LIMIT_CHAR_TWEET,
            text : "If you hit publish, this post will be split in multiple tweets",
            forbidPublish : false
        },
        {
            type : "description",
            compare : "GT",
            value : LIMIT_CHAR_TWEET,
            text : "<a onClick=\"activateSplitTweet()\" id=\"button-status-tweet\" class=\"btn btn-outline-primary\" role=\"button\">See tweets splitted</a>",
            forbidPublish : false
        },
        {
            type : "description",
            compare : "GEQ",
            value : 0,
            text : "",
            forbidPublish : false,
            func : "manageTweet",
            args : ""
        }
    ],
    mail : [
        {
            type : "title",
            compare : "EQ",
            value : 0,
            text : "You need a title for a mail",
            forbidPublish : true
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

// Every checkbox for each plugin implemented by Group 10

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
    if (isInArray(statusChecker.pluginChecked, "twitter") && typeof tweets != 'undefined')
        statusChecker.lengthContent = $(this).val().length + 280 * tweets.length;
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
buttonTweet = false;

function activateSplitTweet() {
    buttonTweet =  !buttonTweet;
    unifyTweet();
    if (buttonTweet) {
         $("#button-status-tweet").val("Unify tweets"); // TODO problem here
         renderTweet();
    }
    else {
         $("#button-status-tweet").val("See tweets splitted"); // TODO problem here
    }
}

 function splitTextForTweet(idOrClassInput) {
    tb = new Array();
    for (var i = 0, charsLength = $(idOrClassInput).val().length; i < charsLength; i += 280) {
        tb.push($(idOrClassInput).val().substring(i, i + 280));
    }
    return tb;
 }

function manageTweet(target) {
    if (buttonTweet == false) {
        tweets = splitTextForTweet("#descriptionpost");
    }
    else if (target.length > 0) {
        tb = splitTextForTweet(target);
        index = 0;
        if (target == '#descriptionpost')
                index = (tweets.length - 1);
            else
                index = (target.split('-')[1] - 1);
        if (tb.length == 0) { //Check if the tweet is empty
            unifyTweet();
            tweets = removeFromArray(tweets, tweets[index]);
            renderTweet();
        }
        else if (tb.length > 1) { // Check if we need to add another tweet
            unifyTweet();
            console.table(tweets);
            tmp = tweets.slice(0, index);
            tmp = tmp.concat(tb);
            if (index + 1 < tweets.length)
                tmp = tmp.concat(tweets.slice(index + 1, tweets.length));
            tweets = tmp.slice();
            renderTweet();
        }
        else {  //Just change the value
           tweets[index] = $(target).val();
        }

        if (tweets.length == 1) {
            activateSplitTweet() // Deactivate button
        }
    }
}

function addListenerTweet(target){
    $(target).on('input', function() {
        manageTweet(target);
    });
}

function renderTweet() {
    tb = tweets.slice();
    nbTweet = tweets.length - 1;
    $('#descriptionpost').val(tb.pop());
    if (tb.length > 0 ) {
        addListenerTweet('#descriptionpost');
        inputToAdd = '<textarea class="form-control tweet-'+nbTweet+'" rows="5" maxlength="'+LIMIT_CHAR_TWEET+'">';
        inputToAdd += tb.pop();
        inputToAdd += '</textarea>';
        $(inputToAdd).insertBefore("#descriptionpost");
        addListenerTweet('.tweet-'+nbTweet);
        while (tb.length != 0) {
            nbTweet  = nbTweet - 1;
            inputToAdd = '<textarea class="form-control tweet-'+nbTweet+'" rows="5" maxlength="'+LIMIT_CHAR_TWEET+'">'
            inputToAdd += tb.pop();
            inputToAdd += '</textarea>';
            before = nbTweet + 1
            $(inputToAdd).insertBefore('.tweet-'+ before );
            addListenerTweet('.tweet-'+nbTweet);
        }
    }
}


function unifyTweet() {
    tweets.forEach(function(item, index) {
        $(".tweet-"+index).off();
        $(".tweet-"+index).remove();
    });
    $("#descriptionpost").val(tweets.toString());
}
