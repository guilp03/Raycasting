import numpy as np
import re
import sys

# Ler arquivo .obj e definir uma malha de triângulos
#
# Como a coloração do triângulo precisa de um arquivo material, a cor rgb será
# fixada.
# Mais especificamente, o vertex texture associado a cada ponto de um polígono
# irá mapear a textura no polígono.
#
# shift translata o opjeto no espaço
#
#

def read_obj(path: str, cor, shift = (0,0,0)):
    triangulos = []
    vertices = []
    with open(path) as file:
        v_pattern = re.compile("v .*")
        vt_pattern = re.compile("vt .*")
        vn_pattern = re.compile("vn .*")
        f_pattern = re.compile("f .*")
        float_pattern = re.compile(r'-?\d+\.?\d*')
        int_pattern = re.compile(r'\d+')
        
        comment_patern = re.compile("#.*")
        for line in file:
            line = line.rstrip()
            if comment_patern.match(line):
                continue
            if v_pattern.match(line):
                # Ler os floats na linha
                nums = tuple(map(float, re.findall(float_pattern, line)))
                vertices.append(nums)
            if vt_pattern.match(line):
                # Não será usado no momento
                pass
            if vn_pattern.match(line):
                # Não será usado no momento
                pass
            if f_pattern.match(line):
                print(line)
                # Nesse caso, espera-se linhas na forma f a/x b/y c/z, particularmente
                nums = tuple(map(int, re.findall(int_pattern, line)))
                print(nums)
                # Reduzir 1 de index
                nums = tuple(map(lambda x: x-1, nums))
                
                if nums.__len__() == 6:
                    triangulo_colorless = (vertices[nums[0]], vertices[nums[2]], vertices[nums[4]])
                elif nums.__len__() == 9:
                    print(f"{nums[0]} {nums[3]} {nums[6]}")
                    triangulo_colorless = (vertices[nums[0]], vertices[nums[3]], vertices[nums[6]])
                # Recuperar vertexes do triângulo
                triangulo = (cor,) + triangulo_colorless
                triangulos.append(triangulo)
    print(triangulos.__len__())
    return triangulos
                
                
                
                
            

#read_obj("square.obj", (0,0,0))