import * as THREE from 'three';

let scene, camera, renderer, raycaster, content, boundingContent;
let mouse = new THREE.Vector2(), INTERSECTED;

const init = (container) => {
  content = container;
  boundingContent = content.getBoundingClientRect();
  scene = new THREE.Scene();
  scene.background = new THREE.Color( 0xf0f0f0 );

  camera = new THREE.PerspectiveCamera( 75, content.offsetWidth / content.offsetHeight, 1, 10000 );
  camera.position.y = 500;
  camera.position.z = 1000;
  camera.lookAt(0,0,0);

  raycaster = new THREE.Raycaster();


  renderer = new THREE.WebGLRenderer();
  renderer.setPixelRatio(content.devicePixelRatio );
  renderer.setSize( content.offsetWidth, content.offsetHeight );
  content.appendChild( renderer.domElement );

  content.addEventListener( 'mousemove', onDocumentMouseMove, false );
  window.addEventListener( 'resize', onWindowResize, false );
}

const addCubes = () => {
  const dimensions = [[112,112,64], [56,56,64], [56,56,192], [28,28,192], [28,28,256], [28,28,480], [14,14,480], [14,14,512]];
  let prevX = -2400;
  for(let i = 0; i < dimensions.length; i++){
    let dim = dimensions[i];

    dim = dim.map((num)=>num*2);

    const material = new THREE.MeshLambertMaterial( { color: Math.random() * 0xffffff } );
    const geometry = new THREE.BoxGeometry( dim[2], dim[1], dim[0] );
    const cube = new THREE.Mesh( geometry, material );

    if( i !== 0){
      prevX += dim[2]/2 + 30
    }
    cube.position.x = prevX;
    prevX += dim[2]/2;
    console.log(prevX)

    scene.add(cube);
  }
}

const addLight = () => {
  const light = new THREE.PointLight( 0xffffff, 1 );
  light.position.set( 1, 500, 1000 );
  scene.add( light )
}

const render = () => {
  raycaster.setFromCamera( mouse, camera );

  var intersects = raycaster.intersectObjects( scene.children );
  if ( intersects.length > 0 ) {
    if ( INTERSECTED != intersects[ 0 ].object ) {
      if ( INTERSECTED ) INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
      INTERSECTED = intersects[ 0 ].object;
      INTERSECTED.currentHex = INTERSECTED.material.emissive.getHex();
      INTERSECTED.material.emissive.setHex( 0xff0000 );
    }
  } else {
    if ( INTERSECTED ) INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
    INTERSECTED = null;
  }

  renderer.render( scene, camera );
}

const animate = () => {
  requestAnimationFrame( animate );


  render();
}

const run = (content) => {
  init(content);
  addCubes();
  addLight();
  animate();
}

const onDocumentMouseMove = ( event ) => {
  event.preventDefault();
  mouse.x = (( event.clientX - boundingContent.left) / content.offsetWidth ) * 2 - 1;
  mouse.y = - (( event.clientY - boundingContent.top) / content.offsetHeight ) * 2 + 1;
}

const onWindowResize = () => {
  camera.aspect = content.offsetWidth / content.offsetHeight;
  camera.updateProjectionMatrix();
  renderer.setSize( content.offsetWidth, content.offsetHeight );
}

export {run};
