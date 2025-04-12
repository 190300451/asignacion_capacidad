import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def intro():
    st.markdown("""
                # ¡Bienvenid@! 🌟

Imagina que tienes un número limitado de lugares en un avión, un autobús, o incluso en un concierto. ¿A quién se los deberías vender primero? ¿A quienes compran con anticipación buscando buen precio? ¿O a quienes compran a última hora, tal vez con urgencia, y están dispuestos a pagar más?

Este es el corazón del problema de **asignación de capacidad**: cómo distribuir un recurso limitado entre diferentes tipos de clientes para obtener el **mejor resultado posible** (por ejemplo, el mayor ingreso).

## 🎯 ¿Cuál es el objetivo?

El objetivo es encontrar una forma inteligente de **reservar espacios** para diferentes grupos de compradores. Por ejemplo, podrías decidir reservar una parte para quienes compran con tiempo (y buscan precios bajos) y otra parte para quienes compran tarde (y pagan más). Pero… ¿cuánta capacidad reservar para cada grupo?

Esa es la gran pregunta que vamos a explorar aquí.

## 🧠 ¿Por qué es importante?

La asignación de capacidad es una herramienta fundamental en:

- ✈️ Aerolíneas, para decidir cuántos asientos vender a cada tarifa.
- 🏨 Hoteles, para manejar reservas anticipadas y de último minuto.
- 🎟️ Eventos, para balancear precios económicos y premium.
- 🚚 Logística y servicios, donde hay que decidir cómo usar recursos limitados de forma eficiente.

Aunque en este caso hablaremos de boletos y reservas, ¡los mismos principios se aplican en muchos contextos reales!

---

En las siguientes secciones, podrás experimentar con diferentes escenarios, ajustar parámetros y ver cómo cambia la situación. Pero por ahora, quédate con esta idea:

> **Distribuir bien la capacidad es clave para tomar decisiones inteligentes cuando los recursos son limitados.**

¡Vamos a descubrir cómo hacerlo! 🚀 
                """)
    
def segmentos():
    st.markdown("""
                # Segmentación del mercado

Para tomar decisiones informadas sobre cómo asignar la capacidad, es importante entender primero **a quién le estamos vendiendo**.

En este caso, suponemos que el mercado está **segmentado en dos grupos de compradores**, de acuerdo con dos criterios:

- 🎯 **Su sensibilidad al precio**
- 🕒 **El momento en el que compran**

Esta segmentación nos permite tratar a los clientes de forma diferente, basándonos en su comportamiento típico de compra.

---

### 🔵 Grupo 1: Sensibles al precio (Clase B)
- Compran con anticipación
- Buscan precios bajos
- Representan una demanda más predecible
- Pagan un precio menor $p_B$

### 🔴 Grupo 2: Menos sensibles al precio (Clase A)
- Compran cerca de la fecha del evento
- Están dispuestos a pagar más
- Representan una demanda más variable
- Pagan un precio mayor $p_A$

---

📌 Esta segmentación es la base de la estrategia de **asignación de capacidad con precios diferenciados**.

A continuación, exploraremos cómo podemos utilizar esta información para tomar decisiones más inteligentes sobre cómo distribuir nuestra capacidad limitada.

---
                """
    )
    st.image("markt_seg.png", caption="Segmentación del mercado",  use_container_width=True)

def supuestos():
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.stats import norm
    import streamlit as st

    st.markdown("""
# Supuestos del modelo

Antes de pasar a la definición formal de los elementos del modelo, es importante dejar en claro dos supuestos fundamentales sobre el comportamiento del mercado:

---

### 💰 Los precios ya están definidos

Cada segmento del mercado paga un precio distinto, y **estos precios ya han sido establecidos previamente** por la empresa. En esta aplicación, **no consideramos los precios como variables de decisión**, sino como valores fijos:

- $ p_A $: precio pagado por la **clase A** (menos sensibles al precio, compran tarde).
- $ p_B $: precio pagado por la **clase B** (más sensibles al precio, compran anticipadamente).

Lo que sí analizaremos será **cómo distribuir la capacidad** entre estos dos grupos, para lograr un mayor ingreso o un equilibrio estratégico.

---

### 📊 La demanda sigue una distribución normal

Para poder analizar escenarios y estimar probabilidades, suponemos que la demanda de cada segmento se comporta como una **variable aleatoria continua** con distribución normal:

- Demanda de la clase A:
  $$
  D_A \sim \mathcal{N}(\mu_A, \sigma_A)
  $$

- Demanda de la clase B:
  $$
  D_B \sim \mathcal{N}(\mu_B, \sigma_B)
  $$

Los valores de $ \mu $ y $ \sigma $ para cada clase representan el comportamiento típico del mercado, y puedes ajustarlos a continuación para explorar distintos escenarios.
    """)

    st.markdown(
        """
> 📌 **Nota:** En la gráfica se han utilizado **dos ejes horizontales en direcciones opuestas**. Por ahora, esto solo sirve para representar las dos distribuciones en un mismo espacio.  
> En la siguiente página explicaremos por qué esta representación es útil y qué significado tienen estos dos ejes en el contexto del problema.
"""
    )

    # Panel lateral para modificar parámetros
    st.sidebar.header("📊 Parámetros de demanda")
    mu_A = st.sidebar.slider("Media Clase A (μ_A)", 5, 80, 25)
    sigma_A = st.sidebar.slider("Desviación estándar Clase A (σ_A)", 1, 30, 8)
    mu_B = st.sidebar.slider("Media Clase B (μ_B)", 5, 150, 60)
    sigma_B = st.sidebar.slider("Desviación estándar Clase B (σ_B)", 1, 30, 8)

    # Parámetros fijos para la gráfica
    C = 100
    x_b = np.linspace(0, C, 1000)
    pdf_B = norm.pdf(x_b, mu_B, sigma_B)

    x_y = C - x_b
    pdf_A = norm.pdf(x_y, mu_A, sigma_A)
    x_A = C - x_y

    # Crear gráfica
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(x_b, pdf_B, label="Demanda Clase B", color='steelblue')
    ax1.plot(x_A, pdf_A, label="Demanda Clase A", color='darkred')

    # Anotar medias
    ax1.axvline(mu_B, color='steelblue', linestyle='--', linewidth=1)
    ax1.text(mu_B + 1, norm.pdf(mu_B, mu_B, sigma_B) + 0.001, r"$\mu_B$", color='steelblue')

    b_mu_A = C - mu_A
    ax1.axvline(b_mu_A, color='darkred', linestyle='--', linewidth=1)
    ax1.text(b_mu_A - 8, norm.pdf(mu_A, mu_A, sigma_A) + 0.001, r"$\mu_A$", color='darkred')

    # Ejes
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim()[::-1])
    #ax2.set_xlabel("Nivel de protección para clase A ($y$)")

    #ax1.set_xlabel("Límite de reserva para clase B ($b$)")
    ax1.set_ylabel("Densidad de probabilidad")
    ax1.set_title("Distribuciones de demanda por segmento")
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)

    st.pyplot(fig)

    st.markdown(
        """ 
> 🔴 Clase A: menos sensibles al precio, compran tarde.  
> 🔵 Clase B: más sensibles al precio, compran anticipadamente.
               
"""
    )


