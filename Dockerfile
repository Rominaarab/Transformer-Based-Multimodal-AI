FROM python:3.11-slim-bookworm
ENV PYTHONUNBUFFERED=1 MPLBACKEND=Agg OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
WORKDIR /pipeline
COPY requirements-demo.txt .
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.6.0 \
    && pip install --no-cache-dir -r requirements-demo.txt
COPY Thesis_pieline_demo.ipynb .
WORKDIR /output
CMD ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--ExecutePreprocessor.timeout=7200", "--ExecutePreprocessor.kernel_name=python3", "--output", "/output/executed.ipynb", "/pipeline/Thesis_pieline_demo.ipynb"]
