# origin sim.py from Chat

import math
import numpy


def paRandom( ) :
  # pick random point on surface of a sphere, compute PA of projection along the line of sight
  # coordinate system: +Z points at observer; +X, +Y as in polarization measurements; PA = atan(y/x);
  #    ... note: atan, not atan2, because we want all PAs within 180 degree span
  # method (suggested by Wolfram Mathworld): generate 3 gaussian random variables x,y,z; then
  #    compute 1/sqrt(x^2 + y^2 +z^2) * [x y z]

  x = numpy.random.normal()
  y = numpy.random.normal()
  z = numpy.random.normal()  
  length = math.sqrt(x*x + y*y + z*z)
  length_pos = math.sqrt(x*x + y*y)
  incl_angle = 180./math.pi * math.atan2(length_pos,z)
  #this gives angles in range [0,pi], not the default [-pi, pi] range of atan2
  #this is excatly what needed when comparing the inclination angle difference of two vectors with
  #the position angle difference inferred from dust polarization segments,
  #because dust polarization only show the orientation in range [0,pi], not the direction in range [-pi, pi]
  return [ incl_angle, x/length, y/length, z/length ]

def paDifUniform( outfile ) :
  # choose 2 points randomly on surface of sphere; compute PA projected on the plane of
  #  the sky for each of them; then compute angular difference of the two directions;
  #  reorder and compute cumulative distribution function

  ntrials = 100000 #100000
  nsamples = 1000 #1000
  zratio = numpy.zeros( ntrials, dtype=float )
  adif = 0.
  count = 0
  for n in range( 0, ntrials ) :
    [pa1,x1,y1,z1] = paRandom() #core field
    [pa2,x2,y2,z2] = paRandom() #envelope field
    zratio[n] = z1/z2
    if (zratio[n] > 3.0):
        adif_tmp = abs(pa1 - pa2)
        adif += numpy.where(adif_tmp > 180, 360.-adif_tmp, adif_tmp)
        count += 1

  zratioSorted = numpy.msort(zratio)
  nskip = ntrials/nsamples
  print "the mean inclination angle difference in degrees =", adif/count
  fout = open( outfile, "w" )
  for n in range( 0, ntrials, nskip ) :
    fout.write("%10.3f  %10.3f\n" % (zratioSorted[n], float(n)/float(ntrials) ) )
  fout.write("%10.3f  %10.3f\n" % (zratioSorted[ntrials-1], 1.0 ) )


def examples( ) :
  paDifCone( 180, "paDif180.dat" )		# outflows randomly oriented w/ respect to field
  paDifCone( 20, "paDif20.dat" )		# outflows within 20 degrees of field direction

paDifUniform("simBangle.dat" )