def elementos():
    st.markdown("""
                # Elementos clave del modelo

Para poder analizar y optimizar la asignación de capacidad, vamos a definir algunos conceptos fundamentales que usaremos a lo largo de la aplicación:

---

### 🧩 Capacidad total: $C$

Es el número total de unidades disponibles para asignar.  
Por ejemplo: la cantidad de asientos en un vuelo, camas en un hotel, o entradas a un evento.

---

### 🔵 Límite de reserva para la clase B: $b$

Es la cantidad **máxima** de unidades que se pueden vender a la **clase B** (quienes compran con anticipación y buscan precios bajos).  

---

### 🔴 Nivel de protección para la clase A: $y$

Es la cantidad de unidades que se **reservan exclusivamente** para la **clase A** (quienes compran más tarde y pagan más).  
También puede verse como la **capacidad no disponible para la clase B**.

---

## 📐 Relación entre los parámetros

Como estamos dividiendo una capacidad total entre dos clases, se cumple la siguiente igualdad:

$$
b + y = C
$$

Esto significa que si aumentamos el valor de $ b $, estamos reduciendo el nivel de protección $ y $, y viceversa.

---

Con estos elementos en mente, ya podemos avanzar al análisis visual de las distribuciones de demanda y explorar cómo afectan nuestras decisiones de asignación.

                """
    )


def pagina_distribuciones():
    st.set_page_config(page_title="Distribución de demanda", layout="centered")
    st.title("Distribuciones de demanda por clase")

    st.markdown(
        """

✅ En la gráfica que verás a continuación:

- El eje inferior representa el valor de $ b $, el **límite de reserva para la clase B**, y se lee de izquierda a derecha.
- El eje superior representa el valor de $ y = C - b $, el **nivel de protección para la clase A**, y se lee de derecha a izquierda.

Ambas distribuciones se grafican en el mismo eje horizontal, pero orientadas de forma complementaria, lo que te permitirá observar de manera clara cómo se comporta la probabilidad de que la demanda de cada clase **supere el límite que se le ha asignado**.


        """
    )
    
    # Parámetros generales
    st.sidebar.header("🎛 Parámetros del modelo")
    #C = st.sidebar.slider("Capacidad total (C)", min_value=20, max_value=200, value=100, step=5)
    C = 100
    b = st.sidebar.slider("Límite de reserva para clase B (b)", min_value=0, max_value=C, value=int(C * 0.65))
    y = C - b
    st.sidebar.markdown(f"**Nivel de protección para clase A (y):** `{y}`")

    # Parámetros de demanda
    st.sidebar.subheader("📊 Parámetros de demanda")
    mu_A = st.sidebar.slider("Demanda media (Clase A)", 5, 80, 25)
    sigma_A = st.sidebar.slider("Desviación estándar (Clase A)", 1, 30, 8)
    mu_B = st.sidebar.slider("Demanda media (Clase B)", 5, 150, 60)
    sigma_B = st.sidebar.slider("Desviación estándar (Clase B)", 1, 30, 8)

    # Dominio para b (izquierda a derecha)
    x_b = np.linspace(0, C, 1000)
    pdf_B = norm.pdf(x_b, mu_B, sigma_B)

    # Dominio para y (de derecha a izquierda), reflejado sobre eje de b
    x_y = C - x_b
    pdf_A = norm.pdf(x_y, mu_A, sigma_A)
    x_A = C - x_y  # para graficar contra eje de b

    # Gráfica
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Curvas de densidad
    ax1.plot(x_b, pdf_B, label="Demanda Clase B", color='steelblue')
    ax1.plot(x_A, pdf_A, label="Demanda Clase A", color='darkred')

    # Sombrear colas relevantes
    ax1.fill_between(x_b, 0, pdf_B, where=(x_b >= b), color='steelblue', alpha=0.3)
    ax1.fill_between(x_A, 0, pdf_A, where=(x_A <= b), color='darkred', alpha=0.3)

    # Línea de umbral
    ax1.axvline(b, linestyle='--', color='gray', label=f"Límite b = {b}")

    # Eje superior invertido para y
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim()[::-1])
    ax2.set_xlabel("Nivel de protección para clase A ($y$)")

    # Eje inferior
    ax1.set_xlabel("Límite de reserva para clase B ($b$)")
    ax1.set_ylabel("Densidad de probabilidad")
    ax1.set_title("Distribuciones de probabilidad y áreas correspondientes a $P(D > b)$ y $P(D > y)$")
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)

    st.pyplot(fig)

    st.markdown(
        """
---

## 🧠 ¿Qué representan las áreas sombreadas?

Las áreas sombreadas bajo las curvas corresponden a la **probabilidad de desbordamiento**, es decir, la probabilidad de que la demanda de un segmento **supere la capacidad asignada**:

- El área azul representa la probabilidad de que la **demanda de la clase B supere el límite $ b $**:
  $$
  P(D_B > b)
  $$

  **Observa** que $P(D_B > b) = 1-F_B(b) = \overline{F}_B(b)$, siendo $F_B(b)$ la función de distribución acumulativa de la clase B.

- El área roja representa la probabilidad de que la **demanda de la clase A supere el nivel de protección $ y $**:
  $$
  P(D_A > y)
  $$

  **Observa** que $P(D_A > y) = 1-F_A(y) = \overline{F}_A(y)$, siendo $F_A(y)$ la función de distribución acumulativa de la clase A.

Estas probabilidades son importantes para evaluar el **riesgo de dejar a clientes sin atender** si la capacidad asignada a su segmento resulta insuficiente.

A lo largo de esta aplicación podrás observar cómo cambian estas probabilidades al modificar los valores de $ b $ y $ y $.

        """

    )
    st.markdown(
        """
---

## 🧠 Preguntas para reflexionar

Mientras ajustas el valor de $ b $ en la gráfica, considera lo siguiente:

- 🔵 ¿Qué ocurre con la **probabilidad de desbordamiento para la clase B** cuando aumentas el límite $ b $?
- 🔴 ¿Y qué pasa con la **probabilidad de desbordamiento para la clase A** cuando disminuyes $ y $ (lo cual sucede al aumentar $ b $)?

- 🧮 ¿En qué parte del eje están centradas las distribuciones de demanda de cada clase? ¿Cómo afecta eso la forma en la que compiten por la capacidad?

- ⚖️ ¿Qué te parece más riesgoso: asignar mucha capacidad a la clase B (precio bajo) o reservar demasiada capacidad para la clase A (precio alto)? ¿Por qué?

- 💡 ¿Se te ocurre una forma de decidir cuánta capacidad deberíamos asignar a cada clase para lograr un equilibrio?

---

> **Tip:** Observa cómo se comportan las áreas sombreadas a medida que mueves el valor de $ b $ y reflexiona sobre a qué segmento estamos dejando fuera con mayor frecuencia.

        """
    )

