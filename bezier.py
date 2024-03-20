import objeto as obj
import numpy as np
from typing import List
from functools import cache
from scipy.special import comb

class BezierCurve:
    n: int
    m: int
    pontos_de_controle: List[List[np.ndarray]]
    
    @cache
    def b(self, u, i, n):
        return comb(n, i)*pow(u,i)*pow(1-u, n-i)
    
    def B(self, u, v):
        res = 0
        for i in range(0, self.m + 1):
            for j in range(0, self.n + 1):
                res += self.pontos_de_controle[i][j] * (self.b(u,i,self.m) * self.b(v,j,self.n))
        return res
    
    
    def __init__(self, m, n, *listas_de_pontos) -> None:
        self.pontos_de_controle = []
        self.n = n
        self.m = m
        for lista in listas_de_pontos:
            assert lista.__len__() == n+1
            lista_ndarray = []
            for i in lista:
                lista_ndarray.append(np.array(i))
            self.pontos_de_controle.append(lista_ndarray)  
        assert self.pontos_de_controle.__len__() == m+1
        # print(self.pontos_de_controle)
        
    
    def criar_malha(self, resolucao = 5, _material = None, text = None) -> obj.Objeto:
        """Cria uma malha de triângulos com base na especificação da curva
        A malha irá consistir de uma bounding box exterior e um conjunto de triângulos
        
        Por padrão, os triângulos serão coloridos com cores alternadas: magenta e ciano
        
        FUTURO: especificar textura
        

        Args:
            resolucao (int, optional): a malha será representada por Res x Res triangulos. Padrão = 5.
            altura (int, optional): quantas camadas de bounding box terá . Padrão e mínimo = 2

        Returns:
            triangulo.Objeto: malha de triângulos, sob as bounding boxes calculadas
        """
        # Gerar pontos de 'sample' da curva, com base na resolução
        pontos_render: List[List[np.ndarray]] = []
        vt_render: List[List[np.ndarray]] = []
        
        for u in np.linspace(0,1,resolucao):
            pontos_render_linha: List[np.ndarray] = []
            vt_render_linha: List[np.ndarray] = []
            for v in np.linspace(0,1,resolucao):
                val = self.B(u, v)
                # print(f"{u},{v}: {val}")
                pontos_render_linha.append(val)
                vt_render_linha.append(np.array((u,v)))
                
            pontos_render.append(pontos_render_linha)
            vt_render.append(vt_render_linha)
        
        # Gerar triângulos
        objeto = obj.Objeto()
        
        # Magenta
        for i in range(0, resolucao-1):
            for j in range(0, resolucao-1):
                if text is None:
                    objeto.adcionar_triangulo((255, 0, 255), pontos_render[i][j], pontos_render[i+1][j], pontos_render[i][j+1], _material = _material)
                else:
                    objeto.adcionar_triangulo((255, 0, 255), pontos_render[i][j], pontos_render[i+1][j], pontos_render[i][j+1],
                                              vt_render[i][j], vt_render[i+1][j], vt_render[i][j+1], text, _material)
        # Ciano
        for i in range(0,resolucao-1):
            for j in range(1,resolucao):
                if text is None:
                    objeto.adcionar_triangulo((0, 255, 255), pontos_render[i][j], pontos_render[i+1][j-1], pontos_render[i+1][j], _material = _material)
                else:
                    objeto.adcionar_triangulo((0, 255, 255), pontos_render[i][j], pontos_render[i+1][j-1], pontos_render[i+1][j],
                                            vt_render[i][j], vt_render[i+1][j-1], vt_render[i+1][j], text, _material)
                
        # TODO: consertar textura
        return objeto
                