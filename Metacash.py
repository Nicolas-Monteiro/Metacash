import os

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
                            print("✅ Seu login foi realizado com sucesso!")
                            return
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
    central_do_site()


def central_do_site():
    while True:
        print("======= Bem vindo ao Metacash =======")
        print("O que você deseja?")
        print("1 - Login")
        print("2 - Cadastro")
        print("3 - Sair")
        resposta = input("Digite o número correspondente ao que você deseja: ")
        if resposta == "1":
            login()
        elif resposta == "2":
            cadastro()
        elif resposta == "3":
            print("Até a proxima")
            break
        else:
            print("❌ Resposta inválida", "\n")
            continue
central_do_site()

def menu_metacash ()
    while True:
        print("======= Metacash =======")
        print("1 - ")
        print("2 - ")