def pagina_probabilidades():
    
    st.markdown("""
    # Riesgo de desbordamiento: ¿quién se queda sin lugar?

Imagina que ya configuraste tu sistema de reservas. Empiezas a asignar espacios a los clientes que compran con anticipación (clase B), pero... ¿qué pasa si luego llegan clientes de último minuto (clase A) y ya no hay espacio para ellos?

En esta página podrás visualizar el **riesgo de quedarte corto** para alguno de los dos segmentos.

---

Cada curva representa la probabilidad de que la **demanda de un segmento supere el espacio que le asignaste**:

- 🔵 La curva azul muestra el riesgo de **no poder atender a la clase B**.
- 🔴 La curva roja muestra el riesgo de **quedarte sin espacio para la clase A**.

Puedes mover el límite de reserva $ b $, ajustar las características de la demanda y ver cómo cambia el riesgo para ambos grupos.

> Explora y pregúntate: ¿quién está más expuesto al desbordamiento? ¿Cómo podrías lograr un equilibrio?

    """)

    # Parámetros interactivos
    st.sidebar.header("🎚 Parámetros")
    #C = st.sidebar.slider("Capacidad total (C)", 20, 200, 100, step=5)
    C = 100
    b = st.sidebar.slider("Límite de reserva para clase B (b)", 0, C, int(C * 0.65))
    y = C - b
    st.sidebar.markdown(f"**Nivel de protección para clase A (y):** `{y}`")

    mu_A = st.sidebar.slider("Media Clase A (μ_A)", 5, 80, 25)
    sigma_A = st.sidebar.slider("Desviación estándar Clase A (σ_A)", 1, 30, 8)

    mu_B = st.sidebar.slider("Media Clase B (μ_B)", 5, 150, 60)
    sigma_B = st.sidebar.slider("Desviación estándar Clase B (σ_B)", 1, 30, 8)

    # Dominio
    x_b = np.linspace(0, C, 1000)
    fb = 1 - norm.cdf(x_b, mu_B, sigma_B)  # P(D_B > b)
    fa = 1 - norm.cdf(C - x_b, mu_A, sigma_A)  # P(D_A > y)

    prob_b = 1 - norm.cdf(b, mu_B, sigma_B)
    prob_a = 1 - norm.cdf(y, mu_A, sigma_A)

    # Gráfica
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(x_b, fb, label=r"$P(D_B > b)$", color='steelblue')
    ax1.plot(x_b, fa, label=r"$P(D_A > y)$", color='darkred')

    ax1.axvline(b, linestyle='--', color='gray')
    ax1.plot(b, prob_b, 'o', color='steelblue')
    ax1.plot(b, prob_a, 'o', color='darkred')

    ax1.text(b + 1, prob_b + 0.02, f"$P(D_B>{b})={prob_b:.2f}$", color='steelblue')
    ax1.text(b - 35, prob_a + 0.02, f"$P(D_A>{y})={prob_a:.2f}$", color='darkred')

    # Eje superior para y
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim()[::-1])
    ax2.set_xlabel("Nivel de protección para clase A ($y$)")

    # Estética
    ax1.set_xlabel("Límite de reserva para clase B ($b$)")
    ax1.set_ylabel("Probabilidad de desbordamiento")
    ax1.set_title(f"Probabilidades de desbordamiento para $b = {b}$ y $y = {y}$")
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend()

    st.pyplot(fig)

    st.markdown(
        """
---

## 🧠 Preguntas para reflexionar

Mientras exploras las curvas de probabilidad de desbordamiento y ajustas el valor de \( b \), considera las siguientes preguntas:

- 🔵 ¿Qué sucede con la probabilidad de desbordamiento de la **clase B** a medida que aumentas el valor de $ b $?
- 🔴 ¿Qué sucede con la probabilidad de desbordamiento de la **clase A** cuando disminuyes el valor de $ y $ (al aumentar $ b $)?
- 📈 ¿Existe un punto donde ambas curvas se cruzan o están muy cerca? ¿Qué interpretación podrías darle a ese punto?
- ⚖️ Si deseas **reducir el riesgo de desbordamiento para ambos segmentos**, ¿en qué rango parece más razonable ubicar el valor de $ b $?
- 💰 Aunque aquí no estamos considerando aún el ingreso, ¿qué relación crees que podrían tener estas probabilidades con una estrategia de maximización de ingresos?
- 🤔 Si consideras el punto en el que **se intersectan ambas curvas** y sabes que el **precio pagado por la clase A es mayor que el de la clase B** (es decir, $ p_B < p_A $),  
  ¿crees que el **límite de reserva óptimo** debería estar a la **izquierda**, a la **derecha**, o **exactamente en el punto de cruce**?

---

> 💡 Recuerda que **modificar el valor de $ b $** no solo cambia el número de espacios asignados a la clase B, sino que **indirectamente también cambia la protección ofrecida a la clase A**.

        """
        )
    

