import * as faceapi from "face-api.js";
import { getAllFaces } from "../api/client";

const MODEL_URL = "/models";
// face-api.js euclideanDistance threshold for a "same person" match.
// This mirrors the 0.45 threshold used by the old dlib-based matcher,
// but face-api.js embeddings are NOT compatible with dlib embeddings,
// so patients enrolled by the old desktop app must be re-enrolled here.
export const MATCH_THRESHOLD = 0.5;

let modelsLoaded = false;
let loadingPromise = null;

export function loadFaceModels() {
  if (modelsLoaded) return Promise.resolve();
  if (loadingPromise) return loadingPromise;

  loadingPromise = Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
    faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
    faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  ]).then(() => {
    modelsLoaded = true;
  });

  return loadingPromise;
}

/**
 * Detects a single face in a video/image element and returns its
 * 128-d descriptor (embedding), or null if no face is found.
 */
export async function getFaceDescriptor(mediaElement) {
  await loadFaceModels();

  const detection = await faceapi
    .detectSingleFace(mediaElement, new faceapi.TinyFaceDetectorOptions())
    .withFaceLandmarks()
    .withFaceDescriptor();

  if (!detection) return null;
  return detection.descriptor; // Float32Array(128)
}

export function descriptorToString(descriptor) {
  return Array.from(descriptor).join(",");
}

export function stringToDescriptor(str) {
  return new Float32Array(str.split(",").map(Number));
}

function euclideanDistance(a, b) {
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    const d = a[i] - b[i];
    sum += d * d;
  }
  return Math.sqrt(sum);
}

/**
 * Compares a live descriptor against every enrolled patient's stored
 * embedding (fetched from the backend) and returns the closest match
 * within MATCH_THRESHOLD, mirroring FaceIdentifier.identify() in the
 * original Python app.
 */
export async function identifyFace(descriptor) {
  const faces = await getAllFaces();

  let best = null;
  let bestDistance = Infinity;

  for (const face of faces) {
    const raw = face.embeddingVector;
    if (!raw || !raw.trim()) continue;

    let known;
    try {
      known = stringToDescriptor(raw);
      if (known.length !== descriptor.length) continue;
    } catch {
      continue;
    }

    const distance = euclideanDistance(known, descriptor);
    if (distance < bestDistance) {
      bestDistance = distance;
      best = face;
    }
  }

  if (best && bestDistance < MATCH_THRESHOLD) {
    return { found: true, patientId: best.patientId, distance: bestDistance };
  }

  return { found: false, distance: bestDistance === Infinity ? null : bestDistance };
}
