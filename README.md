# backgroundColorConverter

Convert background color. 

@TODO: Optimise transformer's kernel size to remove edge glitch or sharpen edge. Or, rather, use segmentation approach instead... 

options:
  -h, --help            show help message and exit
  -o OUTDIR, --outdir OUTDIR
  -f FROMCOLOR, --fromColor FROMCOLOR
  -t TOCOLOR, --toColor TOCOLOR

UPDATE#1: 
This program supports watermark removal now. Simply specify the background color in -f --fromColor.
