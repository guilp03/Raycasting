import triangulo
import numpy as np
from typing import List
from functools import cache
from scipy.special import comb

class BezierCurve:
    n: int
    m: int
    pontos_de_controle: List[List[np.ndarray]]
    
    @cache
    def binomial(n, i):
        return comb(n, i)
    
    @cache
    def pow(u, i):
        return u**i
            
    @cache
    def b(self, u, i, n):
        return comb(n, i)*pow(u,i)*pow(1-u, n-i)
    
    def B(self, u, v):
        res = 0
        for i in range(0, self.n + 1):
            for j in range(0, self.m + 1):
                res += self.pontos_de_controle[i][j] * (self.b(u,i,self.n) * self.b(v,j,self.m))
        return res
    
    
    def __init__(self, n, m, *listas_de_pontos) -> None:
        self.pontos_de_controle = []
        self.n = n
        self.m = m
        for lista in listas_de_pontos:
            assert lista.__len__() == m+1
            lista_ndarray = []
            for i in lista:
                lista_ndarray.append(np.array(i))
            self.pontos_de_controle.append(lista_ndarray)  
        assert self.pontos_de_controle.__len__() == n+1
        # print(self.pontos_de_controle)
        
    
    def criar_malha(self, resolucao = 5, altura = 2) -> triangulo.Objeto:
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
        
        for u in np.linspace(0,1,resolucao):
            pontos_render_linha: List[np.ndarray] = []
            for v in np.linspace(0,1,resolucao):
                val = self.B(u, v)
                # print(f"{u},{v}: {val}")
                pontos_render_linha.append(val)
            pontos_render.append(pontos_render_linha)
        
        # Gerar triângulos
        objeto = triangulo.Objeto()
        
        # Magenta
        for i in range(0, resolucao-1):
            for j in range(0, resolucao-1):
                objeto.adcionar_triangulo((255, 0, 255), pontos_render[i][j], pontos_render[i+1][j], pontos_render[i][j+1])
        
        # Ciano
        for i in range(0,resolucao-1):
            for j in range(1,resolucao):
                objeto.adcionar_triangulo((0, 255, 255), pontos_render[i][j],pontos_render[i+1][j],pontos_render[i+1][j-1])
        
        # TODO: diferentes alturas. Ou seja, mais camadas de bounding box e subobjetos
        # TODO: textura 
        return objeto
                