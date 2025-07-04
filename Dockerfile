# Docker 설정파일
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app/main.py", "--server.headless=true", "--server.port=8501"]
