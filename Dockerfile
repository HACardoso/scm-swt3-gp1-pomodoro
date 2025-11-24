FROM python:3.14
WORKDIR /aplication

# Caso requirements sejam necessarios ao projeto
# Adicionamos o requerimento ao arquivo requirements.txt
COPY ./ /aplication

RUN pip install --no-cache-dir -r requirements.txt

# Como estamos trabalhando com tkinter e interessante
# confirmarmos a instalacao das dependecias da biblioteca
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*


EXPOSE 8080

# Definimos o comando de execucao
CMD ["python3", "app/app.py"]