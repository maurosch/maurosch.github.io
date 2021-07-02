---
title: "Cómo funciona el GPS"
date: 2021-07-04T11:47:09-03:00
author: "Mauro"
---

El GPS es algo que nunca nos falla, puede no haber 4G, no haber recepción de celular sin embargo el GPS sigue funcionando. ¿Cómo funciona esta maravilla?

Imaginemos que tenemos un dispositivo que quiere saber donde está. A este le llega una señal de un satélite con la posición del satélite y la hora a la actual envió el mensaje. En nuestro dispositivo también tenemos la hora actual, con lo cual, calculando la diferencia de ambos tiempos podemos saber a que distancia estamos de ese satélite. Es decir, podemos decir que estamos en algún punto de la circunferencia de esa distancia alrededor del satélite.

Si ahora tenemos 2 satélites que nos mandan su posición y su hora, entonces vamos a tener dos circunferencias, las cuales se intersectan en dos puntos. Entonces vamos a estar en alguno de esos dos puntos. Ahora con 3 satélites vamos a obtener un punto donde se intersectan las 3 circunferencias, y ahí es la posición donde estamos con nuestro dispositivo parados. Y con más de 4 satélites podemos obtener también la altitud en donde estamos.

<div style="text-align:center">

![](/images/gps-2d.jpg)

<p class="caption">Tomada de wikipedia.</p>

</div>

Notar que es una simplificación y hablamos de circunferencias pero tendrían que ser esferas alrededor de los satélites. 
Increíblemente nuestros dispositivos nunca tienen que mandar ninguna señal y los satélites se encargan de todo. Esto es la razón por la cual nuestro celular puede ser tan pequeño y tener GPS, si tuviera que responder entonces tendría que tener una antena muy grande.

¿Qué pasa si mi reloj del dispositivo está mal/movido?
Primero que todo que el reloj de nuestro dispositivo seguramente no sea atómico como el de los satélites lo cual genera bastante error. Pero si recibimos la señal de 4 satélites se puede calcular la hora actual del dispositivo, así teniendo la precisión del reloj atómico. Mientras más satélites de utilizan mayor precisión se va a tener de la posición de la posición y de la hora.

¿Cómo sabe en que posición está cada satélite?
Ellos su vez tienen el sistema GPS pero al revés, utilizando torres de comunicación de la tierra que les dicen la hora y su posición.

Lo increíble de este sistema es que funciona en cualquier parte del mundo (si tenés vista al cielo) y a cualquier hora. 

Asimismo es interesante la propuesta de Starlink, el sistema de internet satelital para todo público que traería las mismas ventajas que el GPS pero para internet.