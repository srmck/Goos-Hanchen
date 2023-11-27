# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

from mantid.simpleapi import *

Load(Filename=r'X:\LARMOR00079096.nxs', OutputWorkspace='w1', LoadMonitors=True)
MoveInstrumentComponent(Workspace='w1', ComponentName='SEMSANSWLSFDetector', X=0.5)
CropWorkspace(InputWorkspace='w1', OutputWorkspace='w1', StartWorkspaceIndex=40960, EndWorkspaceIndex=41023)
ConvertUnits(InputWorkspace='w1', OutputWorkspace='w1lam', Target='Wavelength', AlignBins=True)
ExtractSingleSpectrum(InputWorkspace='w1_monitors', OutputWorkspace='w1m1', WorkspaceIndex=0)
ConvertUnits(InputWorkspace='w1m1', OutputWorkspace='w1m1Lam', Target='Wavelength')
Rebin(InputWorkspace='w1lam', OutputWorkspace='w1lam', Params='2.9,0.1,13.3', PreserveEvents=False)
Rebin(InputWorkspace='w1m1Lam', OutputWorkspace='w1m1Lam', Params='2.9,0.1,13.3')
Divide(LHSWorkspace='w1lam', RHSWorkspace='w1m1Lam', OutputWorkspace='w1norm')
Minus(LHSWorkspace='w1norm_1', RHSWorkspace='w1norm_2', OutputWorkspace='__python_op_tmp0')
CreateSingleValuedWorkspace(OutputWorkspace='__python_binary_op_single_value', DataValue=-1)
Multiply(LHSWorkspace='__python_binary_op_single_value', RHSWorkspace='__python_op_tmp0', OutputWorkspace='__python_op_tmp1')
Plus(LHSWorkspace='w1norm_1', RHSWorkspace='w1norm_2', OutputWorkspace='__python_op_tmp2')
Divide(LHSWorkspace='__python_op_tmp1', RHSWorkspace='__python_op_tmp2', OutputWorkspace='polAll')
RenameWorkspace(InputWorkspace='polAll', OutputWorkspace='79096_polAll')
SumSpectra(InputWorkspace='79096_polAll', OutputWorkspace='avPol', StartWorkspaceIndex=30, EndWorkspaceIndex=36)
CreateSingleValuedWorkspace(OutputWorkspace='__python_binary_op_single_value', DataValue=7)
Divide(LHSWorkspace='avPol', RHSWorkspace='__python_binary_op_single_value', OutputWorkspace='avPol')
Fit(Function='name=Polynomial,n=2,A0=0.952356,A1=-0.00345038,A2=-0.00201979', InputWorkspace='avPol', Output='avPol', OutputCompositeMembers=True, StartX=3, EndX=11.675817151262118)
