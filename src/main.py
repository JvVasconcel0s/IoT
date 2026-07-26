from hx711 import HX711
import time


DATA_PIN = 19
CLOCK_PIN = 21

FULL_WEIGHT_G = 5000
LOW_STOCK_G = 150
RAW_AT_FULL_WEIGHT = 2100


def raw_to_grams(raw_value):
    if raw_value <= 0:
        return 0

    return (
        raw_value * FULL_WEIGHT_G + RAW_AT_FULL_WEIGHT // 2
    ) // RAW_AT_FULL_WEIGHT


sensor = HX711(DATA_PIN, CLOCK_PIN)

last_regular_weight = None
replenishment_pending = False
has_seen_load = False
anomaly_active = False

print("Sistema Kanban Inicializado")

while True:
    raw_value = sensor.read_raw()

    if raw_value is not None:
        weight_g = raw_to_grams(raw_value)

        if weight_g > 0:
            has_seen_load = True

        if has_seen_load:
            if weight_g == 0:
                replenishment_pending = False

                if not anomaly_active:
                    print(
                        "ALERTA: Caixa ausente ou erro de calibração no sensor HX711!"
                    )

                anomaly_active = True

            else:
                anomaly_active = False

                if replenishment_pending:
                    if weight_g >= FULL_WEIGHT_G:
                        print("Abastecimento concluído. Caixa cheia.")
                        replenishment_pending = False
                        last_regular_weight = weight_g

                elif weight_g <= LOW_STOCK_G:
                    print("Evento de reposição disparado! Caixa vazia detectada.")
                    replenishment_pending = True
                    last_regular_weight = None

                elif weight_g != last_regular_weight:
                    print("Status: Estoque Regular ({}g)".format(weight_g))
                    last_regular_weight = weight_g

    time.sleep_ms(10)