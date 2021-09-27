var currentLocation = window.location;
var str = String(currentLocation.pathname)
var urlLanguage = ''
if (str.indexOf("/ru/") !=-1 ) {
    urlLanguage = "/ru/"
} else if (str.indexOf("kk") !=-1) {
    urlLanguage = "/kk/"
} else urlLanguage = "/"


