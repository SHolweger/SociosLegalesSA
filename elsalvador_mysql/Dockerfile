# Usar una imagen oficial de Python más estable
FROM python:3.11.7-slim-bullseye

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt primero (para aprovechar el cache)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la app
COPY . .

# Exponer el puerto por donde corre Flask
EXPOSE 5001

# Comando para iniciar el microservicio
CMD ["python", "app.py"]
