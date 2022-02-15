---
title: "Análisis: ¿Qué tan privados son los mensajes de Whatsapp/Telegram/Signal?"
date: 2022-02-11T15:20:09-03:00
draft: false
---

Primero hablemos de encriptación de mensajes. Existen 2 tipos de encriptaciones: 
- Encriptación simétrica: se usa la misma clave para encriptar y desencriptar. Si querés utilizar esta encriptación para establecer una comunicación se necesita previamente que ambas partes conozcan la clave. 
- Encriptación asimétrica: se usa distinta clave para encriptar y desencriptar (y no tienen relación, no podes obtener una de la otra). En "general" se las llama clave privada con al que desencriptamos y clave pública con la que encriptamos. Digo en general porque puede ser que sea al revés, por ejemplo en firma digital.

Lo interesante de que con encriptación asimétrica podemos empezar una conversación entre 2 computadoras y nadie en el medio que lea todos los mensajes pueda entender la conversación (también se le dice man in the middle attack). Esto es posible también sin tener que tener claves previamente mediadas como en el caso de encriptación simétrica.

Ya con estos conceptos podemos analizar las aplicaciones:

## Whatsapp

Whatsapp cuenta con end-to-end encryption. Esto significa que los mensajes se encriptan en un celular y se desencriptan en el celular a donde llegan y nadie en el medio los puede leer. Esto seguramente se realiza utilizando encriptación asimétrica. 

¿Es chequeable que whatsapp hace end-to-end encryption? La verdad que es sumamente difícil verificarlo. El gran problema es que la aplicación no es código abierto/público. Entonces tenemos que creer en la palabra de ellos en muchos casos.

¿Es probable que lean los mensajes? Seguramente no. Whatsapp es una empresa grande (~500 empleados), me parece poco probable que mientan a toda la gente que la usa.

Es interesante que end-to-end encryption no nos deja leer el historial de mensajes desde un dispositivo nuevo. Esto sucede en whatsapp, lo cual indicaría que ellos no pueden leer los mensajes. Whatsapp igual dejan pasar el historial de un dispositivo a otro si ambos están conectados (algo que también es factible usando end-to-end encryption).
 
Sin embargo, la opción de whatsapp de hacer un buckup en google drive es un agujero muy grande en la privacidad. Actualmente esa funcionalidad es imposible agregarle una clave al buckup, asiendo que se suban a google drive en texto plano. Basicamente estamos regalando el historial de mensajes a google. Esto es algo que recién ahora dicen estar solucionándolo (si es que no lo hicieron a propósito). Basicamente nos obligan a decidir entre guardar el historial o tener privacidad 😤.  
ACTUALIZACION: ahora whatsapp nos deja hacer un buckup encriptado 😄. Es gracioso que al mismo tiempo que habilitaron el buckup encriptado google comenzó a contar el espacio del buckup como espacio de almacenamiento de google drive.

## Telegram

Telegram tiene el cliente de celular open source, asi que se puede ver el código fuente. Interesantemente, comprobar si una aplicación viene de un código fuente dado es muy difícil, pero es un problema para otra nota[^1].

Telegram no tiene el código fuente de el servidor abierto, con lo cual no podemos saber lo que se hace en el servidor. Pero viendo lo que hace la app es suficiente para saber si los mensajes se mandan de manera encriptada y si ellos lo pueden leer.

Telegram sin embargo viene sin end-to-end encryption por defecto. Entonces en el servidor pueden leer todos los mensajes. Se puede activar end-to-end encryption pero perdiendo el historial de mensajes al cambiar entre dispositivos. Yo creo que vienen sin end-to-end encryption porque perdería la posibilidad de utilizar la versión web sin tener el celular.

## Signal

En esta aplicación tenemos el cliente y el servidor open source y tenemos end-to-end encryption activado por defecto. 
También ofrece hacer buckups (no viene activado por default). Por suerte es un buckup encriptado.
Lo malo de signal es que no tiene muy buen soporte para usar la aplicación de la computadora: a veces no llegan los mensajes a la PC, también al conectar un dispositivo nuevo no traslada el historial desde el celular a la computadora (no supone riesgo hacerlo, pero no debe estar implementado).

## Otros riesgos

Tenemos que pensar que Android/ios, al ser el sistema operativo de nuestro dispositivo, también tiene acceso a los datos de nuestra aplicación instalada, pudiendo leer los mensajes que tenemos. También al ver los mensajes en el navegador Chrome/Safari/Firefox estamos dependiendo de estos programas que no lo lean.
Android es open source (no estoy seguro si completamente), lo cual lo vuelve más confiable.


## Alternativa con Blockchain

Mi hermano trajo esta idea: Utilizar la blockchain como historial para mensajes. Esto tiene algunos problemas: cada mensaje saldría plata publicar (muy poco igual) y que tendría un delay considerable (también poco). Pero lo bueno de esta idea es que sería descentralizado, no tendría downtime y se podría manejar con contratos inteligentes que sería open-source.

[^1]: https://blogs.kde.org/2013/06/19/really-source-code-software