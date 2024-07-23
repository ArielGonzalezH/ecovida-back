FROM python:3.8-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos y instalar dependencias
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar el resto del código de la aplicación
COPY . /app

# Exponer el puerto
EXPOSE 7000

# Comando para ejecutar el servicio
CMD ["python", "run_services.py"]
