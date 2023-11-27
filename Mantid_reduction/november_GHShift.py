# Script created by SANSScript at 09/10/2023 14:09:44

import sys
from genie_python import genie as g, BLOCK_NAMES as b
sys.path.append(r"c:\instrument\scripts")
from instrument.larmor import * # pylint: disable=wildcard-import, unused-wildcard-import
import LSS.SESANSroutines as ss
import time as time

def rezerofields1MHz():
    g.cset(DCMagField1=3.0)
    time.sleep(0.5)
    g.cset(DCMagField2=3.0)
    time.sleep(0.5)
    g.cset(DCMagField3=-3.0)
    time.sleep(0.5)
    g.cset(DCMagField4=-3.0)
    time.sleep(60)
    g.cset(DCMagField1=34.5)
    time.sleep(0.5)
    g.cset(DCMagField2=34.5)
    time.sleep(0.5)
    g.cset(DCMagField3=-34.8)
    time.sleep(0.5)
    g.cset(DCMagField4=-34.8)
    time.sleep(60)

def nov2023():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()

    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        g.cset("ChangerTranslation",26)
        do_sans(title='{Empty beam Reproducibility Check CT=26mm}', uamps=20, thickness=1, dae='sesans')
        
        g.cset("ChangerTranslation",25)
        do_sans(title='{Empty beam Reproducibility Check CT=25mm}', uamps=20, thickness=1, dae='sesans')
        g.cset("ChangerTranslation",25.5)
        do_sans(title='{Empty beam Reproducibility Check CT=25.5mm}', uamps=20, thickness=1, dae='sesans')
        g.cset("ChangerTranslation",26.5)
        do_sans(title='{Empty beam Reproducibility Check CT=26.5mm}', uamps=20, thickness=1, dae='sesans')
        g.cset("ChangerTranslation",27)
        do_sans(title='{Empty beam Reproducibility Check CT=27mm}', uamps=20, thickness=1, dae='sesans')

def Woensdag():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.06)
    g.cset("PiRot",57.83)

    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{GH_perp 0.35deg CT=27.06mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
        
        


def DonderdagMorgen():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",26.87)
    g.cset("PiRot",57.83)

    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{P0 0.35deg CT=26.87mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
        
        
def DonderdagAvond():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.05)
    g.cset("PiRot",57.83)

    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{Sample Par 0.35deg CT=27.05mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
        
def FridayMorning():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.05)
    g.cset("PiRot",57.83)

    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{Sample Par G27 (2um period,10.5um depth,560nm groove) 0.35deg CT=27.05mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
        
        
def FridayEvening():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.05)
    g.cset("PiRot",57.83)

    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{Sample Par After G27  (2um period,10.5um depth,560nm groove) 0.35deg CT=27.05mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
        
def SatMorning():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.05)
    g.cset("PiRot",57.83)

    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{Sample Par After (for real) G27 (2um period,10.5um depth,560nm groove) 0.35deg CT=27.05mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
        
def SatAfternoon():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.05)
    g.cset("PiRot",57.83)

    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{Blank 0.35deg PiRot=57.83 CT=27.05mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
        
        
        
def SatEvening():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.54)
    g.cset("PiRot",57.77)
    do_sans(title='{Sample Par Quick 0.40deg PiRot=57.77 CT=27.54mm 90deg 1MHz}', uamps=5, thickness=1, dae='sesans')
    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{Sample Par 0.40deg PiRot=57.77 CT=27.54mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
                
                
def SatRotscan():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.05)
    g.cset("PiRot",57.78)
    do_sans(title='{Blank 0.40deg PiRot=57.78 CT=27.05mm 90deg 1MHz}', frames=500, thickness=1, dae='sesans')


def SunMorning():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.54)
    g.cset("PiRot",57.77)
    do_sans(title='{Sample Par GR before Quick 0.40deg PiRot=57.77 CT=27.54mm 90deg 1MHz}', uamps=5, thickness=1, dae='sesans')
    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{Sample Par GR before 0.40deg PiRot=57.77 CT=27.54mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')
        
def SunNight():
    g.change_sample_par('Width', '0.5')
    g.change_sample_par('height', '25')
    g.change_sample_par('Geometry', 'Flat Plate')

    # ss.set_poleshoe_angle2(-90,1171.2,1)
    # rezerofields1MHz()
    g.cset("ChangerTranslation",27.54)
    g.cset("PiRot",57.77)
    do_sans(title='{Sample Par GR after Quick 0.40deg PiRot=57.77 CT=27.54mm 90deg 1MHz}', uamps=5, thickness=1, dae='sesans')
    for i in range(100):
        setup_dae_event()
        setup_dae_alanis()
        # # always include this between an autotune and a measurement       
    
        do_sans(title='{Sample Par GR after 0.40deg PiRot=57.77 CT=27.54mm 90deg 1MHz}', uamps=40, thickness=1, dae='sesans')




        