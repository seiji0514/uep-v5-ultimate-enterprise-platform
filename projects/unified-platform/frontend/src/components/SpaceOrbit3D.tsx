/**
 * 軌道の簡易3D可視化（Three.js）
 */
import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface Satellite {
  id: string;
  name: string;
  orbit_km: number;
  inclination: number;
  period_min: number;
  status: string;
}

interface SpaceOrbit3DProps {
  satellites: Satellite[];
}

const FALLBACK_SATELLITES: Satellite[] = [
  { id: 'ISS', name: 'ISS', orbit_km: 408, inclination: 51.6, period_min: 92.9, status: 'Active' },
  { id: 'HUBBLE', name: 'Hubble', orbit_km: 547, inclination: 28.5, period_min: 96, status: 'Active' },
  { id: 'STARLINK', name: 'Starlink', orbit_km: 550, inclination: 53, period_min: 96.2, status: 'Active' },
  { id: 'LANDSAT', name: 'Landsat 9', orbit_km: 705, inclination: 98.2, period_min: 99, status: 'Active' },
  { id: 'GOES', name: 'GOES-18', orbit_km: 35786, inclination: 0, period_min: 1436, status: 'Active' },
];

export const SpaceOrbit3D: React.FC<SpaceOrbit3DProps> = ({ satellites }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const data = satellites?.length ? satellites : FALLBACK_SATELLITES;

  useEffect(() => {
    if (!containerRef.current) return;

    const width = Math.max(containerRef.current.clientWidth || 400, 100);
    const height = 320;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 10000);
    camera.position.set(0, 400, 600);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setClearColor(0x0a0e14, 1);
    containerRef.current.innerHTML = '';
    containerRef.current.appendChild(renderer.domElement);

    // Earth
    const earthGeo = new THREE.SphereGeometry(40, 32, 32);
    const earthMat = new THREE.MeshPhongMaterial({
      color: 0x1a4d6e,
      emissive: 0x0d2137,
      specular: 0x00d4ff,
      shininess: 8,
    });
    const earth = new THREE.Mesh(earthGeo, earthMat);
    scene.add(earth);

    // Ambient + directional light
    scene.add(new THREE.AmbientLight(0x333333));
    const light = new THREE.DirectionalLight(0xffffff, 0.8);
    light.position.set(300, 200, 200);
    scene.add(light);

    // Orbit rings and satellites
    const orbitColor = (km: number) => (km < 2000 ? 0x00ff41 : km < 36000 ? 0x00d4ff : 0xffb000);
    const meshes: THREE.Mesh[] = [];

    data.slice(0, 5).forEach((s, i) => {
      const r = 50 + Math.min((s.orbit_km || 400) / 20, 120) + i * 15;
      const ringGeo = new THREE.RingGeometry(r - 1, r + 1, 64);
      const ringMat = new THREE.MeshBasicMaterial({
        color: orbitColor(s.orbit_km || 400),
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.6,
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = Math.PI / 2;
      ring.rotation.z = ((s.inclination || 0) * Math.PI) / 180;
      scene.add(ring);

      const satGeo = new THREE.SphereGeometry(3, 16, 16);
      const satMat = new THREE.MeshBasicMaterial({ color: orbitColor(s.orbit_km || 400) });
      const sat = new THREE.Mesh(satGeo, satMat);
      const angle = (i * 72 + (Date.now() / 1000) * (60 / (s.period_min || 90))) * (Math.PI / 180);
      sat.position.set(r * Math.cos(angle), 0, r * Math.sin(angle));
      sat.position.applyAxisAngle(new THREE.Vector3(1, 0, 0), ((s.inclination || 0) * Math.PI) / 180);
      scene.add(sat);
      meshes.push(sat);
    });

    let animId: number;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      const t = Date.now() / 1000;
      data.slice(0, 5).forEach((s, i) => {
        if (meshes[i]) {
          const r = 50 + Math.min((s.orbit_km || 400) / 20, 120) + i * 15;
          const angle = (i * 72 + t * (60 / (s.period_min || 90))) * (Math.PI / 180);
          meshes[i].position.set(r * Math.cos(angle), 0, r * Math.sin(angle));
          meshes[i].position.applyAxisAngle(new THREE.Vector3(1, 0, 0), ((s.inclination || 0) * Math.PI) / 180);
        }
      });
      earth.rotation.y += 0.002;
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth || 400;
      camera.aspect = w / height;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
      containerRef.current?.removeChild(renderer.domElement);
    };
  }, [data]);

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        minHeight: 320,
        backgroundColor: '#0a0e14',
        borderRadius: 4,
        border: '1px solid #00d4ff40',
      }}
    />
  );
};
