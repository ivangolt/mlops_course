FROM mambaorg/micromamba
USER root
WORKDIR /app 
COPY env.yml /app/env.yml


RUN micromamba create -f env.yml
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock 
RUN micromamba run -n mlops_course poetry install \
    && micromamba run -n mlops_course poetry config virtualenvs.create false
 
EXPOSE 8888

# ENTRYPOINT ["micromamba", "run", "-n", "mlops_course", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root" ]
