file="${0}"
dir=`dirname "${file}"`
cd "${dir}" || exit 1
make html
if [ "`uname`" = "Darwin" ]; then
  open "_build/html/index.html"
elif [ "`uname`" = "Linux" ]; then
  xdg-open "_build/html/index.html"
else
  exit 1
fi