def pagina_ingreso_exploracion():
    
    st.set_page_config(page_title="Exploración de ingreso y riesgo", layout="centered")
    st.markdown("""
    # ¿Estoy ganando lo que debería?

Supón que ya tomaste algunas decisiones sobre cómo asignar la capacidad entre las dos clases de clientes. Ahora llega la gran pregunta:  
**¿Estoy aprovechando bien mi capacidad? ¿Podría estar ganando más?**

---

En esta página puedes **jugar con los parámetros** y ver cómo cambia:

- 📉 El **riesgo de no poder atender** a un segmento.
- 💰 El **ingreso total que esperas obtener**, calculado paso a paso con base en las decisiones que tomas.

Puedes modificar:

- El límite de reserva para la clase B.
- Las características de la demanda (media y variabilidad).
- Los precios que paga cada segmento.

---

> ¡Explora distintos escenarios y busca pistas! ¿Qué combinación parece darte el mejor resultado? ¿Qué pasa si favoreces mucho a un segmento y descuidas al otro?

    """)

    # Capacidad total
    C = 100

    # Parámetros en barra lateral
    st.sidebar.markdown("## Parámetros de control")
    b = st.sidebar.slider("Límite de reserva para clase B (b)", 0, C, 60)
    y = C - b
    st.sidebar.markdown(f"**Nivel de protección para clase A (y):** `{y}`")

    st.sidebar.markdown("### Clase A (último momento)")
    mu_A = st.sidebar.slider("Media demanda clase A (μ_A)", 5, 80, 40)
    sigma_A = st.sidebar.slider("Desviación estándar clase A (σ_A)", 1, 30, 8)
    p_A = st.sidebar.number_input("Precio clase A (p_A)", 1.0, 100.0, 5.0)

    st.sidebar.markdown("### Clase B (anticipada)")
    mu_B = st.sidebar.slider("Media demanda clase B (μ_B)", 5, 150, 60)
    sigma_B = st.sidebar.slider("Desviación estándar clase B (σ_B)", 1, 30, 8)
    p_B = st.sidebar.number_input("Precio clase B (p_B)", 1.0, 100.0, 2.0)

    # ----------- Gráfica 1: Probabilidades de desbordamiento -----------
    x_vals = np.linspace(0, C, 1000)
    prob_B = 1 - norm.cdf(x_vals, mu_B, sigma_B)
    prob_A = 1 - norm.cdf(C - x_vals, mu_A, sigma_A)

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(x_vals, prob_B, label=r"$P(D_B > b)$", color='steelblue')
    ax1.plot(x_vals, prob_A, label=r"$P(D_A > y)$", color='darkred')
    ax1.axvline(b, linestyle='--', color='gray')
    ax1.plot(b, 1 - norm.cdf(b, mu_B, sigma_B), 'o', color='steelblue')
    ax1.plot(b, 1 - norm.cdf(y, mu_A, sigma_A), 'o', color='darkred')
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim()[::-1])
    ax2.set_xlabel("Nivel de protección para clase A ($y$)")
    ax1.set_xlabel("Límite de reserva para clase B ($b$)")
    ax1.set_ylabel("Probabilidad de desbordamiento")
    ax1.set_title("Probabilidades de desbordamiento para cada clase")
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)

    st.pyplot(fig1)

    # ----------- Gráfica 2: Ingreso incremental acumulado -----------
    b_vals = np.arange(0, C + 1)
    ingresos = [p_A * (C * norm.cdf((C - mu_A) / sigma_A))]

    for b_iter in b_vals[1:]:
        y_iter = C - b_iter
        delta = (
            p_B * (1 - norm.cdf(b_iter, mu_B, sigma_B)) * norm.cdf(y_iter, mu_A, sigma_A) +
            (p_B - p_A) * (1 - norm.cdf(b_iter, mu_B, sigma_B)) * (1 - norm.cdf(y_iter, mu_A, sigma_A))
        )
        ingresos.append(ingresos[-1] + delta)

    ingreso_actual = ingresos[b]

    fig2, ax = plt.subplots(figsize=(10, 4))
    ax.plot(b_vals, ingresos, label="Ingreso esperado", color='mediumblue')
    ax.axvline(b, linestyle='--', color='gray', label=f"b = {b}")
    ax.plot(b, ingreso_actual, 'o', color='mediumblue')
    ax.set_xlabel("Límite de reserva para clase B ($b$)")
    ax.set_ylabel("Ingreso esperado")
    ax.set_title("Ingreso esperado en función de $b$")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    st.pyplot(fig2)   
    

    st.markdown(
    """
---

## 🧠 Preguntas para reflexionar

Mientras exploras el comportamiento del ingreso esperado y las probabilidades de desbordamiento, considera lo siguiente:

- 🔍 ¿Qué ocurre con la **probabilidad de desbordamiento** de la clase B cuando aumentas el límite de reserva \( b \)?
- 🔴 ¿Cómo cambia la **probabilidad de desbordamiento** para la clase A cuando reduces el nivel de protección \( y \)?
- 💰 ¿En qué rango de valores de \( b \) el **ingreso esperado** parece aumentar más rápidamente?
- 📉 ¿Qué sucede si el precio de la clase A aumenta mucho más que el de la clase B? ¿Cómo cambia la forma de la curva de ingreso?
- 📦 ¿Cómo afecta la **dispersión** (desviación estándar) de la demanda en cada clase al ingreso total?
- 🤔 ¿Puedes identificar un punto en el que el ingreso parece dejar de crecer? ¿Qué tan cerca está ese punto de un equilibrio entre ambos segmentos?

"""
)

def pagina_formula_marginal():
    st.markdown("""
# ¿Podemos predecir el mejor valor de $b$ sin probar uno por uno?

En la página anterior estuviste jugando con diferentes valores de $ b $ —el límite de reserva para la clase B— para ver cómo afectaban al ingreso.  
Y seguramente notaste que hay un punto donde **el ingreso parece alcanzar su máximo**.

Pero entonces surge una gran idea:

> 💭 *¿Y si pudiéramos encontrar ese valor óptimo sin tener que probar todos los posibles? ¿Y si existiera una fórmula que nos diga cuándo conviene o no aumentar \( b \)?*

¡La buena noticia es que sí existe una forma de hacerlo!  
Y en esta página vamos a construir esa lógica paso a paso, de forma sencilla y sin usar derivadas.

---

## 📈 ¿Qué sucede cuando aumentamos el valor de $b$?

Supón que ya tienes un cierto valor de $ b $ definido. Ahora te preguntas:  
**¿Qué pasaría si le cediera una unidad más de capacidad a la clase B?**

Es decir, si aumentas $ b $ en una unidad, ¿cuánto ingreso adicional esperas obtener?

Vamos a analizar los posibles escenarios:

---

## 🧩 Caso 1: Llega un cliente de clase B y **no** llega uno de clase A

¡Perfecto! El nuevo espacio fue aprovechado por un cliente que sí llegó (clase B) y **no desplazó a nadie**.  
➡️ En este caso, ganas lo que paga ese cliente: $ p_B $

Pero, como esto no ocurre siempre, hay que multiplicarlo por la probabilidad de que **ocurra así**:

- $ P(D_B > b) $: que llegue alguien de clase B que antes no tenía lugar
- $ P(D_A \leq y) $: que no llegue un cliente de clase A que hubiera usado ese espacio

Entonces, el ingreso esperado en este caso es:

$$
p_B \cdot (1 - F_B(b)) \cdot F_A(y)
$$

---

## 🧩 Caso 2: Llega un cliente de clase B **y también** llega uno de clase A

Ahora se complica un poco: el nuevo espacio se lo lleva un cliente de clase B…  
pero **desplazamos a uno de clase A que hubiera pagado más** 😬

En este caso, el ingreso neto que obtienes es:

$$
p_B - p_A
$$

Y la probabilidad de que pase esto es:

- $ P(D_B > b) $: llega alguien de clase B
- $ P(D_A > y) $: también llega alguien de clase A que ya no tendrá espacio

Así que el ingreso esperado en este caso es:

$$
(p_B - p_A) \cdot (1 - F_B(b)) \cdot (1 - F_A(y))
$$

---

## 🧮 Sumamos ambos casos

Entonces, el ingreso **esperado total** al aumentar \( b \) en una unidad es:

$$
\Delta I(b) = p_B (1 - F_B(b)) F_A(y) + (p_B - p_A)(1 - F_B(b))(1 - F_A(y))
$$

Este es el **incremento marginal esperado** del ingreso.  
Nos dice si **vale la pena seguir cediendo espacios a la clase B**, o si **es momento de frenar y proteger a la clase A**.

---

> En la siguiente página, usaremos esta expresión para **ubicar el valor de $ b $** donde el ingreso ya no aumenta más…  
> o incluso **empieza a disminuir**. 🧠💰
""")

