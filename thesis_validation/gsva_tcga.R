# Usage: Rscript gsva_tcga.R TCGA.LUAD.sampleMap_HiSeqV2.gz output_dir
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) stop("Supply the original Xena expression file and output directory.")
if (!requireNamespace("GSVA", quietly = TRUE) || !"gsvaParam" %in% getNamespaceExports("GSVA")) {
    stop("Install a Bioconductor GSVA release that exports gsvaParam().")
}

# The four gene lists are transcribed from thesis page 30.
sets <- list(
    Glycolysis = c("HK2", "GPI", "PFKM", "ALDOA", "TPI1", "GAPDH", "PGK1", "ENO1", "PKM"),
    Arginine = c("ARG1", "ARG2", "ASS1", "ASL", "OTC", "CPS1"),
    Tryptophan = c("IDO1", "IDO2", "TDO2", "KYNU", "KMO", "HAAO"),
    Glutamine = c("GLS", "GLS2", "GLUD1", "GLUL", "SLC1A5")
)

tab <- read.delim(args[[1]], check.names = FALSE, quote = "", comment.char = "")
genes <- tab[[1]]
primary <- grepl("^TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-01$", names(tab))
if (!any(primary) || anyDuplicated(names(tab)[primary])) stop("Invalid primary tumor sample IDs.")
expr <- as.matrix(tab[, primary, drop = FALSE])
if (!is.numeric(expr)) stop("Expression columns must be numeric.")
# Keep the transcriptome as the ranking background. Exclude ambiguous and
# non-informative rows explicitly, and record coverage after filtering.
valid <- nzchar(genes) & !duplicated(genes) & !duplicated(genes, fromLast = TRUE)
valid <- valid & rowSums(!is.finite(expr)) == 0L
valid <- valid & apply(expr, 1L, function(row) length(unique(row)) > 1L)
expr <- expr[valid, , drop = FALSE]
rownames(expr) <- genes[valid]
coverage <- do.call(rbind, lapply(names(sets), function(set) {
    data.frame(pathway = set, gene = sets[[set]], mapped = sets[[set]] %in% rownames(expr))
}))
dir.create(args[[2]], recursive = TRUE, showWarnings = FALSE)
write.table(coverage, file.path(args[[2]], "gsva_coverage.tsv"),
            sep = "\t", row.names = FALSE, quote = FALSE)
if (any(tapply(coverage$mapped, coverage$pathway, sum) < 3L)) {
    stop("A pathway has fewer than three mapped genes. Inspect gsva_coverage.tsv.")
}
param <- GSVA::gsvaParam(expr, sets, kcdf = "Gaussian", minSize = 3)
scores <- GSVA::gsva(param, verbose = FALSE)
stopifnot(setequal(rownames(scores), names(sets)),
          identical(colnames(scores), colnames(expr)), all(is.finite(scores)))
result <- data.frame(sample_id = colnames(scores), t(scores), check.names = FALSE)
write.table(result, file.path(args[[2]], "gsva_scores.tsv"),
            sep = "\t", row.names = FALSE, quote = FALSE)
writeLines(capture.output(sessionInfo()), file.path(args[[2]], "gsva_session.txt"))
