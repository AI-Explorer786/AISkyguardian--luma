# 1️⃣ Use Python as base image
FROM python:3.9

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy all project files
COPY . /app

# 4️⃣ Install dependencies
RUN pip install -r requirements.txt

# 5️⃣ Expose port 5000
EXPOSE 5000

# 6️⃣ Run Flask app
CMD ["python", "app.py"]
