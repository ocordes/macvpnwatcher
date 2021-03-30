#!/bin/sh

inkscape=/Applications/Inkscape.app/Contents/MacOS/inkscape
insvg="appicon appicon-dark appicon-offline appicon-offline-dark"

icondir=src/icons/

for icon in ${insvg}
do
   svg_image=${icon}.svg
   outdir=${icon}.iconset
   mkdir ${outdir}
   for sz in 16 32 128 256 512
   do
      echo "[+] Generate ${sz}x${sz} png..."
      $inkscape  --export-type=png --export-filename=${outdir}/icon_${sz}x${sz}.png -w $sz -h $sz ${svg_image}
      $inkscape  --export-type=png --export-filename=${outdir}/icon_${sz}x${sz}@2x.png -w $((sz*2)) -h $((sz*2)) ${svg_image}
   done
   iconutil --convert icns --output ${icondir}${icon}.icns ${outdir}
   echo "[v] The icon is saved to ${icondir}${icon}.icns."
   rm -rf ${outdir}
done
