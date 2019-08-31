//Parameters
const s = document.getElementById('objDetect');
const sourceVideo = s.getAttribute("data-source");  //the source video to use
const uploadWidth = s.getAttribute("data-uploadWidth") || 640; //the width of the upload file
const mirror = s.getAttribute("data-mirror") || false; //mirror the boundary boxes
const apiServer = s.getAttribute("data-apiServer") || window.location.origin + '/image';
// variables to upload the model
var model, modelRotY=0, tmpMesh;
var scene, camera, renderer, light,X=0,Y=0;
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
            if (typeof objects.x === "undefined") {
                console.log("something is undefined");
            }else{
             console.log("X " +objects.x+ " Y " +objects.y);
            //draw the boxes
            X = objects.x;
            Y = objects.y;
            drawVase(objects);
            }
            //Send the next image
            imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
            imageCanvas.toBlob(postFile, 'image/jpeg');
            console.log("onload function end");
        }
        else{
            console.error(this.statusText);

        }
    };
     xhr.send(formdata);
}

function drawVase(objects){
    init(v.videoWidth,v.videoHeight);
    initLight();
    initPlane();
    initVase();
    requestAnimationFrame(render);

}

// update position of objects on the scene
function update() {
        /* bisogna aspettare che
        il modello sia caricato */
        if (model) {

          modelRotY += 0.01;
          model.rotation.y = modelRotY;
          model.position.x = X ;
          model.position.y = Y;
        }

      }

function render() {
  update();
  //projection();
  renderer.setClearColor(0x000000, 0);
  renderer.render( scene, camera );
  //schedule another frame
  requestAnimationFrame( render );
}

function init(width, height){
  var aspect = window.innerWidth/window.innerHeight;
   scene = new THREE.Scene();
 camera = new THREE.PerspectiveCamera( 45, aspect, 0.1, 1000 );
  camera.position.set(0, 0, 3);
   renderer = new THREE.WebGLRenderer({antialias: true, alpha : true});
  renderer.setSize( window.innerWidth, window.innerHeight);
  //renderer.setPixelRatio( window.devicePixelRatio );
  renderer.gammaOutput = true;
  renderer.gammaFactor = 2.2;
  document.body.appendChild( renderer.domElement );
}

function initPlane() {
    // The plane needs to be large to always cover entire scene
    var tmpGeometry = new THREE.PlaneGeometry(1000, 1000, 1, 1);
    tmpGeometry.position = new THREE.Vector3(0, 0, 0);
    tmpMesh = new THREE.Mesh(tmpGeometry);
}

function initVase(){
    var loader = new THREE.GLTFLoader();
    loader.load(
       "./static/vaso.glb",
       function ( gltf ) {
        model = gltf.scene

        scene.add(model);
        //model.rotation.y = 4.5
        gltf.animations; // Array<THREE.AnimationClip>
    		gltf.scene; // THREE.Scene
    		gltf.scenes; // Array<THREE.Scene>
    		gltf.cameras; // Array<THREE.Camera>
    		gltf.asset; // Object

       },
    );
  }

  function initLight() {
    light = new THREE.SpotLight(0xffffff);
    // Position the light slightly to a side to make shadows look better.
    light.position.set(400, 100, 1000);
    light.castShadow = true;
    scene.add(light);
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