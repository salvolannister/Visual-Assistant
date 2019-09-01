var model, modelRotY=0, tmpMesh;
var Myhistory = [];
const video = document.getElementById('video');
var scene, camera, renderer, light;
var mouse = {};
var  i = 0;

const constrains = {
  audio: true,
  video: {
     mandatory: {
        minWidth: window.innerWidth,
    }
  }
}
// var axes = new THREE.AxisHelper(60);
// axes.position.set(0, 0, 0);
// scene.add(axes);

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



function onDocumentMouseMove(event) {
    // Current mouse position with [0,0] in the center of the window
    // and ranging from -1.0 to +1.0 with `y` axis inverted.
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

}

function initVase(){
    var loader = new THREE.GLTFLoader();
    loader.load(
       "./vaso.glb",
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


function onWindowResize() {
				camera.aspect = window.innerWidth / window.innerHeight;
				camera.updateProjectionMatrix();
				renderer.setSize( window.innerWidth, window.innerHeight );
			}

function update() {
        /* bisogna aspettare che
        il modello sia caricato */
        if (model) {

          modelRotY += 0.01;
          model.rotation.y = modelRotY;
          model.position.x = 0.5 ;
        }

      }

function projection(){
  var vector = new THREE.Vector3(mouse.x, mouse.y, 0.0);
    // Unproject camera distortion (fov, aspect ratio)
    vector.unproject(camera);
    var norm = vector.sub(camera.position).normalize();
    // Cast a line from our camera to the tmpMesh and see where these
    // two intersect. That's our 2D position in 3D coordinates.
    var ray = new THREE.Raycaster(camera.position, norm);

  if(tmpMesh)  var intersects = ray.intersectObject(tmpMesh);
  if(model) {
      //window.alert(mouse.x);
      model.position.x = intersects[0].point.x;
      model.position.y = intersects[0].point.y;
    }
}

function animate() {
  update();
  //projection();
  renderer.setClearColor(0x000000, 0);
  renderer.render( scene, camera );
  requestAnimationFrame( animate );


}

async function getMedia() {

  try {
    const  stream = await navigator.mediaDevices.getUserMedia(constrains);
    handleSuccess(stream);
    /* use the stream */


  } catch(err) {
    /* handle the error */
    console.log(err.toString());
  }
}

function handleSuccess(stream){
  window.stream = stream;
  video.srcObject = stream;
var width = stream.clientWidth;
}

document.addEventListener('DOMContentLoaded', function(event) {
 //document.addEventListener('mousemove', onDocumentMouseMove, false);
 init(50,50);
 initLight();
 initPlane();
 initVase();
 console.log("vaso inizializzato")
 animate();

 getMedia();
 /*initLight();
 initPlane();
 initVase();
 console.log("vaso inizializzato")
 animate();
 requestAnimationFrame(render);*/
    }
  );

 var ws = new WebSocket('ws://localhost:9000/');
 ws.onopen = function() {
    console.log("connected")
 };

 ws.onmessage = function (event) {
     var m = JSON.parse(event.data);
     Myhistory.push({
       x: m.x * 2 - 1,
       y: -m.y * 2 + 1
     });

/* funzione per osservare i valori
     for (var i=0; i<Myhistory.length; i++) {
      var counter = Myhistory[i];
     console.log(counter.x );} */



  /* ... rest of the function. */
 };
