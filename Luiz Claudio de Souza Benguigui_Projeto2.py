#!/usr/bin/env python
# coding: utf-8

# In[1]:


class ConteudoInvalido(Exception):
    def __init__(self, item, mensagem='O Conteúdo digitado é INVÁLIDO!'):
        self.item = item
        self.message = mensagem
        super().__init__(self.message)


# In[2]:


class Cliente():
    __total_clientes = 0
    __lista_cliente = {}

    # Construtor
    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nome = nome
        Cliente.__total_clientes += 1
        Cliente.__lista_cliente[cpf] = nome
                         
    # Métodos privados - getter e setter para cpf
    def __get_cpf(self):
        return self.__cpf
    def __set_cpf(self, valor_cpf):
        cpf_validado, novo_cpf = Cliente.ValidarCpf(valor_cpf)
        if cpf_validado == False:
            raise ConteudoInvalido(valor_cpf, f'CPF {valor_cpf} Inválido')
        elif novo_cpf in Cliente.__lista_cliente:
            raise ConteudoInvalido(valor_cpf, f'CPF {valor_cpf} Já Cadastrado')                    
        else:
            self.__cpf = novo_cpf            
    cpf = property(__get_cpf, __set_cpf)

    # Métodos privados - getter e setter para nome
    def __get_nome(self):
        return self.__nome
    def __set_nome(self, valor_nome):        
        if len(valor_nome) < 5:
            raise ConteudoInvalido(valor_nome, 'Nome deve ter mais de 5 caracteres')
        if valor_nome.isdigit():
            raise ConteudoInvalido(valor_nome, 'Nome Não pode ser numérico')
        else:
            self.__nome = valor_nome
    nome = property(__get_nome, __set_nome)

    @staticmethod
    def TotalClientes():
        print(f'Total de {Cliente.__total_clientes} Clientes Cadastrados')

    @staticmethod
    def ListarClientes():
        print('CPF\t\t Nome')
        for cpf, nome in Cliente.__lista_cliente.items():
            print(f'{cpf}\t {nome}')
        
    #Método para imprimir as informações de 1 Cliente
    def __repr__(self):
        return (f'Nome: {self.nome}, CPF: {self.cpf}')

    def LimparCPF(cpf):

        if type(cpf) != str:
            novo_cpf = str(cpf)
        else:
            novo_cpf = cpf.replace(".","")
            novo_cpf = novo_cpf.replace("-","")

        if len(novo_cpf) <= 11:
            novo_cpf = novo_cpf.rjust(11,'0')

        return novo_cpf

    def ValidarCpf(cpf):

        novo_cpf = Cliente.LimparCPF(cpf)

        if len(novo_cpf) > 11:
            return False, str(cpf)

        if novo_cpf.isdigit() != True:
            return False, str(cpf)

        #Validando os dígitos verificadores
        if int(novo_cpf[9]) == Cliente.ValidarDV1Cpf(novo_cpf) and int(novo_cpf[10]) == Cliente.ValidarDV2Cpf(novo_cpf):
            return True, str(novo_cpf)
        else:
            return False, str(cpf)

    def ValidarDV1Cpf(cpf):        
            somadv1 = 0
            for i in range(9):
                somadv1 += int(cpf[i]) * (10 - i)

            restodv1 = somadv1 % 11
            return restodv1 if restodv1 == 0 else (11 - restodv1)

    def ValidarDV2Cpf(cpf):
        somadv2 = 0
        for i in range(10):
            somadv2 += int(cpf[i]) * (11 - i)

        restodv2 = somadv2 % 11
        return restodv2 if restodv2 == 0 else (11 - restodv2)


# In[3]:


