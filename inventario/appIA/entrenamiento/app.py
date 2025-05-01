from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
import torch

# Cargar el tokenizer
tokenizer = AutoTokenizer.from_pretrained("modelo_ajustad")

# Cargar el modelo base primero
base_model = AutoModelForCausalLM.from_pretrained("datificate/gpt2-small-spanish")

# Cargar la configuración LoRA y aplicarla al modelo base
config = PeftConfig.from_pretrained("modelo_ajustad")
modelo = PeftModel.from_pretrained(base_model, "modelo_ajustad")

# Asegurar que el modelo esté en modo evaluación
modelo.eval()

def responder(texto_usuario):
    # Formatear el texto igual que durante el entrenamiento
    prompt_formateado = f"### Pregunta: {texto_usuario.strip()}\n\n### Respuesta:"
    
    # Tokenizar con los parámetros adecuados
    entrada = tokenizer(prompt_formateado, return_tensors="pt")
    
    # Mover a GPU si está disponible
    if torch.cuda.is_available():
        modelo.cuda()
        entrada = {k: v.cuda() for k, v in entrada.items()}
    
    # Parámetros de generación optimizados
    generacion_params = {
        "max_length": 256,
        "temperature": 0.7,           # Temperatura más alta para diversidad
        "top_p": 0.92,                # Nucleus sampling
        "top_k": 50,                  # Top-k sampling
        "repetition_penalty": 1.5,    # Penalizar fuertemente las repeticiones
        "no_repeat_ngram_size": 3,    # Evitar repetir secuencias de 3+ tokens
        "do_sample": True,            # Usar sampling (no greedy)
        "pad_token_id": tokenizer.eos_token_id,
        "eos_token_id": tokenizer.eos_token_id,
        "num_return_sequences": 1     # Generar solo una respuesta
    }
    
    with torch.no_grad():  # No acumular gradientes durante la inferencia
        salida = modelo.generate(
            **entrada,
            **generacion_params
        )
    
    # Decodificar solo la respuesta (no la pregunta)
    respuesta_completa = tokenizer.decode(salida[0], skip_special_tokens=True)
    
    # Extraer solo la parte de respuesta
    if "### Respuesta:" in respuesta_completa:
        respuesta_final = respuesta_completa.split("### Respuesta:")[1].strip()
    else:
        respuesta_final = respuesta_completa.replace(prompt_formateado, "").strip()
    
    return respuesta_final

# Ejemplo de uso
if __name__ == "__main__":
    preguntas = [
        "problema de latencia",
        "mi computadora no enciende",
        "no tengo acceso a internet",
        "la pantalla muestra error azul"
    ]
    
    print("Probando el modelo con diferentes preguntas:\n")
    for pregunta in preguntas:
        print(f"Pregunta: {pregunta}")
        print(f"Respuesta: {responder(pregunta)}")
        print("-" * 50)