def pagina_optimo_teorico():
    
    st.set_page_config(page_title="Condición óptima", layout="centered")
    st.title("¿Dónde se encuentra el mejor valor de $b$?")

    st.markdown(r"""
Ya construimos paso a paso la fórmula del ingreso esperado al aumentar el límite de reserva $ b $, y vimos cómo ese ingreso crece... pero no para siempre.

Llega un punto en el que ceder más capacidad a la clase B **ya no genera beneficio adicional**. Ese es el punto que buscamos:  
🎯 el **nivel de reserva óptimo**.

---

## 📉 ¿Cuándo dejar de aumentar $ b $?

La lógica es sencilla:  
si el ingreso esperado **deja de crecer** o incluso **empieza a disminuir**, es momento de frenar.

Eso ocurre exactamente cuando:

$
\Delta I(b) = 0
$

Donde recordamos que:

$$
\Delta I(b) = p_B (1 - F_B(b)) F_A(y) + (p_B - p_A)(1 - F_B(b))(1 - F_A(y))
$$

---

## 🧩 Despejando la condición de optimalidad

Sabemos que $ y = C - b $.  
Entonces, si queremos encontrar el punto donde el ingreso marginal se vuelve cero, planteamos:

$$
p_B (1 - F_B(b)) F_A(y) + (p_B - p_A)(1 - F_B(b))(1 - F_A(y)) = 0
$$

Factorizamos $ (1 - F_B(b)) $:

$$
(1 - F_B(b)) \left[ p_B F_A(y) + (p_B - p_A)(1 - F_A(y)) \right] = 0
$$

Dado que $ (1 - F_B(b)) > 0 $, la expresión se anula cuando:

$$
p_B F_A(y) + (p_B - p_A)(1 - F_A(y)) = 0
$$

Ahora solo queda despejar $ F_A(y) $:

$$
p_B F_A(y) + (p_B - p_A)(1 - F_A(y)) = 0
$$

$$
p_B F_A(y) + (p_B - p_A) - (p_B - p_A)F_A(y) = 0
$$

$$
\left[p_B - (p_B - p_A)\right] F_A(y) = p_A - p_B
$$

$$
p_A F_A(y) = p_A - p_B
$$

$$
F_A(y) = 1 - \frac{p_B}{p_A}
$$

¡Y ahí lo tenemos!  
Como $ \overline{F}_A(y) = 1 - F_A(y) $, llegamos a la condición final:

---
## ✅ Condición para el nivel óptimo de protección:

$$
\boxed{\overline{F}_A(y^*) = \frac{p_B}{p_A}}
$$

Esta fórmula nos dice que el valor óptimo $ y^* $ debe ser tal que la **probabilidad de que la demanda de clase A supere ese nivel** sea **igual a la razón entre los precios**.

---

## 🧮 ¿Cómo encontramos el valor de $y^*$?

Para encontrar $ y^* $, basta con **despejarlo de la función acumulativa complementaria** de la distribución normal. Es decir:

$$
P(D_A > y^*) = \frac{p_B}{p_A}
\Rightarrow
F_A(y^*) = 1 - \frac{p_B}{p_A}
$$

Como $ D_A \sim \mathcal{N}(\mu_A, \sigma_A) $, podemos usar la función de cuantiles (inversa de la distribución acumulativa):

$$
y^* = F_A^{-1}\left(1 - \frac{p_B}{p_A} \right)
$$

Esto se puede calcular con la función `norm.ppf()` de la librería SciPy:

```python
from scipy.stats import norm
y_star = norm.ppf(1 - (p_B / p_A), loc=mu_A, scale=sigma_A)
```

Mientras que en R:

```r 
                y_star <- qnorm(1 - (p_B / p_A), mean = mu_A, sd = sigma_A)
```
    """)


def pagina_ejemplo_resuelto_estatico():
    import streamlit as st

    st.set_page_config(page_title="Ejemplo resuelto", layout="centered")
    st.title("Ejemplo resuelto: ¿Cuántos asientos debo reservar para clase B?")

    st.markdown(r"""
Estás a cargo de administrar un vuelo con **100 asientos disponibles**. Como parte de tu estrategia de precios, tienes dos segmentos de clientes:

- ✈️ **Clase A**: personas que reservan tarde y están dispuestas a pagar un precio más alto.
- 💼 **Clase B**: personas que compran con anticipación buscando un precio con descuento.

Tu objetivo es **maximizar el ingreso esperado**, decidiendo **cuántos asientos reservar para la clase B** sin poner en riesgo los ingresos potenciales que podrían generar los clientes de clase A.

---

### 🎯 El problema

Se sabe que la **demanda de espacios para clase A** sigue una distribución normal con:

- Media: $ \mu_A = 30 $
- Desviación estándar: $ \sigma_A = 10 $

Además, la razón entre los precios es:

$$
\frac{p_d}{p_f} = 0.4
$$

donde $ p_d $ es el precio con descuento (clase B) y $ p_f $ el precio sin descuento (clase A).

Queremos encontrar el valor de $ b $, el límite de reserva para la clase B, que **maximiza los ingresos esperados**.

---

### 🧮 Aplicando la condición óptima

Recordemos que el ingreso se maximiza cuando:

$$
\overline{F}_A(y^*) = \frac{p_d}{p_f}
$$

Es decir:

$$
F_A(y^*) = 1 - \frac{p_d}{p_f} = 1 - 0.4 = 0.6
$$

Queremos encontrar el valor $ y^* $ tal que $ F_A(y^*) = 0.6 $.  
Este valor corresponde al **cuantil 60%** de la distribución normal con media 30 y desviación estándar 10:

---

### 📐 Cálculo de $ y^* $:

$$
y^* = F_A^{-1}(0.6) = \text{qnorm}(0.6, \mu_A = 30, \sigma_A = 10) \approx 33
$$

Finalmente, el límite de reserva se calcula como:

$$
b^* = C - y^* = 100 - 33 = 67
$$

---

### ✅ Conclusión

Para maximizar los ingresos:

- Deberías reservar hasta **67 asientos** para la clase B (clientes con descuento).
- Esto deja una **protección de 33 asientos** para los clientes de clase A (precio completo).

Así logras un equilibrio entre aprovechar las ventas anticipadas **sin dejar fuera a quienes pagan más**. 🎯
    """)


