FROM python:3


# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add source code
COPY src src


ENTRYPOINT ["python"]
CMD ["src/app.py"]
