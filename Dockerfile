# Usa a imagem Python slim como base
FROM python:3.12-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de definição de dependências (pyproject.toml) e o lock file (poetry.lock) para o container
COPY pyproject.toml poetry.lock /app/

# Instala o Poetry
RUN pip install poetry

# Instala as dependências do projeto usando o Poetry
RUN poetry install

# Copia o código da aplicação para o container
COPY . /app

# Expõe a porta 5000 (porta padrão do Flask)
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["poetry", "run", "gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:create_app()"]