/*
* CUSTOM BY GROUP 10
*/
tweetChecker = {
    lengthDescription : 0,
    lengthUrl : 0,
    checked : false,
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
    set isChecked(val) {
        this.checked = val;
        this.lengthListener(this.lengthDescription + 1 + this.lengthUrl, this.checked);
    },
    get isChecked() {
        return this.checked;
    },
    lengthListener : function(listener) {
        this.lengthListener = listener;
    }
}

tweetChecker.lengthListener(function (val, isTwitterChecked) {
    if (val > 280 && isTwitterChecked)
    {
        document.getElementById("status-content").innerHTML = "If you hit publish, this post will be split in multiple tweets";
    }
    else
    {
        document.getElementById("status-content").innerHTML = "Content";
    }

});



$('input.checkbox').change(function () {

    if ($(this).is(":checked")){
        if ($(this).hasClass('superform.plugins.twitter')) {
           tweetChecker.isChecked = true;
        }
    }
    else {
        if ($(this).hasClass('superform.plugins.twitter')) {
           tweetChecker.isChecked = false;
        }
    }
});

$( "#descriptionpost" ).on('input', function() {
    tweetChecker.lengthContent = $(this).val().length;
});

$( "#linkurlpost" ).on('input', function() {
    tweetChecker.lengthLinkUrl = $(this).val().length;
});

