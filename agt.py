import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from sympy import *

class graph:
    def __init__(self, A, if_diGraph = False, special_layout = False):
        self.adjacency_matrix = np.array(A)
        self.diGraph = if_diGraph
        self.layout = special_layout
        
    def show_A(self, t: int) -> np.array:
        '''
        Метод вычисляет и выводит t-ую степень
        матрицы смежности.
        
        '''
        
        A = np.array(self.adjacency_matrix)
        return np.linalg.matrix_power(A, t)
    
    def write_paths(self, t: int):
        '''
        Заменяем значения матрицы на переменные и 
        символьно вычисляем t-ую степень.
        Выводим все полученные пути.
        
        '''
        #self.all_paths = [] 
            
        #Переводим матрицу смежности в нужный формат для sympy
        A = self.__convert_to_2d_list()
        
        #Заменяем единицы на переменные x_ij
        #Важно сделать переменные некоммутативными для сохранения порядка
        for i in range(len(A)):
            for j in range(len(A)):
                if A[i][j] == 1: A[i][j] = symbols("x" + str(i+1) + "x" + str(j+1), commutative=False)

        #Символьно вычисляем t-ую степень
        A = Matrix(A) ** t
        
        #Раскрываем скобки в выражениях
        for i in range(len(np.array(A))):
            for j in range(len(np.array(A))):
                A[i,j] = expand(A[i,j])
            
        B = np.array(A)
        
        for i in range(len(B)):
            for j in range(len(B)):
                if B[i,j] != 0: 
                    
                    #каждый элемент матрицы разбиваем по плюсу
                    #получаем все пути из i в j
                    paths = str(B[i,j]).split('+')
                    
                    print(f'Пути из {i+1} в {j+1}:')

                    #Выводим каждый путь в более читаемом формате
                    for path in paths:
                        path = path.strip().replace('*', '').replace('x', "->x").split('x')
                        path = path[1:]
                        
                        if_first = True
                        path_str = ""
                        save_path = []
                        
                        while(len(path)>1):
                            if if_first: 
                                path_str += path[0] + path[1]
                                if_first = False
                            else:
                                path_str += path[1]

                            path = path[2:]
                        #self.all_paths.append(path_str.split('->'))
                        print(path_str)
                    print('-'*20)
            
    def show_paths_on_graph(self, v1 :int, v2 :int, t: int):
        '''
        Отрисовываем все пути из i в j длины t
        '''
        v1 = v1 - 1
        v2 = v2 - 1
        #Переводим матрицу смежности в нужный формат для sympy
        A = self.__convert_to_2d_list()
        
        #Заменяем единицы на переменные x_ij
        #Важно сделать переменные некоммутативными для сохранения порядка
        for i in range(len(A)):
            for j in range(len(A)):
                if A[i][j] == 1: A[i][j] = symbols("x" + str(i+1) + "x" + str(j+1), commutative=False)
             
        #Символьно вычисляем t-ую степень
        A = Matrix(A) ** t
        
        #Раскрываем скобки в выражениях
        for i in range(len(np.array(A))):
            for j in range(len(np.array(A))):
                A[i,j] = expand(A[i,j])
        
        B = np.array(A)
        
        if B[v1,v2] != 0: 
            paths = str(B[v1,v2]).split('+')
            #Выводим каждый путь в более читаемом формате
            edges = []
            for path in paths:
                path = path.strip().replace('*', '').split('x')
                edges.append(path[1:])
                
            
        #отрисовываем графы
        print(f'Все пути из {v1+1} в {v2+1} длины {t}:')
        print('-'*40)
        if edges:
            for elem in edges:
                
                edges2_colors = []
                edges2 = []
                
                for i in range(len(self.adjacency_matrix)):
                    for j in range(len(self.adjacency_matrix)):
                        if self.adjacency_matrix[i][j] > 0: 
                                edges2.append([i+1,j+1])
                                if not self.diGraph: edges2.append([j+1,i+1])
                                edges2_colors.append('k')
                                if not self.diGraph: edges2_colors.append('k')


                for i in range(len(elem)-1):
                    if int(elem[i]) != int(elem[i+1]):
                        idx1 = edges2.index([int(elem[i]), int(elem[i+1])])
                        if not self.diGraph: idx2 = edges2.index([int(elem[i+1]), int(elem[i])])
                        edges2_colors[idx1] = 'r'
                        if not self.diGraph: edges2_colors[idx2] = 'r'

                if self.diGraph:
                    G = nx.DiGraph()
                    for elem in edges2:
                        idx = edges2.index(elem)
                        G.add_edge(elem[0], elem[1], color = edges2_colors[idx])
                
                    colors = nx.get_edge_attributes(G,'color').values()

                    pos = nx.circular_layout(G)
                    if self.layout: pos = nx.shell_layout(G, nlist = [range(6,11), range(1,6)]);
                    nx.draw(G, pos = pos, edge_color=colors, with_labels=True, connectionstyle='arc3, rad = 0.1')
                    plt.show()
                else:
                    G = nx.Graph()
                    for elem in edges2:
                        idx = edges2.index(elem)
                        G.add_edge(elem[0], elem[1], color = edges2_colors[idx])
                
                    colors = nx.get_edge_attributes(G,'color').values()

                    pos = nx.circular_layout(G)
                    if self.layout: pos = nx.shell_layout(G, nlist = [range(6,11), range(1,6)]);
                    nx.draw(G, pos = pos, edge_color=colors, with_labels=True)
                    plt.show()
    
    
    def show_graph(self):
        '''
        По матрице смежности вычисляем ребра
        и выводим граф с помощью networkx
        
        '''
        
        edges = []
        
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] > 0: 
                    for k in range(self.adjacency_matrix[i][j]):
                        edges.append([i+1,j+1])
                    
        if self.diGraph: 
            G = nx.DiGraph()
            G.add_edges_from(edges) 
            pos = nx.circular_layout(G)
            if self.layout: pos = nx.shell_layout(G, nlist = [range(6,11), range(1,6)]);
            nx.draw(G, pos = pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
            plt.show()
        else: 
            G = nx.Graph()
            G.add_edges_from(edges) 
            pos = nx.circular_layout(G)
            if self.layout: pos = nx.shell_layout(G, nlist = [range(6,11), range(1,6)]);
            nx.draw(G, pos = pos, with_labels=True)
            plt.show()
        
    def __convert_to_2d_list(self):
        '''
        Функция переводит матрицу смежности в нужный формат
        для библиотеки sympy.
        '''
        
        A = []
        for elem in self.adjacency_matrix:
            A.append(list(elem));
        return A;

if __name__ == '__main__':      
    A = graph([[0,1,1],[1,0,1],[1,1,0]])
    A.show_graph()
    A.show_paths(2)
    A.show_paths_on_graph(1,2,2)