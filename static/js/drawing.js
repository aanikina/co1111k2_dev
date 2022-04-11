// The code in this file is from a
// publicly available snippet and can be found here:
// https://stackoverflow.com/questions/2368784/draw-on-html5-canvas-using-a-mouse

var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;

var x = "black",
    y = 2;

function init() {

    canvas=document.getElementById( 'can' );
    ctx=canvas.getContext( "2d" );
    w=canvas.width;
    h=canvas.height;

    //console.log( `width: ${w} height: ${h}` );

    canvas.addEventListener( "mousemove", function( e ) {
        findxy( 'move', e )
    }, false );
    canvas.addEventListener( "mousedown", function( e ) {
        findxy( 'down', e )
    }, false );
    canvas.addEventListener( "mouseup", function( e ) {
        findxy( 'up', e )
    }, false );
    canvas.addEventListener( "mouseout", function( e ) {
        findxy( 'out', e )
    }, false );

    // The code for the following event listeners that
    // handle touch interaction
    // is appropriated from publicly available snippet which can be found here:
    // https://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html

    canvas.addEventListener( "touchstart", function( e ) {
        mousePos=getTouchPos( canvas, e );
        var touch=e.touches[ 0 ];
        var mouseEvent=new MouseEvent( "mousedown", {
            clientX: touch.clientX,
            clientY: touch.clientY
        } );
        canvas.dispatchEvent( mouseEvent );
    }, false );
    canvas.addEventListener( "touchend", function( e ) {
        var mouseEvent=new MouseEvent( "mouseup", {} );
        canvas.dispatchEvent( mouseEvent );
    }, false );
    canvas.addEventListener( "touchmove", function( e ) {
        var touch=e.touches[ 0 ];
        var mouseEvent=new MouseEvent( "mousemove", {
            clientX: touch.clientX,
            clientY: touch.clientY
        } );
        canvas.dispatchEvent( mouseEvent );
    }, false );

    // Get the position of a touch relative to the canvas
    function getTouchPos( canvasDom, touchEvent ) {
        var rect=canvasDom.getBoundingClientRect();
        return {
            x: touchEvent.touches[ 0 ].clientX-rect.left,
            y: touchEvent.touches[ 0 ].clientY-rect.top
        };
    }

    // Prevent scrolling when touching the canvas
    document.body.addEventListener("touchstart", function (e) {
        if (e.target == canvas) {
            e.preventDefault();
        }
    }, false);
    document.body.addEventListener("touchend", function (e) {
        if (e.target == canvas) {
            e.preventDefault();
        }
    }, false);
    document.body.addEventListener("touchmove", function (e) {
        if (e.target == canvas) {
            e.preventDefault();
        }
    }, false);

}

function colorUi(obj) {

    x = obj.id; // assign colour
    if(x == "eraser") {
        x="beige";
        y = 14;
    }
    else y = 2;

    // record ui button being used
    let yaml = `---\nbt: ${x}\ntimestamp: ${getCurrentTimestamp()}\n`;
    statsUi += yaml;

}

function colorAlt( color ) {

    x = color
    if( color=="eraser") {
        x="beige";
        y = 14;
    }
    else y = 2;

}

function draw() {
    //console.log( x );
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = x;
    ctx.lineWidth = y;
    ctx.stroke();
    ctx.closePath();
}

function erase() {
    ctx.clearRect(0, 0, w, h);
}
function eraseUi() {

    // record ui button being used
    let yaml = `---\nbt: erase\ntimestamp: ${getCurrentTimestamp()}\n`;
    statsUi += yaml;

    erase();

}

function save() {

    // this form data will be populated by various items
    // on server i will access them as python dictionary
    const formData = new FormData();

    // image
    var dataURL = canvas.toDataURL();
    formData.append( 'image64', dataURL );

    // user agent
    formData.append( 'user_agent', navigator.userAgent );

    // user id, chosen bodypart and final timestamp
    let user_id = getCookie('user_id');
    let tstamp = getCurrentTimestamp();
    formData.append( 'user_id', user_id );
    formData.append( 'bodypartiloc', getCookie('bodypartiloc') );
    formData.append( 'timestamp', tstamp );

    // usage stats
    formData.append( 'stats_keyboard', statsKeyboard );
    formData.append( 'stats_ui', statsUi );

    // submit time
    formData.append( 'submit_time', getCurrentTimestamp() );

    // upload form data to the server
    const request = new XMLHttpRequest();
    request.open( 'POST', `/upload`, true );
    request.send( formData );

    // show result with the submitted image
    // help:
    // https://stackoverflow.com/questions/1226714/how-to-get-the-browser-to-navigate-to-url-in-javascript
    let filename = `${user_id}___${tstamp}.png`;
    window.location.href = `/result/${filename}`;

}
function saveUi() {

    // record ui button being used
    let yaml = `---\nbt: save\ntimestamp: ${getCurrentTimestamp()}\n`;
    statsUi += yaml;

    save();

}

function findxy(res, e) {
    if (res == 'down') {
        prevX = currX;
        prevY = currY;
        currX = e.clientX - canvas.offsetLeft;
        currY = e.clientY - canvas.offsetTop;

        flag = true;
        dot_flag = true;
        if (dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(currX, currY, 2, 2);
            ctx.closePath();
            dot_flag = false;
        }
    }
    if (res == 'up' || res == "out") {
        flag = false;
    }
    if (res == 'move') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;
            draw();
        }
    }
}