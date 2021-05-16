# Create your models here.
from django.db import models
from graphviz import Digraph
import os
from django.conf import settings
import re


class Automato(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    alfabeto = models.CharField(max_length=100)
    estados = models.CharField(max_length=100)
    estadoInicial = models.CharField(max_length=100)
    estadosDeAceitacao = models.CharField(max_length=100)
    dicionarioTransicao = models.CharField(max_length=1000)
    diagrama = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

    def printAlfabeto(self):
        return str(set(self.alfabeto.split()))

    def printEstados(self):
        return str(set(self.estados.split()))

    def printEstadosDeAceitacao(self):
        return str(set(self.estadosDeAceitacao.split()))

    def dTransInTable(self):
        dTrans = {(t.split('-')[0], t.split('-')[1]):t.split('-')[2] for t in self.dicionarioTransicao.split()}

        table = []

        linha = ['']
        for simbolo in self.alfabeto.split():
            linha.append(simbolo)
        table.append(linha)

        for estado in self.estados.split():
            linha =[estado]
            for simbolo in self.alfabeto.split():
                linha.append(dTrans[(estado, simbolo)])
            table.append(linha)

        return table

    def valida_sequencia(self, sequencia):

        estado = self.estadoInicial

        dTrans = {(t.split('-')[0], t.split('-')[1]):t.split('-')[2] for t in self.dicionarioTransicao.split()}

        for simbolo in sequencia:
            if simbolo in self.alfabeto:
                estado = dTrans[(estado, simbolo)]
            else:
                return False

        if estado in self.estadosDeAceitacao:
            return True
        else:
            return False


    def desenha_diagrama(self):

        d = Digraph(name=self.descricao)

        # configurações gerais
        d.graph_attr['rankdir'] = 'LR'
        d.edge_attr.update(arrowhead='vee', arrowsize='1')
        # d.edge_attr['color'] = 'blue'
        d.node_attr['shape'] = 'circle'
        # d.node_attr['color'] = 'blue'

        # Estado inicial
        d.node('Start', label='', shape='none')

        # Estados de transição
        estadosDeTransicao = set(self.estados.split()) - set(self.estadosDeAceitacao.split())
        for estado in estadosDeTransicao:
            d.node(estado)

        # Estado aceitação
        for estado in self.estadosDeAceitacao.split():
            d.node(estado, shape='doublecircle')

        # Transicoes
        d.edge('Start', self.estadoInicial)

        for transicao_comma in self.dicionarioTransicao.split():
            transicao = transicao_comma.split('-')
            d.edge(transicao[0], transicao[2], label=transicao[1])

        d.format = 'svg'
        self.diagrama = f"computacao/images/afd/{str(self.nome).replace(' ', '_')}.svg"
        d.render(f"computacao/static/computacao/images/afd/{str(self.nome).replace(' ', '_')}")

class Maquina(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    alfabeto = models.CharField(max_length=100)
    estados = models.CharField(max_length=100)
    estadoInicial = models.CharField(max_length=100)
    estadosDeAceitacao = models.CharField(max_length=100)
    dicionarioTransicao = models.CharField(max_length=1000)
    diagrama = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

    def printAlfabeto(self):
        return str(set(self.alfabeto.split()))

    def printEstados(self):
        return str(set(self.estados.split()))

    def printEstadosDeAceitacao(self):
        return str(set(self.estadosDeAceitacao.split()))

    def dTransInTable(self):
        dTrans = {(t.split('-')[0], t.split('-')[1]):t.split('-')[2] for t in self.dicionarioTransicao.split()}

        table = []

        linha = ['']
        for simbolo in self.alfabeto.split():
            linha.append(simbolo)
        table.append(linha)

        linha = ["", "0", "1"]

        aux = linha[1:]
        for estado in self.estados.split():
            linha =[estado]
            for simbolo in aux:
                find = False
                for dicEstado, dicSimbolo in dTrans:
                    if dicSimbolo[0] == simbolo and dicEstado == estado:
                        linha.append("(" + dicSimbolo[1] + "," + dicSimbolo[2] + "," + dTrans[(estado, dicSimbolo)] + ")")
                        find = True
                        break
                if find == False:
                    linha.append("-")        
            table.append(linha)

        return table

    def valida_sequencia(self, sequencia):
        fita = ["*"]*200
        indice = 50
        nTicks = 0
        for i in sequencia:
            fita[indice] = i
            indice += 1
        indice = 50

        estado = self.estadoInicial

        dTrans = {(t.split('-')[0], t.split('-')[1][0]):{"proxSimbolo":t.split('-')[1][1],"direcao":t.split('-')[1][2],"proxEstado":t.split('-')[2]} for t in self.dicionarioTransicao.split()}

        while(estado != self.estadosDeAceitacao and nTicks < 15000):
            if((estado,fita[indice]) not in dTrans): return False
            novoEstado = dTrans[estado,fita[indice]]["proxEstado"]
            frente = False
            if dTrans[estado,fita[indice]]["direcao"] == "R":
                frente = True
            novoSimbolo = dTrans[estado,fita[indice]]["proxSimbolo"]
            fita[indice] = novoSimbolo
            estado = novoEstado
            if frente:
                indice += 1
            else: 
                indice -= 1
            nTicks += 1
        return estado == self.estadosDeAceitacao




    def desenha_diagrama(self):

        d = Digraph(name=self.descricao)

        # configurações gerais
        d.graph_attr['rankdir'] = 'LR'
        d.edge_attr.update(arrowhead='vee', arrowsize='1')
        # d.edge_attr['color'] = 'blue'
        d.node_attr['shape'] = 'circle'
        # d.node_attr['color'] = 'blue'

        # Estado inicial
        d.node('Start', label='', shape='none')

        # Estados de transição
        estadosDeTransicao = set(self.estados.split()) - set(self.estadosDeAceitacao.split())
        for estado in estadosDeTransicao:
            d.node(estado)

        # Estado aceitação
        for estado in self.estadosDeAceitacao.split():
            d.node(estado, shape='doublecircle')

        # Transicoes
        d.edge('Start', self.estadoInicial)

        for transicao_comma in self.dicionarioTransicao.split():
            transicao = transicao_comma.split('-')
            d.edge(transicao[0], transicao[2], label=transicao[1])

        d.format = 'svg'
        self.diagrama = f"computacao/images/maquinas/{str(self.nome).replace(' ', '_')}.svg"
        d.render(f"computacao/static/computacao/images/maquinas/{str(self.nome).replace(' ', '_')}")

class Expressao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    regex = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao
    
    def printRegex(self):
        return self.regex
    
    def validaSequencia(self, sequencia):
        regex = re.compile(self.regex)
        if re.match(regex, sequencia):
            return True
        else:
            return False


