# ✈️ Aplicación interactiva: Asignación de capacidad y maximización de ingresos

Esta aplicación fue desarrollada como parte del curso de Analítica para la Inteligencia de Negocios, y tiene como objetivo ayudarte a explorar y comprender los principios del **Revenue Management** mediante una interfaz interactiva construida con Streamlit.

Podrás aprender paso a paso:

- Cómo se asignan espacios entre distintos segmentos de clientes
- Cómo calcular el ingreso esperado y tomar decisiones óptimas
- Qué son los límites de reserva y niveles de protección
- Cómo aplicar heurísticas como **EMSR-a** y **EMSR-b**
- Y todo esto ¡con ejemplos explicativos, escenarios reales y casos divertidos como un partido de Quidditch!

---

## 🚀 ¿Cómo ejecutar la aplicación?

Puedes hacerlo de dos maneras:

---

### ✅ Opción 1: Usar GitHub Codespaces (recomendado)

1. Asegúrate de tener una cuenta de GitHub.
2. Ve al repositorio y haz clic en el botón **`<> Code` → `Open with Codespaces` → `New codespace`**.
3. Una vez cargado el entorno, abre una terminal y ejecuta:

```bash
streamlit run asigna.py
```

¡Y listo! La app se abrirá en una nueva pestaña del navegador.  
Es la forma más fácil de ejecutarla sin tener que instalar nada en tu computadora.

---

### 💻 Opción 2: Ejecutar localmente en tu máquina

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # en Mac/Linux
venv\Scripts\activate     # en Windows
```

3. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:

```bash
streamlit run asigna.py
```

---

## 🧠 Requisitos

- Python 3.8 o superior
- Librerías utilizadas:
  - `streamlit`
  - `numpy`
  - `scipy`
  - `matplotlib` (solo si agregas gráficas adicionales)

---

## 📚 Créditos y referencias

Esta aplicación fue diseñada como herramienta educativa interactiva para apoyar el aprendizaje de los conceptos de gestión de ingresos.  
Si te interesa profundizar en estos temas, puedes consultar:

- Talluri, K. T., & Van Ryzin, G. J. (2004). *The Theory and Practice of Revenue Management*.
- MIT OpenCourseWare: Revenue Management (https://ocw.mit.edu)

---

## ✨ Autor

**Fernando Gómez-García**  
Profesor del curso *Analítica para la Inteligencia de Negocios*

---

¿Listo para aprender a tomar decisiones inteligentes con recursos limitados?  
¡Dale run a la app y comienza a explorar! 🎯📊

---

## 🪪 Licencia

Este proyecto está distribuido bajo la licencia [MIT](LICENSE).  
Eres libre de usar, modificar y compartir esta aplicación, siempre y cuando mantengas los créditos correspondientes.


```

