#!/usr/bin/python

import os, inspect
DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
activate_this = DIR + "/venv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

from astropy.io import fits
from glob import glob

def list_fits(tgtDir=None, prefix = "", imageType = "fit"):
	filePattern = prefix + "*." + imageType
	
	if tgtDir is None:
		tgtDir = os.getcwd()
	else:
		os.chdir(tgtDir)

	images = glob(filePattern)
	images.sort()

	return images

def clean_header(filename):
	data,hdr = fits.getdata(filename, header=True)

	hdr['SITELAT'] = hdr['SITELAT'].replace('d', ' ')
	hdr['SITELAT'] = hdr['SITELAT'].replace('m', ' ')
	hdr['SITELAT'] = hdr['SITELAT'].replace('s', ' ')

	isSouth = hdr['SITELAT'].find("  S") >= 0
	if isSouth:
		hdr['SITELAT'] = hdr['SITELAT'].replace("  S", "")
		hdr['SITELAT'] = "-" + hdr['SITELAT']
	else:
		hdr['SITELAT'] = hdr['SITELAT'].replace("  N", "")


	hdr['SITELONG'] = hdr['SITELONG'].replace('d', ' ')
	hdr['SITELONG'] = hdr['SITELONG'].replace('m', ' ')
	hdr['SITELONG'] = hdr['SITELONG'].replace('s', ' ')

	isWest = hdr['SITELONG'].find("  W") >= 0
	if isWest:
		hdr['SITELONG'] = hdr['SITELONG'].replace("  W", "")
		hdr['SITELONG'] = "-" + hdr['SITELONG']
	else:
		hdr['SITELONG'] = hdr['SITELONG'].replace("  E", "")

	fits.writeto(filename, data, hdr, overwrite=True)

if __name__ == "__main__":
	images = list_fits(TGT)

	for f in images:
		print("Processing file: " + f)
		clean_header(f)
