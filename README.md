# Song Weather Api 
API para buscar músicas a partir da temperatura de uma cidade, seguindo as seguintes regras:

Busca a temperatura em graus celsius de uma cidade e seguindo as seguintes regras irá listar 10 músicas dos genêros musicais: POP, ROCK e CLÁSSICO, dependendo da sua temperatura:

- Se acima de 25C - Retorna músicas de POP
- Se entre 10C e 25C - Retorna músicas sugeridas de ROCK
- Se abaixo de 10C - Retorna músicas clássicas

## Tecnologias Utilizadas

- Linguagem: Python 3.12
- Bibliotecas:
    - httpx - Auxiliar com requisições HTTP para integrações
    - marshmallow - Auxilia na validação de objetos
    - flask - Framework para lidar com as requisições HTTP
    - flask-caching - Auxilia no armazenamento de informações que podem ser cacheadas para ser utilizadas entre as requisições
- Bibliotecas de desenvolvimento
    - pytest - Auxilia no desenvolvimento de testes unitários / integração
    - pytest-httpx - Auxilia criando mocks das requisições de integrações realizadas
    - pytest-dotenv - Auxilia o carregamento de váriaveis de ambiente durante os testes

### Padrões utilizado

Para manter o código manutenível, de facil entendimento e desenvolvimento, implementei as ideias passadas através do livro Clean Architecture, aplicando conceitos como S.O.L.I.D. e T.D.D, seguindo essas ideias estruturei o projeto da seguinte forma

- application - Conterá todas a lógica de camada da aplicação, apresentação e roteamento.
- configs - Conterá arquivos de configuração do flask
- domain - Conterá toda a lógica de negócio, sendo ela isenta de toda dependência técnica externa, inclusive os testes unitários desse dominio.
- extensions - Como o flask é baseado em extenção mapeei essa pasta para configurar extensões que serão utilizadas dentro da aplicação como o flask-caching
- infra - Toda dependencia externa como os clients utilizados para integrações em outras apis
- tests - Testes de integração

## Requisitos

- Python >= 3.12
- Poetry
- Chave de acesso a Open Weather ([Documentação](https://openweathermap.org/api))
- Chave de acesso ao Spotify ([Documentação](https://developer.spotify.com/))

## Váriaveis de ambientes necessárias para executar a API

- WEATHER_API_URL - URL de acesso a API da Open Weather
- WEATHER_API_SECRET - Secret key para acesso a API da Open Weather
- SPOTIFY_AUTH_API_URL - URL de acesso a api de autenticação do Spotify
- SPOTIFY_API_URL - URL de acesso a api do spotify
- SPOTIFY_API_SECRET - Secret key para acesso a API do Spotify
- SPOTIFY_API_ID - ID Client da API do Spotify

## Executando manualmente

### Executando via docker

1. Vá para o diretório root do projeto
2. Gere a imagem da aplicação 

```bash
docker build . -t song-weather-api
```

3. Execute o container

```bash
docker run -p 5000:5000 --name song-weather-api --env-file .env song-weather-api
```

Obs: É necessário que você tenha informado as váriveis de ambiente, gerando o arquivo .env ou passando manualmente as váriaveis ao executar o container.

### Executando manualmente


1. Clone o projeto (https://github.com/torresgustavo/song-wheater-api.git)
2. Abra o terminal ou prompt de comando.
3. Execute o seguinte comando para instalar o Poetry com pip (caso não tenha pip siga [este](https://pip.pypa.io/en/stable/installation/) passo a passo):

```bash
pip install poetry
```

4. Instale as dependências do projeto com

```bash
poetry install
```

5. Execute a aplicação:
```bash
poetry run flask run --host=0.0.0.0
```

6. A aplicação estará disponível na porta 5000

## Acessando a aplicação

### Endpoints

Endpoint /v1/music
## Endpoint /v1/music

### Descrição
Este endpoint é responsável por buscar músicas com base na temperatura de uma cidade.

### Parâmetros
- **city**: Cidade para a qual deseja-se buscar músicas. Deve ser passado como parâmetro na URL.

### Retornos Possíveis
- **Status 200 OK**
  - **Descrição**: Retorna a lista de músicas com base na temperatura da cidade.
  - **Corpo da Resposta**:
    ```json
    {
        "weather": {
            "temperature": 25.0,
            "city": "São Paulo",
            "country": "BR"
        },
        "music_list": [
            {
                "name": "Música 1",
                "artist": "Artista 1"
            },
            {
                "name": "Música 2",
                "artist": "Artista 2"
            }
        ]
    }
    ```

- **Status 400 Bad Request**
  - **Descrição**: Erro de validação nos parâmetros da requisição.
  - **Corpo da Resposta**:
    ```json
    {
        "message": "Payload schema validation error",
        "error_code": "VALIDATION_ERROR",
        "detail": {
            "errors": ["Descrição do erro de validação"]
        }
    }
    ```

- **Status 401 Unauthorized**
  - **Descrição**: Requisição não autenticada.
  - **Corpo da Resposta**:
    ```json
    {
        "message": "Unauthorized on [RESOURCE NAME]",
        "error_code": "UNAUTHORIZED"
    }
    ```

- **Status 403 Forbidden**
  - **Descrição**: Acesso não autorizado.
  - **Corpo da Resposta**:
    ```json
    {
        "message": "Forbidden",
        "error_code": "FORBIDDEN_ERROR"
    }
    ```

- **Status 429 Too Many Requests**
  - **Descrição**: Limite de requisições excedido.
  - **Corpo da Resposta**:
    ```json
    {
        "message": "Too Many Requests",
        "error_code": "TOO_MANY_REQUESTS_ERROR"
    }
    ```

- **Status 500 Internal Server Error**
  - **Descrição**: Erro inesperado no servidor.
  - **Corpo da Resposta**:
    ```json
    {
        "message": "Internal Server Error",
        "error_code": "UNEXPECTED_CLIENT_ERROR"
    }
    ```

### Exemplo de Requisição
GET /v1/music?city=São Paulo

### Exemplo de Resposta
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "weather": {
        "temperature": 25.0,
        "city": "São Paulo",
        "country": "BR"
    },
    "music_list": [
        {
            "name": "Música 1",
            "artist": "Artista 1"
        },
        {
            "name": "Música 2",
            "artist": "Artista 2"
        }
    ]
}
```

## Testes

Para executar os testes vá para a pasta raiz do projeto e execute
```bash
pytest .
```

## Outras informações

Não identifiquei problemas/facilidades em utilizar outra linguagem, por isso decidi utilizar python + flask pois tenho vivência com essas tecnologias.