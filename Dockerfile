FROM python:3.9

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY . /app

EXPOSE 8501

WORKDIR /app

ENTRYPOINT ["streamlit","run"]
CMD ["src/app.py"]