# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np
from mantid.plots.utility import MantidAxType
from mantid.api import AnalysisDataService as ADS

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

def SELrange1MHz(test_angle=-90,lambda_min=3,lambda_max=13):
    """Calculates the spin-echo length (SEL) range at RF 1MHz at a given poleshoe angle and max/min wavelength"""
    print("---")
    print("angle: ",test_angle)
    print("RF: 1 MHz")
    print("lambda min: ",lambda_min)
    print("lambda max: ",lambda_max)
    print("SEL min: ",echo_cal1MHz(test_angle)*lambda_min**2)
    print("SEL max: ",echo_cal1MHz(test_angle)*lambda_max**2)
    print("---")
SELrange1MHz()

def calcpol(wksp1,wksp2,wkspname):
    u=mtd[wksp1]
    d=mtd[wksp2]
    pol=(u-d)/(u+d)

    # calculate the error bars correctly
    nhist=mtd[wksp1].getNumberHistograms()
    for i in range(nhist):
        uy=u.dataY(i)
        ue=u.dataE(i)
        dy=d.dataY(i)
        de=d.dataE(i)
        upd4=(uy+dy)*(uy+dy)*(uy+dy)*(uy+dy)
        polE=4.0*((dy*dy*ue*ue)+(uy*uy*de*de))/upd4
        polE=np.sqrt(polE)
        for j in range(len(uy)):
            pol.dataE(i)[j]=polE[j]
    pol=ReplaceSpecialValues('pol',0.0,0.0,0.0,0.0)
    RenameWorkspace('pol',wkspname)

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
    '''Old method with incorrect error bars, here for legacy purposes.'''
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

def quickpolAlanis(rnum,binning='2.0,0.1,13.3'):
    '''Polarization analysis with proper error bars.'''
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
    calcpol('w1norm_2','w1norm_1',str(rnum)+'_polAll')
    w1lamInt=SumSpectra('w1lam')
    w1norm=w1lamInt/w1m1Lam
    w1lam=w1lam/w1m1Lam
    calcpol('w1norm_2','w1norm_1',str(rnum)+'_pol')
    if type(rnum) == int:
        RenameWorkspace('w1lam',str(rnum)+'_lam')
    else:
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
    temp = ADS.retrieve(str(rnum)+'_polAll_Q')
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

def save_Mantid_output(run_num,new_name='',path=r'C:\\Users\\samckay\\Documents\\GitHub\\Goos-Hanchen\\Reduced_data_correct_eb\\',lams=False):
    '''Saves the intensity data into a text file.'''
    SaveAscii(str(run_num)+'_lam_1',path+new_name+'up'+'.txt')  #monitor normalization issue?
    SaveAscii(str(run_num)+'_lam_2',path+new_name+'dn'+'.txt')
    SaveAscii(str(run_num)+'_polAll',path+new_name+'pol'+'.txt')
    SaveAscii(str(run_num)+'_pol',path+new_name+'pol_av'+'.txt')

#####################################################
#                  Data reduction                   #
#####################################################
binning='2.5,0.05,13.0'  #wavelength binning

#Blank, NiMo sample that was used for normalization
blank_perp = [i for i in range(79096,79098)]
quickpolAlanis(blank_perp,binning)
save_Mantid_output(79096,new_name=r'blank_perp\\')

blank_para1 = [i for i in range(79120,79127)]
quickpolAlanis(blank_para1,binning)
save_Mantid_output(79120,new_name=r'blank_para1\\')

blank_para2 = [i for i in range(79167,79170)]
quickpolAlanis(blank_para2,binning)
save_Mantid_output(79167,new_name=r'blank_para2\\')

blanks = blank_perp + blank_para1 + blank_para2
quickpolAlanis(blanks,binning)
save_Mantid_output(79096,new_name=r'blank_all\\')

#Perpendicular magnetic sample (M perp B_guide)
perp = range(79100,79116)
quickpolAlanis(perp,binning)
save_Mantid_output(79100,new_name=r'perp_p35\\')
convertToQ('79100_polAll',41005,0.35)
#plot_q(79100)

#Parallel magnetic sample (M parallel B_guide), incident angle 0.35 degrees
para_p35 = range(79130,79143)
quickpolAlanis(para_p35,binning)
save_Mantid_output(79130,new_name=r'para_p35\\')
convertToQ('79130_polAll',41005,0.35)
#plot_q(79130)

#Parallel magnetic sample, incident angle 0.35 degrees, grating AFTER sample
para_p35_after = [i for i in range(79143,79145)] + [i for i in range(79160,79165)]
quickpolAlanis(para_p35_after,binning)
save_Mantid_output(79143,new_name=r'para_p35_after\\')
convertToQ('79143_polAll',41005,0.35)
#plot_q(79143)

#Parallel magnetic sample, incident angle 0.35 degrees, grating BEFORE sample
para_p35_before = [i for i in range(79145,79160)]
quickpolAlanis(para_p35_before,binning)
save_Mantid_output(79145,new_name=r'para_p35_before\\')
convertToQ('79145_polAll',41005,0.35)
#plot_q(79145)

#----------------------------------------------------------------------------#
#Parallel magnetic sample, incident angle 0.4 degrees, no grating
para_p40 = [i for i in range(79179,79189)]
quickpolAlanis(para_p40,binning)
save_Mantid_output(79179,new_name=r'para_p40\\')
convertToQ('79179_polAll',41005,0.35)
#plot_q(79179)

#originally these were mixed up. Fixed as of 1/22/24
#Parallel magnetic sample, incident angle 0.4 degrees, grating BEFORE sample
para_p40_before = [i for i in range(79189,79200)]
quickpolAlanis(para_p40_before,binning)
save_Mantid_output(79189,new_name=r'para_p40_before\\')
convertToQ('79189_polAll',41005,0.35)
#plot_q(79189)

#Parallel magnetic sample, incident angle 0.4 degrees, grating AFTER sample
para_p40_after = [i for i in range(79200,79213)]
quickpolAlanis(para_p40_after,binning)
save_Mantid_output(79200,new_name=r'para_p40_after\\')