def pagina_ejemplo_editorial():
    import streamlit as st

    st.set_page_config(page_title="Ejemplo editorial", layout="centered")
    st.title("Ejemplo 2: ¿Cuántos libros debo proteger para el mercado principal?")

    st.markdown(r"""
Estás a cargo de la gestión de ingresos de una **editorial** que está por lanzar un nuevo libro. El tiraje inicial es de **10,000 ejemplares** 📚.

El plan de distribución considera dos mercados:

- 🇺🇸 **Estados Unidos** (mercado principal): precio de venta de **\$150 USD**
- 🌍 **Resto del mundo** (mercado internacional): precio de venta de **\$90 USD**

Como en todo negocio, tu objetivo es claro:  
🎯 **maximizar los ingresos** aprovechando la capacidad de impresión de la mejor manera posible.

---

### 📦 Lo que sabemos:

- Capacidad total de libros: $ C = 10{,}000 $
- Precio en EE.UU.: $ p_f = 150 $
- Precio internacional: $ p_d = 90 $
- Demanda esperada en EE.UU.: $ \mu = 8000 $, $ \sigma = 1500 $
- Demanda internacional: **más alta**: media de 23,000 libros (pero limitada por lo que no se proteja)

---

### 🧠 ¿Cuál es el dilema?

Como hay alta demanda internacional, fácilmente se pueden colocar todos los libros fuera del país.  
Pero los libros vendidos internacionalmente **dejan menos ingreso** que los vendidos en EE.UU.

Entonces...  
> 💭 ¿Cuántos ejemplares deberías **proteger para EE.UU.**, para no dejar fuera a los compradores que pagan más?

---

### ✅ Aplicando la condición óptima

Recordamos que:

$$
\overline{F}_f(y^*) = \frac{p_d}{p_f}
\Rightarrow
F_f(y^*) = 1 - \frac{p_d}{p_f} = 1 - \frac{90}{150} = 0.4
$$

Queremos encontrar $ y^* $ tal que $ F_f(y^*) = 0.4 $, es decir, el **cuantil 40%** de una normal con media 8000 y desviación estándar 1500.

---

### 📐 Cálculo de $ y^* $:

$$
y^* = F_f^{-1}(0.4) = \text{qnorm}(0.4, \mu = 8000, \sigma = 1500) \approx 7680
$$

---

### 🧾 Conclusión

Para maximizar los ingresos:

- Se deben **proteger aproximadamente 7680 ejemplares** para su venta en los Estados Unidos.
- El resto (unos 2320 ejemplares) puede destinarse a la venta internacional.

Así se garantiza que el mercado de mayor valor **no quede desatendido**, y al mismo tiempo se aprovecha el exceso de demanda global 🌍.
    """)


def pagina_emsr():
    st.set_page_config(page_title="Múltiples clases (EMSR)", layout="centered")
    st.title("Múltiples clases y la heurística EMSR")

    st.markdown(r"""
En todos los ejemplos anteriores, asumimos que existían **solo dos clases** de clientes. Pero ¿qué pasa si hay más?

✈️ Esto es muy común en aerolíneas, hoteles o editoriales, donde los productos pueden ofrecerse a **muchos niveles de precio**, dependiendo de las condiciones de compra.

---

### 🧭 El desafío

Supón que tienes **varios segmentos de clientes**, cada uno con su propio precio:

$$
p_1 > p_2 > p_3 > \cdots > p_{n-1} > p_n
$$

y quieres decidir **cuántos espacios proteger** para los que pagan más, antes de abrir ventas a los que pagan menos.

El problema se vuelve más complejo, y resolverlo de forma exacta puede ser **costoso computacionalmente**.  
Por eso, en la práctica se utilizan estrategias heurísticas que, aunque no son perfectas, ofrecen resultados muy cercanos al óptimo con menos esfuerzo.

---

## ✨ Heurística EMSR (Expected Marginal Seat Revenue)

Una de las más utilizadas es la llamada **EMSR**, que busca estimar el ingreso esperado marginal al ceder asientos a clases más bajas.

Existen variantes, pero aquí explicaremos la más conocida: **EMSR-a**.

---

### 🚪 EMSR-a: protegiendo a los que pagan más

La idea es sencilla: cuando estás a punto de abrir la venta a una clase de menor precio, digamos la clase \( j+1 \), quieres proteger cierto número de unidades para las clases que pagan más: \( 1, 2, \ldots, j \).

¿Cómo? Aplicando la regla de Littlewood entre la clase $ j+1 $ y **cada una de las superiores**, de forma independiente.

El nivel total de protección se calcula así:

$$
y_{j,\ldots,1} = \sum_{k = 1}^{j} F_k^{-1} \left(1 - \frac{p_{j+1}}{p_k} \right)
$$

🔍 Es decir:

- Para cada clase $ k $ que paga más que $ j+1 $,
- Calculamos cuántos clientes esperados deben protegerse para que valga más la pena **esperar a un cliente de clase $ k $** que venderle ya a uno de clase $ j+1 $.

---

### 🧠 ¿Por qué funciona?

Esta regla no intenta modelar todas las combinaciones posibles entre clases.  
En su lugar, **compara por separado** el valor de cada clase cara con respecto a la clase que está por abrirse.

Aunque es una aproximación, en la práctica **funciona sorprendentemente bien**.  
Y se ha convertido en una herramienta clave en el Revenue Management moderno.

---

¿Te gustaría ver cómo se aplica esto con datos reales o con un ejemplo interactivo? 😄
    """)

def pagina_ejemplo_emsr():
    
    st.set_page_config(page_title="Ejemplo EMSR", layout="centered")
    st.title("Ejemplo 3: Estrategia de precios para la final de Quidditch 🧹🏆")

    st.markdown(r"""
Se acerca la gran final de la **Copa de Quidditch**, y tú estás a cargo de gestionar la venta de **1000 boletos** para el partido que se jugará dentro de tres semanas.

Como buen gestor de ingresos, decides implementar una **estrategia escalonada de precios**, sabiendo que distintos tipos de fanáticos valoran de manera distinta el acceso al evento.

---

### 🎯 Política de precios

Has decidido lo siguiente:

1. **Esta semana**: boletos a **\$100**
2. **La próxima semana**: boletos a **\$200**
3. **Semana del juego**: boletos a **\$250**

Cada grupo de compradores representa una **clase distinta**, con su propio comportamiento de compra y disposición a pagar:

| Clase  | Descripción                       | Precio | $ \mu $ (demanda esperada) | $ \sigma $ |
|--------|-----------------------------------|--------|-------------------------------|--------------|
| $ c_3 $ | Aficionados normales (anticipados) | \$100  | 1000                          | 300          |
| $ c_2 $ | Aficionados interesados (semana 2) | \$200  | 525                           | 50           |
| $ c_1 $ | Seguidores fieles (último momento) | \$250  | 275                           | 75           |

---

### 🧠 Objetivo

Ya sabemos que no podemos simplemente vender todos los boletos al primer grupo. Si lo hiciéramos, dejaríamos sin oportunidad a los más fieles… que están dispuestos a pagar más.

> Entonces, ¿cuántos boletos deberíamos **proteger para las clases de mayor precio**?

---

### ✍️ Solución con EMSR-a

Aplicamos la regla de Littlewood para calcular los niveles de protección que evitan vender demasiado pronto a precios bajos.

Primero comparamos la clase $ c_3 $ con las clases superiores:

- Con clase $ c_1 $:

$$
y_{31} = F_1^{-1}\left(1 - \frac{100}{250} \right) = F_1^{-1}(0.6)
$$

- Con clase $ c_2 $:

$$
y_{32} = F_2^{-1}\left(1 - \frac{100}{200} \right) = F_2^{-1}(0.5)
$$

---

### 📐 Cálculo final

Usamos los parámetros de las clases:

- $ F_1^{-1}(0.6) \approx \text{qnorm}(0.6, 275, 75) \approx 294 $
- $ F_2^{-1}(0.5) = \text{qnorm}(0.5, 525, 50) = 525 $

Entonces, el total de boletos a proteger es:

$$
y = y_{31} + y_{32} = 294 + 525 = 819
$$

---

### ✅ Conclusión

Debes proteger aproximadamente **819 boletos** para las clases que pagan más, y vender **hasta 181 boletos** esta semana a \$100.

Esta estrategia te permite maximizar ingresos, **sin cerrar las puertas a quienes valoran más el evento**. 🎫💰
    """)

