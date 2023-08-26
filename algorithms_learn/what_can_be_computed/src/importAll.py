# script importAll.py

# This script imports all the SISO functions and some other useful
# functionality provided with the WCBC materials. Usually, importing
# this many functions into the global namespace would be considered
# poor practice, but it is a good way to permit easy experimentation.

# The usage of this script is extremely simple. Simply run it as follows

# >>> importAll.py

# Now almost any function in the WCBC materials can be employed. For
# example,

# >>> containsGAGA('TTTTTA')
# 'no'

from F import F
from FThresh import FThresh
from G import G
from GAGAOnString import GAGAOnString
from GnTn import GnTn
from GthenOneT import GthenOneT
from H import H
from MCopiesOfC import MCopiesOfC
from P1 import P1
from all3Sets import all3Sets
from allSubsets import allSubsets
from alterGAGAtoTATA import alterGAGAtoTATA
from alterGAGAtoTATA2 import alterGAGAtoTATA2
from alterYesToComputesF import alterYesToComputesF
from alterYesToGAGA import alterYesToGAGA
from alterYesToHalt import alterYesToHalt
from alterYesToNumChars import alterYesToNumChars
from alterYoEToEoE import alterYoEToEoE
# from binAd import binAd
from brokenSort import brokenSort
from bubbleSort import bubbleSort
# from cfg import cfg
# from checkRuntimes import checkRuntimes
# from checkTuringMachine import checkTuringMachine
# from checkUtils import checkUtils
# from circuit import circuit
from clique import clique
from computesF import computesF
from containsGAGA import containsGAGA
from containsGAGAandCACAandTATA import containsGAGAandCACAandTATA
# from containsGAGAcopy1 import containsGAGAcopy1
# from containsGAGAcopy2 import containsGAGAcopy2
# from containsGAGAcopy3 import containsGAGAcopy3
from containsNANA import containsNANA
from convertDHCtoUHC import convertDHCtoUHC
from convertHaltToPeano import convertHaltToPeano
from convertNfaToDfa import convertNfaToDfa
from convertPartitionToPacking import convertPartitionToPacking
from convertSatTo3Sat import convertSatTo3Sat
from convertSatToClique import convertSatToClique
from convertUHCtoDHC import convertUHCtoDHC
from convertUhcToHalfUhc import convertUhcToHalfUhc
from countLines import countLines
from countLinesPlus1 import countLinesPlus1
from crashOnSelf import crashOnSelf
from crashOnString import crashOnString
# from createRelease import createRelease
from dfa import Dfa
from dhc import dhc
from dpda import Dpda
from emptyOnEmpty import emptyOnEmpty
from evaluateSat import evaluateSat
from evaluateSatNoDummy import evaluateSatNoDummy
from factor import factor
from factorUnary import factorUnary
from godel import godel
from graph import *
# from graphTests import graphTests
from halfUhc import halfUhc
from haltExTuring import haltExTuring
from haltsOnString import haltsOnString
from haltsViaCompletePeano import haltsViaCompletePeano
from haltsViaNumSteps import haltsViaNumSteps
from haltsViaPeano import haltsViaPeano
from hmmmm import hmmmm
from ignoreInput import ignoreInput
from infiniteLoop import infiniteLoop
from isEmpty import isEmpty
from isEven import isEven
from isOdd import isOdd
from isOddViaReduction import isOddViaReduction
from isPeanoProof import isPeanoProof
from lastDigitIsEven import lastDigitIsEven
from listEvens import listEvens
from longerThan1K import longerThan1K
from longestWord import longestWord
from loop import loop
from loopIfContainsGAGA import loopIfContainsGAGA
from matchingCharIndices import matchingCharIndices
from maybeLoop import maybeLoop
from multiply import multiply
from multiplyAll import multiplyAll
from multiplyTimings import multiplyTimings
from mysteryMultiply import mysteryMultiply
from ndContainsNANA import ndContainsNANA
from ndFactor import ndFactor
from ndFindNANA import ndFindNANA
from ndFindNANADivConq import ndFindNANADivConq
from ndTuringMachine import NDTuringMachine
from nfa import Nfa
from no import no
# from noMainFunction import noMainFunction
from notYesOnSelf import notYesOnSelf
from notYesOnSelfApprox import notYesOnSelfApprox
from npda import Npda
from numCharsOnString import numCharsOnString
from numStepsOnString import numStepsOnString
from onlyZs import onlyZs
from oooops import oooops
from packing import packing
from partition import partition
from provableInPeano import provableInPeano
from pythonSort import pythonSort
from recYesOnString import recYesOnString
from recognizeEvenLength import recognizeEvenLength
from repeatCAorGA import repeatCAorGA
from returnsNumber import returnsNumber
from rule110 import rule110
# from runAllTests import runAllTests
from sat import sat
from shortestPath import shortestPath
from showCATTAGhist import showCATTAGhist
from simulate2TDCM import simulate2TDCM
from simulateDfa import simulateDfa
from simulateDpda import simulateDpda
from simulateNfa import simulateNfa
from simulateNpda import simulateNpda
from simulateTM import simulateTM
from simulateTM1 import simulateTM1
from simulateTMv2 import simulateTMv2
from slow10thPower import slow10thPower
# from someTests import someTests
from sortTimings import sortTimings
# from syntaxError import syntaxError
from threshToOpt import threshToOpt
from throwsException import throwsException
from trueInPeano import trueInPeano
from tsp import tsp
from tspDir import tspDir
from tspDirK import tspDirK
from tspPath import tspPath
from turingMachine import TuringMachine
from twoTDCM import TwoTDCM
from uhc import uhc
from universal import universal
# from utils import utils
from verifyAdd import verifyAdd
from verifyCheckMultiply import verifyCheckMultiply
from verifyFactor import verifyFactor
from verifyFactorPolytime import verifyFactorPolytime
from verifyTspD import verifyTspD
from verifyTspDPolytime import verifyTspDPolytime
from weirdCountLines import weirdCountLines
from weirdCrashOnSelf import weirdCrashOnSelf
from weirdH import weirdH
from weirdYesOnString import weirdYesOnString
from yes import yes
from yesOnAll import yesOnAll
from yesOnEmpty import yesOnEmpty
from yesOnPosIntsViaYoS import yesOnPosIntsViaYoS
from yesOnSelf import yesOnSelf
from yesOnSelfApprox import yesOnSelfApprox
from yesOnSome import yesOnSome
from yesOnString import yesOnString
from yesOnStringApprox import yesOnStringApprox
from yesViaAll import yesViaAll
from yesViaComputesF import yesViaComputesF
from yesViaEmpty import yesViaEmpty
from yesViaGAGA import yesViaGAGA
from yesViaHalts import yesViaHalts
from yesViaNumChars import yesViaNumChars
from yesViaSome import yesViaSome
