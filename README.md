# Relatório do Candidato


## Identificação do Candidato

- **Nome completo:** João Victor da Silva Costa Vasconcelos
- **GitHub:** [@JvVasconcel0s](https://github.com/JvVasconcel0s)

---

## Visão Geral da Solução

O projeto implementa um sistema Kanban de monitoramento de estoque por peso. Um ESP32 simulado lê um sensor HX711 ligado a uma caixa de até 5 kg. A leitura é convertida para gramas e o status aparece no monitor serial.

Com o estoque em nível regular, o sistema mostra o peso atual. Quando detecta 150 g ou menos, dispara um evento de reposição. Quando o peso volta para 5.000 g, confirma que a caixa foi abastecida. Se a leitura for 0 g depois que uma carga já foi identificada, o sistema gera um alerta de caixa ausente ou erro de calibração. O peso da caixa é alterado virtualmente no Wokwi e pelos cenários de teste.

---

## Arquitetura do Sistema Embarcado

O arquivo `main.py` inicia o sensor e executa um loop contínuo. A cada ciclo, ele solicita uma leitura ao HX711, converte o valor bruto para gramas e decide qual mensagem deve aparecer no monitor serial.

A leitura do HX711 foi separada no arquivo `hx711.py`. Esse arquivo faz a comunicação pelos pinos DT e SCK e devolve o valor bruto de 24 bits ao programa principal.

O sistema usa variáveis de controle para evitar mensagens repetidas e acompanhar o fluxo de reposição:

- `last_regular_weight` guarda o último peso regular informado.
- `replenishment_pending` registra que a reposição foi solicitada e aguarda a caixa voltar ao peso cheio.
- `has_seen_load` evita um alerta de caixa ausente antes da primeira leitura com carga.
- `anomaly_active` evita repetir o alerta enquanto a leitura permanece em zero.

A lógica prioriza leituras de peso zero, depois a confirmação de abastecimento, a solicitação de reposição e, por fim, o status regular. Ao final de cada ciclo, `time.sleep_ms(10)` cria uma pequena pausa sem bloquear o monitoramento.

---

## Componentes Utilizados na Simulação

- **ESP32 DevKit C V4:** é o microcontrolador que executa o programa em MicroPython e controla a leitura do sensor.
- **HX711 de 5 kg:** é o módulo usado para simular a medição de peso da caixa.
- **Monitor serial do Wokwi:** mostra as mensagens de status, reposição, abastecimento e alerta.

As conexões do circuito são:

- `ESP32 3V3` → `HX711 VCC`
- `ESP32 GND` → `HX711 GND`
- `ESP32 GPIO 19` → `HX711 DT`
- `ESP32 GPIO 21` → `HX711 SCK`

---

## Decisões Técnicas Relevantes

- Separei a leitura do sensor em `hx711.py` e deixei a regra de negócio em `main.py`. Isso torna o código mais organizado e facilita ajustes futuros.

- Usei um driver próprio para o HX711. Ele lê os 24 bits enviados pelo sensor pelos pinos DT e SCK.

- Defini constantes para os valores importantes do projeto, como capacidade total de 5.000 g, limite de reposição em 150 g e valor bruto de referência do sensor.

- A conversão de leitura bruta para gramas usa aritmética inteira. Assim, o programa evita depender de números decimais no microcontrolador.

- Usei variáveis de estado para evitar mensagens repetidas no monitor serial e para garantir a sequência correta entre reposição e abastecimento.

- O loop tem uma pausa de 10 ms. Isso evita uso desnecessário do processador sem deixar a leitura do sensor lenta.

- Mantive as mensagens do monitor serial exatamente como solicitadas nos cenários de teste.
---

## Resultados Obtidos

O circuito com ESP32 e HX711 foi configurado no Wokwi. O arquivo `fs.bin` foi gerado com sucesso no ambiente Docker local e também na etapa de build do GitHub Actions. A esteira de CI identificou corretamente o cenário de monitoramento de peso.

---

## Comentários Adicionais (Opcional)

Durante o desafio, configurei o ambiente com WSL, Docker, VS Code, GitHub Actions e Wokwi.

O principal aprendizado foi entender o fluxo completo de um projeto IoT, desde a ligação do sensor e o código embarcado até a validação automatizada na nuvem.

---