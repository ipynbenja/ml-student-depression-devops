# Registro de cambios

Todas las modificaciones notables de este proyecto serán documentadas en este archivo. Esto refiere a todo lo que afecte cómo se entiende, ejecuta y/o instala el proyecto.

## - 2026-08-28

### Añadido
- Se añadió documentación CHANGELOG.md para la documentación de cambios notables.
- Se añadió el archivo YAML para el workflow de Integración Continua (CI) que se ejecutará por cada push o pull request realizado a la rama main.

### Cambiado
- Se actualizó la documentación README.md para esta nueva versión del proyecto, donde el propósito es integrar prácticas de la cultura DevOps, se define nuevo objetivo, estrategia de ramas y commits.

## - 2026-08-31

### Añadido
- Se añadió un entorno de testing para realizar pruebas unitarias a la API utilizando `pytest` y `TestClient` para los endpoints de la API (`/`, `/predict` y `/predict-file`).
- Se esperará aprobación del docente para antes de integrar las pruebas en el workflow CI para su ejecución automática. 

### Cambiado
- Se añadieron filtros de exclusión (`paths-ignore`) en GitHub Actions para omitir la ejecución del pipeline en cambios exclusivos de documentación (para cualquier archvio .md)
- Actualizaciones pequeñas en .gitignore y requirements.txt para las pruebas unitarias

### Corregido
- Error en una fecha de este documento.