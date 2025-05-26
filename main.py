import os

def alterar_dados_cadastro(usuario):
    """
Permite a alteração dos dados de cadastro pelo usuário no arquivo "Cadastros.txt"
Podem ser alterações de nome, senha e e-mail fazendo as respectivas validações
    - Nome de usuário não pode estar duplicado.
    - Senha deve conter letras, números e no mínimo 8 caracteres.
    - E-mail deve possuir um domínio válido e não pode estar duplicado.

Parâmetros: Usuario, o nome de usuário que está logado no momento

Retorna: O usuario atualizado ou apenas usuario se não houver alterações

Exceções: Caso o arquivo "Cadastros.txt" não for encontrado exibe uma mensagem de erro

Esta função precisa do auxílio das seguintes funções:
    - ja_cadastrado_usuario(nome_usuario)
    - ja_cadastrado_email(email)
    """
    try:
        with open("Cadastros.txt", "r", encoding='cp1252') as f:
            linhas = f.readlines()

        alterado = False
        usuario_antigo = usuario
        novo_usuario = None
        nova_senha = None
        novo_email = None

        for i in range(0, len(linhas), 4):
            if linhas[i].strip() == usuario:
                print("============================================")
                print("Qual informação você deseja alterar?")
                print("1 - Nome de usuário")
                print("2 - Senha")
                print("3 - Email\n")
                resposta = input("Digite o número correspondente: ")

                if resposta == "1":
                    while True:
                        novo_usuario = input("Digite seu novo nome de usuário: ").strip()
                        if ja_cadastrado_usuario(novo_usuario):
                            print("❌ Nome de usuário já existe.")
                        else:
                            linhas[i] = novo_usuario + "\n"
                            usuario = novo_usuario
                            break

                elif resposta == "2":
                    nova_senha = input("Digite sua nova senha (mínimo 8 caracteres, letras e números): ").strip()
                    if len(nova_senha) < 8:
                        print("❌ A senha precisa ter no mínimo 8 caracteres.\n")
                        return usuario
                    elif not any(char.isalpha() for char in nova_senha):
                        print("❌ A senha deve conter pelo menos uma letra.\n")
                        return usuario
                    elif not any(char.isdigit() for char in nova_senha):
                        print("❌ A senha deve conter pelo menos um número.\n")
                        return usuario
                    else:
                        print("✅ Senha válida.\n")
                        linhas[i + 1] = nova_senha + "\n"

                elif resposta == "3":
                    novo_email = input("Digite seu novo email: ").strip()
                    if not novo_email.endswith(("@gmail.com", "@hotmail.com", "@yahoo.com.br", "@outlook.com")):
                        print("❌ Domínio inválido.\n")
                        return usuario
                    if ja_cadastrado_email(novo_email):
                        print("❌ Este email já está sendo usado.\n")
                        return usuario
                    linhas[i + 2] = novo_email + "\n"

                else:
                    print("❌ Resposta inválida.\n")
                    return usuario

                alterado = True
                break

        if alterado:
            with open("Cadastros.txt", "w", encoding='cp1252') as f:
                f.writelines(linhas)

            # Atualiza também no usuarios.txt
            atualizar_dados_no_txt(usuario_antigo, usuario_novo=novo_usuario, nova_senha=nova_senha, novo_email=novo_email)

            print("✅ Dados alterados com sucesso!\n")
            global login_usuario
            login_usuario = usuario
        else:
            print("❌ Usuário não encontrado.\n")

        return usuario

    except FileNotFoundError:
        print("❌ Arquivo Cadastros.txt não encontrado.\n")
        return usuario
    

def atualizar_dados_no_txt(usuario_antigo, usuario_novo=None, nova_senha=None, novo_email=None):
    """
    Atualiza os dados de um usuário no arquivo usuarios.txt.

    Permite atualizar o nome de usuário, a senha e o e-mail. 
    O usuário é identificado pelo nome atual (usuario_antigo).
    Caso algum dos novos dados não seja informado, esse campo permanece inalterado.

    Args:
        usuario_antigo (str): Nome atual do usuário que terá os dados alterados.
        usuario_novo (str, opcional): Novo nome de usuário. Default é None (não altera).
        nova_senha (str, opcional): Nova senha. Default é None (não altera).
        novo_email (str, opcional): Novo e-mail. Default é None (não altera).

    Returns:
        None
    """
    try:
        with open("usuarios.txt", "r", encoding='cp1252') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("❌ Arquivo usuarios.txt não encontrado.")
        return

    novas_linhas = []

    for linha in linhas:
        dados = linha.strip().split(':')

        if dados[0] == usuario_antigo:
            if usuario_novo:
                dados[0] = usuario_novo
            if nova_senha:
                dados[1] = nova_senha
            if novo_email:
                dados[2] = novo_email

            nova_linha = ":".join(dados) + "\n"
            novas_linhas.append(nova_linha)
        else:
            novas_linhas.append(linha)

    with open("usuarios.txt", "w", encoding='cp1252') as f:
        f.writelines(novas_linhas)

    print("🔄 Dados atualizados no usuarios.txt")
    
