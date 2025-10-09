
from Objeto3D import *


class Transicao3D():
    def __init__(self):
        self.o1 = Objeto3D()
        self.o2 = Objeto3D()
        self.interpolated = Objeto3D()
        self.stagesVertex = []
        self.progess = 0.0

    def loadObj1(self, file:str):
        self.o1.LoadFile(file)
    
    def loadObj2(self, file:str):
        self.o2.LoadFile(file)

    def preprocess(self):
        if len(self.o2.faces) > len(self.o1.faces):
            aux = self.o2
            self.o2 = self.o1
            self.o1 = aux

        mid_o1 = self.getMidPoint(self.o1)
        mid_o2 = self.getMidPoint(self.o2)
        mid_diff = mid_o1 - mid_o2;

        for vertex in self.o2.vertices:
            vertex.set(
                vertex.x + mid_diff.x,
                vertex.y + mid_diff.y,
                vertex.z + mid_diff.z
                )

        self.stagesVertex = [[] for _ in range(10)]

        self.interpolated.faces = self.o1.faces.copy()
        self.interpolated.vertices = self.o1.vertices.copy()

        self.stagesVertex[0] = self.interpolated.vertices.copy()

        for i in range(1,10):
            self.stagesVertex[i] = [Ponto(b.x, b.y, b.z) for b in self.o1.vertices]
            porcento1 = (10-i)/10
            porcento2 = i/10
            for face in self.interpolated.faces:
                mid = Ponto(0, 0, 0)
                for iv in face:
                    mid += self.stagesVertex[i-1][iv]
                mid/=len(face)
                nearest_face_idx, nearest_distance, nearest_mid = self.findNearest(mid, self.o2)
                nearFace = self.o2.faces[nearest_face_idx]
                diff = nearest_mid - mid

                #problema: alguns poligonos tem 4 vertices, outros 3

                while(len(nearFace)>len(face)):
                    face.append(face[0])
                while(len(face)>len(nearFace)):
                    nearFace.append(nearFace[0])
                
                for ix in range(len(face)):
                    vertex = self.o1.vertices[face[ix]]
                    nearVertex = self.o2.vertices[nearFace[ix]]  # Fixed: use len(nearFace) instead of len(face)
                    new_vet = Ponto(
                        vertex.x*porcento1 + nearVertex.x * porcento2,
                        vertex.y*porcento1 + nearVertex.y*porcento2,
                        vertex.z*porcento1 + nearVertex.z*porcento2
                    )
                    self.stagesVertex[i][face[ix]] = new_vet

                """ for ixv in face:
                    vertex = self.o1.vertices[ixv]
                    _, _, o2_vec = self.findNearestVertex(vertex, self.o2)
                    new_vec = Ponto(
                        vertex.x * porcento1 + o2_vec.x * porcento2,
                        vertex.y * porcento1 + o2_vec.y * porcento2,
                        vertex.z * porcento1 + o2_vec.z * porcento2
                    )

                    self.stagesVertex[i][ixv] = new_vec """
    
    def update(self):
        #self.stagesVertex.append(self.interpolated.vertices)
        if len(self.stagesVertex)>0:
            self.interpolated.vertices = self.stagesVertex.pop(0)
        self.interpolated.Desenha()
        #self.interpolated.DesenhaVertices()
        self.interpolated.DesenhaWireframe()
    
                
                
    def findNearest(self, target_point, obj):

        nearest_face_index = 0
        nearest_distance = float('inf')
        nearest_face_center = None
        
        for face_idx, face in enumerate(obj.faces):

            face_center = Ponto(0, 0, 0)
            for vertex_idx in face:
                face_center += obj.vertices[vertex_idx]
            face_center /= len(face)

            distance = self._calculate_distance(target_point, face_center)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_face_index = face_idx
                nearest_face_center = face_center
                
        return nearest_face_index, nearest_distance, nearest_face_center
    
    def _calculate_distance(self, point1, point2):
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        dz = point1.z - point2.z
        return (dx*dx + dy*dy + dz*dz) ** 0.5
    
    def findNearestVertex(self, target_point, obj):
        nearest_vertex_index = 0
        nearest_distance = float('inf')
        nearest_vertex = None
        
        for vertex_idx, vertex in enumerate(obj.vertices):
            distance = self._calculate_distance(target_point, vertex)
            
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_vertex_index = vertex_idx
                nearest_vertex = vertex
                
        return nearest_vertex_index, nearest_distance, nearest_vertex
    
    def getFaceCenter(self, face, obj):

        center = Ponto(0, 0, 0)
        for vertex_idx in face:
            center += obj.vertices[vertex_idx]
        center /= len(face)
        return center


    def getMidPoint(self, obj: Objeto3D):
        if not obj.vertices:
            return Ponto(0, 0, 0)
        mid = Ponto(0, 0, 0)
        for v in obj.vertices:
            mid += v
        mid /= len(obj.vertices)
        return mid