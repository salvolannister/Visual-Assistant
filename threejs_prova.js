var model, modelRotY=0;
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 1000 );
var renderer = new THREE.WebGLRenderer({antialias: true, alpha : true});
renderer.setSize( window.innerWidth, window.innerHeight );
//renderer.setPixelRatio( window.devicePixelRatio );
renderer.gammaOutput = true;
renderer.gammaFactor = 2.2;
document.body.appendChild( renderer.domElement );

camera.position.z= 1;



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
        }

      }



function animate() {
  update();
	requestAnimationFrame( animate );
	renderer.render( scene, camera );

}
animate();