def pagina_emsr_b():
    st.set_page_config(page_title="EMSR-b", layout="centered")
    st.title("EMSR-b: Una versión mejorada para proteger múltiples clases")

    st.markdown(r"""
En la página anterior exploraste la heurística **EMSR-a**, donde aplicamos la regla de Littlewood **varias veces**, una por cada clase de mayor precio.  
Ahora te presentamos una variante más refinada (y práctica): **EMSR-b**.

---

### 🧠 ¿Cuál es la idea?

En lugar de aplicar muchas reglas individuales, en EMSR-b construimos una **clase ficticia combinada** que representa la demanda conjunta de todas las clases más caras que la que está a punto de abrirse.

¡Así reducimos la comparación a un solo paso! 😎

---

### 🛠️ ¿Cómo se construye esta clase ficticia?

Supongamos que estamos por abrir la clase $ j+1 $, y queremos proteger asientos para las clases más rentables:  
$ 1, 2, \ldots, j $

Agrupamos todas esas clases en una sola, con los siguientes parámetros:

- **Demanda total esperada** (media):

$$
\mu = \sum_{i=1}^{j} \mu_i
$$

- **Variabilidad total** (desviación estándar combinada):

$$
\sigma = \sqrt{\sigma_1^2 + \sigma_2^2 + \cdots + \sigma_j^2}
$$

- **Precio promedio ponderado**:

$$
p = \sum_{i=1}^{j} p_i \cdot \frac{\mu_i}{\mu}
$$

Este precio representa el ingreso medio que podrías esperar si sigues vendiendo a ese grupo de clases más caras.

---

### ✨ Paso final: aplicamos la regla de Littlewood

Una vez construida la clase combinada, simplemente comparamos esta clase ficticia contra la clase \( j+1 \) con un solo cálculo:

$$
y = F^{-1}\left(1 - \frac{p_{j+1}}{p} \right)
$$

¡Y listo! 🚀

---

### ✅ ¿Por qué es útil?

- Es más simple de aplicar que EMSR-a.
- Tiene buena precisión, especialmente cuando hay **muchas clases superiores con demanda baja**.
- Reduce el número de comparaciones, haciendo el modelo más eficiente.

---

> EMSR-b es una gran herramienta para cuando necesitas una decisión rápida pero fundamentada.  
> En la siguiente página podrás probarla con un ejemplo. 📊
""")


def pagina_ejemplo_emsr_b():
    
    st.set_page_config(page_title="Ejemplo EMSR-b", layout="centered")
    st.title("Ejemplo 4: Aplicando EMSR-b para proteger boletos valiosos")

    st.markdown(r"""
Continuamos con el ejemplo de la gran final de Quidditch 🧹🏆, pero ahora aplicaremos la **heurística EMSR-b** para calcular de manera eficiente el nivel de protección necesario antes de abrir la venta al público de menor precio.

---

### 🎟️ Recordatorio de la política de precios

| Clase  | Descripción                       | Precio | $ \mu $ (demanda esperada) | $ \sigma $ |
|--------|-----------------------------------|--------|-------------------------------|--------------|
| $ c_3 $ | Aficionados normales (anticipados) | \$100  | 1000                          | 300          |
| $ c_2 $ | Aficionados interesados (semana 2) | \$200  | 525                           | 50           |
| $ c_1 $ | Seguidores fieles (último momento) | \$250  | 275                           | 75           |

---

### 🎯 ¿Qué queremos hacer?

Vamos a calcular **cuántos boletos proteger** antes de abrir la venta para la clase $ c_3 $, es decir, para los compradores menos rentables.

Para ello, agrupamos las clases más caras $ c_1 $ y $ c_2 $ como una **clase ficticia**, y luego aplicamos la **regla de Littlewood** contra $ c_3 $.

---

### 🧮 Paso 1: Parámetros de la clase combinada

- Media total:
$$
\mu = 275 + 525 = 800
$$

- Desviación estándar combinada:
$$
\sigma = \sqrt{75^2 + 50^2} = \sqrt{5625 + 2500} = \sqrt{8125} \approx 90.14
$$

- Precio promedio ponderado:
$$
p = \frac{275}{800} \cdot 250 + \frac{525}{800} \cdot 200 = 85.94 + 131.25 = 217.19
$$

---

### 🧠 Paso 2: Aplicamos la regla de Littlewood

$$
y = F^{-1} \left( 1 - \frac{100}{217.19} \right ) = F^{-1}(0.5396)
$$

Buscamos el cuantil 53.96% de una normal con $ \mu = 800 $ y $ \sigma \approx 90.14 $:

$$
y \approx \text{qnorm}(0.5396, 800, 90.14) \approx 815
$$

---

### ✅ Conclusión

Para proteger el ingreso proveniente de las clases de mayor valor, debes **reservar alrededor de 815 boletos**.  
Eso significa que esta semana (clase $ c_3 $) solo deberías vender **hasta 185 boletos** a \$100.

EMSR-b te ofrece una forma rápida y efectiva de tomar esta decisión sin necesidad de múltiples comparaciones. 💡
    """)


