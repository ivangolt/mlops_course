FROM mambaorg/micromamba

WORKDIR /app

COPY . /app

RUN micromamba create -f env.yml
RUN micromamba run -n mlops_course poetry install 

EXPOSE 8888

# ENTRYPOINT ["micromamba", "run", "-n", "mlops_course", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root" ]
