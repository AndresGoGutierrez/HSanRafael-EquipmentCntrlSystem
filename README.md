# 🏥 Sistema de Control de Ingreso de Equipos Tecnológicos y Biomédicos Externos (PDS-006)

## 📘 Descripción General

El **Sistema de Control de Ingreso de Equipos Tecnológicos y Biomédicos Externos (PDS-006)** es una aplicación desarrollada en **FastAPI** que permite registrar, monitorear y controlar el ingreso y egreso de equipos externos en el **Hospital San Rafael de Tunja**.  

Este sistema busca reemplazar los procesos manuales de registro mediante un sistema digital **seguro, trazable y confiable**, garantizando la integridad de la información y el cumplimiento de los protocolos institucionales.

---

## 🎯 Objetivos Principales

- Registrar el ingreso y salida de equipos tecnológicos y biomédicos de manera automatizada.
- Implementar la lectura de **códigos QR** para optimizar el proceso de control.
- Garantizar la **verificación de salida** de los equipos registrados.
- Mantener **logs de trazabilidad** para auditoría y control.
- Generar **reportes dinámicos** por fecha o rango de fechas.
- Incorporar herramientas de **monitoreo de rendimiento y métricas en tiempo real**.

---

## 🧩 Arquitectura del Sistema

El sistema se desarrolla bajo los principios de **Arquitectura Limpia (Clean Architecture)** y **Arquitectura Hexagonal (Ports & Adapters)**, aplicando los fundamentos **SOLID** para garantizar mantenibilidad, testabilidad y escalabilidad.  

Esta estructura modular permite aislar la lógica de negocio de la infraestructura, facilitando la integración con nuevos componentes como servicios externos o adaptadores de persistencia.

---

## ⚙️ Tecnologías Principales

| Categoría | Tecnología / Herramienta |
|------------|---------------------------|
| Lenguaje base | Python 3.10+ |
| Framework backend | FastAPI |
| Base de datos | PostgreSQL (SQLAlchemy + Alembic) |
| Autenticación | JWT + Passlib + Python-Jose |
| Monitoreo | Prometheus + Grafana |
| Testing | Pytest + Coverage |
| Contenedores | Docker Compose |
| Métricas | prometheus_fastapi_instrumentator |
| Documentación API | Swagger / ReDoc (integrados en FastAPI) |

---

## 📦 Instalación y Configuración

### 🔹 Requisitos Previos

- **Python 3.10 o superior**
- **Docker y Docker Compose**
- **Git**

---

### 🔹 Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/pds006-control-equipos.git
cd pds006-control-equipos

python -m venv venv
# Activar entorno virtual
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
alembic upgrade head

#Ejecutar las Pruebas con Unittest
python -m unittest discover test/unittest/

#Ejecutar las Pruebas con Pytest
pytest --cov=app tests/ -v


#Ejecucion del proyecto
uvicorn app.main:app --reload

Por defecto, la aplicación estará disponible en:

- **API Base:** [http://localhost:8000](http://localhost:8000)  
- **Documentación Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)  
- **Documentación ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)  

---

## 📊 Monitoreo y Métricas

El sistema cuenta con monitoreo en tiempo real a través de **Prometheus** y visualización de métricas mediante **Grafana**.

### 🔹 Levantar los Servicios de Monitoreo

```bash
docker compose -p equipment_monitoring up -d --build

## 📈 Monitoreo de Rendimiento con Grafana

El rendimiento del sistema puede ser analizado directamente en **Grafana**, utilizando las métricas recolectadas por **Prometheus**.  
Estas métricas permiten evaluar el comportamiento del sistema, detectar cuellos de botella y garantizar la estabilidad de la aplicación.

### 🔹 Principales Métricas Disponibles

- **Latencia de endpoints:** tiempo promedio de respuesta por solicitud.  
- **Cantidad de solicitudes por segundo:** volumen de peticiones atendidas.  
- **Porcentaje de errores HTTP:** tasa de fallos o respuestas no exitosas.  
- **Tiempo medio de respuesta:** promedio global de procesamiento de solicitudes.  
- **Consumo de CPU y memoria:** monitoreo de recursos del servicio FastAPI.  

---

## 🧠 Buenas Prácticas Aplicadas

- Implementación de **principios SOLID** en la estructura de código.  
- Aplicación de **Clean Code** y consistencia en la nomenclatura (todo en inglés).  
- **Separación de capas** según la arquitectura hexagonal (infraestructura, dominio, aplicación).  
- Uso de **type hints** y documentación con **docstrings** descriptivos.  
- Cumplimiento de las normas de estilo **PEP8**.  
- Cobertura mínima de pruebas **≥ 80%**.  
- Integración continua con herramientas de monitoreo (**Prometheus**, **Grafana**) y testing automatizado (**Pytest**).  

---

## 👥 Equipo de Desarrollo

| Nombre | Rol | Responsabilidad |
|---------|-----|-----------------|
| **Nicolás Otero** | Desarrollador | 
| **Andrés Gómez** | Desarrollador |
| **Wilton Higuera** | Desarrollador | 
  **Juan David Gomez** | Desarrollador | 
---

## 📄 Licencia

Proyecto académico desarrollado bajo licencia **MIT**  
Universidad Santo Tomás – Espacio Académico **Calidad de Software**.

---

## 📚 Referencias Técnicas

- **IEEE Std. 730-1989** — *Software Quality Assurance Plans*  
- **IEEE Std. 829-2008** — *Software and System Test Documentation*  
- **ISO/IEC 25010:2011** — *System and Software Quality Models*  
