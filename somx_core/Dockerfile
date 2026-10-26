# Isticmaal nuqulka casriga ah ee Python ee fudud
FROM python:3.10-slim

# Deji galka shaqada ee gudaha container-ka
WORKDIR /app

# Koobi garow faylka requirements.txt oo ku rakib maktabadaha
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Koobi garow dhammaan faylasha mashruuca
COPY . .

# Fur dekedda (port) 8000 ee FastAPI
EXPOSE 8000

# Amarka uu container-ku bilaabmarka ku shaqeynayo
CMD ["uvicorn", "somx_core.main:app", "--host", "0.0.0.0", "--port", "8000"]
