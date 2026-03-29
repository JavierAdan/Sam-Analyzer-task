params.sam = ""
params.script = ""

process analyze_sam {
    tag "SAM analysis"

    input:
    path samfile
    path script

    output:
    path "resultado.txt"

    """
  uv run python3 ${script} ${samfile} > resultado.txt 2> log.txt
    """
}

workflow {
    if (!params.sam) {
        error "Debes proporcionar un archivo SAM con --sam"
    }

    if (!params.script) {
        error "Debes proporcionar el script con --script"
    }

    analyze_sam(params.sam, params.script)
}