def pagina_resumen():
    import streamlit as st

    st.set_page_config(page_title="Resumen", layout="centered")
    st.title("📌 Resumen de conceptos clave")

    st.markdown(r"""
¡Felicidades por llegar hasta aquí! 🎉  
Has recorrido una serie de conceptos que forman la base del **Revenue Management por control de capacidad**.

Esta página resume lo más importante que aprendiste a lo largo del camino.

---

## 🎯 El problema que queremos resolver

Dado un recurso limitado (como asientos, habitaciones o ejemplares), y múltiples segmentos de clientes que pagan precios distintos:

- ¿Cómo debo asignar la capacidad?
- ¿Cuándo conviene proteger espacios para los que pagan más?
- ¿Cuántos espacios debo reservar para cada clase?

---

## 🔑 Conceptos fundamentales

| Concepto | Descripción breve |
|---------|-------------------|
| **Límite de reserva $ b $** | Máximo número de unidades asignadas a la clase de menor precio |
| **Nivel de protección $ y $** | Cantidad mínima reservada para la clase de mayor precio |
| **Función de distribución acumulativa $ F $** | Probabilidad de que la demanda sea menor o igual a un valor |
| **Función de cuantiles $ F^{-1} $** | Valor que corresponde a una probabilidad acumulada dada |

---

## 📐 Regla de decisión óptima (Littlewood)

$$
\overline{F}_A(y^*) = \frac{p_B}{p_A}
\quad \Rightarrow \quad
b^* = C - y^*
$$

Usamos esta fórmula para ubicar el punto donde **ya no conviene vender más a la clase de menor precio**, porque el ingreso marginal se vuelve menor.

---

## 🔁 Heurísticas para múltiples clases

| Heurística | Idea central |
|------------|--------------|
| **EMSR-a** | Aplica la regla de Littlewood varias veces, comparando la clase que se abrirá con cada clase más rentable |
| **EMSR-b** | Agrupa todas las clases más rentables en una sola clase ficticia y aplica una única regla de decisión |

---

## 📊 ¿Qué sigue?

Explora tus propios escenarios, juega con los precios y la demanda, y **aplica estas ideas a casos reales**.  
Recuerda que el Revenue Management es una combinación de **modelo, intuición y experiencia**.

¡Gracias por formar parte de este recorrido! 🙌
    """)

def pagina_practica_emsr():
    
    st.set_page_config(page_title="Ponlo en práctica (EMSR)", layout="centered")
    st.title("Ponlo en práctica: EMSR-a y EMSR-b")

    st.markdown("""
Define un escenario con **3 clases de clientes**, ajusta los parámetros de demanda y precios,  
y compara el nivel de protección sugerido por **EMSR-a** y **EMSR-b**.

---

🎯 **Objetivo:** Calcular cuántas unidades deberías proteger **antes de abrir la clase 3** (la de menor precio).

""")

    st.sidebar.markdown("## Parámetros de cada clase")

    with st.sidebar.expander("Clase 1 (precio más alto)"):
        mu1 = st.number_input("μ₁", value=275)
        sigma1 = st.number_input("σ₁", value=75)
        p1 = st.number_input("Precio clase 1", value=250.0)

    with st.sidebar.expander("Clase 2 (precio medio)"):
        mu2 = st.number_input("μ₂", value=525)
        sigma2 = st.number_input("σ₂", value=50)
        p2 = st.number_input("Precio clase 2", value=200.0)

    with st.sidebar.expander("Clase 3 (precio más bajo)"):
        mu3 = st.number_input("μ₃", value=1000)
        sigma3 = st.number_input("σ₃", value=300)
        p3 = st.number_input("Precio clase 3", value=100.0)

    st.markdown("### 🔍 Resultados:")

    # EMSR-a: suma de dos reglas Littlewood
    y31 = norm.ppf(1 - (p3 / p1), loc=mu1, scale=sigma1)
    y32 = norm.ppf(1 - (p3 / p2), loc=mu2, scale=sigma2)
    y_emsr_a = y31 + y32

    # EMSR-b: clase ficticia
    mu_fict = mu1 + mu2
    sigma_fict = np.sqrt(sigma1**2 + sigma2**2)
    p_fict = (p1 * mu1 + p2 * mu2) / mu_fict
    p_ratio_b = p3 / p_fict
    y_emsr_b = norm.ppf(1 - p_ratio_b, loc=mu_fict, scale=sigma_fict)

    st.latex(rf"""
    \text{{EMSR-a: }}\quad y = F_1^{{-1}}\left(1 - \frac{{{p3}}}{{{p1}}} \right)
    + F_2^{{-1}}\left(1 - \frac{{{p3}}}{{{p2}}} \right) = {y31:.0f} + {y32:.0f} = {y_emsr_a:.0f}
    """)

    st.latex(rf"""
    \text{{EMSR-b: }}\quad y = F^{{-1}}\left(1 - \frac{{{p3:.0f}}}{{{p_fict:.2f}}} \right) = {y_emsr_b:.0f}
    """)

    st.success(f"🔒 Nivel de protección recomendado:\n\n- EMSR-a: {y_emsr_a:.0f} unidades\n- EMSR-b: {y_emsr_b:.0f} unidades")





pages = [st.Page(intro, title="Introducción", icon=":material/home:"), 
         st.Page(segmentos, title="Segmentación del mercado", icon=":material/price_check:"),
         st.Page(supuestos, title="Supuestos del modelo", icon=":material/psychology:"),
         st.Page(elementos, title="Elementos clave", icon=":material/settings:"),
         st.Page(pagina_distribuciones, title="Distribuciones de demanda", icon=":material/grouped_bar_chart:"),
         st.Page(pagina_probabilidades, title="Probabilidad de desbordamiento", icon=":material/stacked_line_chart:"),
         st.Page(pagina_ingreso_exploracion, title="Ingreso esperado", icon=":material/paid:"),
         st.Page(pagina_formula_marginal, title="Construyendo la fórmula del ingreso marginal", icon=":material/psychology_alt:"),
         st.Page(pagina_optimo_teorico, title="Condición óptima", icon=":material/flag:"),
         st.Page(pagina_ejemplo_resuelto_estatico, title="Ejemplo 1: Vuelo y límite de reserva óptimo", icon=":material/task_alt:"),
         st.Page(pagina_ejemplo_editorial, title="Ejemplo 2: Editorial y protección óptima", icon=":material/menu_book:"),
         st.Page(pagina_emsr, title="Múltiples clases (EMSR)", icon=":material/grouped_bar_chart:"),
         st.Page(pagina_ejemplo_emsr, title="Ejemplo 3: Quidditch y EMSR-a", icon=":material/sports_esports:"),
         st.Page(pagina_emsr_b, title="EMSR-b", icon=":material/insights:"),
         st.Page(pagina_ejemplo_emsr_b, title="Ejemplo 4: EMSR-b aplicado al Quidditch", icon=":material/stars:"),
         st.Page(pagina_resumen, title="Resumen", icon=":material/flag_circle:"),
         st.Page(pagina_practica_emsr, title="Ponlo en práctica (EMSR)", icon=":material/science:")         
         ]

pg = st.navigation(pages)
pg.run()


