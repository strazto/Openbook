import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';

var camera = null;
var scene = null;
var renderer = null;

function main() {
	const canvas = document.querySelector('#c');
	renderer = new THREE.WebGLRenderer({antialias: true, canvas, alpha: true});

	const fov = 75;
  const aspect = 2;  // the canvas default
  const near = 0.1;
  const far = 500;
  camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

  camera.position.z = 20;

  scene = new THREE.Scene();

  const boxWidth = 1;
  const boxHeight = 1;
  const boxDepth = 1;
  const geometry2 = new THREE.BoxGeometry(boxWidth, boxHeight, boxDepth);

  const material = new THREE.MeshBasicMaterial({color: 0x44aa88});
  const material2 = new THREE.MeshBasicMaterial({color: 0xFF0000});

  const cube = new THREE.Mesh(geometry2, material);

  cube.userData.draggable = true
	cube.userData.name = 'CUBE'

  const radius =  5.0;
	const widthSegments = 32;
	const heightSegments = 16;
	const geometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);

	const sphere = new THREE.Mesh(geometry, material2);

	sphere.position.x = 20;

  scene.add(cube);
  scene.add(sphere);

  sphere.userData.draggable = true
	sphere.userData.name = 'SPHERE'

	const controls = new OrbitControls( camera, renderer.domElement );

	const color = 0xFFFFFF;
  const intensity = 3;
  const light = new THREE.DirectionalLight(color, intensity);
  light.position.set(-1, 2, 4);
  scene.add(light);

  function resizeRendererToDisplaySize(renderer) {
    const canvas = renderer.domElement;
    // const width = canvas.clientWidth;
    const width = 2000;
    // const height = canvas.clientHeight;
	  const height = 2000;

    const needResize = canvas.width !== width || canvas.height !== height;
    if (needResize) {
	    renderer.setSize(width, height, false);
    }
    return needResize;
    }

    function render(time) {
	    time *= 0.001;  // convert time to seconds

	    if (resizeRendererToDisplaySize(renderer)) {
	   		const canvas = renderer.domElement;
	    	camera.aspect = canvas.clientWidth / canvas.clientHeight;
	    	camera.updateProjectionMatrix();
	  	}

	    const canvas = renderer.domElement;
  		camera.aspect = canvas.clientWidth / canvas.clientHeight;
  		camera.updateProjectionMatrix();
	     
	    // cube.rotation.x = time;
	    // cube.rotation.y = time;

	    // sphere.rotation.x = time;
	    // sphere.rotation.y = time;
	     
	    renderer.render(scene, camera);
	    
	    requestAnimationFrame(render);
    }

requestAnimationFrame(render);
}

const raycaster = new THREE.Raycaster(); // create once
const clickMouse = new THREE.Vector2();  // create once
const moveMouse = new THREE.Vector2();   // create once
var draggable;

export function animate() {
  dragObject();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

function intersect(pos) {
  raycaster.setFromCamera(pos, camera);
  return raycaster.intersectObjects(scene.children);
}

window.addEventListener('click', event => {
  if (draggable != null) {
    console.log(`dropping draggable ${draggable.userData.name}`)
    draggable = null
    return;
  }

  // THREE RAYCASTER
  clickMouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  clickMouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  const found = intersect(clickMouse);
  if (found.length > 0) {
    if (found[0].object.userData.draggable) {
      draggable = found[0].object
      console.log(`found draggable ${draggable.userData.name}`)
    }
  }
})

window.addEventListener('mousemove', event => {
  moveMouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  moveMouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
});

function dragObject() {
  if (draggable != null) {
    const found = intersect(moveMouse);
    if (found.length > 0) {
      for (let i = 0; i < found.length; i++) {
        // if (!found[i].object.userData.ground)
        //   continue
        
        let target = found[i].point;
        draggable.position.x = target.x
        draggable.position.z = target.z
      }
    }
  }
}

function createFloor() {
  let pos = { x: 0, y: -10, z: 3 };
  let scale = { x: 100, y: 2, z: 100 };

  let blockPlane = new THREE.Mesh(new THREE.BoxGeometry(),
       new THREE.MeshPhongMaterial({ color: 0xf9c834 }));
  blockPlane.position.set(pos.x, pos.y, pos.z);
  blockPlane.scale.set(scale.x, scale.y, scale.z);
  blockPlane.castShadow = true;
  blockPlane.receiveShadow = true;
  scene.add(blockPlane);

  blockPlane.userData.ground = true
}

main();
createFloor();
animate()