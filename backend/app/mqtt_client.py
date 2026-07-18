import paho.mqtt.client as mqtt

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC_TESTE = "home/p2s/power"

def on_connect(client, userdata, flags, rc, properties=None):
    """!
    @brief Callback executado quando o backend se liga com sucesso ao broker

    @param client: Instância do cliente MQTT
    @param userdata: Dados do utilizador (não utilizado neste caso)
    @param flags: Flags de conexão
    @param rc: Código de retorno
    @param properties: Propriedades da conexão (não utilizado neste caso)
    """
    if rc == 0:
        print("✅ Backend ligado com sucesso ao Broker MQTT!")
        client.subscribe(MQTT_TOPIC_TESTE) # Subscreve o tópico do ESP32/P2S para testar
        print(f"📡 Subscrito no tópico: {MQTT_TOPIC_TESTE}")

    else:
        print(f"❌ Falha ao ligar ao MQTT. Código de erro: {rc}")

def on_message(client, userdata, msg):
    """!
    @brief Callback executado sempre que uma nova mensagem chega no tópico subscrito

    @param client: Instância do cliente MQTT
    @param userdata: Dados do utilizador (não utilizado neste caso)
    @param msg: Mensagem recebida, contendo tópico e payload
    """
    try:
        payload = msg.payload.decode("utf-8")
        print(f"📥 [MQTT MENSAGEM] Tópico: {msg.topic} | Payload: {payload}")

    except Exception as e:
        print(f"⚠️ Erro ao processar mensagem MQTT: {e}")

def start_mqtt():
    """!
    @brief Inicializa o cliente MQTT numa thread separada
    """
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2) # Instancia o cliente usando a API estável mais recente
    
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start() # Cria thread em background para gerir as mensagens sem bloquear a API

    except Exception as e:
        print(f"❌ Não foi possível ligar ao broker MQTT: {e}")