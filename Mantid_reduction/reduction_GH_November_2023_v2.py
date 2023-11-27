# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np
from mantid.plots.utility import MantidAxType
from mantid.api import AnalysisDataService as ADS

def SELrange1MHz(test_angle=-89,lambda_min=3,lambda_max=13):
    """Calculates the spin-echo length (SEL) range at RF 1MHz at a given poleshoe angle and max/min wavelength"""
    print("---")
    print("angle: ",test_angle)
    print("RF: 1 MHz")
    print("lambda min: ",lambda_min)
    print("lambda max: ",lambda_max)
    print("SEL min: ",echo_cal1MHz(test_angle)*lambda_min**2)
    print("SEL max: ",echo_cal1MHz(test_angle)*lambda_max**2)
    print("---")

def echo_cal1MHz(angle):
    # type: (float) -> float
    # return 1/np.tan(np.array(np.abs(angle))*np.pi/180)*0.05647
    # return np.polyval([-4.00540061e-07, 8.88410387e-05, -
    #                    7.57804680e-03, 2.54373296e-01], np.abs(angle))
    #return 1e3*np.polyval([5.10018568e-09, -1.51816309e-6, 1.7463217e-04, -
    #                    1.02919899e-02, 2.84070156e-01], np.abs(angle))
    # September 2022 Calibration using GR23
    return 1e3*np.polyval([4.75228210324542e-09, -1.43845384239847e-6, 1.68261606108429e-04,
                        -1.00632959255936e-02, 2.80475509656419e-01], np.abs(angle))
print(echo_cal1MHz(60.)*10**2)

def quickpol(rnum):
    w1=Load(str(rnum),LoadMonitors=1)
    MaskDetectors('w1',MaskedWorkspace='MaskWorkspace')
    w1lam=ConvertUnits('w1','Wavelength',AlignBins=1)
    w1m1=ExtractSingleSpectrum('w1_monitors',0)
    w1m1Lam=ConvertUnits('w1m1','Wavelength')
    w1lam=Rebin('w1lam','1.0,0.2,12.0',PreserveEvents=0)
    w1m1Lam=Rebin('w1m1Lam','1.0,0.2,12.0')
    w1norm=w1lam/w1m1Lam
    w1lamInt=SumSpectra('w1norm')
    pol=-1.0*(mtd['w1lamInt_1']-mtd['w1lamInt_2'])/(mtd['w1lamInt_1']+mtd['w1lamInt_2'])
    RenameWorkspace('pol',str(rnum)+'_pol')

def quickpolAlanis(rnum,binning='2.0,0.1,13.3'):
    # if/else statement below allows adding of multiple workspaces
    if type(rnum) == int:
            w1=Load(str(rnum),LoadMonitors=1)
    elif isinstance(rnum,str):
            w1=Load(rnum,LoadMonitors=1)
            rnum=int(rnum[-10:-5])
    else:
        w1=Load(str(rnum[0]),LoadMonitors=1)
        if len(rnum) > 1:
            for i in range(1,len(rnum)):
                wtemp=Load(str(rnum[i]),LoadMonitors=1)
                w1=mtd['wtemp']+mtd['w1']
                w1_monitors=mtd['wtemp_monitors']+mtd['w1_monitors']  
        rnum=rnum[0]  
    MoveInstrumentComponent('w1','SEMSANSWLSFDetector',X=0.5,RelativePosition=True)
    w1=CropWorkspace('w1',StartWorkspaceIndex=40960,EndWorkspaceIndex=40960+63)
    w1lam=ConvertUnits('w1','Wavelength',AlignBins=1)
    w1m1=ExtractSingleSpectrum('w1_monitors',0)
    w1m1Lam=ConvertUnits('w1m1','Wavelength')
    w1lam=Rebin('w1lam',binning,PreserveEvents=0)
    w1m1Lam=Rebin('w1m1Lam',binning)
    w1norm=w1lam/w1m1Lam
    polAll=-1.0*(mtd['w1norm_1']-mtd['w1norm_2'])/(mtd['w1norm_1']+mtd['w1norm_2'])
    w1lamInt=SumSpectra('w1lam')
    w1norm=w1lamInt/w1m1Lam
    w1lam=w1lam/w1m1Lam
    pol=-1.0*(mtd['w1norm_1']-mtd['w1norm_2'])/(mtd['w1norm_1']+mtd['w1norm_2'])
    if type(rnum) == int:
        RenameWorkspace('pol',str(rnum)+'_pol')
        RenameWorkspace('polAll',str(rnum)+'_polAll')
        RenameWorkspace('w1lam',str(rnum)+'_lam')
    else:
        RenameWorkspace('pol',str(rnum)+'_pol')
        RenameWorkspace('polAll',str(rnum)+'_polAll')
        RenameWorkspace('w1lam',str(rnum)+'_lam')

