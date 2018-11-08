/*
* CUSTOM BY GROUP 10
*/
PLUGINS_TO_CHECK = ["mail","wiki", "twitter"];

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

    this._pluginChecked.forEach(function(item, index){
        addStatusBox(item);
        window[item]();
    });
});


function twitter() {
    if (statusChecker.lengthContent > 280) {
        addStatus("twitter","If you hit publish, this post will be split in multiple tweets","tweet-too-long");
    }
    else {
        removeStatus("tweet-too-long");
    }

}

function mail() {
    addStatus("mail", "TODO", "thisid");
}

function wiki() {
    addStatus("wiki", "TODO", "thisid");
}



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
$( "#descriptionpost" ).on('input', function() { //TO DO REFACTOR FOR TWITTER
    statusChecker.lengthContent = $(this).val().length;
});

// Link URL
$( "#linkurlpost" ).on('input', function() {
    statusChecker.lengthUrl = $(this).val().length;
});



/*
* Utility functions
*/

function addStatusBox(name) {
    var title = name.substring(0,1).toUpperCase() + name.substring(1,name.length);
    if($("#status-"+name).length == 0)  { // If it doesn't exist, create it
        $("#status-content").append("<ul class=\"list-group\" id=\"status-"+name+"\"><li class=\"list-group-item active\">"+title+"</li> </ul>");
    }
}

function removeStatusBox(name) {
    $("#status-"+name).remove();
}

function addStatus(plugin, text, id) {
    if ($("#"+id).length == 0) { // If it doesn't exist, create it
         $("#status-"+plugin).append("<li class=\"list-group-item\" id=\""+plugin+"-"+id+"\">"+text+"</li>");
    }
}

function removeStatus(plugin, id) {
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
    tb2 = new Array();
    tb.forEach(function(item, index) {
        if (item != value)
            tb2.push(item);
    });
    return tb2;
}