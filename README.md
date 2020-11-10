# MBR


**Esquema de desenvolvimento:**

1. Crie, ou atribua uma issue para si
2. Atualize a master `(git pull/git fetch)`
3. Crie uma branch `(git checkout -b nome_da_branch)`. O nome da branch deve se iniciar com o número da issue, seguido de um título simples, Ex: ***1-teste, 2-exemplo***.
4. Concluída a issue, vá para a master `(git checkout master)`, atualize a master `(git pull/git fetch)`, depois volte para a branch cuja issue foi concluída e faça um merge com a master `(git merge master)`e corrija os conflitos encontrados 
6. Rode o códio uma última vez para conferir se tudo funciona corretamente antes de fazer um Pull Request.
5. Abra um Pull Request na sua Branch, e peça revisão de código dos outros colaboradores.


**Padrão de desenvolvimento:**

- constantes:         Sempre ***MAIÚSCULAS***
- variáveis:          Sempre ***minusculas_e_com_underscore***
- nomes de classes:   Maiuscula no inicio, seguida de minúsculas e ***SemUnderscore***
    

**Sugestões para configurar o ambiente:**

Primeiro instale o pyenv, para obter um ambiente python limpo.

O código a seguir executa o instalador automático do pyenv.

    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

Em seguida, instale o python versão 3.8.4 utilizando o pacote pyenv, da seguinte forma:

    pyenv install 3.8.4

Faça um clone do repositório:

    https://github.com/rodrigo-xavier/MBR.git

Ative a versão do python 3.8.4 no seu shell atual para rodar os comandos posteriores (importante dizer que se você mudar de janela do shell, terá que fazer isto novamente, mas não será necessário após ter um virtualenv criado):

    pyenv shell 3.8.4

Agora crie uma virtualenv, ative-a, faça o upgrade do pip e instale os requisitos do projeto:

    python -m venv virtualenv
    source virtualenv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
