---
title: "Calculadora para cuotas"
date: 2022-05-10T10:20:09-03:00
draft: false
---

Hoy en día con la inflación anual gigante que tenemos (> 50%) siempre hay que ver cuando nos conviene pagar con cuotas, cuando nos conviene transferir directo o cuando pagar sin cuotas.

Precio
<input name="precio" value="10000" type="number"/>

Cantidad cuotas
<input name="cuotas" value="12" type="number"/>

Inflación mensual 
<input name="inflacionMensual" value="5" type="number"/> %

Interés cuotas 
<input name="interesCuotas" value="0" type="number"/> %

<button onclick="calcular()">Calcular</button>
<b><div name="res"></div></b>

<script>
    function cuotas(precio, cantidad, porcentajeInflacionMensual, porcentajeIinteresCuota){
        inflacionMensual = 1-porcentajeInflacionMensual/100;
        interesCuota = 1+porcentajeIinteresCuota/100;
        multFinal = inflacionMensual*interesCuota;
        return (precio/cantidad)*((1-Math.pow(multFinal,cantidad+1))/(1-multFinal));
    }

    function calcular(){
        var p = Number(document.querySelector("input[name='precio']").value);
        var c = Number(document.querySelector("input[name='cuotas']").value);
        var iM = Number(document.querySelector("input[name='inflacionMensual']").value);
        var iC = Number(document.querySelector("input[name='interesCuotas']").value);
        var finalValue = cuotas(p, c, iM, iC);
        var discountRecharge = finalValue === 0 ? 0 : Math.floor(-(1-p/finalValue)*100);

        var finalText = "Es como si pagaras $" + Math.floor(finalValue) + " actualmente, es decir, es un " + Math.abs(discountRecharge) + "% de " + (discountRecharge < 0 ? "recargo" : "descuento") + ".";
        
        document.querySelector("div[name='res']").innerHTML = "<p><b>"+finalText+"</b></p>";
    }
</script>

Cuando es muy poca diferencia, no es mucho problema, hay que tener en cuenta que si tenemos la plata actualmente y vamos a usar cuotas, hay que ponerla en algún mecanismo financiero para ganarle/empatar a la inflación. Si con el mecanismo perdemos a la inflación hay que tenerlo en cuenta en el cálculo. 
Como ejemplo, si vamos a usar un plazo fijo, entonces en lugar de poner la inflación prevista ponemos la taza del plazo fijo.