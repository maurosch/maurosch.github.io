---
title: "Comprimir Clases Grabadas"
description: "Someone's blog"
date: 2021-06-20T11:47:09-03:00
---

Cuando empezó la cuarentena y pasamos a las clases virtuales no me di cuenta pero también dejé de tomar apuntes. Cuál era el sentido de tomar apuntes si las clases eran grabadas y podemos repetirlas tantas veces como queramos. Está la controversia de si se aprende más (o nos queda más tiempo en la cabeza) escribiendo las cosas o simplemente escuchandolas.

Ya a partir del secundario tengo el hábito de tener todo ordenado y guardado de los apuntes de las clases por si en el futuro lo necesito de nuevo. Con la virtualidad y los videos está el miedo de perder el acceso a estos, que la facultad saque los videos o que al descargarlos se arruine el disco y se pierdan. 

Obviamente solo vamos a descargar los videos con consentimiento del profesor y nunca redistribuyendolos.

Los videos pueden pesar mucho, y, ¿tiene sentido que pesen mucho si simplemente son diapositivas estáticas cambiando con una voz hablando? La verdad es que no. Primero que nada podemos reducirle la resolución/bitrate, esto va a depender de cada persona que resolución quiere tener el video y dependera de cuanto le importe esa clase. Luego podemos cambiar el codec a x265, el cual es bastante más eficiente en compreción que sus contrincantes. Y por último podemos bajar los FPS lo cual reduce bastante el peso (para las clases muy estáticas y no me importan mucho uso 1 FPS). Aplicando todo podemos guardar clases de 3 horas en 150mb. 

Todo lo anterior lo podemos aplicar con el comando:

`
ffmpeg -i input.mp4 -vcodec libx265 -filter:v fps=1 output.mp4
`

¿Tiene sentido comprimirlo con alguna aplicación de compreción a un zip? No creo que se gane una mejora significativa porque el video ya está comprimido por el codec y si hacemos esto tendriamos que descomprimirlo para reproducir cada video. Aunque si se lo quiere encriptar para subir a la nube (por si acaso) entonces si es una buena opción.

A partir de acá lo pueden tener guardado en su disco y en algún backup como en la nube (drive, dropbox, etc).