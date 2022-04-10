// This code is reused from code the made by team7 in CO1111 treasure hunt assignment.

const COOKIE_EXPIRY_DAYS = 20;

function setCookie( cookieName, cookieValue, expireDays=COOKIE_EXPIRY_DAYS ) {

    // Content-unaware function that sets a cookie.

    // The code is adapted from worksheet "co1111-worksheet15a - Cookies.pdf".

    let date = new Date();
    date.setTime( date.getTime() + (expireDays*24*60*60*1000) );
    let expires = "expires=" + date.toUTCString();
    document.cookie = cookieName + "=" + cookieValue + ";" + expires + ";path=/";
}

function getCookie(cname) {

    // Content-unaware function that gets a cookie value.

    // The code is used from publicly available snippet https://www.w3schools.com/js/js_cookies.asp.

    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return undefined;

}

function eraseCookie(name) {

    // Content-unaware function that deletes a cookie.

    // The code is used from publicly available snippet https://stackoverflow.com/questions/2144386/how-to-delete-a-cookie.

    document.cookie = name+'=; Max-Age=-99999999;';

}

function deleteCookies( name=undefined ) {

    // Content-unaware function that deletes a cookie.

    // The code is used from publicly available snippet https://stackoverflow.com/questions/179355/clearing-all-cookies-with-javascript.

    if( name==undefined ) {
        // simply delete all cookies
        document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
        return
    }

    // delete all cookies with the same name

    // help:
    // https://www.tutorialspoint.com/How-can-I-delete-all-cookies-with-JavaScript
    // https://stackoverflow.com/questions/10593013/delete-cookie-by-name

    document.cookie = name + '=;expires='+ new Date().toUTCString();

}

function getCurrentTimestamp() {

    // Obtains current timestamp.

    // The code is adapted from the CO1111-w19-lec-Testing.pdf worksheet.
    // help:
    // https://www.w3docs.com/snippets/javascript/how-to-get-the-current-date-and-time-in-javascript.html
    // https://stackoverflow.com/questions/6040515/how-do-i-get-month-and-date-of-javascript-in-2-digit-format

    const now = new Date();
    const m = now.getMonth()+1;
    const d = now.getDay()+1;
    let timestamp = `${now.getFullYear()}.${m}.${d}_${now.getHours()}.${now.getMinutes()}.${now.getSeconds()}_${now.getMilliseconds()}`;
    return timestamp;

}

function setUniqueUserId() {

    // I use this function to set unique user id as a cookie when someone
    // loads my app for the first time.

    // For the user id I use current datetime.
    // I expect that only one user will access the app at one given millisecond.

    previousUserId = getCookie( 'user_id' );
    if( previousUserId != undefined ) {
        // cookie already set, no need to do anything
        return;
    }

    // cookie not set, create one

    const userId = getCurrentTimestamp();
    setCookie( 'user_id', userId )

}

async function asyncRequest( link ) {

    // Context-unaware function for sending asynchronous
    // requests and handling
    // request failures.

    // The code is adapted from worksheet "CO1111-w15-lec-NetworkingAndProgrammableWeb.pdf".

    // help:
    // https://javascript.info/fetch
    // https://dmitripavlutin.com/javascript-fetch-async-await/

    const response = await fetch( link );

    if( response.status=="ERROR" ) {

        // handle request errors

        return;

    }

    // data returned by api can contain other errors
    const DATA = await response.json();
    return DATA;

}

//-------------------------------------------------------------------------------------------------------------------+++
// 2022.04.10
// added timestamp and user id functions.