# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

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

def quickpolAlanis(rnum,binning=binning):
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

def patterson(wstemp, const):
    # type: (Workspace, float) -> Workspace
    """Convert workspace into spin echo form"""
    temp = CloneWorkspace(wstemp)
    
    x = temp.extractX()
    x = (x[:, 1:]+x[:, :-1])/2
    temp = Logarithm(temp)
    for i in range(x.shape[0]):
        temp.setY(i, temp.readY(i)/x[i]**2/(temp.sample().getThickness()*0.1))
        temp.setE(i, temp.readE(i)/x[i]**2/(temp.sample().getThickness()*0.1))
        #print('Thickness='+str(temp.sample().getThickness()))
        temp = ConvertUnits(temp, "SpinEchoLength", EFixed=const)
    return temp

#----------
# echo_cals

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

def echo_cal3MHz(angle):
    # Estimated values based on 2MHz calibration
    # type: (float) -> float
    # September 2022 Calibration using GR23 for 2MHz 
    return 1.5*1e3*np.polyval([7.42468285310946e-09, -2.37424465512104e-6, 2.92814364848172e-04,
                       -1.85712645099827e-02, 5.44463590018381e-01], np.abs(angle))  

def echo_cal2MHz(angle):
    # type: (float) -> float
    # September 2022 Calibration using GR23
    return 1e3*np.polyval([7.42468285310946e-09, -2.37424465512104e-6, 2.92814364848172e-04,
                       -1.85712645099827e-02, 5.44463590018381e-01], np.abs(angle))

def echo_cal0p5MHz(angle):
    # type: (float) -> float
    # return 1/np.tan(np.array(np.abs(angle))*np.pi/180)*0.05647
    # return np.polyval([-4.00540061e-07, 8.88410387e-05, -
    #                    7.57804680e-03, 2.54373296e-01], np.abs(angle))
    return 1e3*np.polyval([1.41057273115624e-09, -4.84176246843703e-7, 6.35296271850731e-05,
                       -4.24863310118509e-03, 1.28783274939381e-01], np.abs(angle))

print("---")
print(echo_cal2MHz(-40)*2.5**2)    
print(echo_cal2MHz(-40)*12**2)    
print("---")
print(echo_cal1MHz(-30)*5.5**2)    
print(echo_cal2MHz(-40)*12.1**2)    
print(echo_cal3MHz(-30)*9.5**2)    
print("---")

#-----------

def replotEchoScan(rnum):
    w1=Load(str(rnum),LoadMonitors=1)
    MoveInstrumentComponent('w1','SEMSANSWLSFDetector',X=0.5,RelativePosition=True)
    w1=CropWorkspace('w1',StartWorkspaceIndex=1,EndWorkspaceIndex=1)
    w1lam=ConvertUnits('w1','Wavelength',AlignBins=1)
    w1m1=ExtractSingleSpectrum('w1_monitors',0)
    w1m1Lam=ConvertUnits('w1m1','Wavelength')
    w1lam=Rebin('w1lam','3.0,3.0,12.0',PreserveEvents=0)
    w1m1Lam=Rebin('w1m1Lam','3.0,3.0,12.0')
    w1lamInt=SumSpectra('w1lam')
    w1norm=w1lamInt/w1m1Lam
    wlist=[]
    for  i in range(int(len(mtd['w1norm'].getNames())/2)):
        pol=-1.0*(mtd['w1norm_'+str(i*2+1)]-mtd['w1norm_'+str((i*2)+2)])/(mtd['w1norm_'+str((i*2+1))]+mtd['w1norm_'+str((i*2)+2)])
        RenameWorkspace('pol','pol_'+str(i))
        wlist.append('pol_'+str(i))
    GroupWorkspaces(wlist,OutputWorkspace='pol')
    nper=len(mtd['pol'].getNames())
    xvals=[]
    yvals=[]
    evals=[]
    for j in range(3):
        for i in range(len(mtd['pol'].getNames())):
            xvals.append(i)
            yvals.append(mtd['pol_'+str(i)].dataY(0)[j])
            evals.append(mtd['pol_'+str(i)].dataE(0)[j])
    CreateWorkspace(xvals,yvals,evals,NSpec=3,OutputWorkspace=str(rnum)+'_EchoScan')        