import datetime as datetime
class Loja():
    __estoque_bikes = 0
    __locacoes = {}
    __estoques = {}
    __ultimo_pedido = 0
    # Construtor
    def __init__(self, nome_loja, estoque, preco_hora, preco_dia, preco_mes, desconto_familia):
        self.nome_loja = nome_loja
        self.estoque = estoque
        self.preco_hora = preco_hora
        self.preco_dia = preco_dia
        self.preco_mes = preco_mes
        self.desconto_familia = desconto_familia
        Loja.__estoques[nome_loja] = estoque
        Loja.EstoqueTotal()
        
    # Métodos privados - getter e setter para nome da loja
    def __get_nome_loja(self):
        return self.__nome_loja
    def __set_nome_loja(self, valor_nome_loja):        
        if valor_nome_loja in Loja.__estoques:
            raise ConteudoInvalido(valor_nome_loja, f'Loja {valor_nome_loja} Já Cadastrada')
        if len(valor_nome_loja) < 5:
            raise ConteudoInvalido(valor_nome_loja, 'Nome deve ter mais de 5 caracteres')
        if valor_nome_loja.isdigit():
            raise ConteudoInvalido(valor_nome_loja, 'Nome Não pode ser numérico')
        self.__nome_loja = valor_nome_loja
    nome_loja = property(__get_nome_loja, __set_nome_loja)

    # Métodos privados - getter e setter para estoque_inicial
    def __get_estoque(self):
        return self.__estoque
    def __set_estoque(self, valor_estoque):        
        try:
            valor = int(valor_estoque)
        except:
            raise ConteudoInvalido(valor_estoque, 'Estoque Inicial deve ser Numérico')
            
        if valor < 0:
            raise ConteudoInvalido(valor_estoque, 'Estoque Não pode ser menor do que zero')
        else:
            try:
                self.__estoque = int(valor)
            except:
                raise ConteudoInvalido(valor_estoque, 'Estoque Inicial deve ser Numérico')

    estoque = property(__get_estoque, __set_estoque)

    # Métodos privados - getter e setter para tabela de preços
    def __get_preco_hora(self):
        return self.__preco_hora
    def __set_preco_hora(self, valor_preco_hora):        
        try:
            valor_preco = float(valor_preco_hora)
        except:
            raise ConteudoInvalido(valor_preco_hora, 'Preços por Hora precisam ser do tipo float')
            
        if valor_preco < 0:
            raise ConteudoInvalido(valor_preco_hora, 'Preço por Hora Não pode ser menor do que R$ 0,00')
        else:
            try:
                self.__preco_hora = float(valor_preco)
            except:
                raise ConteudoInvalido(valor_preco_hora, 'Preços por Hora precisam ser do tipo float')
    preco_hora = property(__get_preco_hora, __set_preco_hora)

    def __get_preco_dia(self):
        return self.__preco_dia
    def __set_preco_dia(self, valor_preco_dia):        
        try:
            valor_preco = float(valor_preco_dia)
        except:
            raise ConteudoInvalido(valor_preco_dia, 'Preços por Dia precisam ser do tipo float')

        if valor_preco < 0:
            raise ConteudoInvalido(valor_preco_dia, 'Preço por Dia Não pode ser menor do que R$ 0,00')
        else:
            try:
                self.__preco_dia = float(valor_preco)
            except:
                raise ConteudoInvalido(valor_preco_dia, 'Preços por Dia precisam ser do tipo float')
        
    preco_dia = property(__get_preco_dia, __set_preco_dia)

    def __get_preco_mes(self):
        return self.__preco_mes
    def __set_preco_mes(self, valor_preco_mes):
        try:
            valor_preco = float(valor_preco_mes)
        except:
            raise ConteudoInvalido(valor_preco_mes, 'Preços por Mês precisam ser do tipo float')
    
        if valor_preco < 0:
            raise ConteudoInvalido(valor_preco_mes, 'Preço por Mês Não pode ser menor do que R$ 0,00')
        else:
            try:
                self.__preco_mes = float(valor_preco)
            except:
                raise ConteudoInvalido(valor_preco_mes, 'Preços por Mês precisam ser do tipo float')
        
    preco_mes = property(__get_preco_mes, __set_preco_mes)

    # Métodos privados - getter e setter para desconto
    def __get_desconto_familia(self):
        return self.__desconto_familia
    def __set_desconto_familia(self, valor_desconto_familia):        
        try:
            valor_desconto = float(valor_desconto_familia)
        except:
            raise ConteudoInvalido(valor_desconto_familia, 'Desconto Família precisa ser do tipo float')

        if valor_desconto < 0:
            raise ConteudoInvalido(valor_desconto_familia, 'Desconto Família Não pode ser menor do que R$ 0,00')
        else:
            try:
                self.__desconto_familia = float(valor_desconto)
            except:
                raise ConteudoInvalido(valor_desconto_familia, 'Desconto Família precisa ser do tipo float')
        
    desconto_familia = property(__get_desconto_familia, __set_desconto_familia)

    @staticmethod
    def EstoqueTotal():
        Loja.__estoque_bikes = sum(Loja.__estoques.values())
        return Loja.__estoque_bikes

    @staticmethod
    def Locadas():
        bicicletas_alugadas = 0
        for locacoes in Loja.__locacoes.values():
            if locacoes[8] == 'A Devolver':
                bicicletas_alugadas += locacoes[1]
        return bicicletas_alugadas
    
    @staticmethod
    def ObterLocacao(numero_pedido):
        if numero_pedido in Loja.__locacoes.keys():
            return Loja.__locacoes[numero_pedido]
        else:
            return False

    @staticmethod
    def ListarLocacoes(numero_pedido = None, nome_cliente = None, nome_loja = None):

        print(f'#  Cliente\t\tQt\tModo\tStatus\t\tValor\tLoja')

        for pedido, valor in Loja.__locacoes.items():
            numero = pedido
            cliente = valor[0]
            loja = valor[15]
            if (numero_pedido == None or numero_pedido == numero) and (nome_cliente == None or nome_cliente == cliente) and (nome_loja == None or nome_loja == loja):
                qtd = valor[1]
                modalidade = valor[2]
                if modalidade == 'H': modalidade = 'Hora'
                if modalidade == 'D': modalidade = 'Dia '
                if modalidade == 'M': modalidade = 'Mês '

                inicio = (f'{valor[3]}/{valor[4]}/{valor[5]} {valor[6]}:{valor[7]}')
                status = valor[8] 
                pgto = valor[9] 
                fim = (f'{valor[10]}/{valor[11]}/{valor[12]} {valor[13]}:{valor[14]}')
                print(f'{numero}  {cliente:<20}\t{qtd}\t{modalidade}\t{status}\t{pgto}\t{loja}')
        print(f'Total de {Loja.Locadas()} bicicletas alugadas')
        print(f'Estoque disponível de {Loja.__estoque_bikes} bicicletas')
        

    @staticmethod
    def ListarLojas():
        print(f'Loja\t\t\t Estoque')
        for nome, estoque in Loja.__estoques.items():
            print(f'{nome:<25}{estoque:<0}')
        print(f'Estoque disponível de {Loja.__estoque_bikes} bicicletas')
        print(f'Total de {Loja.Locadas()} bicicletas alugadas')

    #Método para imprimir as informações
    def __repr__(self):
        return (f'Loja: {self.nome_loja} - Estoque: {self.estoque} bicicletas\nEstoque Todas as Lojas: {Loja.EstoqueTotal()}')
        
    def Locar(self, cliente, qtd_bikes, modalidade, dia, mes, ano, hora, minuto):

        modalidades = ['H', 'D', 'M']

        if qtd_bikes > self.estoque:
            raise ConteudoInvalido(qtd_bikes, f'O estoque de {self.estoque} da Loja {self.nome_loja} não é suficiente para atender ao seu pedido')
        elif modalidade.upper() not in modalidades:
            raise ConteudoInvalido(modalidade, f'A modalidade de locação deve ser "h" para hora, "d" para dia ou "s" para semana')
        else:
            try:
                Loja.__locacoes[Loja.__ultimo_pedido + 1] = [cliente.nome, 
                                                             qtd_bikes, 
                                                             modalidade.upper(), 
                                                             dia, 
                                                             mes, 
                                                             ano, 
                                                             hora, 
                                                             minuto, 
                                                             'A Devolver', 
                                                             0.0,
                                                             dia, 
                                                             mes, 
                                                             ano, 
                                                             hora, 
                                                             minuto,
                                                             self.nome_loja,
                                                             cliente.cpf] 
                Loja.__ultimo_pedido += 1
                self.estoque -= qtd_bikes
                Loja.__estoques[self.nome_loja] =  self.estoque
                Loja.EstoqueTotal()
                print(f'Locação Cadastrada com sucesso - Número {Loja.__ultimo_pedido}')

            except:
                raise ConteudoInvalido(cliente, f'Não foi possível registrar sua Locação')
            
    def CancelarPedido(self, pedido):

        if pedido in Loja.__locacoes:
            qtd = Loja.__locacoes[pedido][1]
            self.estoque += qtd
            Loja.__locacoes.pop(pedido)
            Loja.__estoques[self.nome_loja] = self.estoque
            Loja.EstoqueTotal()
            print(f'Locação número {pedido} Cancelada com Sucesso')

        else:
            raise ConteudoInvalido(pedido, f'Pedido de Locação Número {pedido} Não encontrado')


    def Devolver(self, pedido):
        if pedido in Loja.__locacoes:
            cliente = Loja.__locacoes[pedido][0]
            qtd = Loja.__locacoes[pedido][1]
            modalidade = Loja.__locacoes[pedido][2]
            dia = int(Loja.__locacoes[pedido][3])
            mes = int(Loja.__locacoes[pedido][4])
            ano = int(Loja.__locacoes[pedido][5])
            hora = int(Loja.__locacoes[pedido][6])
            minuto = int(Loja.__locacoes[pedido][7])
            inicio = datetime.datetime(ano, mes, dia, hora, minuto)
    
            # Cálculo do tempo e Valor de Cobrança
            valor_pagamento = 0
            devolucao = datetime.datetime.now()
            decorrido = (devolucao - inicio).seconds

            if modalidade.upper() == 'H':
                tempo = decorrido / (60 ** 2)
                if tempo % (60 ** 2) > 0:
                    tempo += 1
                valor_pagamento = qtd * tempo * self.preco_hora

            if modalidade.upper() == 'D':
                tempo = decorrido / (60 ** 2 * 24)
                if tempo % (60 ** 2 * 24) > 0:
                    tempo += 1
                valor_pagamento = qtd * tempo * self.preco_dia

            if modalidade.upper() == 'M':
                tempo = decorrido / (60 ** 2 * 24 * 30)
                if tempo % (60 ** 2 * 24 * 30) > 0:
                    tempo += 1
                valor_pagamento = qtd * tempo * self.preco_mes

            if qtd >= 3: valor_pagamento * (1 - self.desconto_familia)

            Loja.__locacoes[pedido][8] = 'Devolvida'
            Loja.__locacoes[pedido][9] = (f'{valor_pagamento:03.2f}')
            Loja.__locacoes[pedido][10] = devolucao.day
            Loja.__locacoes[pedido][11] = devolucao.month
            Loja.__locacoes[pedido][12] = devolucao.year
            Loja.__locacoes[pedido][13] = devolucao.hour
            Loja.__locacoes[pedido][14] = devolucao.minute
            self.estoque += qtd
            Loja.__estoques[self.nome_loja] = self.estoque
            Loja.EstoqueTotal()
            print(f'Locação número {pedido} Paga com Sucesso no valor de R$ {valor_pagamento:03.2f}')
                
        else:
            raise ConteudoInvalido(pedido, f'A Locação de número {pedido} não foi Devolvida')
            


