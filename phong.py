'''FUNÇÕES REFERENTES AO MODELO DE ILUMINAÇÃO'''
import numpy as np
import objeto
from objeto import Luz, Material
import cena
from math import pow
INF = 9999999999
#Coeficiente_difuso = np.array((0.5,0.5,0.5))

def test_bounding_box(ponto_reta, vetor_reta, x_max, x_min, y_max, y_min, z_max, z_min):
    c = ponto_reta
    r = vetor_reta
    
    if r[0] == 0:
        if c[0] > x_max or c[0] < x_min:
            return False
        t1_max = INF
        t1_min = 0
    else: 
        t1_max = (x_max - c[0])/r[0]
        t1_min = (x_min  - c[0])/r[0]
        if t1_min > t1_max:
            (t1_max, t1_min) = (t1_min, t1_max)
        if t1_max < 1:
            return False
    
    if r[1] == 0:
        if c[1] > y_max or c[1] < y_min:
            return False
        t2_max = INF
        t2_min = 0
    else: 
        t2_max = (y_max - c[1])/r[1]
        t2_min = (y_min  - c[1])/r[1]
        if t2_min > t2_max:
            (t2_max, t2_min) = (t2_min, t2_max)
        if t2_max < 1:
            return False
    
    if r[2] == 0:
        if c[2] > z_max or c[2] < z_min:
            return False
        t3_max = INF
        t3_min = 0
    else: 
        t3_max = (z_max - c[2])/r[2]
        t3_min = (z_min  - c[2])/r[2]
        if t3_min > t3_max:
            (t3_max, t3_min) = (t3_min, t3_max)
        if t3_max < 1:
            return False
        
    t_min = max(t1_min, t2_min, t3_min)
    t_max = min(t1_max, t2_max, t3_max)
    
    return t_max >= t_min and t_max >= 1
        

def normalize(v):
    ''''' NORMALIZAÇÃO DE VETOR (NÃO TEM NO NUMPY) '''''
    v = v/np.linalg.norm(v)
    return v

def intersect_triangle(ray, camera, triangulo_: objeto.Triangulo):
    '''''FUNÇÃO DADA NO LIVRO PRA CALCULAR A INTERSECÇÃO COM O TRIANGULO'''''
    v0 = triangulo_[2]
    v1 = triangulo_[3]
    v2 = triangulo_[4]
    cor = triangulo_[1]
    vt0 = triangulo_[6]
    vt1 = triangulo_[7]
    vt2 = triangulo_[8]
    text = triangulo_[9]
    
    # Faz o teste de bounding box, para economizar processamento
    x_max = triangulo_.x_max
    x_min = triangulo_.x_min
    y_max = triangulo_.y_max
    y_min = triangulo_.y_min
    z_max = triangulo_.z_max
    z_min = triangulo_.z_min
    if not test_bounding_box(camera, ray, x_max, x_min, y_max, y_min, z_max, z_min):
        return (INF, None)
    
    a = v0[0] - v1[0]
    b = v0[0] - v2[0]
    c = ray[0]
    d = v0[0] - camera[0]

    e = v0[1] - v1[1]
    f = v0[1] - v2[1]
    g = ray[1]
    h = v0[1] - camera[1]

    i = v0[2] - v1[2]
    j = v0[2] - v2[2]
    k = ray[2]
    l = v0[2] - camera[2]

    m = f*k - g*j
    n = h*k - g*l
    p = f*l - h*j

    q = g*i - e*k
    s = e*j - f*i
######################################
    #evita divisão por 0
    div0 = a*m + b*q + c*s
    if div0 == 0:
        inv_denom = 0
    else:
        inv_denom = 1/div0
    
    e1 = d*m - b*n - c*p
    beta = e1*inv_denom
    if beta < 0:
        return (INF, None)
    
    r = e*l - h*i
    e2 = a*n + d*q + c*r
    gamma = e2 * inv_denom
    if gamma < 0:
        return (INF, None) 
    if beta + gamma > 1:
        return (INF, None)
    
    e3 = a*p - b*r + d*s
    t = e3 * inv_denom
    if t< 0.01:
        return (INF, None)
    
    # Determina a cor
    alpha = 1 - beta - gamma
    # P = alpha*v0 + beta*v1 + gama*v2
    if type(vt0) is not np.ndarray and vt0 == None:
        cor_res = cor
    else:
        # Encontrar o pixel correspondente na textura
        Ptextura = alpha*vt0 + beta*vt1 + gamma*vt2
        cor_res = text.map(Ptextura[0], Ptextura[1])
    
