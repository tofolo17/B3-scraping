"""Rascunho: formato da lista de diretores extraída da página da CVM.

A página devolve uma lista plana [nome, CPF, cargo, nome, ...]. Os
dados abaixo são fictícios, apenas para ilustrar o formato.
"""
diretores = [
    'Fulano de Tal', '000.000.000-00', '19 - Outros Diretores',
    'Ciclana da Silva', '000.000.000-00',
    '12 - Diretor de Relações com Investidores',
    'Beltrano Souza', '000.000.000-00',
    '20 - Presidente do Conselho de Administração',
]

for i in range(len(diretores)):
    print(diretores[i])
