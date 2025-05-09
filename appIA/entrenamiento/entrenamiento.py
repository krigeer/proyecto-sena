from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
import torch

# Cargar datos
dataset = load_dataset("json", data_files="datasets.json", split="train")

# Modelo base y tokenizer
modelo = "datificate/gpt2-small-spanish"
tokenizer = AutoTokenizer.from_pretrained(modelo)
tokenizer.pad_token = tokenizer.eos_token  # Configurar pad_token adecuadamente
modelo_preentrenado = AutoModelForCausalLM.from_pretrained(modelo)

# Preparar datos con mejor estructura
def preparar_ejemplo(ejemplo):
    # Formato claro con separadores distintos
    texto = f"### Pregunta: {ejemplo['prompt'].strip()}\n\n### Respuesta: {ejemplo['completion'].strip()}\n\n"
    resultado = tokenizer(texto, truncation=True, padding="max_length", max_length=256)
    
    # Configurar labels igual que input_ids para causal LM
    resultado["labels"] = resultado["input_ids"].copy()
    return resultado

dataset_tokenizado = dataset.map(preparar_ejemplo, remove_columns=dataset.column_names)

# LoRA con configuración optimizada
config_lora = LoraConfig(
    r=32,                              # Aumentado a 32 para mejor capacidad
    lora_alpha=64,                     # Típicamente 2*r
    target_modules=["c_attn", "c_proj"],
    lora_dropout=0.1,                  # Ligeramente aumentado
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

modelo_lora = get_peft_model(modelo_preentrenado, config_lora)
modelo_lora.print_trainable_parameters()  # Ver cantidad de parámetros ajustables

# Clase personalizada para data collator
class DataCollatorForCausalLM:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        
    def __call__(self, examples):
        batch = self.tokenizer.pad(
            examples,
            padding=True,
            return_tensors="pt"
        )
        
        # Asegúrate que los labels estén bien configurados
        batch["labels"] = batch["input_ids"].clone()
        
        # Opcionalmente: mascara los tokens de padding en labels para no incluirlos en loss
        if self.tokenizer.pad_token_id is not None:
            batch["labels"][batch["labels"] == self.tokenizer.pad_token_id] = -100
            
        return batch

# Entrenamiento con parámetros mejorados
args = TrainingArguments(
    output_dir="lora0.0",
    evaluation_strategy="steps",       # Evaluar durante entrenamiento
    eval_steps=200,                    # Evaluar cada 200 pasos
    per_device_train_batch_size=4,     # Aumentado a 4 (o más si tu GPU lo permite)
    gradient_accumulation_steps=4,     # Acumular gradientes para simular batch más grande
    num_train_epochs=2,
    save_strategy="steps",
    save_steps=200,
    learning_rate=3e-4,                # Ligeramente aumentado
    warmup_steps=100,                  # Agregar warmup
    logging_steps=10,
    save_total_limit=3,
    fp16=torch.cuda.is_available(),
    weight_decay=0.01,                 # Agregar regularización
    lr_scheduler_type="cosine",        # Scheduler coseno para mejor convergencia
    load_best_model_at_end=True
)

# Dividir dataset para evaluación
dataset_split = dataset_tokenizado.train_test_split(test_size=0.1)
train_dataset = dataset_split["train"]
eval_dataset = dataset_split["test"]

collator = DataCollatorForCausalLM(tokenizer)

trainer = Trainer(
    model=modelo_lora,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=collator,
)

trainer.train()

# Guardar modelo con prefijo adecuado
modelo_lora.save_pretrained("lora0.0")
tokenizer.save_pretrained("lora0.0")