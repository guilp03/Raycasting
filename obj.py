import numpy as np
import re
import sys

# Ler arquivo .obj e definir uma malha de triângulos
#
# O vertex texture associado a cada ponto de um polígono
# irá mapear a textura no polígono.
#
# O vt será guardado depois do triângulo. Ou seja, o triângulo será de uma das seguintes formas:
# (cor, ponto, ponto, ponto)
# (cor, ponto, ponto, ponto, vt, vt, vt)
#

def read_obj(path: str, cor, texture_on = False):
    triangulos = []
    vertices = []
    texturas = []
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
            if vt_pattern.match(line) and texture_on:
                # Ler os floats na linha
                nums = tuple(map(float, re.findall(float_pattern, line)))
                texturas.append(nums)
            if vn_pattern.match(line):
                # Não será usado no momento
                pass
            if f_pattern.match(line):
                # Nesse caso, espera-se linhas na forma f a/x b/y c/z, particularmente
                nums = tuple(map(int, re.findall(int_pattern, line)))
                # Reduzir 1 de index
                nums = tuple(map(lambda x: x-1, nums))
                
                if nums.__len__() == 6 and not texture_on:
                    triangulo_colorless = (vertices[nums[0]], vertices[nums[2]], vertices[nums[4]])
                elif nums.__len__() == 6 and texture_on:
                    triangulo_colorless = (vertices[nums[0]], vertices[nums[2]], vertices[nums[4]], 
                                                texturas[nums[1]], texturas[nums[3]], texturas[nums[5]])
                elif nums.__len__() == 9:
                    triangulo_colorless = (vertices[nums[0]], vertices[nums[3]], vertices[nums[6]])
                # Recuperar vertexes do triângulo
                triangulo = (cor,) + triangulo_colorless
                triangulos.append(triangulo)
    return triangulos
                
                
                
                
            

#read_obj("square.obj", (0,0,0))