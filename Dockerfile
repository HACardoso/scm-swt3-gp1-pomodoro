FROM python:3.14-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /aplication

# Copia todo o projeto para /aplication
COPY ./ /aplication

# Garante que exista um requirements.txt (caso não tenha, cria vazio)
RUN [ -f requirements.txt ] || touch requirements.txt

# Instala dependências Python (se houver)
RUN pip install --no-cache-dir -r requirements.txt

# Instala dependências do sistema para tkinter / X11
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3-tk \
      tk \
      tcl \
      libx11-6 \
      x11-utils \
      xauth && \
    rm -rf /var/lib/apt/lists/*

# Cria diretório de dados (será montado por volume no host)
RUN mkdir -p /aplication/data

EXPOSE 8080

CMD ["python3", "app/app.py"]