def deletar_conta(usuario):
    """
Permite que o usuário apague seus dados salvos no arquivo "Cadastros.txt"
Verifica se o usuário realmente quer apagar conta 
    - Se sim a conta é deletada
    - Se não o usuário volta para o menu_metacash

Parâmetros: Usuario, o nome de usuário que está logado no momento

Exceções: 
    - Caso o arquivo "Cadastros.txt" não for encontrado exibe uma mensagem de erro
    - Caso o nome de usuário não for encontrado exibe um erro

    """
    resposta = input("Você realmente deseja deletar a sua conta? (S/N) ")
    if resposta.upper() == "S":
        try:
            with open("Cadastros.txt", "r", encoding='cp1252') as f:
                linhas = f.readlines()

            nova_lista = []
            deletado = False
            for i in range(0, len(linhas), 4):
                if linhas[i].strip() == usuario:
                    deletado = True
                    continue  
                nova_lista.extend(linhas[i:i + 4])  
            if deletado:
                with open("Cadastros.txt", "w", encoding='cp1252') as f:
                    f.writelines(nova_lista)
                print("✅ Sua conta foi deletada com sucesso")
                central_do_site()
            else:
                print("❌ Usuário não encontrado")
        except FileNotFoundError:
            print("❌ Arquivo de cadastro não encontrado.")
    else:
        print("❌ Operação cancelada.")


def ver_perfil_usuario(usuario):
    """
Permite que o usuário veja as informações que ele cadastrou no arquivo "Cadastros.txt"
Redireciona o usuário para as funções:
    - alterar_dados_cadastro
    - deletar_conta
    - menu_metacash

Parâmetros: Usuario, o nome de usuário que está logado no momento

Retorna: O usuario 

Exceções: Caso o arquivo "Cadastros.txt" não for encontrado exibe uma mensagem de erro

    """
    try:
        with open ("Cadastros.txt", "r", encoding = 'cp1252') as f:
            linhas = f.readlines()
            for i in range(0, len(linhas), 4):
                try:
                    usuario_cadastrado = linhas[i].strip()
                    if usuario_cadastrado == usuario:
                        senha = linhas[i + 1].strip()
                        email = linhas[i + 2].strip()
                        print("======== 👤 Perfil de usuário 👤 ========", "\n")
                        print(f"Usuário: {usuario_cadastrado}")
                        print(f"Senha: {senha}")
                        print(f"Email: {email}", "\n")
                        print("1 - Alterar informações")
                        print("2 - Deletar conta")
                        print("3 - Sair do menu de perfil", "\n")
                        opcao = input("Digite o número correspondente para prosseguir: ")
                        if opcao == "1":
                            usuario = alterar_dados_cadastro(usuario)
                        elif opcao == "2":
                            deletar_conta(usuario)
                        elif opcao == "3":
                            return usuario
                except IndexError:
                    continue
            return usuario
    except FileNotFoundError:
        print("❌ Arquivo de cadastro não encontrado")
        return usuario


def ja_cadastrado_email(email):
    """
Verifica se o email já está salvo no arquivo "Cadastros.txt"

Parâmetros: email

Retorna: True se o email for = ao email cadastrado, se não retorna False
    """
    try:
        with open("Cadastros.txt", "r", encoding = 'cp1252') as f:
            linhas = f.readlines()
            for i in range(0, len(linhas), 4):
                try:
                    email_cadastrado = linhas[i + 2].strip()
                    if email == email_cadastrado:
                        return True
                except IndexError:
                    continue
    except FileNotFoundError:
        return False


def ja_cadastrado_usuario(usuario):
    """
Verifica se o usuário já está salvo no arquivo "Cadastros.txt"

Parâmetros: usuario

Retorna: True se o usuário for = ao usuário cadastrado, se não retorna False
    """
    try:
        with open("Cadastros.txt", "r", encoding = 'cp1252') as f:
            linhas = f.readlines()
            for i in range(0, len(linhas), 4):
                try:
                    usuario_cadastrado = linhas[i].strip()
                    if usuario == usuario_cadastrado:
                        return True
                except IndexError:
                    continue
    except FileNotFoundError:
        return False


def login():
    """
Permite que o usuário use os dados que ele cadastrou, para acessar o site com suas informações
Redireciona o usuário para a função 
    - menu_metacash()

Parâmetros: ()
    """
    while True:
        global login_usuario
        login_usuario = input("Digite o seu nome de usuário: ")
        login_senha = input("Digite sua senha: ")
        try:
            with open("Cadastros.txt", "r", encoding = 'cp1252') as f:
                linhas = f.readlines()
                for i in range(0, len(linhas), 4):
                    try:
                        usuario_cadastrado = linhas[i].strip()
                        senha_cadastrada = linhas[i + 1].strip()
                        if usuario_cadastrado == login_usuario and senha_cadastrada == login_senha:
                            print("✅ Seu login foi realizado com sucesso!", "\n")
                            return usuario_cadastrado
                    except IndexError:
                        continue
            print("❌ Usuário ou senha incorretos")
        except FileNotFoundError:
            print("❌ Cadastro não existe")


