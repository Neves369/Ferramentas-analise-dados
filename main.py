import os
from modules import  animationLoading,  analiseQuantitativa
import inquirer


def coletar_colunas():
    colunas = []
    continuar = True

    while continuar:
        # 1. Pergunta o nome da coluna
        perguntas_nome = [
            inquirer.Text(
                'coluna',
                message=f"Informe os o nomes da colunas a serem analisadas",
                validate=lambda _, x: len(x) > 0  # No inquirer, o validate recebe (respostas_atuais, valor)
            )
        ]
        
        res_nome = inquirer.prompt(perguntas_nome)
        
        # Caso o usuário interrompa com Ctrl+C
        if not res_nome: break 
        
        colunas.append(res_nome['coluna'])

        # 2. Pergunta se deseja continuar
        perguntas_proxima = [
            inquirer.Confirm(
                'proxima',
                message="Deseja adicionar outra coluna?",
                default=True
            )
        ]
        
        res_proxima = inquirer.prompt(perguntas_proxima)
        
        if not res_proxima: break
        
        continuar = res_proxima['proxima']

    return colunas

def main():

  os.system('cls')

  print("""
     ____________________________________________________________________
    |--------------------------------------------------------------------|
    |      ██╗    ███████████╗     ██████╗██████╗███╗   ██████████╗      |
    |      ██║    ████╔════██║    ██╔════██╔═══██████╗ ██████╔════╝      |
    |      ██║ █╗ ███████╗ ██║    ██║    ██║   ████╔████╔███████╗        |
    |      ██║███╗████╔══╝ ██║    ██║    ██║   ████║╚██╔╝████╔══╝        |
    |      ╚███╔███╔██████████████╚██████╚██████╔██║ ╚═╝ █████████╗      |
    |       ╚══╝╚══╝╚══════╚══════╝╚═════╝╚═════╝╚═╝     ╚═╚══════╝      |
    |                                                                    | 
    |                                                                    |
    |                                                                    |
    |                              _.-~~.)                               |
    |        _.--~~~~~---....__  .' . .,'                                |
    |      ,'. . . . . . . . . .~- ._ (                                  |
    |     ( .. (@) . . . . . . . . . .~-._                               | 
    |  .~__.-~    ~`. . . . . . . . . . . -.                             |
    |  `----..._      ~-=~~-. . . . . . . . ~-.                          |   
    |            ~-._   `-._ ~=_~~--. . . . . .~.                        |
    |             | .~-.._  ~--._-.    ~-. . . . ~-.                     |
    |              \ .(   ~~--.._~'       `. . . . .~-.                , |
    |               `._\         ~~--.._    `. . . . . ~-.          ,'/  |
    |                  _                 ~~--.`_. . . . . ~-_     ,-'    |
    |            ` ._           ~                ~--. . . . .~=.-'. /.   |
    |      - . -~            -. _ . - ~ - _   - ~     ~--..__~ _,. /     |
    |             . __ ..                   ~-               ~~_. (      |
    |                       `-       ..  - .                     ~-      |
    |                                                          @neves369 |
    |-------------------------Dulfin Analytics---------------------------|
    |--Escolha um arquivo para ser analisado                             |
    |--Selecione o tipo de análise                                       |
    |--Informe as colunas a serem analisadas                             |
    |                                                                    |
    |   obs.: Caso escolha análise qualitativa,                          |
    |         informe a coluna de identificação.                         |
    |--------------------------------------------------------------------|
    |____________________________________________________________________| 
  """) 



  # listar arquivos da pasta data
  caminhos = [os.path.join("data", nome) for nome in os.listdir("data")]
  arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
  csv = [arq[5:] for arq in arquivos if arq.lower().endswith(".csv")]


  questions = [
    inquirer.List(
      'filename',
      message="Selecione o arquivo: ",
      choices=csv,
    ),

 
  inquirer.List(
     'options',
      message="Selecione a tipo de análise: ",
      choices=["Análise Completa", "Análise Quantitativa", "Análise Qualitativa"],
    ),
   
  ]

  answers = inquirer.prompt(questions)
  colunas = coletar_colunas() 
  filename =  answers["filename"]
  options =  answers["options"]

  print(f"Colunas selecionadas: {', '.join(colunas)}")
  
  if (os.path.exists('output') == False):
    try:
      os.mkdir('output')
    except:
      print("Não foi possível criar diretório") 

  match options:
    case "Análise Completa":  
      print("Gerando arquivos de visualização...")
      
    case "Análise Quantitativa":
      resultado = analiseQuantitativa.analiseQuantitiva(filename, colunas)
      print(resultado)
  
  
    case "Análise Qualitativa":
      print("Gerando arquivos de visualização...")



  animationLoading.load_animation()

  print("""
   ___________________________________________________________________
  |-------------------------------------------------------------------|
  |                                                                   |
  |   ██████╗██████╗███╗   █████████╗██╗    ██████████████████████╗   |
  |  ██╔════██╔═══██████╗ ██████╔══████║    ██╔════╚══██╔══██╔════╝   |
  |  ██║    ██║   ████╔████╔████████╔██║    █████╗    ██║  █████╗     |
  |  ██║    ██║   ████║╚██╔╝████╔═══╝██║    ██╔══╝    ██║  ██╔══╝     |
  |  ╚██████╚██████╔██║ ╚═╝ ████║    ██████████████╗  ██║  ███████╗   |
  |  ╚═════╝╚═════╝╚═╝     ╚═╚═╝    ╚══════╚══════╝  ╚═╝  ╚══════╝    |
  |                                                                   |
  |  ---------------------GERADOS ARQUIVOS--------------------------  |
  |                  --confira a pasta output--                       |
  |                                                                   |
  |                                         __                        |
  |                                     _.-~  )                       |
  |                          _..--~~~~,'   ,-/     _                  |
  |                       .-'. . . .'   ,-','    ,' )                 |
  |                     ,'. . . _   ,--~,-'__..-'  ,'                 |
  |                   ,'. . .  (@)' ---~~~~      ,'                   |
  |                  /. . . . '~~             ,-'                     |
  |                 /. . . . .             ,-'                        |              
  |                ; . . . .  - .        ,'                           |
  |               : . . . .       _     /                             |
  |              . . . . .          `-.:                              |
  |             . . . ./  - .          )                              |
  |            .  . . |  _____..---.._/ ____@neves369_                |
  |      ~---~~~~----~~~~             ~~                              |
  | ================================================================= |
  | ================================================================= |        
  |___________________________________________________________________|
  """) 

  confirm = {
    inquirer.Confirm(
      'confirmed',
      message="Deseja sair?" ,
      default=True),
  }
  confirmation = inquirer.prompt(confirm)

  if(confirmation["confirmed"]):
    quit()


if __name__ == '__main__':
  while True:
    main()