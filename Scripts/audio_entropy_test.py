#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 18:13:22 2018

@author: "Anirban Das"
"""

#!/usr/bin/env python3
#
# Released under the HOT-BEVERAGE-OF-MY-CHOICE LICENSE: Bastian Rieck wrote
# this script. As long you retain this notice, you can do whatever you want
# with it. If we meet some day, and you feel like it, you can buy me a hot
# beverage of my choice in return.

import numpy
import scipy.io.wavfile
import scipy.stats
import sys

def chunks(l, k):
  """
  Yields chunks of size k from a given list.
  """
  for i in range(0, len(l), k):
    yield l[i:i+k]

def shortTermEnergy(frame):
  """
  Calculates the short-term energy of an audio frame. The energy value is
  normalized using the length of the frame to make it independent of said
  quantity.
  """
  return sum( [ abs(x)**2 for x in frame ] ) / len(frame)

def rateSampleByVariation(chunks):
  """
  Rates an audio sample using the coefficient of variation of its short-term
  energy.
  """
  energy = [ shortTermEnergy(chunk) for chunk in chunks ]
  return scipy.stats.variation(energy)

def zeroCrossingRate(frame):
  """
  Calculates the zero-crossing rate of an audio frame.
  """
  signs             = numpy.sign(frame)
  signs[signs == 0] = -1

  return len(numpy.where(numpy.diff(signs))[0])/len(frame)

def rateSampleByCrossingRate(chunks):
  """
  Rates an audio sample using the standard deviation of its zero-crossing rate.
  """
  zcr = [ zeroCrossingRate(chunk) for chunk in chunks ]
  return numpy.std(zcr)

def entropyOfEnergy(frame, numSubFrames):
  """
  Calculates the entropy of energy of an audio frame. For this, the frame is
  partitioned into a number of sub-frames.
  """
  lenSubFrame = int(numpy.floor(len(frame) / numSubFrames))
  shortFrames = list(chunks(frame, lenSubFrame))
  energy      = [ shortTermEnergy(s) for s in shortFrames ]
  totalEnergy = sum(energy)
  energy      = [ e / totalEnergy for e in energy ]

  entropy = 0.0
  for e in energy:
    if e != 0:
      entropy = entropy - e * numpy.log2(e)

  return entropy

def rateSampleByEntropy(chunks):
  """
  Rates an audio sample using its minimum entropy.
  """
  entropy = [ entropyOfEnergy(chunk, 20) for chunk in chunks ]
  return numpy.min(entropy)

#
# main
#

# Frame size in ms. Will use this quantity to collate the raw samples
# accordingly.
frameSizeInMs = 0.01

frequency          = 44100 # Frequency of the input data
numSamplesPerFrame = int(frequency * frameSizeInMs)

  
import os  
for file in os.listdir("/home/anirban/Music/Audiofiles"):
	filepath = "/home/anirban/Music/Audiofiles/"+file
	data        = scipy.io.wavfile.read(filepath)
	chunkedData = list(chunks(list(data[1]), numSamplesPerFrame))
	
	variation = rateSampleByVariation(chunkedData)
	zcr       = rateSampleByCrossingRate(chunkedData)
	entropy   = rateSampleByEntropy(chunkedData)
	
	print("File Size = %f"
	      "Coefficient of variation  = %f"
	      "Standard deviation of ZCR = %f"
	      "Minimum entropy           = %f" % (os.path.getsize(filepath), variation, zcr, entropy) )
# =============================================================================
# 	
# 	if variation >= 1.0:
# 	  print("Coefficient of variation suggests that the sample contains speech")
# 	
# 	if zcr >= 0.05:
# 	  print("Standard deviation of ZCR suggests that the sample contains speech")
# 	
# 	if entropy < 2.5:
# 	  print("Minimum entropy suggests that the sample contains speech")
# =============================================================================



  