from models import Categoria, Estoque, Pessoa, Produtos, Fornecedor, Funcionario, Venda
from dao import DaoCategoria, DaoEstoque, DaoFornecedor, DaoFuncionario, DaoPessoa, DaoVenda
from datetime import datetime

class ControllerCategoria:
    def cadastra_categoria(self, novaCategoria):
        existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe = True
            
        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print("Categoria cadastrada com sucesso!")
        else:
            print("A categoria que deseja cadastrar ja existe.")

    
    def remover_categoria(self, categoriaRemover):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))

        if len(cat) <= 0:
            print("A categoria que deseja remover nao existe.")
        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break

            print("Categoria removida com sucesso!")

            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')


    def alterar_categoria(self, categoriaAlterar, categoriaAlterada):
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaAlterada, x))

            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaAlterada) if(x.categoria == categoriaAlterar) else(x), x))
                print('A alteracao foi efetuada com sucesso!')
            else:
                print('A categoria para qual deseja alterar ja existe.')

        else:
            print('A categoria que deseja alterar nao existe.')


        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')


    def mostrar_categoria(self):
        categorias = DaoCategoria.ler()
        if len(categorias) == 0:
            print("Categoria vazia")
        else:
            for i in categorias:
                print(f"Categoria: {i.categoria}")


class ControllerEstoque:
    def cadastrar_produto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print("Produto cadastrado com sucesso!")
            else:
                print("Produto ja existe em estoque.")
        else:
            print("Categoria inexistente")


    def remover_produto(self, nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    break  
            print("Produto removido com sucesso")

        else:
            print("O produto que deseja remover nao existe.")

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + 
                            i.produto.preco + "|" + 
                            i.produto.categoria + "|" +
                            str(i.quantidade))
                arq.writelines('\n')

    def alterar_produto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == novaCategoria, y))

        if len(h) > 0:
            est = list(filter(lambda x: x.produto.nome == nomeAlterar, x))
            if len(est) > 0:
                est1 = list(filter(lambda x: x.produto.nome == novoNome, x))
                if len(est1) == 0:
                    x =list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if(x.produto.nome == nomeAlterar) else(x), x))
                    print('Produto alterado com sucesso')
                else:
                    print("Produto ja cadastrado no sistema")

            else:
                print("O Produto que deseja alterar nao existe.")
        else:
            print("Categoria informada nao existe.")

        
        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + 
                            i.produto.preco + "|" + 
                            i.produto.categoria + "|" +
                            str(i.quantidade))
                arq.writelines('\n')

    def mostrar_estoque(self):
        estoque = DaoEstoque.ler()
        if len(estoque) == 0:
            print("Estoque vazio")
        else:
            print("==========Produtos==========")
            for i in estoque:
                print(f'Nome: {i.produto.nome}\n'
                      f'Preco: {i.produto.preco}\n'
                      f'Categoria: {i.produto.categoria}\n'
                      f'Quantidade: {i.quantidade}\n'
                )
                print('----------------')


class ControllerVenda:
    def cadastrar_venda(self, nomeProduto, vendedor, comprador, quantidadeVendida):
        x = DaoEstoque.ler()
        temp = []
        existe = False 
        quantidade = False
        
        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= quantidadeVendida:
                        quantidade = True
                        
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)

                        valor_compra = int(quantidadeVendida) * int(i.produto.preco)

                        DaoVenda.salvar(vendido)

            temp.append([Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade])

            arq = open('estoque.txt', 'w')
            arq.write('')

            for i in temp:
                with open('estoque.txt', 'a') as arq:
                    arq.writelines(i[0].nome + "|" + i[0].preco, + "|" + i[0].categoria + "|" + str(i[1]))
                    arq.writelines('\n')

            if existe == False:
                print('O produto nao existe.')
                return None
            elif not quantidade:
                print('A quantidade nao contem em estoque.')
                return None
            else:
                print('Venda realizada com sucesso.')
                return valor_compra


a = ControllerVenda()
a.cadastrar_venda('banana', 'bruno', 'caio', 1000)