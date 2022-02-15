---
title: "About"
date: "2020-01-01"
#menu: "main"
description: "A description of the page"
---

<p>Me llamo Mauro, tengo <span id="age"></span> años y estoy estudiando ciencias de la computación en la UBA argentina.</p>

<script>
    var age = new Date().getFullYear() - 1999 - 1;   
    if(new Date().getMonth() > 9 || (new Date().getMonth() == 9 && new Date().getDate() == 26)){
        age = age+1;
    }
    document.getElementById("age").innerHTML = age;
</script>
