# Mileage Tracker

## Descrição
O Mileage Tracker é um aplicativo de desktop simples projetado para indivíduos e empresas rastrearem a quilometragem percorrida. Seu objetivo principal é facilitar a prestação de contas (expense reporting) e o reembolso de despesas de viagem.
A ferramenta automatiza o cálculo da distância e permite a exportação de todos os dados para um formato de tabela (.csv).

## Funcionalidades
- Registro de Viagens: Inserção de dados básicos da viagem (endereços, hodômetro, pedágios, estacionamento).
- Cálculo Automático de KM: Utiliza a Google Maps API para calcular a distância entre os endereços.
- Cálculo de Despesas: Consolida o custo total baseado na quilometragem, pedágios e taxas de estacionamento.
- Exportação de Dados: Gera e exporta os dados e cálculos da viagem para um arquivo .csv.

## Executando a aplicação

1. Faça clone do repositório ou baixe o ZIP.
2. No diretório principal do projeto, crie a imagem Docker:
```
docker build -t mileage_app .
```
3. Crie a pasta de dados (host) para persistência do CSV:
```
mkdir -p data
```

4. Execução por sistema operacional

- Linux (X11 nativo)
  - Permita acesso ao X para o container e rode:
  ```
  xhost +local:root
  docker run -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$(pwd)/data":/aplication/data \
    -it --rm mileage_app
  xhost -local:root
  ```

- macOS (XQuartz)
  - Instale e abra o XQuartz. Em Preferences → Security, habilite "Allow connections from network clients". Reinicie o XQuartz.
  - No terminal:
  ```
  xhost + 127.0.0.1
  docker run -e DISPLAY=host.docker.internal:0 \
    -v "$(pwd)/data":/aplication/data \
    -it --rm mileage_app
  xhost - 127.0.0.1
  ```
  - Observação: algumas configurações podem exigir ajustes no DISPLAY (por exemplo host.docker.internal:0.0).

- Windows (VcXsrv / Xming / Docker Desktop)
  - Inicie VcXsrv (ou Xming) com "Disable access control" para testes locais.
  - Abra PowerShell/CMD no diretório do projeto:
  ```
  docker run -e DISPLAY=host.docker.internal:0 \
    -v "%cd%/data":/aplication/data \
    -it --rm mileage_app
  ```
  - Se usar WSL2 + X server no Windows, ajuste DISPLAY conforme seu setup (ex.: export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0).

5. Execução local sem Docker (para teste rápido)
```
python3 app/app.py
```

## Testes
Os testes da aplicação encontram-se no diretório `test`. Execute:
```
python3 -m unittest discover -s test
```

## Observações
- A aplicação grava em `/aplication/data/trips.csv` dentro do container; ao mapear `./data` do host para `/aplication/data`, os registros ficam no host.
- Uso de X11 em contêiner envolve riscos de segurança; habilite acesso apenas para testes e revogue com `xhost -` após o uso.
