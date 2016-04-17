FROM spectralcoding/aspnet:1.0.0-rc1-update2-coreclr

COPY . /app
WORKDIR /app
RUN ["dnu", "restore"]

EXPOSE 80
ENTRYPOINT ["dnx", "-p", "project.json", "web"]
