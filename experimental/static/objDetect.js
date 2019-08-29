//Parameters
const s = document.getElementById('objDetect');
const sourceVideo = s.getAttribute("data-source");  //the source video to use
const uploadWidth = s.getAttribute("data-uploadWidth") || 640; //the width of the upload file
const mirror = s.getAttribute("data-mirror") || false; //mirror the boundary boxes
const apiServer = s.getAttribute("data-apiServer") || window.location.origin + '/image';

//Video element selector
v = document.getElementById(sourceVideo);

//for starting events
let isPlaying = false,
    gotMetadata = false;

//Canvas setup

//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d");

//create a canvas for drawing object boundaries
let drawCanvas = document.createElement('canvas');
document.body.appendChild(drawCanvas);
let drawCtx = drawCanvas.getContext("2d");

//Start object detection
function startObjectDetection() {

    console.log("starting object detection");

    //Set canvas sizes base don input video
    drawCanvas.width = v.videoWidth;
    drawCanvas.height = v.videoHeight;
    // the image that is sent is reduced in order to decrease the bandwidth needed
    imageCanvas.width = uploadWidth;
    imageCanvas.height = uploadWidth * (v.videoHeight / v.videoWidth);

    //Some styles for the drawcanvas
    drawCtx.lineWidth = "4";
    drawCtx.strokeStyle = "cyan";
    drawCtx.font = "20px Verdana";
    drawCtx.fillStyle = "cyan";

    //Save and send the first image
imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
imageCanvas.toBlob(postFile, 'image/jpeg');

}

function postFile(file) {
      // perché la mando due volte l'immagine??
    //Set options as form data
    let formdata = new FormData();
    formdata.append("image", file);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiServer, true);

    xhr.onload = function () {
        if (this.status === 200) {
        // 200 is loaded and it means the request succeded
        // so now we have to send domething
            let objects = JSON.parse(this.response);
            //console.log(objects);
             console.log(String(objects));
            //draw the boxes
            //drawBoxes(objects);

            //Send the next image
            imageCanvas.toBlob(postFile, 'image/jpeg');
            console.log("ma siamo qui??");
        }
        else{
            console.error(this.statusText);

        }
    };
     xhr.send(formdata);
}


//check if metadata is ready - we need the video size
v.onloadedmetadata = () => {
    console.log("video metadata ready");
    gotMetadata = true;
    if (isPlaying)
        startObjectDetection();
};

//see if the video has started playing
v.onplaying = () => {
    console.log("video playing");
    isPlaying = true;
    if (gotMetadata)
        startObjectDetection();

};