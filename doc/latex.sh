file="${0}"
dir=`dirname "${file}"`
cd "${dir}" || exit 1
make latex
cd "_build/latex" || exit 1
make
mv "FuelTestingSuit.pdf" "../.."
