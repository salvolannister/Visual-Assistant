var model, modelRotY=0, tmpMesh;
var history = [];
var ws = new WebSocket('ws://localhost:9000');

var mouse = {};
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 1000 );
var renderer = new THREE.WebGLRenderer({antialias: true, alpha : true});
renderer.setSize( window.innerWidth, window.innerHeight );
//renderer.setPixelRatio( window.devicePixelRatio );
renderer.gammaOutput = true;
renderer.gammaFactor = 2.2;
document.body.appendChild( renderer.domElement );



camera.position.set(0, 0, 3);
// var axes = new THREE.AxisHelper(60);
// axes.position.set(0, 0, 0);
// scene.add(axes);



function initPlane() {
    // The plane needs to be large to always cover entire scene
    var tmpGeometry = new THREE.PlaneGeometry(1000, 1000, 1, 1);
    tmpGeometry.position = new THREE.Vector3(0, 0, 0);
    tmpMesh = new THREE.Mesh(tmpGeometry);
}
initPlane()


function onDocumentMouseMove(event) {
    // Current mouse position with [0,0] in the center of the window
    // and ranging from -1.0 to +1.0 with `y` axis inverted.
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

}

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

function initLight() {
    light = new THREE.SpotLight(0xffffff);
    // Position the light slightly to a side to make shadows look better.
    light.position.set(400, 100, 1000);
    light.castShadow = true;
    scene.add(light);
}
initLight();

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
  projection();
	requestAnimationFrame( animate );
	renderer.render( scene, camera );

}
animate();

document.addEventListener('DOMContentLoaded', function(event) {
 document.addEventListener('mousemove', onDocumentMouseMove, false);

});

 ws.onopen = function() {
    console.log("connected")
 };

 ws.onmessage = function (event) {
     var m = JSON.parse(event.data);
     history.push({ x: m.x * 2 - 1, y: -m.y * 2 + 1});
     window.alert("X: "+x + " Y "+ y)
     // ... rest of the function.
 };