def reduceSESANS3MHz(P0,Sample,PSAng,reload=False,binning='5,0.05,12.0',topandbottom=False):
    if not mtd.doesExist(str(P0)+'_pol') or reload:
        quickpolAlanis(P0,binning=binning,topandbottom=topandbottom)
    quickpolAlanis(Sample,binning=binning,topandbottom=topandbottom)
    Divide(str(Sample)+'_pol',str(P0)+'_pol',OutputWorkspace=str(Sample)+'_pnorm')
    Divide(str(Sample)+'_polAll',str(P0)+'_polAll',OutputWorkspace=str(Sample)+'_pnormAll')
    temp2=ConvertUnits(str(Sample)+'_pnorm', "SpinEchoLength", EFixed=echo_cal3MHz(PSAng))
    temp3=ConvertUnits(str(Sample)+'_pnormAll', "SpinEchoLength", EFixed=echo_cal3MHz(PSAng))
    temp=patterson(str(Sample)+'_pnorm', echo_cal3MHz(PSAng))
    RenameWorkspace('temp',str(Sample)+'_sesans')
    RenameWorkspace('temp2',str(Sample)+'_PnormSE')
    RenameWorkspace('temp3',str(Sample)+'_PnormAllSE')

def reduceSESANS2MHz(P0,Sample,PSAng,reload=False,binning='2.5,0.05,12.0'):
    if not mtd.doesExist(str(P0)+'_pol') or reload:
        quickpolAlanis(P0,binning=binning)
    quickpolAlanis(Sample,binning=binning)
    Divide(str(Sample)+'_pol',str(P0)+'_pol',OutputWorkspace=str(Sample)+'_pnorm')
    Divide(str(Sample)+'_polAll',str(P0)+'_polAll',OutputWorkspace=str(Sample)+'_pnormAll')
    temp2=ConvertUnits(str(Sample)+'_pnorm', "SpinEchoLength", EFixed=echo_cal2MHz(PSAng))
    temp3=ConvertUnits(str(Sample)+'_pnormAll', "SpinEchoLength", EFixed=echo_cal2MHz(PSAng))
    temp=patterson(str(Sample)+'_pnorm', echo_cal2MHz(PSAng))
    RenameWorkspace('temp',str(Sample)+'_sesans')
    RenameWorkspace('temp2',str(Sample)+'_PnormSE')
    RenameWorkspace('temp3',str(Sample)+'_PnormAllSE')

def reduceSESANS1MHz(P0,Sample,PSAng,reload=False):
    if not mtd.doesExist(str(P0)+'_pol') or reload:
        quickpolAlanis(P0,binning='2.5,0.2,12.0')
    quickpolAlanis(Sample,binning='2.5,0.2,12.0')
    Divide(str(Sample)+'_pol',str(P0)+'_pol',OutputWorkspace=str(Sample)+'_pnorm')
    temp2=ConvertUnits(str(Sample)+'_pnorm', "SpinEchoLength", EFixed=echo_cal1MHz(PSAng))
    temp=patterson(str(Sample)+'_pnorm', echo_cal1MHz(PSAng))
    RenameWorkspace('temp',str(Sample)+'_sesans')
    RenameWorkspace('temp2',str(Sample)+'_PnormSE')
    
