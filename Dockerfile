# Utiliser l'image légère de Nginx
FROM nginx:alpine

# Copier le fichier HTML généré par le pipeline vers le dossier par défaut de Nginx
COPY public/index.html /usr/share/nginx/html/index.html

# Exposer le port 80
EXPOSE 80