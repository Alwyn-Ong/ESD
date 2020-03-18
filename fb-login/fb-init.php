<?php

// Start the session

session_start();

// Include autoload file from vendor folder
require 'vendor/autoload.php';

$fb = new Facebook\Facebook([
    'app_id' => '624950598329147',
    'app_secret' => 'e375735cfdef22f60aa30ee8c3c0bdcf',
    'default_graph_version' => 'v6.0'
]);

$helper = $fb->getRedirectLoginHelper();
$login_url = $helper->getLoginUrl('http://localhost/esdproject/fb-login/fb.php');

try {

    $accessToken = $helper->getAccessToken();
    if(isset($accessToken)){
        $_SESSION['access_token'] = (string)$accessToken; // convert to string

        // if session is set we can redirect to the user to any page
        header("Location:fb.php");
    }

} catch (Exception $exc) {
    echo $exc->getTraceAsString();
}


// now we will get users first name , email , last name
if(isset($_SESSION['access_token'])){
    try{
        $fb->setDefaultAccessToken($_SESSION['access_token']);
        $res = $fb->get('/me?locale=en_US&fields=name,email');
        $user = $res->getGraphUser();
        echo 'Hello, ', $user->getField('name');

    } catch (Exception $exc) {
        echo $exc->getTraceAsString();
    }
}

?>