def convertToQ(wksp,specPixel,th0):
    '''Converts polarization data to function of Q.'''
    pixel=0.65
    samp2det=4350
    specIndex=specPixel-40971
    npix=mtd[wksp].getNumberHistograms()
    X1=mtd[wksp].dataX(0)
    w1Q=mtd[wksp]*1.0
    th0rad=th0*np.pi/180.0
    for j in range(npix):
        for i in range(len(X1)):
            thpix=0.5*np.arctan((j-specIndex)*pixel/samp2det)
            w1Q.dataX(j)[i]=4*np.pi*np.sin(th0rad-thpix)/X1[i]
    RenameWorkspace('w1Q',OutputWorkspace=wksp+'_Q')

def plot_q(rnum,pix_range=(31,38)):
    '''Plots q-corrected polarization (pixel range is inclusive).'''
    temp = ADS.retrieve(str(rnum)+'_polAllNorm_Q')
    fig, axes = plt.subplots(edgecolor='#ffffff', figsize=[8.3211, 6.1284], num=str(rnum)+'_polAllNorm_Q-2', subplot_kw={'projection': 'mantid'})
    magic_number = 41002  #conversion between what the DAC calls the detector pixel in two separate places?
    for indx,pix in enumerate(range(pix_range[0],pix_range[-1]+1)):
        axes.errorbar(temp, color='C'+str(indx), elinewidth=1.0, label=str(rnum)+'_polAllNorm_Q: spec '+str(magic_number+indx), wkspIndex=pix)
    axes.tick_params(axis='x', which='major', **{'gridOn': True, 'tick1On': True, 'tick2On': False, 'label1On': True, 'label2On': False, 'size': 6, 'tickdir': 'out', 'width': 1})
    axes.tick_params(axis='y', which='major', **{'gridOn': True, 'tick1On': True, 'tick2On': False, 'label1On': True, 'label2On': False, 'size': 6, 'tickdir': 'out', 'width': 1})
    axes.set_title(str(rnum)+'_polAllNorm_Q')
    axes.set_xlabel('Q ($\\AA^{-1}$)')
    axes.set_ylabel('Normalised Polarization')
    axes.set_ylim([-0.1, 1.1])
    legend = axes.legend(fontsize=8.0).set_draggable(True).legend
    plt.show()

def get_norm(rnum):
    '''Normalizes polarization using fit.'''
    Divide(str(rnum)+'_pol',avPolFit,OutputWorkspace=str(rnum)+'_polNorm')
    Divide(str(rnum)+'_polAll',avPolFit,OutputWorkspace=str(rnum)+'_polAllNorm')

