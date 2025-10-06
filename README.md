# Bizz Summit 2025 - Demo Microsoft Fabric CI/CD

Este repositorio contiene una demostración completa de un flujo de trabajo CI/CD para Microsoft Fabric, presentado en el Bizz Summit 2025. El proyecto ilustra cómo implementar integración y despliegue continuos para artefactos de Fabric utilizando GitHub Actions.

## 🎯 Propósito del Proyecto

Esta demo muestra cómo automatizar el despliegue de artefactos de Microsoft Fabric desde un repositorio Git hacia workspaces de Fabric, implementando mejores prácticas de DevOps para plataformas de datos.

## 📋 Requisitos Previos

- [Microsoft Fabric workspace](https://docs.microsoft.com/en-us/fabric/get-started/create-workspaces) configurado
- [Service Principal de Azure AD](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) con permisos en Fabric
- Repositorio GitHub con GitHub Actions habilitado

## 🏗️ Estructura del Proyecto

### 📁 `fabric-artifacts/`

Contiene todos los artefactos de Microsoft Fabric exportados en formato de desarrollo:

#### 📊 **Demo Bizz Summit 2025.pbip**
- **Descripción**: Archivo de proyecto de Power BI en formato PBIP (Power BI Project)
- **Propósito**: Permite el desarrollo colaborativo y control de versiones de informes Power BI
- **Documentación**: [Power BI Project files (.pbip)](https://docs.microsoft.com/en-us/power-bi/developer/projects/projects-overview)

#### ⚙️ **parameter.yml**
- **Descripción**: Archivo de configuración para la parametrización de artefactos
- **Propósito**: Define valores que serán reemplazados automáticamente durante el despliegue (IDs de workspace, conexiones, etc.)
- **Documentación**: [Fabric CI/CD Parameterization](https://microsoft.github.io/fabric-cicd/latest/how_to/parameterization/)

#### 📈 **Demo Bizz Summit 2025.Report/**
- **Descripción**: Definición del informe Power BI descompuesta en archivos JSON
- **Componentes**:
  - `definition.pbir`: Metadatos del informe
  - `report.json`: Configuración de páginas y visualizaciones
  - `CustomVisuals/`: Visualizaciones personalizadas
  - `StaticResources/`: Temas y recursos estáticos

#### 🗃️ **Demo Bizz Summit 2025.SemanticModel/**
- **Descripción**: Modelo semántico (dataset) en formato TMDL (Tabular Model Definition Language)
- **Componentes**:
  - `definition.pbism`: Metadatos del modelo
  - `definition/`: Archivos TMDL con definiciones de tablas, relaciones y medidas
- **Documentación**: [TMDL Overview](https://docs.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview)

#### 🏠 **lh_data.Lakehouse/**
- **Descripción**: Definición del Lakehouse de Fabric
- **Propósito**: Almacenamiento de datos en formato Delta Lake
- **Documentación**: [Microsoft Fabric Lakehouse](https://docs.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview)

#### 📓 **nb_process_data.Notebook/**
- **Descripción**: Notebook de Fabric para procesamiento de datos
- **Contenido**: Scripts PySpark para transformar archivos CSV a tablas Delta
- **Documentación**: [Fabric Notebooks](https://docs.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)

#### 🔄 **pip_extract_data.DataPipeline/**
- **Descripción**: Pipeline de datos de Fabric
- **Propósito**: Automatiza la extracción y carga de datos desde archivos Excel
- **Documentación**: [Fabric Data Pipelines](https://docs.microsoft.com/en-us/fabric/data-factory/create-first-pipeline-with-sample-data)

### 📁 `scripts/`

Contiene los scripts Python que implementan la lógica de CI/CD:

#### 🚀 **run_fabric_cicd.py**
- **Descripción**: Script principal para el despliegue automatizado de artefactos
- **Funcionalidades**:
  - Autenticación con Service Principal
  - Publicación de todos los artefactos al workspace de destino
  - Limpieza de artefactos huérfanos (no presentes en el repositorio)
- **Dependencias**: [fabric-cicd Python package](https://pypi.org/project/fabric-cicd/)
- **📖 [Ver documentación detallada →](./docs/run_fabric_cicd.md)**

#### 🔄 **run_fabric_update_ds.py**
- **Descripción**: Script para actualizar datasets y gestionar permisos
- **Funcionalidades**:
  - Toma de control (takeover) de datasets por Service Principal
  - Actualización de conexiones a fuentes de datos
  - Configuración de gateways y credenciales
- **APIs utilizadas**: [Power BI REST API](https://docs.microsoft.com/en-us/rest/api/power-bi/)
- **📖 [Ver documentación detallada →](./docs/run_fabric_update_ds.md)**

## 🔧 Variables de Entorno Requeridas

El proyecto utiliza las siguientes variables de entorno que deben configurarse en GitHub Secrets:

```bash
FABRIC_CLIENT_ID          # ID del Service Principal
FABRIC_CLIENT_SECRET      # Secret del Service Principal  
FABRIC_TENANT_ID          # ID del tenant de Azure AD
FABRIC_WORKSPACE_ID       # ID del workspace de destino
TARGET_ENVIRONMENT_NAME   # Nombre del entorno (dev/prod)
FABRIC_CLOUD_CONNECTION_ID # ID de la conexión en la nube (opcional)
IS_ONLY_UPDATE           # Flag para solo actualizar (true/false)
```

## 🤖 GitHub Actions Workflow

### 📁 `.github/workflows/deploy-fabric.yml`
- **Descripción**: Workflow principal que automatiza todo el proceso de CI/CD
- **Trigger**: Se ejecuta automáticamente en push a `main` o manualmente
- **Funcionalidades**:
  - Configuración automática del entorno Python
  - Ejecución secuencial de scripts de despliegue
  - Manejo de secrets y variables de entorno
  - Gestión de errores y logging
- **📖 [Ver documentación detallada del workflow →](./docs/deploy-fabric-workflow.md)**

## 🚀 Flujo de Trabajo CI/CD

1. **Desarrollo Local**: Los desarrolladores trabajan con los artefactos de Fabric exportados
2. **Control de Versiones**: Los cambios se commitean al repositorio Git
3. **Trigger de Despliegue**: GitHub Actions detecta cambios en la rama principal
4. **Autenticación**: El workflow se autentica usando el Service Principal
5. **Parametrización**: Los valores se reemplazan según el entorno de destino
6. **Despliegue**: Los artefactos se publican al workspace de Fabric
7. **Limpieza**: Se eliminan artefactos huérfanos del workspace

## � Documentación Interna Detallada

### 🔧 Scripts de Despliegue
- **[run_fabric_cicd.py](./docs/run_fabric_cicd.md)** - Despliegue principal de artefactos (análisis paso a paso)
- **[run_fabric_update_ds.py](./docs/run_fabric_update_ds.md)** - Gestión de datasets y conexiones (código explicado)

### 🤖 Automatización
- **[deploy-fabric.yml](./docs/deploy-fabric-workflow.md)** - Workflow de GitHub Actions (configuración completa)

## 📚 Documentación Externa

- [Microsoft Fabric CI/CD](https://microsoft.github.io/fabric-cicd/)
- [Fabric Git Integration](https://docs.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration)
- [Power BI Deployment Pipelines](https://docs.microsoft.com/en-us/power-bi/create-reports/deployment-pipelines-overview)
- [GitHub Actions for Azure](https://docs.microsoft.com/en-us/azure/developer/github/github-actions)

## 🤝 Contribución

Este proyecto fue desarrollado como material de demostración para el Bizz Summit 2025. Para implementar en tu organización, adapta las configuraciones según tus necesidades específicas.

---

*Desarrollado para Bizz Summit 2025 - Automatización de Microsoft Fabric con DevOps*
