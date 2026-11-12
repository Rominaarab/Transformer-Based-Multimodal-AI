FROM bioconductor/bioconductor_docker:RELEASE_3_21
RUN Rscript -e 'BiocManager::install("GSVA", ask=FALSE, update=FALSE); stopifnot("gsvaParam" %in% getNamespaceExports("GSVA"))'
COPY gsva_tcga.R /opt/gsva_tcga.R
ENTRYPOINT ["Rscript", "/opt/gsva_tcga.R"]
