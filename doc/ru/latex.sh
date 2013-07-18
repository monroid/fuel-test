file="${0}"
dir=`dirname "${file}"`
cd "${dir}" || exit 1
make latex
cd "_build/latex" || exit 1
make
mv "FuelTestingSuit.pdf" "../.."
cd "../.."
if [ "`uname`" = "Darwin" ]; then
  open "FuelTestingSuit.pdf"
elif [ "`uname`" = "Linux" ]; then
  xdg-open "FuelTestingSuit.pdf"
else
  exit 1
fi