######################################
    
    return (t, cor_res)

def intersect_esfera(ray, camera, esfera_: objeto.Esfera):
    '''''INTERSECÇÃO COM A ESFERA'''''
    
    # Faz o teste de bounding box, para economizar processamento
    x_max = esfera_.x_max
    x_min = esfera_.x_min
    y_max = esfera_.y_max
    y_min = esfera_.y_min
    z_max = esfera_.z_max
    z_min = esfera_.z_min
    if not test_bounding_box(camera, ray, x_max, x_min, y_max, y_min, z_max, z_min):
        return None
    
    
    cor = esfera_.cor
    oc = camera - esfera_.centro
    a = np.dot(ray, ray)
    b = 2 * np.dot(oc, ray)
    c = np.dot(oc, oc) - (esfera_.raio ** 2)
    delta = b ** 2 - (4 * a * c)

    if delta < 0:
        return None
    # ENCONTRA OS PONTOS DE INTERSECÇÃO COM BHASKARA
    tmp1 = (-b + np.sqrt(delta))/(2*a)
    tmp2 = (-b - np.sqrt(delta))/(2*a)
    # tratamento de exceções
    if tmp1 < 0 and tmp2 < 0:
        return None
    if tmp1 < 0.01:
        tmp1 = INF
    if tmp2 < 0.01:
        tmp2 = INF
    
    # TODO: textura
        
    # current recebe a menor distancia
    if tmp1 < tmp2:
        return (tmp1, cor)
    else:
        return (tmp2, cor)

def collor(camera, vetor_atual, objetos, return_obj = False):
    ''''' FUNÇÃO PARA CALCULAR A COR DE CADA OBJETO COM BASE NA MENOR DISTANCIA DA CAMERA '''''
    t = INF
    cor = np.array([0,0,0])
    collor_obj = None
    for i in objetos:
        current = INF
        current_obj = i
        cor_t = i[1]
        if i[0].lower() == "esfera":
            '''''INTERSECÇÃO COM A ESFERA'''''
            res = intersect_esfera(vetor_atual, camera, i)
            if res == None:
                continue
            (current, cor_t) = res
        elif i[0].lower() == "plano":
            '''''INTERSECÇÃO COM O PLANO'''''
            #verifica se o plano não é paralelo com os raios da camera
            tmp = np.dot(i[3],vetor_atual)
            if tmp == 0:
                continue
            #calcula a intersecção dos pontos
            current = (np.dot(i[3], i[2]) - np.dot(i[3], camera)) / tmp
            if current < 0.01:
                current = INF
        elif i[0].lower() == "triangulo":
            '''''INTERSECÇÃO COM O TRIANGULO'''
            #verifica se o raio não é paralelo com o triangulo
            tmp = np.dot(i[5],vetor_atual)
            if tmp == 0:
                continue
            (current, cor_t) = intersect_triangle(vetor_atual, camera, i)
        elif i[0] == "objeto":
            '''Intersecção com objeto'''
            # Verifica bouding box
            x_max = i.x_max
            x_min = i.x_min
            y_max = i.y_max
            y_min = i.y_min
            z_max = i.z_max
            z_min = i.z_min
            if not test_bounding_box(camera, vetor_atual, x_max, x_min, y_max, y_min, z_max, z_min):
                continue
            
            # Verifica intersecção com os subobjetos
            (current, cor_t, current_obj) = collor(camera, vetor_atual, i.subobjetos, return_obj)
        # pega o menor tempo e joga em T
        if current < t:
            t = current
            cor = cor_t
            collor_obj = current_obj
    if return_obj:
        return(t, cor, collor_obj)
    return (t, cor, None)

def raycast(camera, vetor_atual, objetos):
    return collor(camera, vetor_atual, objetos)[1]

