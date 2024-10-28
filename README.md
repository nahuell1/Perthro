Bot de telegram de pruebas para function calls de LLM locales. Para utilizarlo, enviar mensaje al bot configurado con la apikey. En mi caso, el bot configurado es  "@perthro_bot" en Telegram. Actualmente tiene 4 funciones:
> No funcionará el bot que mencioné debido a que el código no está corriendo en ningún servidor. En caso de requerirlo para una demo, contactarse conmigo por nahueljl@proton.me
- `ollama` para chatear con el modelo deployado en el servidor que corre el bot (está configurado para correr llama3.1
- `hello` para probar el bot. Responde con "Hola {nombre de usuario}".
- `tiempo` para consultar el clima en tiempo real con información obtenida de internet, con inferencia de inteligencia artificial, y preparado para consultar la api de `openmeteo`, con respuesta humanizada.
- Envío de PDF: Al enviar un PDF, este se procesará y se obtendrá el texto, el cual se le envía al usuario que lo consulta. La idea final de esto es poder hacer un etiquetado por medio de una IA, utilizando el código de https://github.com/nahuell1/extract-information-from-pdf-cv y así almacenarse sistematizado para una búsqueda
