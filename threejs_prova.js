var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer({alpha : true});
renderer.setSize( window.innerWidth, window.innerHeight );
//renderer.setPixelRatio( window.devicePixelRatio );
renderer.gammaOutput = true;
renderer.gammaFactor = 2.2;
document.body.appendChild( renderer.domElement );

camera.position.z = 1;



var loader = new THREE.GLTFLoader();
loader.load(
   "./vaso.glb",
   function ( gltf ) {
    scene.add(gltf.scene);

    gltf.animations; // Array<THREE.AnimationClip>
		gltf.scene; // THREE.Scene
		gltf.scenes; // Array<THREE.Scene>
		gltf.cameras; // Array<THREE.Camera>
		gltf.asset; // Object

   },
);

function animate() {
	requestAnimationFrame( animate );
	renderer.render( scene, camera );
}
animate();
