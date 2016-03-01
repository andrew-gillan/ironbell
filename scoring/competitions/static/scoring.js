function doCenter(){
    $('.score').css({
        position:'absolute',
        left: ($(window).width() - $('.score').outerWidth())/2,
        top: ($(window).height() - $('.score').outerHeight())/2
    });
    $('.timer-large').css({
        position:'absolute',
        left: ($(window).width() - $('.timer-large').outerWidth())/2,
        top: ($(window).height() - $('.timer-large').outerHeight())/2
    });
}
function getScoreAndTiming(eventId, stationNum){
    $.ajax({
        type: 'GET',
        dataType: "json",
        url: '/api/score/' + eventId + "/" + stationNum,
        success: function(data){
            var score = data.score;
            if ( document.getElementById("score") != null ) {
                document.getElementById("score").innerHTML = score;
            }
            if ( document.getElementById("score-half") != null ) {
                document.getElementById("score-half").innerHTML = score;
            }
            doCenter();

            var timer = data.event;
            if ( document.getElementById("timer") != null ) {
                // Update the timer unless this is station number 1
                document.getElementById("timer").innerHTML = timer;
            }
            if ( document.getElementById("timer-large") != null ) {
                document.getElementById("timer-large").innerHTML = timer;
            }
            if ( document.getElementById("timer-half") != null ) {
                document.getElementById("timer-half").innerHTML = timer;
            }
            checkCurrentEvent(data, eventId);
        }
    });
}
function getTimer(eventId, stationNum, isJudge){
    $.ajax({
        type: 'GET',
        dataType: "json",
        url: '/api/timer/' + eventId,
        success: function(data){
            // Judging Station #1 sets timing and score and so it doesn't need to
            // set UI values, all other judging stations need timing.
            if ( !isJudge || (isJudge && stationNum != 1) ) {
                var timer = data.timer;
                if ( document.getElementById("timer") != null ) {
                    document.getElementById("timer").innerHTML = timer;
                }
                if ( document.getElementById("timer-large") != null ) {
                    document.getElementById("timer-large").innerHTML = timer;
                }
            }

            checkCurrentEvent(data, eventId);
        }
    });
}
function checkCurrentEvent(data, eventId) {
    // Check to to verify that the current event matches
    if ( data.current_event_id > 0 && data.current_event_id != eventId ) {
        // redirect to the current event
        var currentPath = document.location.pathname;

        //                               comp     evt       stn
        // Spectator URL example: /scoring/1/event/1/station/1/
        // Timing URL example:    /scoring/1/event/1/timer/
        // Judging URL example:   /scoring/1/event/1/judging/1/

        if ( currentPath.indexOf("station") != -1 ||
             currentPath.indexOf("timer") != -1 ||
             currentPath.indexOf("judging") != -1 )
        {
            var pathArray = currentPath.split( '/' );

            // Setup new path as a relative path
            currentPath = "";
            pathArray[4] = data.current_event_id;
            for ( i = 0; i < pathArray.length; i++ ) {
                if ( pathArray[i] != "" ) {
                    currentPath += "/";
                    currentPath += pathArray[i];
                }
            }

            var newURL = window.location.protocol + "//" + window.location.host + currentPath;
            //window.location.replace(newURL);
            window.location.href = newURL;
        }
    }
}
// Found on http://stackoverflow.com/questions/1191865/code-for-a-simple-javascript-countdown-timer
function Countdown(options) {
    var timer,
    instance = this,
    seconds = options.seconds || 10,
    updateStatus = options.onUpdateStatus || function () {},
    counterEnd = options.onCounterEnd || function () {};

    var startTime = null;
    var elapsed = '0.0';

    function decrementCounter() {
        var time = new Date().getTime() - startTime;
        elapsed = Math.floor(time / 100) / 10;
        if ( Math.round(elapsed) == elapsed ) {
            elapsed += '.0';
        }

        updateStatus(options.seconds-elapsed);
        if (options.seconds-elapsed <= 0) {
            counterEnd();
            instance.stop();
        }
    }

    this.start = function () {
        clearInterval(timer);
        updateStatus(options.seconds);
        startTime = new Date().getTime();
        timer = setInterval(decrementCounter, 1000);
    };

    this.stop = function () {
        clearInterval(timer);
    };
}
