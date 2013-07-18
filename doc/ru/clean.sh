file="${0}"
dir=`dirname "${file}"`
cd "${dir}" || exit 1
make clean
