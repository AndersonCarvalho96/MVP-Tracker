# MVP Tracker

O **MVP Tracker** é um aplicativo de desktop desenvolvido com Python e Tkinter para rastrear MVPs em um jogo. Ele permite adicionar, editar e excluir entradas de MVP, com funcionalidades para calcular o tempo de respawn com base na hora da morte.

## Funcionalidades

- Adicionar novos MVPs com detalhes como mapa, tempo de respawn, hora da morte e coordenadas.
- Editar e excluir MVPs existentes.
- Visualizar MVPs em uma tabela com a capacidade de ordenar por colunas.
- Calcula automaticamente o horário em que o MVP deve reaparecer com base na hora da morte e no tempo de respawn.

## Requisitos

- Python 3.x
- Biblioteca `Pillow` para manipulação de imagens.
- Biblioteca `sqlite3` para gerenciamento de banco de dados SQLite.
- Biblioteca `tkinter` para a interface gráfica.

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/AndersonCarvalho96/MVP-Tracker.git
   ```

2. Navegue para o diretório do projeto:
   ```bash
   cd mvp-tracker
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install pillow
   ```

4. Certifique-se de que você tem a imagem de fundo `background-MVP.jpg` no diretório do projeto.

## Uso

1. Execute o aplicativo:
   ```bash
   python app.py
   ```

2. A interface gráfica será aberta com os seguintes componentes:
   - **Campos de Entrada**: Para adicionar ou editar MVPs.
   - **Botões**: Para adicionar, editar e excluir MVPs.
   - **Tabela (Treeview)**: Para exibir e gerenciar os MVPs existentes.

3. Preencha os campos com as informações do MVP e clique em "Adicionar" para adicionar um novo MVP. Use os botões "Editar" e "Excluir" para modificar ou remover MVPs existentes.

## Estrutura do Banco de Dados

O aplicativo usa um banco de dados SQLite para armazenar os dados dos MVPs. A tabela `mvps` possui os seguintes campos:

- `id`: Identificador único do MVP.
- `mvp`: Nome do MVP.
- `mapa`: Mapa onde o MVP aparece.
- `tempo_respawn`: Tempo de respawn em minutos.
- `hora_morte`: Hora da morte do MVP (formato HH:MM).
- `coordenadas`: Coordenadas do túmulo do MVP.
- `nasce_as`: Hora em que o MVP deve reaparecer (calculado automaticamente).

## Credenciais de Conteúdo

A imagem de fundo e ícone usada neste aplicativo foi gerada com a ajuda de IA.

- **Gerado com IA**
- **Data:** 28 de agosto de 2024 às 3:47 PM


## Contribuição

Contribuições são bem-vindas! Se você encontrar bugs ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE.txt para mais detalhes.
