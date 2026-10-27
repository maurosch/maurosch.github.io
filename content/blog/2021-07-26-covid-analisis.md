---
title: "📕 Análisis casos covid CABA 2021"
date: 2021-07-26T00:00:00-03:00
---

Utilizando los datos públicos de la ciudad sobre los casos de covid[^1], me decidí hacer un análisis que no estaba contemplado en los gráficos del diario la nación[^2].

Más que nada me interesaba la probabilidad de fallecimiento dada la edad. Porque se dice que tiene un porcentaje de 3% de fallecimientos. Pero es bastante variable según la edad.
Si vemos los casos por edad:

{{< img src="/images/20210726-covid-analisis/contagiados.svg" title="Casos positivos por edad." >}}

Y ahora los fallecimientos por edad:

{{< img src="/images/20210726-covid-analisis/fallecimiento.svg" title="Fallecimientos por edad." >}}

Notamos que los más jóvenes son mucho más inmunes que los adultos. Entonces sacando la probabilidad de fallecimiento por edad:

{{< img src="/images/20210726-covid-analisis/prob-fallecimiento.svg" title="Probabilidad fallecimiento (fallecidos sobre casos positivos covid) por edad." >}}

Esto nos da un indicio un poco más fuerte del riesgo según la edad.

Por último veamos si superponemos la probabilidad de fallecimiento de 2020 y 2021:

{{< img src="/images/20210726-covid-analisis/prob-fallecimiento-2020-2021.svg" title="Probabilidad fallecimiento por edad separado 2020 y 2021." >}}



Posiblemente sea por las vacunas o puede ser que el servicio médico estaba más preparado. Sea cual sea el caso es algo positivo. Notar que la cantidad de casos positivos en 2021 (hasta julio) fue de 3 veces la cantidad de casos positivos en todo el 2020.

{{< img src="/images/20210726-covid-analisis/casos-covid-tiempo.png" title="Casos positivos covid[2]." >}}

Para jugar con el notebook con el cuál generé los datos: 
<a href="/files/20210726-covid-analisis/analisis.ipynb">link<a>


[^1]: [Datos casos covid CABA](https://data.buenosaires.gob.ar/dataset/casos-covid-19)
[^2]: [Estadísticas LA NACION](https://www.lanacion.com.ar/sociedad/en-detalle-infectados-fallecidos-coronavirus-argentina-nid2350330/)