# In[4]:


class SistemaLocacaoBicicletas():
    
    __cadastro_cliente = {}
    __cadastro_loja = {}
    
    #Construtor
    def __init__(self, nome_sistema):
        self.nome_sistema = nome_sistema

    # Métodos privados - getter e setter para nome
    def __get_nome_sistema(self):
        return self.__nome_sistema
    def __set_nome_sistema(self, valor_nome):        
        if len(valor_nome) < 5:
            raise ConteudoInvalido(valor_nome, 'Nome do Sistema deve ter mais de 5 caracteres')
        if valor_nome_sistema.isdigit():
            raise ConteudoInvalido(valor_nome, 'Nome do Sistema Não pode ser numérico')
        self.__nome_sistema = valor_nome
    nome = property(__get_nome_sistema, __set_nome_sistema)

    def ExibeMenu(self):
        '''
        Essa função exibe as opções do Menu, sem Retorno
        '''
        # Exibe as opções de Menu
        tracos = int((50 - len(self.nome_sistema)) / 2) - 1
        print(f'\n{"-"*tracos} {self.nome_sistema} {"-"*tracos}')
        print("1. Cadastrar Cliente          2. Listar Clientes")
        print("3. Cadastrar Loja             4. Listar Lojas")
        print("5. Alugar Bikes               6. Listar Locações")
        print("7. Devolver Bikes             8. Cancelar Locação")    
        print("9. Locações do Cliente       10. Locações da Loja")
        print("0. Sair")
        print(f'{"-"*tracos} {self.nome_sistema} {"-"*tracos}')

    def Menu(self):   
        '''
        Essa função solicita ao usuário que informe uma opção do Menu
        Até que o mesmo selecione uma opção válida
        Exibe mensagem de erro qdo selecionada opção inválida
        Retorna a opção válida selecionada
        '''
        selecao = 1
        while selecao != 0:
            try:
                SistemaLocacaoBicicletas.ExibeMenu(self)
                selecao = input("Digite sua opção: ")
                selecao = int(selecao)

                if selecao == 0:
                    print(f"Obrigado por utilizar o {self.nome_sistema}!")

                elif selecao == 1:
                    self.CadastrarCliente()

                elif selecao == 2:
                    Cliente.ListarClientes()
                    Cliente.TotalClientes()

                elif selecao == 3:
                    self.CadastrarLoja()

                elif selecao == 4:
                    Loja.ListarLojas()

                elif selecao == 5:
                    self.CadastrarLocacao()

                elif selecao == 6:
                    Loja.ListarLocacoes()

                elif selecao == 7:
                    try:
                        Loja.ListarLocacoes()
                        numero_pedido = input(f"Digite o número da Locação a Devolver e Pagar (ou ENTER para VOLTAR): ")
                        if numero_pedido == '':
                            continue
                        else:
                            numero_pedido = int(numero_pedido)
                            item_pedido = Loja.ObterLocacao(numero_pedido)

                            if item_pedido[8] == 'Devolvida':
                                raise ConteudoInvalido(numero_pedido,f'Locação {numero_pedido} já Devolvida')
                            else:
                                obj_loja = self.ObterObjetoLoja(item_pedido[15])
                                devolucao = obj_loja.Devolver(numero_pedido)
                            
                    except ConteudoInvalido as erro:
                        print(erro)
                    
                    except:
                        print(f'Locação Número {numero_pedido} Não pode ser Devolvida!\n')

                elif selecao == 8:
                    try:
                        Loja.ListarLocacoes()
                        numero_pedido = input(f"Digite o número da Locação a Cancelar (ou ENTER para VOLTAR): ")
                        if numero_pedido == '':
                            continue
                        else:
                            numero_pedido = int(numero_pedido)
                            item_pedido = Loja.ObterLocacao(numero_pedido)

                            if item_pedido[8] == 'Devolvida':
                                raise ConteudoInvalido(numero_pedido,f'Locação {numero_pedido} já Devolvida. Não pode ser Cancelada')
                            else:
                                obj_loja = self.ObterObjetoLoja(item_pedido[15])
                                devolucao = obj_loja.CancelarPedido(numero_pedido)
                            
                    except ConteudoInvalido as erro:
                        print(erro)
                    
                    except:
                        print(f"Locação Número {numero_pedido} Não pode ser Cancelada!\n")

                elif selecao == 9:
                    nome = input("Digite o nome do Cliente (ou ENTER para VOLTAR): ") 
                    if nome == '':
                        continue
                    else:
                        Loja.ListarLocacoes(None, nome)

                elif selecao == 10:
                    nome = input("Digite o nome da Loja (ou ENTER para VOLTAR): ") 
                    if nome == '':
                        continue
                    else:
                        Loja.ListarLocacoes(None, None, nome)
                        
                else:
                    print(f"OPÇÃO {selecao} NÃO DISPONÍVEL! Selecione um número entre 0 e 10\n")
                    
            except:
                print(f"OPÇÃO {selecao} INVÁLIDA! Selecione um número entre 0 e 10\n")

    def CadastrarLocacao(self):

        sair = False
        while sair == False:

            try:
                nome = input("Digite o nome do Cliente (ou ENTER para VOLTAR): ") 
                if nome == '':
                    sair = True
                    break
                
                obj_cliente = self.ObterObjetoCliente(nome)
                if obj_cliente == False:
                    print('Cliente não encontrado')
                    continue

                nome_loja = input("Digite o nome da Loja (ou ENTER para VOLTAR): ") 
                if nome_loja == '':
                    sair = True
                    break
                
                obj_loja = self.ObterObjetoLoja(nome_loja)
                if obj_loja == False:
                    print('Loja não encontrada')
                    continue

                qtde = input("Digite a quantidade a alugar: ") 
                try:
                    qtde = int(qtde)
                    if qtde <= 0:
                        raise ConteudoInvalido(qtde, 'O aluguel deve ser maior do que {qtde} bicicletas')
                except:
                    raise ConteudoInvalido(qtde, 'Quantidade de Bicicletas deve ser numérica maior do que 0')

                modo = input("Digite a modalidade a alugar (H - hora, D - Dia, M - Mês): ") 
                try:
                    if modo.upper() not in ['H', 'D', 'M']:
                        raise ConteudoInvalido(modo, 'Modalidade deve ser H - hora, D - Dia, M - Mês')

                except:
                    raise ConteudoInvalido(qtde, 'Modalidade Inválida')

                dthr_locacao = datetime.datetime.now()
                ano = dthr_locacao.year
                mes = dthr_locacao.month
                dia = dthr_locacao.day
                hora = dthr_locacao.hour
                minuto = dthr_locacao.minute

                try:
                    obj_loja.Locar(obj_cliente, qtde, modo, dia, mes, ano, hora, minuto)
                    print(f'Locação de {nome} Cadastrada com Sucesso para {qtde} bicicletas')
                    print(f'Início em {dia}/{mes}/{ano} às {hora}:{minuto}')
                except:
                    raise ConteudoInvalido(obj_loja, 'Não foi possível Cadastrar Locação')

            except ConteudoInvalido as erro:
                print(erro)

    def CadastrarCliente(self):

        sair = False
        while sair == False:

            nome = input("Digite o nome do Cliente (ou ENTER para VOLTAR): ") 
            if nome == '':
                sair = True
                break

            cpf = input("Digite o CPF do cliente: ")
            try:
                cpf = Cliente.LimparCPF(cpf)
            except:
                print(f'CPF {cpf} inválido')
                continue

            try:
                novo_cliente = Cliente(cpf, nome)
                if self.ObjetoCliente(nome, novo_cliente) == True:
                    print(f'Cliente {nome} Cadastrado com Sucesso')
                else:
                    raise ConteudoInvalido(nome, 'Não foi possível Cadastrar o Cliente {nome}')
            except ConteudoInvalido as invalido:
                print(invalido)
            except:
                print(f'Cliente {nome} Não pode ser Criado')

    def CadastrarLoja(self):

        sair = False
        while sair == False:

            nome = input("Digite o nome da Loja (ou ENTER para VOLTAR): ") 
            if nome == '':
                sair = True
                break

            estoque = input("Digite o estoque inicial de bicicletas: ")
            try:
                estoque = int(estoque)
            except:
                print(f'Estoque precisa ser um valor numérico inteiro')
                continue

            preco_hora = input("Digite o preço do aluguel por hora: ")
            preco_dia = input("Digite o preço do aluguel por dia: ")
            preco_mes = input("Digite o preço do aluguel por mês: ")
            desconto = input("Digite o desconto família (3 ou +): ")

            try:
                nova_loja = Loja(nome, estoque, preco_hora, preco_dia, preco_mes, desconto)
                if self.ObjetoLoja(nome, nova_loja) == True:
                    print(f'Loja {nome} Cadastrada com Sucesso')
                else:
                    raise ConteudoInvalido(nome, 'Não foi possível Cadastrar a Loja {nome}')
            except ConteudoInvalido as invalido:
                print(invalido)
            except:
                print(f'Loja {nome} Não pode ser Criada')

    def ObterPedido(self, numero_pedido):
        
        lista_locacoes = Loja.ListarLocacoes()
        try:
            numero_pedido = int(numero_pedido)
            if numero_pedido in lista_locacoes:
                return lista_locacoes[numero_pedido]
            else:
                print(f'Locação {numero_pedido} não está na lista')
                return False
        except:
            print(f'Locação {numero_pedido} Inválida')
            return False

    def ObjetoLoja(self, nome_loja, loja):
        if nome_loja not in self.__cadastro_loja:
            SistemaLocacaoBicicletas.__cadastro_loja[nome_loja] = [loja]
            return True
        else:
            print('Cadastro de {nome_loja} não criado')
            return False

    def ObterObjetoLoja(self, nome_loja):
        if nome_loja in self.__cadastro_loja:
            return self.__cadastro_loja[nome_loja][0]
        else:
            return False

    def ObjetoCliente(self, nome, cliente):
        if nome not in self.__cadastro_cliente:
            self.__cadastro_cliente[nome] = [cliente]
            return True
        else:
            print('Cadastro de {nome} não criado')
            return False

    def ObterObjetoCliente(self, nome):
        
        if nome in self.__cadastro_cliente:
            return self.__cadastro_cliente[nome][0]
        else:
            return False

        
    def Testar(self):
        luiz = Cliente('16278562421','Luiz Cláudio')
        self.ObjetoCliente('Luiz Cláudio', luiz)
        marcos = Cliente('73488536416','Marcos')
        self.ObjetoCliente('Marcos', marcos)
        joao = Cliente('66280777995','João Pedro Martins')
        self.ObjetoCliente('João Pedro Martins', joao)
        lena = Cliente('43414540568','Helena')
        self.ObjetoCliente('Helena', lena)
        katia = Cliente('73315173176','Katia')
        self.ObjetoCliente('Katia', katia)

        amarela = Loja('Amarela', 12, 5.0, 25.0, 100., 0.3)
        self.ObjetoLoja('Amarela', amarela)
        azul = Loja('Azul Turquesa', 20, 4.9, 24.9, 99., 0.3)
        self.ObjetoLoja('Azul Turquesa', azul)
        lilas = Loja('Lilas', 14, 5.5, 29.0, 95., 0.3)
        self.ObjetoLoja('Lilas', lilas)
        verde = Loja('Verde', 25, 5.4, 23.0, 90., 0.3)
        self.ObjetoLoja('Verde', verde)
        roxa = Loja('Roxinha', 19, 7.0, 24.0, 92.7, 0.3)
        self.ObjetoLoja('Roxinha', roxa)

        roxa.Locar(luiz,2,"h", 19,2,2022,10,0)
        azul.Locar(marcos,3,"h", 18,2,2022,7,0)
        verde.Locar(katia,5,"d", 1,2,2022,8,0)
        lilas.Locar(katia,2,"h", 20,2,2022,10,50)
        verde.Locar(lena,1,"m", 19,2,2022,10,0)
        roxa.Locar(joao,7,"h", 18,2,2022,10,30)
        verde.Locar(lena,4,"m", 20,2,2022,10,0)





SisBike = SistemaLocacaoBicicletas('SisBike')
#SisBike.Testar()

SisBike.Menu()

