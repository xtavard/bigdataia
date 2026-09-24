FROM python:3.12-slim

WORKDIR /workspace

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    scikit-learn \
    duckdb \
    polars \
    pyarrow \
    jupyterlab \
    ipykernel

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
