class Usuario:
    
    def __init__(self, nome: str, sobrenome: str, email: str):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email

    @property
    def novo_email(self):
        return f'{self.nome}.{self.sobrenome}@pythonEmail.com'

    @property
    def nome_completo(self):
        return f'{self.nome} {self.sobrenome}'
    
    @nome_completo.setter
    def nome_completo(self, nome_completo):
        nome, sobrenome = nome_completo.split(' ')
        self.nome = nome
        self.sobrenome = sobrenome
        
    @nome_completo.deleter
    def deletar(self):
        print('Nome Deletado!')
        self.nome = None
        self.sobrenome = None
    
    def __setattr__(self, key, value):
        self.__dict__[key] = value

        return self.__dict__.items
    
    def register(self):
        registers = namedtuple(f"{type(self).__name__}", [
            'nome',
            'sobrenome',
            'email',
        ])
        user_register = registers(nome=self.nome, 
                                sobrenome=self.sobrenome, 
                                email=self.novo_email)
        return user_register
    
    def __str__(self):
        return f"Informações de Usuário:\nNome: {self.nome}\nSobrenome: {self.sobrenome}\nEmail: {self.email}"
    
    def __lt__(self, other):
        if self.sobrenome != other.sobrenome:
            return (self.sobrenome < other.sobrenome)
        else:
            return (self.nome < other.nome)
    

class Desenvolvedor(Usuario):

    horas_totais = 0
    total_pago = 0

    def __init__(self, nome, sobrenome, email, level, salario_hora):
        super().__init__(nome, sobrenome, email)
        self.level = level
        self.salario_hora = salario_hora
    
    def __call__(self, horas_trabalho: int):
        self.horas_totais += horas_trabalho
        self.total_pago += horas_trabalho * self.salario_hora
        if "Pro".lower() in self.level:
            self.total_pago = self.total_pago * 3
        if "Avançado".lower() in self.level:
            self.total_pago = self.total_pago * 2

        return f"Salário médio: ${self.total_pago}"
    
    @classmethod
    def set_language(cls, linguagem):
        return cls({"Linguagem": linguagem})

def write_file(file_name, content):
    file_name = file_name.strip(" ")
    list_dir = os.listdir()
    content = str(content)
    if str(file_name) in list_dir:
        with open(file_name, "a") as f:
            content = content.strip('(').strip(')') + ' ' + '\n'
            f.write(content)
    else:
        with open(file_name, 'w') as f:
            content = content.strip(')')
            content = content + ' ' + '\n'
            f.write(content)

def register_dataset(*user_obj):
    my_list = []
    try:
        for user in user_obj:
            new_register = user.register()
            my_list.append(new_register)
        database = tuple(my_list)
        write_file("users", str(database))
        set_logger().info("Cadastro realizado com sucesso.")
        return database
    except Exception as ex:
        set_logger().error(ex)    
    

def convert_to_dict(dataset):
    response = tuple(map(
        lambda x: {'nome': x.nome, 'sobrenome': x.sobrenome, 'email': x.email},
        dataset
    ))
    return response

def set_logger():
    logger = logging.getLogger()
    logger = logging.getLogger("Register")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
                                datefmt='%Y-%m-%d \n%H:%M:%S')
    file_handler = logging.FileHandler('response.log')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger    

def args():
    try:
        args = sys.argv
        if len(args) > 1:
            args.remove(args[0])
            for arg in args:
                yield arg
    except Exception as ex:
        set_logger().error(ex)


def main():
    results = [str(user_info).strip(' ') for user_info in args()]
    user = Usuario(results[0], results[1], results[2])
    register_dataset(user)
    exit = str(input("Press Enter to exit. "))


if __name__=="__main__":
    from collections import namedtuple
    import logging
    import sys, os
    main()