def replotEchoScan(rnum):
    w1=Load(str(rnum),LoadMonitors=1)
    MoveInstrumentComponent('w1','SEMSANSWLSFDetector',X=0.5,RelativePosition=True)
    w1=CropWorkspace('w1',StartWorkspaceIndex=1,EndWorkspaceIndex=1)
    w1lam=ConvertUnits('w1','Wavelength',AlignBins=1)
    w1m1=ExtractSingleSpectrum('w1_monitors',0)
    w1m1Lam=ConvertUnits('w1m1','Wavelength')
    w1lam=Rebin('w1lam','3.0,3.0,12.0',PreserveEvents=0)
    w1m1Lam=Rebin('w1m1Lam','3.0,3.0,12.0')
    w1lamInt=SumSpectra('w1lam')
    w1norm=w1lamInt/w1m1Lam
    wlist=[]
    for  i in range(int(len(mtd['w1norm'].getNames())/2)):
        pol=-1.0*(mtd['w1norm_'+str(i*2+1)]-mtd['w1norm_'+str((i*2)+2)])/(mtd['w1norm_'+str((i*2+1))]+mtd['w1norm_'+str((i*2)+2)])
        RenameWorkspace('pol','pol_'+str(i))
        wlist.append('pol_'+str(i))
    GroupWorkspaces(wlist,OutputWorkspace='pol')
    nper=len(mtd['pol'].getNames())
    xvals=[]
    yvals=[]
    evals=[]
    for j in range(3):
        for i in range(len(mtd['pol'].getNames())):
            xvals.append(i)
            yvals.append(mtd['pol_'+str(i)].dataY(0)[j])
            evals.append(mtd['pol_'+str(i)].dataE(0)[j])
    CreateWorkspace(xvals,yvals,evals,NSpec=3,OutputWorkspace=str(rnum)+'_EchoScan')  

def calcAverage(rnums):
    ndiv=len(rnums)
    waverage1=mtd[str(rnums[0])+'_PnormSE']
    waverageAll1=mtd[str(rnums[0])+'_PnormAllSE']
    for i in range(1,len(rnums)):
        waverage1=waverage1+mtd[str(rnums[i])+'_PnormSE']
        waverageAll1=waverageAll1+mtd[str(rnums[i])+'_PnormAllSE']
    waverage=waverage1/float(ndiv)
    waverageAll=waverageAll1/float(ndiv)

def calcAveragePol(rnums):
    ndiv=len(rnums)
    waverage1=mtd[str(rnums[0])+'_pol']
    for i in range(1,len(rnums)):
        waverage1=waverage1+mtd[str(rnums[i])+'_pol']
    waverage_pol=waverage1/float(ndiv)
    
################
#reduction
################
binning='2.0,0.1,13.3'
for i in range(79067,79089):
    quickpolAlanis(i,binning)

binning='2.9,0.05,13.3'
quickpolAlanis(79096,binning)
# Perp Sample
#quickpolAlanis(79100,binning)
#Divide('79100_polAll','79096_polAll',OutputWorkspace='79100_polAllNorm')

avPol=SumSpectra('79096_polAll',30,36)
avPol=avPol/7.0
Fit(Function='name=Polynomial,n=2,A0=0.952356,A1=-0.00345038,A2=-0.00201979', InputWorkspace='avPol', Output='avPol', OutputCompositeMembers=True, StartX=3, EndX=11.675817151262118)
avPolpoint=avPol*1.0
avPolpoint=ConvertToPointData(avPolpoint)
X1=avPolpoint.dataX(0)
pars=mtd['avPol_Parameters']
Y1=np.zeros(len(X1))
E1=np.zeros(len(X1))
for i in range(len(X1)):
    Y1[i]=pars.cell(0,1)+X1[i]*pars.cell(1,1)+X1[i]*X1[i]*pars.cell(2,1)
avPolFit=CreateWorkspace(avPol.dataX(0),Y1,E1,NSpec=1,UnitX='Wavelength')

quickpolAlanis(range(79101,79115),binning)
Divide('79101_polAll',avPolFit,OutputWorkspace='79101_polAllNorm')

quickpolAlanis(79100,binning)
Divide('79100_polAll',avPolFit,OutputWorkspace='79100_polAllNorm')

quickpolAlanis(79120,binning)
Divide('79120_polAll',avPolFit,OutputWorkspace='79120_polAllNorm')

'''
def save_Mantid_output(run_num,path=r'U:\User\Users\Pynn\November_2023\'):
    SaveAscii('79096_polAll',r'U:\User\Users\Pynn\November_2023\79096_polAll.txt')
'''
