
from Objeto3D import *


class Transicao3D():
    def __init__(self, num_frames: int):
        self.o1 = Objeto3D()
        self.o2 = Objeto3D()
        self.interpolated = Objeto3D()
        self.interpolatedColors = [() for _ in range(num_frames)]
        self.stagesVertex = []
        self.progess = 0.0
        self.num_frames = num_frames

    def loadObj1(self, src):
        if isinstance(src, str):
            self.o1.LoadFile(src)
        elif isinstance(src, Objeto3D):
            self.o1 = src.copy()
    
    def loadObj2(self, src):
        if isinstance(src, str):
            self.o2.LoadFile(src)
        elif isinstance(src, Objeto3D):
            self.o2 = src.copy()

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
            
        self.interpolateColors()


        self.interpolated.faces = self.o1.faces.copy()
        self.interpolated.vertices = self.o1.vertices.copy()
        self.stagesVertex = [self.interpolated.vertices.copy() for _ in range(self.num_frames)]

        o2_facen = len(self.o2.faces)
        normalizer = self.num_frames-1
        for i in range(len(self.o1.faces)):
            o1_face = self.o1.faces[i]
            target_face = self.o2.faces[i%o2_facen]

            while(len(target_face)>len(o1_face)):
                o1_face.append(o1_face[0])
            while(len(o1_face)>len(target_face)):
                target_face.append(target_face[0])

            for ix in range(len(o1_face)):
                    vertex = self.o1.vertices[o1_face[ix]]
                    nearVertex = self.o2.vertices[target_face[ix]] 
                    for j in range(1, self.num_frames):
                        porcento1 = (normalizer-j)/normalizer
                        porcento2 = j/normalizer
                        new_vet = Ponto(
                            vertex.x*porcento1 + nearVertex.x * porcento2,
                            vertex.y*porcento1 + nearVertex.y*porcento2,
                            vertex.z*porcento1 + nearVertex.z*porcento2
                        )
                        self.stagesVertex[j][o1_face[ix]] = new_vet

    def preprocessProx(self):
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
            
        self.interpolateColors()


        self.interpolated.faces = self.o1.faces.copy()
        self.interpolated.vertices = self.o1.vertices.copy()
        self.stagesVertex = [self.interpolated.vertices.copy() for _ in range(self.num_frames)]

        map = [False for _ in self.interpolated.faces]

        normalizer = self.num_frames-1
        for i in range(len(self.o1.faces)):
            o1_face = self.o1.faces[i]
            target_idx, _, _ = self.findNearest(self.getFaceCenter(o1_face, self.o1), self.o2, map)
            map[target_idx] = True
            target_face = self.o2.faces[target_idx]

            while(len(target_face)>len(o1_face)):
                o1_face.append(o1_face[0])
            while(len(o1_face)>len(target_face)):
                target_face.append(target_face[0])

            for ix in range(len(o1_face)):
                    vertex = self.o1.vertices[o1_face[ix]]
                    nearVertex = self.o2.vertices[target_face[ix]] 
                    for j in range(1, self.num_frames):
                        porcento1 = (normalizer-j)/normalizer
                        porcento2 = j/normalizer
                        new_vet = Ponto(
                            vertex.x*porcento1 + nearVertex.x * porcento2,
                            vertex.y*porcento1 + nearVertex.y*porcento2,
                            vertex.z*porcento1 + nearVertex.z*porcento2
                        )
                        self.stagesVertex[j][o1_face[ix]] = new_vet
    
    def update(self):
        self.stagesVertex.append(self.interpolated.vertices)
        if len(self.stagesVertex)>0:
            self.interpolated.vertices = self.stagesVertex.pop(0)
        newColor = self.interpolatedColors.pop(0)
        self.interpolatedColors.append(newColor)
        self.interpolated.setColor(newColor)
        self.interpolated.Desenha()
        #self.interpolated.DesenhaVertices()
        self.interpolated.DesenhaWireframe()
    
                
                
    def findNearest(self, target_point, obj, map):

        nearest_face_index = 0
        nearest_distance = float('inf')
        nearest_face_center = None
        
        for face_idx, face in enumerate(obj.faces):

            if not map[face_idx]:
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
    def interpolateColors(self):
        denom = self.num_frames - 1
        for i in range(0, self.num_frames):
            w1 = (denom - i) / denom
            w2 = i / denom
            self.interpolatedColors[i] = tuple(w1*a + w2*b for a, b in zip(self.o1.color, self.o2.color))