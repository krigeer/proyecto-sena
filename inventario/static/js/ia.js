   // Funcionalidad del menú móvil
   const mobileMenuBtn = document.getElementById('mobileMenuBtn');
   const sidebar = document.getElementById('sidebar');

   mobileMenuBtn.addEventListener('click', () => {
       sidebar.classList.toggle('active');
   });

   // Auto-resize del textarea
   const messageInput = document.getElementById('messageInput');
   
   messageInput.addEventListener('input', function() {
       this.style.height = 'auto';
       this.style.height = Math.min(this.scrollHeight, 150) + 'px';
   });

   // Funcionalidad de envío de mensajes
   const sendBtn = document.getElementById('sendBtn');
   const chatMessages = document.getElementById('chatMessages');
   const typingIndicator = document.getElementById('typingIndicator');

   sendBtn.addEventListener('click', sendMessage);
   messageInput.addEventListener('keydown', (e) => {
       if (e.key === 'Enter' && !e.shiftKey) {
           e.preventDefault();
           sendMessage();
       }
   });

   async function sendMessage() {
       const message = messageInput.value.trim();
       if (!message) return;

       // Añadir mensaje del usuario
       addMessage(message, 'user');
       messageInput.value = '';
       messageInput.style.height = 'auto';

       // Mostrar indicador de escritura
       typingIndicator.style.display = 'flex';
       chatMessages.scrollTop = chatMessages.scrollHeight;

       try {
           // Enviar mensaje al backend de Django
           const response = await sendMessageToBackend(message);
           
           // Ocultar indicador de escritura
           typingIndicator.style.display = 'none';
           
           if (response && response.reply) {
               // Mostrar la respuesta del backend
               addMessage(response.reply, 'ai');
           } else {
               // Mostrar mensaje de error si no hay respuesta válida
               addMessage("Lo siento, ha ocurrido un error al procesar tu mensaje.", 'ai');
           }
       } catch (error) {
           console.error('Error en el proceso de comunicación:', error);
           typingIndicator.style.display = 'none';
           addMessage("Lo siento, no pude conectarme al servidor.", 'ai');
       }
   }

   function addMessage(text, type) {
       const now = new Date();
       const time = now.getHours().toString().padStart(2, '0') + ':' + 
                    now.getMinutes().toString().padStart(2, '0');
       
       const messageDiv = document.createElement('div');
       messageDiv.classList.add('message', type);
       
       const avatar = type === 'user' ? '{{usuario}}' : 'L'; 
       
       messageDiv.innerHTML = `
           <div class="message-avatar">${avatar}</div>
           <div class="message-content">
               <div class="message-text">${text}</div>
               <div class="message-time">${time}</div>
           </div>
       `;
       
       chatMessages.appendChild(messageDiv);
       chatMessages.scrollTop = chatMessages.scrollHeight;
   }

   // Código para gestionar Django CSRF token en solicitudes AJAX (necesario en producción)
   function getCookie(name) {
       let cookieValue = null;
       if (document.cookie && document.cookie !== '') {
           const cookies = document.cookie.split(';');
           for (let i = 0; i < cookies.length; i++) {
               const cookie = cookies[i].trim();
               if (cookie.substring(0, name.length + 1) === (name + '=')) {
                   cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                   break;
               }
           }
       }
       return cookieValue;
   }

   // Función para enviar mensajes al backend
   async function sendMessageToBackend(message) {
       try {
           // URL del endpoint para procesar mensajes
           const url = 'http://127.0.0.1:8000/Lora/procesar_mensaje/';
           
           const response = await fetch(url, {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json',
                   'X-CSRFToken': getCookie('csrftoken'), // Importante seguridad CSRF 
               },
               body: JSON.stringify({ 
                   mensaje: message,
                   //  añadir más datos
                   // P, ID de conversación, información del usuario, etc.
                   id_conversacion: 1, // Ejemplo
               }),
               credentials: 'same-origin', //  mantener la sesión
           });
           
           if (!response.ok) {
               throw new Error(`Error HTTP: ${response.status}`);
           }
           
           return await response.json();
       } catch (error) {
           console.error('Error al enviar mensaje al backend:', error);
           throw error; // Propaga error para manejarlo en sendMessage()
       }
   }