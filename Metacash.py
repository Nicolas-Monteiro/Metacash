import os

def alterar_dados_cadastro(usuario):
    try:
        with open ("Cadastros.txt", "r", encoding = 'cp1252' ) as f:
            linhas = f.readlines()
        alterado = False
        for i in range(0, len(linhas), 4):
            if linhas[i].strip() == usuario:
                print("============================================")
                print("qual informação você deseja alterar?")
                print("1 - nome de usuário")
                print("2 - senha")
                print("3 - email", "\n")
                resposta = input("Digite o número correspondente: ")
                if resposta == "1":
                    while True:
                        novo_usuario = input("Digite seu novo nome de usuário: ")
                        if ja_cadastrado_usuario(novo_usuario):
                            print("❌ Nome de usuário ja existe")
                        else:
                            linhas[i] = novo_usuario + "\n"
                            usuario = novo_usuario
                            break
                elif resposta =="2":
                    nova_senha = input("Digite a sua nova senha ela precisa ter letras e números e no mínimo 8 caracters: ")
                    if len(nova_senha) < 8:
                        print ("❌ A senha precisa ter no mínimo 8 caracteres", "\n")
                        return usuario
                    elif not any(char.isalpha() for char in nova_senha):
                        print ("❌ A senha deve ter no mínimo uma letra", "\n")
                        return usuario
                    elif not any(char.isdigit() for char in nova_senha):
                        print ("❌ A senha precisa ter pelo menos um número", "\n")
                        return usuario
                    else:
                        print("✅ Senha válida", "\n")
                        linhas [i + 1] = nova_senha + "\n"
                elif resposta == "3":
                    novo_email = input("Digite o seu novo email: ")
                    if not novo_email.endswith(("@gmail.com", "@hotmail.com", "yahoo.com.br", "outlook.com")):
                        print("❌ Domínio inválido.")
                        return usuario
                    if ja_cadastrado_email(novo_email):
                        print("❌ Email já está sendo usado")
                        return usuario
                    linhas[i + 2] = novo_email + "\n"
                else:
                    print("❌ resposta inválida")
                alterado = True
                break
        if alterado:
            with open ("Cadastros.txt", "w", encoding = 'cp1252') as f:
                f.writelines(linhas)
                print("✅ Dados alterados com sucesso")
        else:
            print("❌ Usuário não encontrado")
        return usuario
    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")
        return usuario


def deletar_conta(usuario):
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
    try:
        with open ("Cadastros.txt", "r", encoding = 'cp1252') as f:
            linhas = f.readlines()
            for i in range(0, len(linhas), 4):
                try:
                    usuario_cadastrado = linhas[i].strip()
                    if usuario_cadastrado == usuario:
                        senha = linhas[i + 1].strip()
                        email = linhas[i + 2].strip()
                        print("======= Perfil de usuário =======", "\n")
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
    while True:
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
        email = input("Digite seu email, (domínios aceitos: @gmail.com, @hotmail.com, yahoo.com.br, outlook.com): ")
        if not email.endswith(("@gmail.com", "@hotmail.com", "yahoo.com.br", "outlook.com")):
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
    while True:
        print("======= Metacash =======", "\n")
        print("1 - Coleta de dados ")
        print("2 - Criar meta ")
        print("3 - Registrar gastos")
        print("4 - Ver perfil de usuário")
        print("5 - Sair do Metacash", "\n")
        resposta_menu = input("Digite o número correspondente ao que você deseja: ")
        if resposta_menu == "1":
            print("a")
            continue
        elif resposta_menu == "2":
            print("b")
            continue
        elif resposta_menu == "3":
            print("c")
            continue
        elif resposta_menu == "4":
            usuario = ver_perfil_usuario(usuario)
        elif resposta_menu == "5":
            print("Obrigado por usar o Metacash até logo")
            break

        
def central_do_site():
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
central_do_site()
