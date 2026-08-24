import cv2
import face_recognition
import numpy as np
import requests

class FaceIdentifier:
    def __init__(self):
        self.threshold = 0.45
    
    def identify(self,frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb)
        if len(encodings) == 0:
            return {
                "found": False,
                "message":" No face detected"
            }
        
        current_embedding = encodings[0]
        response = requests.get( "http://localhost:9090/patients/faces")
        if response.status_code != 200:
            return {
                "found": False,
                "message":" Unable to fetch database"
            }
        faces = response.json()
        known_embeddings = []
        valid_faces = []
        for face in faces:
            embedding_string =face["embeddingVector"]
            if(embedding_string is None or embedding_string.strip()==""):
                continue

            try:
                embedding = np.array(list(
                            map(float, embedding_string.split(","))
                ))

                known_embeddings.append(embedding)
                valid_faces.append(face)
            
            except:
                continue

        if len(known_embeddings) == 0:
            return{
                "found": False,
                "message":"No registered embeddings"
            }
        
        distances = face_recognition.face_distance(known_embeddings,current_embedding)
        best_index = np.argmin(distances)
        best_distance = distances[best_index]
        if best_distance< self.threshold:
            return{
                "found": True,
                "patientId": valid_faces[best_index]["patientId"],
                "distance": float(best_distance)\
            }
        
        return{
            "found": False,
            "distance":float(best_distance)
        }
    
  