def phong(camera, vetor_atual, objetos, luzes, recursao_limite = 3, refracao_atual = 1.0, dentro_obj = False):
    '''FUNÇÃO PARA IMPLEMENTAR O MODELO DE ILUMINAÇÃO DE PHONG'''
    # Detecta o objeto de colisão:
    res = collor(camera, vetor_atual, objetos, True)
    t: float = res[0]
    cor: np.ndarray = res[1]
    obj = res[2]
    if obj == None:
        return np.array([0,0,0]) # cor de fundo
    
    mat: Material = obj.material
    if mat == None:
        return cor
    # # Informações necessárias:
    #     # Ponto de contato do raio com o objeto
    #     # normal no ponto da superfície do objeto onde a interseção ocorreu
    #     # Vetores apontando do ponto de contato para as luzes +
    #         # Vetor de reflexão em relação a luz 
    #         # Vetor que aponta para o espectador. Podem haver diferentes espectadores que a câmera no caso de reflexões e refrações
    iluminacao = np.array((0.0,0.0,0.0))
    
    # Cálculo da parcela de ilumiação ambiente
    iluminacao_ambiente = np.multiply(mat.k_ambiental,  cena.COR_AMBIENTE)
    iluminacao += iluminacao_ambiente # + iluminacao difusa e especular
    
    # Encontra o ponto de colisão do raio
    ponto_objeto = camera + vetor_atual*t
    
    # Encontra vetor espectador
    Vetor_espectador = normalize(camera - ponto_objeto)
    
    # Cálculo da parcela de iluminação difusa e especular
    for luz in luzes:
        luz: Luz = luz
        
        # Vetor que parte do ponto da superfície do objeto onde a interseção ocorreu e aponta para a luz
        Li = normalize(luz.ponto - ponto_objeto)
        
        # Normal no ponto da superfície do objeto onde a interseção ocorreu
        normal = np.array((0.0,0.0,0.0))
        match obj[0]:
            case "triangulo":
                normal = obj.normal
            case "plano":
                normal = obj.normal
            case "esfera":
                normal = normalize(ponto_objeto - obj.centro)
        
        
        # Componente difusa
        dot = np.dot(normal, Li)
        if dot > 0:
            dif = luz.intensidade * mat.k_difuso * mat.o_difuso * dot
            iluminacao += dif
        
        # Componente especular

        # Encontrar vetor de reflexão da luz
        Ri = 2*normal*(np.dot(normal, Li)) - Li
        
        dot = np.dot(Ri, Vetor_espectador)
        if dot > 0:
            # Esse último np.array serve para colocar a iluminação proporcional a 255
            esp = luz.intensidade * mat.k_especular * pow(dot, mat.k_rugosidade) * np.array((255.0,255.0,255.0))
            iluminacao += esp
        
    # Componente reflexão
    if recursao_limite > 0 and mat.reflete:
        # Vetor reflexão do espectador
        R = 2*normal*(np.dot(normal,Vetor_espectador)) - Vetor_espectador
        
        Ir = phong(ponto_objeto, R, objetos, luzes, recursao_limite-1, refracao_atual, dentro_obj)
        ref = Ir*mat.k_reflexão
        iluminacao += ref
        
    # Component refração
    if recursao_limite > 0 and mat.refrata:
        if not dentro_obj:
            n_out = refracao_atual
            n_in = mat.ior
            refracao_atual = n_in
            dentro_obj = True
            normal_op = -normal
        elif refracao_atual == mat.ior:
            n_out = mat.ior
            n_in = 1.0 #ar
            refracao_atual = 1.0
            dentro_obj = False
            normal_op = normal
        else:
            raise Exception("Não implementado")
        
        n_rev = n_out/n_in
        sin_teta = np.linalg.norm(np.cross(Vetor_espectador,-normal_op))
        cos_teta = 1 - sin_teta * sin_teta
        sin_teta_t = sin_teta * n_rev
        cos_teta_t = 1 - sin_teta_t * sin_teta_t
        
        # Equação modificada para por T na direção certa
        # normal_op é o oposto da normal no lado do raio
        T = - n_rev*Vetor_espectador - (cos_teta_t - n_rev*cos_teta)*normal_op
        It = phong(ponto_objeto, T, objetos, luzes, recursao_limite-1, refracao_atual, dentro_obj)
        transm = It*mat.k_transmissão
        iluminacao += transm
        
            

            
    # Correção de overflow
    for i in range(0,3):
        if iluminacao[i] > 255:
            iluminacao[i] = 255
    return iluminacao

def phong_no_recursion(camera, vetor_atual, objetos, luzes):
    return phong(camera, vetor_atual, objetos, luzes, recursao_limite=0)