def cadastro():
    """
Permite que o usuário se cadastre no Metacash, colocando usuário senha e email e faz as seguintes verificações
    - Nome de usuário não pode estar duplicado.
    - Senha deve conter letras, números e no mínimo 8 caracteres.
    - E-mail deve possuir um domínio válido e não pode estar duplicado

Parâmetros: ()
    """
    while True:
        usuario = input("Digite um nome de usuário: ")
        if ja_cadastrado_usuario(usuario):
            print("❌ Usuário já cadastrado tente outro", "\n")
        else:
            print("✅ Usuário válido", "\n")
            break
    while True:
        senha = input("Digite uma senha que contenha no mínimo 8 caracteres, e tenha letras e números: ")
        if len(senha) < 8:
            print ("❌ A senha precisa ter no mínimo 8 caracteres", "\n")
            continue
        elif not any(char.isalpha() for char in senha):
            print ("❌ A senha deve ter no mínimo uma letra", "\n")
            continue
        elif not any(char.isdigit() for char in senha):
            print ("❌ A senha precisa ter pelo menos um número", "\n")
            continue
        else:
            print("✅ Senha válida", "\n")
            break
    while True:
        validar_senha = input(" Digite sua senha novamente: ")
        if validar_senha == senha:
            print("✅ Senha correspondennte", "\n")
            break
        else:
            print("❌ Senha não correspondente", "\n")
            continue
    while True:
        email = input("Digite seu email, (domínios aceitos: @gmail.com, @hotmail.com, @yahoo.com.br, @outlook.com): ")
        if not email.endswith(("@gmail.com", "@hotmail.com", "@yahoo.com.br", "@outlook.com")):
            print("❌ O email não possui um dos domínios especificados", "\n")
            continue
        if ja_cadastrado_email(email):
            print("❌ Já existe uma conta com esse email", "\n")
        else:
            print("✅ Email válido","\n")
            print("Redirecionando para o menu do site")
            break
    with open("Cadastros.txt", "a", encoding = 'cp1252') as f:
        f.write(usuario + "\n")
        f.write(senha + "\n")
        f.write(email + "\n")
        f.write("----------\n")
    print("✅ Cadastro concluído. Voltando para o menu inicial")
    return


def menu_metacash(usuario):
    """
Permite que o usuário acesse as principais funções do Metacash
Redireciona o usuário para as funções:
    - coleta_de_dados()
    - menu_metas()
    - ver_perfil_usuario(usuário)
    - central_do_site()


Parâmetros: usuário
    """
    while True:
        print("========== Metacash ==========", "\n")
        print("1 - Coleta de dados ")
        print("2 - Metas ")
        print("3 - Ver perfil de usuário")
        print("4 - Sair do Metacash", "\n")
        resposta_menu = input("Digite o número correspondente ao que você deseja: ")
        if resposta_menu == "1":
            coleta_de_dados()
            continue
        elif resposta_menu == "2":
            menu_metas()
            continue

        elif resposta_menu == "3":
            usuario = ver_perfil_usuario(usuario)
        elif resposta_menu == "4":
            print("\n======================================")
            print("Obrigado por usar o Metacash até logo!👋")
            print("\n======================================")
            break

        
def central_do_site():
    """
Permite que o usuário acesse as funções de login e cadastro necessárias para acessar o site
Redireciona o usuário para as funções:
    - login()
    - cadastro()
    """
    while True:
        print("======= Bem vindo ao Metacash =======", "\n")
        print("O que você deseja?")
        print("1 - Login")
        print("2 - Cadastro")
        print("3 - Sair", "\n")
        resposta = input("Digite o número correspondente ao que você deseja: ")
        if resposta == "1":
            usuario_logado = login()
            if usuario_logado:
                menu_metacash(usuario_logado)
        elif resposta == "2":
            cadastro()
        elif resposta == "3":
            print("Até a proxima")
            break
        else:
            print("❌ Resposta inválida", "\n")
            continue


def carregar_usuarios(arquivo):
    usuarios = []
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            for linha in linhas:
                partes = linha.strip().split('|')
                if len(partes) < 4:
                    partes += [''] * (4 - len(partes))  # Garante que tenha sempre 4 campos
                usuarios.append({
                    'nome': partes[0],
                    'salario': float(partes[1]),
                    'meta': partes[2],
                    'prazo': partes[3]
                })
    except FileNotFoundError:
        print(f"O arquivo {arquivo} não foi encontrado.")
    return usuarios


