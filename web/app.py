
import json
from flask import Flask, render_template, request, url_for, redirect
from mypackage.economie_1 import economie
from mypackage.eco_affaire import eco_affaire
from mypackage.eco_affaire_er import eco_affaire_er
from mypackage.eco_premiere import eco_premiere
from mypackage.MTOW_dig import MTOWdig

"""
set FLASK_ENV=development
python app.py
"""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/avion.html', methods=['GET', 'POST'])
def avion():
    if request.method == 'POST':
        npax = request.form.get('npax','300')
        raction = request.form.get('raction','3500')
        coefremp = request.form.get('coefremp','0.8')
        mach = request.form.get('mach','0.85')
        allongV = request.form.get('allongV','10')
        travel_class = request.form.get('options','classeEco')
        
        
        return redirect(url_for('resultats', npax=npax, raction=raction,coefremp=coefremp,mach=mach,allongV=allongV, travel_class=travel_class))

    return render_template('avion.html')

@app.route('/lesPropiete.html')
def les_propriete():
    return render_template('lesPropiete.html')

@app.route('/resultats.html?npax=<npax>&raction=<raction>&coefremp=<coefremp>&mach=<mach>&allongV=<allongV>&travel_class=<travel_class>')
def resultats(npax, raction,coefremp,mach,allongV, travel_class):

    
    if travel_class == 'classeEco':
        
        
        economie_object = economie(int(npax),int(raction),float(coefremp),float(mach),float(allongV))
        #economie_object.terminer()
        FN0, Masse_carb, MTOW, MC, ZFW, v_croi, MZFW = economie_object.terminer()
        prix = economie_object.TOC(FN0, Masse_carb, MTOW, MC, ZFW, v_croi, MZFW)
        #bg_remov()
        return render_template('resultats.html', prix=prix)
    
    if travel_class == 'classeEcoaff':
        
        mtow_object=MTOWdig(int(npax),int(raction),float(coefremp),float(mach),float(allongV))
        Sref,FN0, Masse_carb, MTOW, MC, ZFW, v_croi, MZFW=mtow_object.terminer()
       
        economie_aff_object = eco_affaire(int(npax),int(raction),float(coefremp),float(mach),float(allongV),float(Sref))
        economie_aff_object.terminer()
        prix = economie_aff_object.TOC(FN0, Masse_carb, MTOW, MC, ZFW, v_croi, MZFW)
        return render_template('resultats.html', prix=prix)
    
    if travel_class == 'classeEcofirstaff':
        
        mtow_object=MTOWdig(int(npax),int(raction),float(coefremp),float(mach),float(allongV))
        Sref,FN0, Masse_carb, MTOW, MC, ZFW, v_croi, MZFW=mtow_object.terminer()
        economie_aff_er_object = eco_affaire_er(int(npax),int(raction),float(coefremp),float(mach),float(allongV),float(Sref))
        economie_aff_er_object.terminer()
        prix = economie_aff_er_object.TOC(FN0, Masse_carb, MTOW, MC, ZFW, v_croi, MZFW)
        return render_template('resultats.html', prix=prix)
    
    if travel_class == 'classeEcofirst':
        
        mtow_object=MTOWdig(int(npax),int(raction),float(coefremp),float(mach),float(allongV))
        Sref,FN0, Masse_carb, MTOW, MC, ZFW, v_croi, MZFW=mtow_object.terminer()
        economie_er_object = eco_premiere(int(npax),int(raction),float(coefremp),float(mach),float(allongV),float(Sref))
        economie_er_object.terminer()
        prix = economie_er_object.TOC(FN0, Masse_carb, MTOW, MC, ZFW, v_croi, MZFW)
        return render_template('resultats.html', prix=prix)
        
    else:
        return render_template('avion.html')

   
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')

    
