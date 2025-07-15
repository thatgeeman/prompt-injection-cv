#! /bin/bash 

# This script compiles the LaTeX document using pdflatex and bibtex.
cd tex/ || exit 1

for TEXFILE in {avery_taylor,alex_smith,jane_doe}; do
    pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder "${TEXFILE}.tex"
    pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder "${TEXFILE}.tex"
    
    # prepare the prompt injected file
    
    cat "${TEXFILE}.tex" | head -n -1 > "${TEXFILE}_extra.tex"
    # get name in sentence case
    NAME=$(echo "${TEXFILE}" | sed -e 's/_/ /g' | sed -e 's/\b\(.\)/\u\1/g')
    cat extra_footer.tex | sed -e s/"NAME"/"${NAME}"/ >> "${TEXFILE}_extra.tex"
    pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder -jobname="${TEXFILE}_extra" "${TEXFILE}_extra".tex
    pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder -jobname="${TEXFILE}_extra" "${TEXFILE}_extra".tex

    if [ -f "${TEXFILE}_extra.pdf" ] && [ -f "${TEXFILE}.pdf" ]; then
        mv "${PWD}/${TEXFILE}_extra.pdf" ..
        mv "${PWD}/${TEXFILE}.pdf" ..
    fi

done

cd .. || exit 1
