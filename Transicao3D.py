
from itertools import combinations
from math import floor
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
        
        orig_len = len(self.o1.vertices)
        cloned_vertices = []
        new_faces = []
        counter = 0
        o1v = self.o1.vertices
        for face in self.o1.faces:
            new_face = []
            for idx in face:
                v = o1v[idx]
                cloned_vertices.append(Ponto(v.x, v.y, v.z))
                new_face.append(orig_len + counter)
                counter += 1
            new_faces.append(new_face)

        self.o1.vertices.extend(cloned_vertices)
        self.o1.faces = new_faces

        global maxDist1, maxDist2

        maxDist1 = 0.0
        if len(self.o1.vertices) >= 2:
            maxDist1 = max(self._calculate_distance(a, b) for a, b in combinations(self.o1.vertices, 2))
        maxDist2 = 0.0
        if len(self.o2.vertices) >= 2:
            maxDist2 = max(self._calculate_distance(a, b) for a, b in combinations(self.o1.vertices, 2))

        self.interpolated.color = self.o1.color

        #normalizar os dados nao adiantou
        """
        maxX, maxY, maxZ = [max(getattr(v, a) for v in self.o1.vertices) for a in ('x', 'y', 'z')]
        maxxx = max(maxX, maxY, maxZ)
        self.o1.vertices = [Ponto(v.x/maxxx, v.y/maxxx, v.z/maxxx) for v in self.o1.vertices]
        maxX, maxY, maxZ = [max(getattr(v, a) for v in self.o2.vertices) for a in ('x', 'y', 'z')]
        maxxx = max(maxX, maxY, maxZ)
        self.o2.vertices = [Ponto(v.x/maxxx, v.y/maxxx, v.z/maxxx) for v in self.o2.vertices] 
        """

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

        map = [False for _ in self.o1.faces]

        #face_map1 = {v: set() for v in range(len(self.o1.vertices))}
        #for f_idx, f in enumerate(self.o1.faces):
        #    for v_idx in f: 
        #        face_map1[v_idx].add(f_idx)
        #face_map2 = {v: set() for v in range(len(self.o2.vertices))}
        #for f_idx, f in enumerate(self.o2.faces):
        #    for v_idx in f: 
        #        face_map2[v_idx].add(f_idx)
        
        
        #o2_facen = len(self.o2.faces)
        for i in range(len(self.o1.faces)):
            o1_face = self.o1.faces[i]
            #target_face = self.o2.faces[i%o2_facen]
            target_idx, _, _ = self.findNearest(self.getFaceCenter(o1_face, self.o1), self.o2, map)
            map[target_idx] = True
            target_face = self.o2.faces[target_idx]
            self.subdivide(i, target_idx, face_map1, 1)
            self.subdivide(target_idx, i, face_map2, 2)

        """ self.vertex_check = [False for _ in self.o2.vertices]
        self.vertex_map = {
            vidx: self.findNearestVertex(v1, self.o2)[0]
            for vidx, v1 in enumerate(self.o1.vertices)
        } """


        self.interpolated.faces = [list(f) for f in self.o1.faces]
        self.interpolated.vertices = [Ponto(p.x, p.y, p.z) for p in self.o1.vertices]
        self.stagesVertex = [[Ponto(p.x, p.y, p.z) for p in self.o1.vertices] for _ in range(self.num_frames)]

        map = [False for _ in self.interpolated.faces]
        o2_facen = len(self.o2.faces)
        normalizer = self.num_frames-1
        for i in range(len(self.o1.faces)):
            o1_face = list(self.o1.faces[i])
            target_idx, _, _ = self.findNearest(self.getFaceCenter(o1_face, self.o1), self.o2, map)
            map[target_idx] = True
            target_face = list(self.o2.faces[target_idx])


            for ix in range(len(o1_face)):
                    vertex_idx = o1_face[ix]
                    vertex = self.o1.vertices[vertex_idx]
                    mapped_idx = target_face[ix%len(target_face)]#self.vertex_map[vertex_idx]
                    nearVertex = self.o2.vertices[mapped_idx]
                    for j in range(1, self.num_frames):
                        porcento1 = (normalizer-j)/normalizer
                        porcento2 = j/normalizer
                        new_vet = Ponto(
                            vertex.x*porcento1 + nearVertex.x * porcento2,
                            vertex.y*porcento1 + nearVertex.y*porcento2,
                            vertex.z*porcento1 + nearVertex.z*porcento2
                        )
                        self.stagesVertex[j][o1_face[ix]] = new_vet

        #pra repetir o primeiro e ultimo frame
        for i in range(4):
            self.stagesVertex.insert(0, self.stagesVertex[0])
            self.stagesVertex.insert(-1, self.stagesVertex[-1])
            self.interpolatedColors.insert(0, self.interpolatedColors[0])
            self.interpolatedColors.insert(-1, self.interpolatedColors[-1])
        

    def subdivide(self, face_idx, target_face_idx, face_map, selector):
        vertices = self.o1.vertices if selector == 1 else self.o2.vertices
        faces = self.o1.faces if selector == 1 else self.o2.faces
        target_faces = self.o2.faces if selector == 1 else self.o1.faces
        face = faces[face_idx]
        tf = target_faces[target_face_idx]

        while(len(face)<len(tf)):
            facemid = floor(len(face)/2)
            vet1_idx = face[facemid]
            vet2_idx = face[facemid + 1]

            vet1 = vertices[vet1_idx]
            vet2 = vertices[vet2_idx]

            newVet = Ponto(
                (vet1.x + vet2.x)/2,
                (vet1.y + vet2.y)/2,
                (vet1.z + vet2.z)/2
                )
            
            vertices.append(newVet)
            new_idx = len(vertices)-1
            face.insert(facemid+1, new_idx)
            face_map[new_idx] = set()
            if face_idx >= 0:
                face_map[new_idx].add(face_idx)

            #codigo pra adicionar esse vertice nas faces que compartilham vertices, mas da errado
            #affected_faces = face_map.get(vet1_idx, []) | face_map.get(vet2_idx, []) 
            """ for f_idx in list(affected_faces):
                if f_idx == face_idx:
                    continue

                f = faces[f_idx]
                inserted = False
                m = len(f)

                for k in range(m):
                    i0 = f[k]
                    i1 = f[(k + 1) % m]
                    if i0 == vet1_idx and i1 == vet2_idx:
                        f.insert(k + 1, new_idx)
                        inserted = True
                        break 
                    elif i0 == vet2_idx and i1 == vet1_idx:
                        f.insert(k + 1, new_idx)
                        inserted = True
                        break 
                if inserted:
                    face_map[new_idx].add(f_idx) """


    def update(self):
        self.stagesVertex.append(self.interpolated.vertices)
        if len(self.stagesVertex)>0:
            self.interpolated.vertices = self.stagesVertex.pop(0)
        self.interpolatedColors.append(self.interpolated.color)
        newColor = self.interpolatedColors.pop(0)
        self.interpolated.setColor(newColor)
        self.interpolated.Desenha()
        #self.interpolated.DesenhaVertices()
        self.interpolated.DesenhaWireframe()
    
                
                
    def findNearest(self, target_point, obj, map):
        global maxDist1, maxDist2
        maxDist = (maxDist1 if obj is self.o1 else maxDist2)/2
        nearest_face_index = -1
        nearest_distance = float('inf')
        nearest_face_center = None

        nearest_unnocupied_face_index = -1
        nearest_unnocupied_distance = float('inf')
        nearest_unnocupied_face_center = None

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

            if not map[face_idx] and distance<=maxDist and distance < nearest_unnocupied_distance:
                nearest_unnocupied_face_index = face_idx
                nearest_unnocupied_distance = distance
                nearest_unnocupied_face_center = face_center
        
        if nearest_unnocupied_face_index != -1:
            return nearest_unnocupied_face_index, nearest_unnocupied_distance, nearest_unnocupied_face_center

        return nearest_face_index, nearest_distance, nearest_face_center
    
    def _calculate_distance(self, point1, point2):
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        dz = point1.z - point2.z
        return (dx*dx + dy*dy + dz*dz) ** 0.5
    
    def findNearestVertex(self, target_point, obj):
        nearest_vertex_index = -1
        nearest_distance = float('inf')
        nearest_vertex = None
        
        for vertex_idx, vertex in enumerate(obj.vertices):
            if self.vertex_check[vertex_idx] == False:
                distance = self._calculate_distance(target_point, vertex)
                
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_vertex_index = vertex_idx
                    nearest_vertex = vertex
        if nearest_vertex_index == -1:
             for vertex_idx, vertex in enumerate(obj.vertices):
                distance = self._calculate_distance(target_point, vertex)
                
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_vertex_index = vertex_idx
                    nearest_vertex = vertex
                    
        self.vertex_check[nearest_vertex_index] = True  
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
        denom = self.num_frames-1
        for i in range(0, self.num_frames):
            w1 = (denom - i) / denom
            w2 = i / denom
            self.interpolatedColors[i] = tuple(w1*a + w2*b for a, b in zip(self.o1.color, self.o2.color))