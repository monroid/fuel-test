file="${0}"
dir=`dirname "${file}"`
cd "${dir}" || exit 1
make latex
cd "_build/latex" || exit 1
make
mv "FuelTest.pdf" "../.."
cd "../.."
if [ "`uname`" = "Darwin" ]; then
  open "FuelTest.pdf"
elif [ "`uname`" = "Linux" ]; then
  xdg-open "FuelTest.pdf"
else
  exit 1
fi
