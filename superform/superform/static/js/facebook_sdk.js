            
    // This is called with the results from from FB.getLoginStatus().
    function statusChangeCallback(response) {
        console.log('statusChangeCallback');
        console.log(response);
        // The response object is returned with a status field that lets the
        // app know the current login status of the person.
        // Full docs on the response object can be found in the documentation
        // for FB.getLoginStatus().
        if (response.status === 'connected') {
        // Logged into your app and Facebook.
        testAPI();
        } else {
            console.log('passe dans le else')
        // The person is not logged into your app or we are unable to tell.
        document.getElementById('status').innerHTML = 'Please log ' +
            'into this app.';
        }
        //loginWithPermissions();

    }
    
    // This function is called when someone finishes with the Login
    // Button.  See the onlogin handler attached to it in the sample
    // code below.
    function checkLoginState() {
        FB.getLoginStatus(function(response) {
            statusChangeCallback(response);
        }
        
        );
    }
    
    window.fbAsyncInit = function() {
        FB.init({
        appId      : '523437948128033',
        cookie     : true,  // enable cookies to allow the server to access 
        xfbml      : true,  // parse social plugins on this page
        version    : 'v3.2' // use graph api version 2.8
        });

        // Now that we've initialized the JavaScript SDK, we call 
        // FB.getLoginStatus().  This function gets the state of the
        // person visiting this page and can return one of three states to
        // the callback you provide.  They can be:
        //
        // 1. Logged into your app ('connected')
        // 2. Logged into Facebook, but not your app ('not_authorized')
        // 3. Not logged into Facebook and can't tell if they are logged into
        //    your app or not.
        //
        // These three cases are handled in the callback function.

        /*FB.getLoginStatus(function(response) {
            statusChangeCallback(response);
        });
        */
        

    };

    // Load the SDK asynchronously
    (function(d, s, id) {
        console.log("tessssst, passe mnt")
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = 'https://connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v3.2&appId=523437948128033&autoLogAppEvents=1';
        fjs.parentNode.insertBefore(js, fjs);
      }(document, 'script', 'facebook-jssdk'));

    // Here we run a very simple test of the Graph API after login is
    // successful.  See statusChangeCallback() for when this call is made.
    function testAPI() {
        console.log('Welcome!  Fetching your information.... ');
        FB.api('/me', function(response) {
        console.log('Successful login for: ' + response.name);
        document.getElementById('status').innerHTML =
            'Thanks for logging in, ' + response.name + '!';
            
        });
        
    }
    function loginWithPermissions(){
        
    }
    function requestPermissionsForPage(callback){
        FB.api (
            "/me/accounts",
            function (response) {
                console.log("DEVANT LE IIIIIIFFFF")
                console.log(response);
                
                if(response && !response.error){
                    console.log("DAAAANS APIIIIII")
                    console.log (response);
                    callback(response);
                }
                
                
                
            }
        ), {Scope: "manage_pages"};
    }

    var credentials = "";
    function startConnexion(){
                FB.login(function(response) {
                    console.log("in loginWithPermissions()");
                    console.log(response);
                }, {
                    scope: 'email, manage_pages, pages_show_list, publish_pages, business_management, publish_to_groups, public_profile', 
                    return_scopes: true
                });
                FB.getLoginStatus (function (response) {
                    if(response.status === 'connected'){
                        console.log("DAAAANS GET LOOOOGIIIIN")

                        console.log (response);
                    }
                });
                requestPermissionsForPage(function(res){
                    credentials = res;
                    console.log("credentials are : ");
                    console.log(credentials)
                    $.ajax({
                        type: "POST",
                        contentType:"application/json;charset=utf-8",
                        url:"/facebook_credentials",
                        data: JSON.stringify({credentials}),
                        dataType: "json",
                    });
                     
                });    
        };