#Old code:
'''_79100_polAllNorm_Q = ADS.retrieve('79130_polAllNorm_Q')
fig, axes = plt.subplots(edgecolor='#ffffff', figsize=[8.3211, 6.1284], num='79100_polAllNorm_Q-2', subplot_kw={'projection': 'mantid'})
axes.errorbar(_79100_polAllNorm_Q, color='#1f77b4', elinewidth=1.0, label='79100_polAllNorm_Q: spec 41002', wkspIndex=31)
axes.errorbar(_79100_polAllNorm_Q, color='#ff7f0e', elinewidth=1.0, label='79100_polAllNorm_Q: spec 41003', wkspIndex=32)
axes.errorbar(_79100_polAllNorm_Q, color='#2ca02c', elinewidth=1.0, label='79100_polAllNorm_Q: spec 41004', wkspIndex=33)
axes.errorbar(_79100_polAllNorm_Q, color='#d62728', elinewidth=1.0, label='79100_polAllNorm_Q: spec 41005', wkspIndex=34)
axes.errorbar(_79100_polAllNorm_Q, color='#9467bd', elinewidth=1.0, label='79100_polAllNorm_Q: spec 41006', wkspIndex=35)
axes.errorbar(_79100_polAllNorm_Q, color='#8c564b', elinewidth=1.0, label='79100_polAllNorm_Q: spec 41007', wkspIndex=36)
axes.errorbar(_79100_polAllNorm_Q, color='#e377c2', elinewidth=1.0, label='79100_polAllNorm_Q: spec 41008', wkspIndex=37)
axes.errorbar(_79100_polAllNorm_Q, color='#7f7f7f', elinewidth=1.0, label='79100_polAllNorm_Q: spec 41009', wkspIndex=38)
axes.tick_params(axis='x', which='major', **{'gridOn': True, 'tick1On': True, 'tick2On': False, 'label1On': True, 'label2On': False, 'size': 6, 'tickdir': 'out', 'width': 1})
axes.tick_params(axis='y', which='major', **{'gridOn': True, 'tick1On': True, 'tick2On': False, 'label1On': True, 'label2On': False, 'size': 6, 'tickdir': 'out', 'width': 1})
axes.set_title('79100_polAllNorm_Q')
axes.set_xlabel('Q ($\\AA^{-1}$)')
axes.set_ylabel('Normalised Polarisation')
axes.set_ylim([-0.2, 1.2])
legend = axes.legend(fontsize=8.0).set_draggable(True).legend
plt.show()'''
#w2=mtd['79100_polAll']

#####################################################
#                  Data reduction                   #
#####################################################
binning='2.0,0.1,13.3'  #wavelength binning

quickpolAlanis(79061,binning)  #empty beam test 1MHz

#Overnight beam reproducibilty check while translating the sample stack
for i in range(79067,79091):
    quickpolAlanis(i,binning)

#Polarization normalization using the NiMo non-magnetic blank
quickpolAlanis(79096,binning)
avPol=SumSpectra('79096_polAll',30,36)  #using the center 7 pixels (each ~0.6 mm)
avPol=avPol/7.0
Fit(Function='name=Polynomial,n=2,A0=0.952356,A1=-0.00345038,A2=-0.00201979', InputWorkspace='avPol', Output='avPol', OutputCompositeMembers=True, StartX=4, EndX=11.675817151262118)
avPolpoint=avPol*1.0
avPolpoint=ConvertToPointData(avPolpoint)
X1=avPolpoint.dataX(0)
pars=mtd['avPol_Parameters']
Y1=np.zeros(len(X1))
E1=np.zeros(len(X1))
for i in range(len(X1)):
    Y1[i]=pars.cell(0,1)+X1[i]*pars.cell(1,1)+X1[i]*X1[i]*pars.cell(2,1)
avPolFit=CreateWorkspace(avPol.dataX(0),Y1,E1,NSpec=1,UnitX='Wavelength')

#Normalization using the long overnight scan, doesn't work????
quickpolAlanis(range(79120,79127),binning)
avPol=SumSpectra('79120_polAll',30,36)  #using the center 7 pixels (each ~0.6 mm)
avPol=avPol/7.0
Fit(Function='name=Polynomial,n=2,A0=0.952356,A1=-0.00345038,A2=-0.00201979', InputWorkspace='avPol', Output='avPol', OutputCompositeMembers=True, StartX=4, EndX=11.675817151262118)
avPolpoint=avPol*1.0
avPolpoint=ConvertToPointData(avPolpoint)
X1=avPolpoint.dataX(0)
pars=mtd['avPol_Parameters']
Y1=np.zeros(len(X1))
E1=np.zeros(len(X1))
for i in range(len(X1)):
    Y1[i]=pars.cell(0,1)+X1[i]*pars.cell(1,1)+X1[i]*X1[i]*pars.cell(2,1)