# Função para salvar os dados no arquivo
def salvar_usuarios(arquivo, usuarios):
    """
    Salva a lista de usuários em um arquivo de texto usuarios.txt.

    Cada usuário é salvo no formato: nome|salario|meta|prazo.

    Parâmetros:
    - arquivo (str): Caminho do arquivo onde os dados serão salvos.
    - usuarios (list): Lista de dicionários contendo os dados dos usuários.

    Retorna:
    - None
    """
    with open(arquivo, 'w', encoding='utf-8') as f:
        for u in usuarios:
            linha = f"{u['nome']}|{u['salario']}|{u['meta']}|{u['prazo']}\n"
            f.write(linha)


# Função para criar ou atualizar a meta e o prazo
def criar_ou_atualizar_meta(arquivo, nome_usuario):
    """
    Cria ou atualiza a meta financeira e o prazo de um usuário específico.

    Valida se a meta é viável com base no salário, gera uma análise da meta (diária, semanal, mensal) 
    e salva as informações no arquivo usuarios.txt.

    Parâmetros:
    - arquivo (str): Caminho do arquivo onde os dados estão armazenados.
    - nome_usuario (str): Nome do usuário que terá a meta definida ou atualizada.

    Retorna:
    - None
    """
    usuarios = carregar_usuarios(arquivo)
    usuario_encontrado = None

    for usuario in usuarios:
        if usuario['nome'].lower() == nome_usuario.lower():
            usuario_encontrado = usuario
            break

    if not usuario_encontrado:
        print("\n===========================")
        print("❌-Usuário não encontrado!")
        print("\n===========================")
        return

    # Converter salário para float para garantir cálculos corretos
    salario = float(usuario_encontrado['salario'])

    # ====== INPUT DO VALOR DA META ======
    while True:
        try:
            valor_meta = float(input("\n💵-Qual é o valor total da sua meta? R$"))
            if valor_meta > salario:
                print("\n=========================================================================")
                print("❌-O valor da meta não pode ser maior que o seu salário! Tente novamente.")
                print("\n=========================================================================")
                continue
            elif valor_meta <= 0:
                print("\n===============================================================================")
                print("❌-Meta inválida, sua meta não pode ser negativa ou igual a 0. Tente novamente.")
                print("\n===============================================================================")
                continue
        except ValueError:
            print("\n==================================")
            print("❌-Digite um valor numérico válido.")
            print("\n==================================")
            continue
        break

    # ====== INPUT DO PRAZO DA META ======
    while True:
        try:
            dias = int(input("\n⏰-Em quantos dias você deseja alcançar essa meta? "))
            if dias <= 0:
                print("❌-O número de dias deve ser maior que 0. Tente novamente.")
                continue
        except ValueError:
            print("❌-Digite um número inteiro válido.")
            continue
        break

    # ====== VALIDAÇÃO SE A META É REALISTA ======
    meta_diaria = valor_meta / dias
    if meta_diaria > salario * 0.35:
        print("================================================================================================")
        print("⚠️CUIDADO: Sua meta diária é maior que 35% do seu salário. Isso pode ser arriscado.⚠️")
        print("================================================================================================")
    else:
        print("===============================================")
        print("✅-Sua meta parece realista, continue assim!👏")
        print("===============================================")

    # ====== EXIBINDO OS CÁLCULOS ======
    print("\n=======================(META DEFINIDA)=======================\n")

    if dias < 7:
        print("Você tem uma meta diária!📄")
        print(f"Meta Diária: R$ {meta_diaria:.2f} por dia")

    elif dias < 30:
        semanas = max(1, dias // 7)
        meta_semanal = valor_meta / semanas
        print("Você tem uma meta diária e semanal!📋")
        print(f"Meta Diária: R$ {meta_diaria:.2f} por dia")
        print(f"Meta Semanal: R$ {meta_semanal:.2f} por semana")

    else:
        meta_semanal = meta_diaria * 7
        meta_mensal = meta_diaria * 30
        print("Você tem uma meta diária, semanal e mensal!📑")
        print(f"Meta Diária: R$ {meta_diaria:.2f} por dia")
        print(f"Meta Semanal: R$ {meta_semanal:.2f} por semana")
        print(f"Meta Mensal: R$ {meta_mensal:.2f} por mês")

    print(f"\nMeta total: R$ {valor_meta:.2f}")
    print(f"Prazo: {dias} dias")
    print("\n====================================================")

    # ====== ATUALIZA NO BLOCO DE NOTAS ======
    usuario_encontrado['meta'] = str(valor_meta)
    usuario_encontrado['prazo'] = str(dias)

    salvar_usuarios(arquivo, usuarios)

    print("✅-Meta e prazo salvos com sucesso!\n")


# Função para consultar metas
def consultar_metas(arquivo):
    """
    Exibe todas as metas cadastradas pelos usuários no arquivo.

    Mostra o nome, o valor da meta e o prazo de cada usuário que possui uma meta cadastrada.

    Parâmetros:
    - arquivo (str): Caminho do arquivo onde os dados estão armazenados.

    Retorna:
    - None
    """
    usuarios = carregar_usuarios(arquivo)
    print("\n=======================(METAS ATUAIS)=======================\n")
    encontrou = False
    for u in usuarios:
        if u['meta'] and u['prazo']:
            print(f"Nome: {u['nome']} | Meta: R$ {u['meta']} | Prazo: {u['prazo']} dias")
            encontrou = True
    if not encontrou:
        print("❌Nenhuma meta cadastrada até o momento.❌")
    print("\n=============================================================\n")


#  Função para cadastrar novo usuário
def cadastrar_usuario(arquivo):
    """
    Ler os dados imputados pelo usuário como nome, salário, prazo e metas. Para armazenar as informações, para as utilizar em outras funções
    Solicita nome e salário do usuário, verifica se já existe 
    um usuário com o mesmo nome, e adiciona um novo usuário ao arquivo.

    Args:
        arquivo (str): Caminho do arquivo onde os dados dos usuários estão armazenados.

    Returns:
        None
    """
    usuarios = carregar_usuarios(arquivo)
    nome = input("Digite o nome do novo usuário: ").strip()

    # Verifica se o usuário já existe
    for u in usuarios:
        if u['nome'].lower() == nome.lower():
            print("\n========================")
            print("❌-Usuário já cadastrado.")
            print("\n========================")
            return

    while True:
        try:
            salario = float(input("Digite o salário do usuário: R$"))
            if salario <= 0:
                print("\n=======================================")
                print("❌-Salário inválido, tente novamente.")
                print("\n=======================================")
                continue
            break
        except ValueError:
            print("\n==================================")
            print("❌-Digite um valor numérico válido.")
            print("\n==================================")

    usuarios.append({
        'nome': nome,
        'salario': salario,
        'meta': '',
        'prazo': ''
    })

    salvar_usuarios(arquivo, usuarios)
    print("\n=========================================")
    print(f"✅-Usuário {nome} cadastrado com sucesso!")
    print("\n=========================================")

#Registro de Gasto#
def validar_registro_gasto(mensagem):
    """
    Valida a entrada de um valor monetário.

    Solicita um valor numérico, garantindo que seja positivo e válido.

    Parâmetros:
    - mensagem (str): Mensagem exibida ao usuário na solicitação do input.

    Retorna:
    - float: Valor inserido e validado pelo usuário.
    """
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor < 0:
                print("⚠️ Digite um valor positivo.")
                continue
            return valor
        except ValueError:
            print("⚠️ Digite um número válido.")


def validar_preferencia(categoria):
    """
    Valida a entrada de um peso de preferência para uma categoria de gasto.

    O peso deve ser um inteiro entre 1 e 5, representando a prioridade.

    Parâmetros:
    - categoria (str): Nome da categoria (ex.: 'Alimentação', 'Lazer', 'Transporte').

    Retorna:
    - int: Peso de prioridade validado.
    """
    while True:
        try:
            peso = int(input(f"Peso de prioridade para {categoria} (1 a 5): "))
            if peso < 1 or peso > 5:
                print("⚠️ O peso deve ser entre 1 e 5.")
                continue
            return peso
        except ValueError:
            print("⚠️ Digite um número inteiro válido.")


# Função para salvar ou substituir usuário no arquivo usuarios.txt
def salvar_ou_substituir_usuario(usuario, senha, email, salario, valor_meta, progresso,
                                alimentacao, lazer, transporte, fixos, preferencias, prazo):
    """
    Salva ou atualiza as informações de um usuário no arquivo 'usuarios.txt'.

    Se o usuário já existir no arquivo, substitui os dados. Caso contrário, adiciona um novo registro.

    Parâmetros:
    - usuario (str): Nome do usuário.
    - senha (str): Senha do usuário.
    - email (str): E-mail do usuário.
    - salario (float): Salário mensal do usuário.
    - valor_meta (float): Valor da meta financeira.
    - progresso (float): Progresso atual na meta.
    - alimentacao (float): Gastos com alimentação.
    - lazer (float): Gastos com lazer.
    - transporte (float): Gastos com transporte.
    - fixos (float): Gastos fixos mensais.
    - preferencias (dict): Dicionário com pesos de prioridade para categorias.
    - prazo (int): Prazo (em dias) para alcançar a meta.

    Retorna:
    - None
    """
    nova_linha = (f"{usuario}:{senha}:{email}:{salario}:{valor_meta}:{progresso}:{prazo}:"
                f"{alimentacao}:{lazer}:{transporte}:{fixos}:"
                f"{preferencias['Alimentação']}:{preferencias['Lazer']}:"
                f"{preferencias['Transporte']}\n")

    try:
        with open("usuarios.txt", "r") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        linhas = []

    usuario_encontrado = False
    novas_linhas = []

    for linha in linhas:
        if linha.startswith(f"{usuario}:"):
            novas_linhas.append(nova_linha)
            usuario_encontrado = True
        else:
            novas_linhas.append(linha)

    if not usuario_encontrado:
        novas_linhas.append(nova_linha)

    with open("usuarios.txt", "w") as f:
        f.writelines(novas_linhas)

def coleta_de_dados():
    """
    Coleta dados financeiros do usuário logado.

    Solicita informações como salário, gastos fixos, alimentação, lazer e transporte,
    além dos pesos de prioridade para cada categoria.

    Salva ou atualiza os dados no arquivo 'usuarios.txt' associado ao usuário logado.

    Parâmetros:
    - Nenhum (usa a variável global login_usuario).

    Retorna:
    - None
    """
    global login_usuario  # garante que estamos usando o usuário logado

    print("================================")
    print("Informe seus dados financeiros")
    print("================================")

    usuario = None
    senha = None
    email = None

    try:
        with open("Cadastros.txt", "r", encoding='cp1252') as arquivo:
            linhas = arquivo.readlines()
            for i in range(0, len(linhas), 4):
                u = linhas[i].strip()
                s = linhas[i+1].strip()
                e = linhas[i+2].strip()

                if u == login_usuario:  # ✅ usa login_usuario corretamente
                    usuario = u
                    senha = s
                    email = e
                    break

    except FileNotFoundError:
        print("\n=========================================")
        print("⚠️ Arquivo Cadastros.txt não encontrado.")
        print("\n=========================================")
        return

    if usuario is None:
        print("\n========================================================")
        print(f"⚠️ Usuário '{login_usuario}' não encontrado no cadastro.")
        print("\n========================================================")
        return

    # Coleta de dados financeiros
    salario = validar_registro_gasto("Salário mensal: R$ ")
    fixos = validar_registro_gasto("Gastos com Custos Fixos: R$ ")
    alimentacao = validar_registro_gasto("Gastos com Alimentação: R$ ")
    lazer = validar_registro_gasto("Gastos com Lazer: R$ ")
    transporte = validar_registro_gasto("Gastos com Transporte: R$ ")

    # Preferências financeiras
    preferencias = {}
    preferencias['Alimentação'] = validar_preferencia("Alimentação")
    preferencias['Lazer'] = validar_preferencia("Lazer")
    preferencias['Transporte'] = validar_preferencia("Transporte")

    # Dados da meta inicial
    valor_meta = 0
    progresso = 0
    prazo = 0

    # Salvar dados no arquivo
    salvar_ou_substituir_usuario(
        usuario, senha, email, salario, valor_meta, progresso,
        alimentacao, lazer, transporte, fixos, preferencias, prazo
    )

    print("\n================================================")
    print("✅ Dados financeiros registrados com sucesso!")
    print("================================================\n")
# Função para carregar usuários do arquivo (necessária para algumas funções acima)
def carregar_usuarios(arquivo):
    """
    Carrega os dados dos usuários a partir de um arquivo de texto.

    Espera que cada linha do arquivo esteja no formato: nome|salario|meta|prazo.

    Parâmetros:
    - arquivo (str): Caminho do arquivo com os dados dos usuários.

    Retorna:
    - list: Lista de dicionários, cada um representando um usuário.
    """
    usuarios = []
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split('|')
                if len(partes) >= 4:
                    usuarios.append({
                        'nome': partes[0],
                        'salario': partes[1],
                        'meta': partes[2],
                        'prazo': partes[3]
                    })
    except FileNotFoundError:
        pass
    return usuarios
def carregar_usuarios_arquivo(arquivo):
    """
    Carrega os dados dos usuários a partir de um arquivo de texto.

    Cada linha do arquivo deve estar no formato separado por dois-pontos (:)
    representando os atributos do usuário.

    Args:
        arquivo (str): Caminho do arquivo contendo os dados dos usuários.

    Returns:
        list: Lista de dicionários, onde cada dicionário representa um usuário.
    """
    usuarios = []
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(':')
                if len(partes) >= 13:
                    usuarios.append({
                        'usuario': partes[0],
                        'senha': partes[1],
                        'email': partes[2],
                        'salario': float(partes[3]),
                        'valor_meta': float(partes[4]),
                        'progresso': float(partes[5]),
                        'prazo': int(partes[6]),
                        'alimentacao': float(partes[7]),
                        'lazer': float(partes[8]),
                        'transporte': float(partes[9]),
                        'fixos': float(partes[10]),
                        'pref_alimentacao': int(partes[11]),
                        'pref_lazer': int(partes[12]),
                        'pref_transporte': int(partes[13]) if len(partes) > 13 else 0
                    })
    except FileNotFoundError:
        pass
    return usuarios


def salvar_usuarios_arquivo(arquivo, usuarios):
    """
    Salva a lista de usuários em um arquivo de texto usuarios.txt.

    Cada usuário é salvo no formato: nome|salario|meta|prazo.

    Parâmetros:
    - arquivo (str): Caminho do arquivo onde os dados serão salvos.
    - usuarios (list): Lista de dicionários contendo os dados dos usuários.

    Retorna:
    - None
    """
    with open(arquivo, 'w', encoding='utf-8') as f:
        for u in usuarios:
            linha = (f"{u['usuario']}:{u['senha']}:{u['email']}:{u['salario']}:{u['valor_meta']}:"
                     f"{u['progresso']}:{u['prazo']}:{u['alimentacao']}:{u['lazer']}:"
                     f"{u['transporte']}:{u['fixos']}:{u['pref_alimentacao']}:{u['pref_lazer']}:"
                     f"{u['pref_transporte']}\n")
            f.write(linha)


def encontrar_usuario(usuarios, nome):
    """
    Procura um usuário na lista de usuários pelo nome.

    Args:
        usuarios (list): Lista de dicionários contendo dados dos usuários.
        nome (str): Nome do usuário a ser encontrado.

    Returns:
        dict or None: Retorna o dicionário do usuário se encontrado, 
                      caso contrário retorna None.
    """
    for u in usuarios:
        if u['usuario'].lower() == nome.lower():
            return u
    return None


def criar_ou_atualizar_meta(arquivo, nome_usuario):
    """
    Cria ou atualiza a meta financeira e o prazo de um usuário específico.

    Valida se a meta é viável com base no salário, gera uma análise da meta (diária, semanal, mensal) 
    e salva as informações no arquivo usuarios.txt.

    Parâmetros:
    - arquivo (str): Caminho do arquivo onde os dados estão armazenados.
    - nome_usuario (str): Nome do usuário que terá a meta definida ou atualizada.

    Retorna:
    - None
    """
    usuarios = carregar_usuarios_arquivo(arquivo)
    usuario = encontrar_usuario(usuarios, nome_usuario)
    if not usuario:
       print("\n==========================")
       print("❌ Usuário não encontrado.")
       print("\n==========================")
       return

    salario = usuario['salario']

    while True:
        try:
            valor_meta = float(input("\n 💵- Digite o valor total da meta: R$ "))
            if valor_meta <= 0 or valor_meta > salario * 10:  # limite arbitrário para evitar erro
                print("\n======================================")
                print(" ❌ Valor da meta irrealita, tente novamente.")
                print("\n======================================")
                continue
            break
        except ValueError:
            print("\n====================================")
            print("\n ❌Digite um valor numérico válido.")
            print("\n====================================")


    while True:
        try:
            prazo = int(input("\n 🕰️- Em quantos dias deseja alcançar a meta? "))
            if prazo <= 0:
                print("\n===============================")
                print(" ❌ Prazo deve ser maior que zero.")
                print("\n===============================")
                continue
            break
        except ValueError:
            print("\n===============================")
            print("❌ Digite um número inteiro válido.")
            print("\n===============================")
    usuario['valor_meta'] = valor_meta
    usuario['prazo'] = prazo
    usuario['progresso'] = 0  # reseta progresso ao criar/atualizar meta

    salvar_usuarios_arquivo(arquivo, usuarios)
    print("\n=========================================")
    print("✅ Meta e prazo atualizados com sucesso.")
    print("\n=========================================")


def registrar_progresso(arquivo, nome_usuario):
    """
    Permite que um usuário registre um valor de economia no progresso de sua meta.

    Verifica se o usuário existe e se possui uma meta definida. 
    Atualiza o progresso e reduz o prazo em 1 dia (se maior que zero).

    Args:
        arquivo (str): Caminho do arquivo onde os dados dos usuários estão armazenados.
        nome_usuario (str): Nome do usuário que deseja registrar o progresso.

    Returns:
        None
    """
    usuarios = carregar_usuarios_arquivo(arquivo)
    usuario = encontrar_usuario(usuarios, nome_usuario)
    if not usuario:
        print("\n===============================")
        print("❌ Usuário não encontrado. ❌")
        print("\n===============================")
        return

    if usuario['valor_meta'] == 0 or usuario['prazo'] == 0:
        print("\n===============================================================")
        print("❌ Você precisa criar uma meta antes de registrar progresso. ❌")
        print("\n===============================================================")
        return

    while True:
        try:
            valor = float(input("Quanto você economizou hoje? R$ "))
            if valor < 0:
                print("Valor inválido. Não pode ser negativo.")
                continue
            break
        except ValueError:
            print("\n==================================")
            print(" ❌ Digite um número válido. ❌ ")
            print("\n==================================")

    usuario['progresso'] += valor
    # Reduz o prazo em 1, mas garantindo que não fique negativo
    if usuario['prazo'] > 0:
        usuario['prazo'] -= 1

    salvar_usuarios_arquivo(arquivo, usuarios)
    print("\n==============================================================")
    print(f"✅ Progresso atualizado! Total economizado: R$ {usuario['progresso']:.2f}")
    print(f"⏳ Prazo restante: {usuario['prazo']} dias")
    print("\n==============================================================")

def ver_progresso(arquivo, nome_usuario):
    """
    Exibe o progresso atual de um usuário em relação à sua meta de economia.

    Mostra valores como total da meta, valor economizado, quanto falta,
    prazo restante e metas auxiliares (diária, semanal e mensal).
    Exibe também uma barra de progresso visual e dá feedback ao usuário.

    Args:
        arquivo (str): Caminho do arquivo onde os dados dos usuários estão armazenados.
        nome_usuario (str): Nome do usuário que deseja visualizar o progresso.

    Returns:
        None
    """
    usuarios = carregar_usuarios_arquivo(arquivo)
    usuario = encontrar_usuario(usuarios, nome_usuario)
    if not usuario:
        print("\n=========================================")
        print("❌ Usuário não encontrado. Tente novamente")
        print("=========================================")
        return

    valor_meta = usuario['valor_meta']
    progresso = usuario['progresso']
    prazo = usuario['prazo']

    if valor_meta == 0 or prazo == 0:
        print("\n================================")
        print("❌ Você ainda não definiu uma meta.")
        print("================================")
        return

    faltando = max(0, valor_meta - progresso)
    porcentagem = (progresso / valor_meta) * 100 if valor_meta > 0 else 0
    porcentagem = min(porcentagem, 100)  # Limita no máximo 100%

    dias_restantes = prazo

    # Metas auxiliares
    meta_diaria = valor_meta / (prazo if prazo != 0 else 1)
    meta_semanal = meta_diaria * 7
    meta_mensal = meta_diaria * 30

    # Barra de progresso
    total_blocos = 10  # Número de blocos visuais
    blocos_preenchidos = int((porcentagem / 100) * total_blocos)
    blocos_vazios = total_blocos - blocos_preenchidos

    barra = '●●' * blocos_preenchidos + '○○' * blocos_vazios

    print("\n================(PROGRESSO DA META)==================")
    print(f"🎯 Meta Total:           R$ {valor_meta:.2f}")
    print(f"💰 Progresso Atual:      R$ {progresso:.2f}")
    print(f"📉 Faltando:             R$ {faltando:.2f}")
    print(f"📅 Dias Restantes:       {dias_restantes} dia(s)")

    print(f"\n🗓️  Meta Diária:         R$ {meta_diaria:.2f}")
    print(f"📆 Meta Semanal:         R$ {meta_semanal:.2f}")
    print(f"🗓️  Meta Mensal:         R$ {meta_mensal:.2f}")

    print("\n==========", f"({porcentagem:.0f}%)".center(10), "==========")
    print(f"    {barra}")
    print("\n===============================================")

    # Feedback ao usuário
    if progresso >= valor_meta:
        print("\n🎉 Parabéns! Você já atingiu sua meta! 🥳")
    elif dias_restantes <= 0 and progresso < valor_meta:
        print("\n⚠️ Prazo encerrado e a meta não foi alcançada.")
    elif progresso >= (valor_meta - (meta_diaria * dias_restantes)):
        print("\n✅ Você está no ritmo certo! Continue assim!")
    else:
        print("\n⚠️ Atenção! Você está um pouco atrasado com a meta.")

def menu_metas():
    """
    Exibe o menu de gerenciamento de metas financeiras do usuário.

    Permite que o usuário escolha entre as opções disponíveis para:
    
Criar uma nova meta financeira.
Ver o progresso da meta atual.
Registrar um novo progresso (economias realizadas).,
Voltar ao menu principal.,
,
,

    A função executa a ação correspondente à opção selecionada e permanece no menu 
    até que o usuário opte por voltar.

    Returns:
        None
    """
    global login_usuario
    arquivo = "usuarios.txt"
    print("======== MENU DE METAS ========")
    nome_usuario = login_usuario 

    while True:
        print("\nEscolha uma opção:")
        print("1 - Criar/Atualizar Meta")
        print("2 - Registrar Progresso")
        print("3 - Ver Progresso")
        print("4 - Sair")
        print("\n===========================")
        opcao = input("\nOpção: ").strip()

        if opcao == '1':
            criar_ou_atualizar_meta(arquivo, nome_usuario)
        elif opcao == '2':
            registrar_progresso(arquivo, nome_usuario)
        elif opcao == '3':
            ver_progresso(arquivo, nome_usuario)
        elif opcao == '4':
            print("Saindo...")
            menu_metacash()
            break  # <-- Importante: precisa ter break para não ficar em loop infinito

        else:
            print("\n=====================================")
            print("❌ Opção inválida. Tente novamente. ❌")
            print("\n=====================================")
central_do_site() #Começa a rodar o codigo