#!/usr/bin/python

import os, inspect, sys
DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
activate_this = DIR + "/venv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

from astropy.io import fits
from glob import glob


def list_fits(prefix = "", imageType = "fit"):
	filePattern = prefix + "*." + imageType

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


def process_subfolders(tgtDir = None):
	if tgtDir is None:
		tgtDir = os.getcwd()
	else:
		os.chdir(tgtDir)

	for subdir, dirs, files in os.walk(tgtDir):
		os.chdir(subdir)
		images = list_fits()

		for f in images:
			print "Processing file:", os.path.join(subdir,f)
			try:
				clean_header(f)
			except KeyError:
				pass
			except:
				print "*** Error processing file:", f," ***"
				raise

		os.chdir(tgtDir)


if __name__ == "__main__":
	try:
		tgtDir = sys.argv[1]
	except IndexError:
		tgtDir = None
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise

	process_subfolders(tgtDir)