avPolFit=CreateWorkspace(avPol.dataX(0),Y1,E1,NSpec=1,UnitX='Wavelength')

'''#Linear version, also doesn't work
quickpolAlanis(range(79120,79127),binning)
avPol=SumSpectra('79120_polAll',30,36)  #using the center 7 pixels (each ~0.6 mm)
avPol=avPol/7.0
Fit(Function='name=LinearBackground', InputWorkspace='avPol', Output='avPol', OutputCompositeMembers=True, StartX=4, EndX=11.675817151262118)
avPolpoint=avPol*1.0
avPolpoint=ConvertToPointData(avPolpoint)
X1=avPolpoint.dataX(0)
pars=mtd['avPol_Parameters']
Y1=np.zeros(len(X1))
E1=np.zeros(len(X1))
for i in range(len(X1)):
    Y1[i]=pars.cell(0,1)+X1[i]*pars.cell(1,1)
avPolFit=CreateWorkspace(avPol.dataX(0),Y1,E1,NSpec=1,UnitX='Wavelength')'''

#Perpendicular magnetic sample (M perp B_guide)
quickpolAlanis(range(79100,79116),binning)
get_norm(79100)
convertToQ('79100_polAllNorm',41005,0.35)
plot_q(79100)

#Parallel magnetic sample
quickpolAlanis(range(79130,79143),binning)
get_norm(79130)
convertToQ('79130_polAllNorm',41005,0.35)
plot_q(79130)

#Quick grating before sample check
quickpolAlanis(range(79143,79145),binning)

#Quick grating after sample check
binning='2.0,0.1,13.3'  #wavelength binning
quickpolAlanis(range(79145,79159),binning)


quickpolAlanis(79100,binning)
Divide('79100_polAll',avPolFit,OutputWorkspace='79100_polAllNorm')

quickpolAlanis(range(79120,79125),binning)
Divide('79120_polAll',avPolFit,OutputWorkspace='79120_polAllNorm')

quickpolAlanis(79120,binning)
convertToQ('79120_polAllNorm',41005,0.35)
Divide('79120_polAll',avPolFit,OutputWorkspace='79120_polAllNorm')

quickpolAlanis(range(79130,79142),binning)
Divide('79130_polAll',avPolFit,OutputWorkspace='79130_polAllNorm')
convertToQ('79130_polAllNorm',41005,0.35)

quickpolAlanis(79143,binning)
Divide('79143_polAll',avPolFit,OutputWorkspace='79143_polAllNorm')
convertToQ('79143_polAllNorm',41005,0.35)
plot_q(79143)

quickpolAlanis(79144,binning)
Divide('79144_pol',avPolFit,OutputWorkspace='79144_polNorm')

convertToQ('79101_polAllNorm',41005,0.35)


quickpolAlanis(range(79160,79165),binning)

quickpolAlanis(79167,'2.0,0.5,13.3')

temp = [i for i in range(79172,79174)]+[i for i in range(79167,79170)]+[i for i in range(79120,79127)]
print(temp)
quickpolAlanis(temp,binning)

quickpolAlanis(range(79067,79091),binning)

quickpolAlanis(range(79179,79189),binning)



quickpolAlanis(range(79189,79196),binning)  #grating before sample


# variable binning is easy enough steps of 0.05 up to 6.5Ang and then 0.1 after
binning="2.0,0.05,6.5,0.1,13.3"
quickpolAlanis(range(79189,79196),binning)  #grating before sample
convertToQ('79189_polAll',41005,0.4)

