# FROM python:3.12-alpine3.20

# # Upgrade apk packages to fix vulnerabilities
# # RUN apk update && apk upgrade --no-cache

# # # Install security updates and common dependencies
# # RUN apk add --no-cache --upgrade \
# # 	libffi \
# # 	openssl \
# # 	&& rm -rf /var/cache/apk/*

# WORKDIR /app
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 5000
# CMD ["python", "app.py"]
FROM python:3.12-alpine3.20

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]