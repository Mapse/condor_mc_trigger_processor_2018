from coffea import processor, hist

import awkward as ak
from coffea.util import load

from coffea.lookup_tools import extractor

import numpy as np


pileup_file = "/afs/cern.ch/work/m/mabarros/public/CMSSW_10_6_12/src/OniaOpenCharmRun2ULAna/pileup_reweight/2018/pileup_weight_2018.root"
def extract_mc_weight(pileup_file):
    # creates the extractor
    ext = extractor()
    # add the weights from the pileup histograms
    ext.add_weight_sets(["weight_histogram weight_histogram " + pileup_file])
    ext.finalize()

    evaluator = ext.make_evaluator()

    return evaluator

def build_p4(acc):
    p4 = ak.zip({'x': acc['x'].value, 
                 'y': acc['y'].value,
                 'z': acc['z'].value,
                 't': acc['t'].value}, with_name="LorentzVector")

    return p4

class HistogramingProcessor(processor.ProcessorABC):
    def __init__(self, analyzer_name):
        self.analyzer_name = analyzer_name
        
        self._accumulator = processor.dict_accumulator({
            'JpsiDstar': processor.dict_accumulator({
                'Jpsi_mass': hist.Hist("Events", hist.Bin("mass", "$M_{\mu^+\mu^-}$ [GeV]", 100, 2.95, 3.25)), 
                'Jpsi_p': hist.Hist("Events", 
                                    hist.Bin("pt", "$p_{T,\mu^+\mu^-}$ [GeV]", 100, 0, 100),
                                    hist.Bin("eta", "$\eta_{\mu^+\mu^-}$", 60, -2.5, 2.5),
                                    hist.Bin("phi", "$\phi_{\mu^+\mu^-}$", 70, -3.5, 3.5)),
                'Jpsi_rap': hist.Hist("Events", hist.Bin("rap", "y", 60, -2.5, 2.5)),
                'JpsiDstar_deltarap': hist.Hist("Events", hist.Bin("deltarap", "$\Delta y$", 50, -5, 5)),
                'JpsiDstar_mass': hist.Hist("Events", hist.Bin("mass", "$m_{J/\psi D*}$ [GeV]", 50, 0, 100)),
                'Dstar_p': hist.Hist("Events",
                                 hist.Cat("chg", "charge"), 
                                 hist.Bin("pt", "$p_{T,D*}$ [GeV]", 100, 0, 50),
                                 hist.Bin("eta", "$\eta_{D*}$", 80, -2.5, 2.5),
                                 hist.Bin("phi", "$\phi_{D*}$", 70, -3.5, 3.5)),
                'Dstar_rap': hist.Hist("Events", 
                                    hist.Cat("chg", "charge"), 
                                    hist.Bin("rap", "y", 60, -2.5, 2.5)),
                'Dstar_deltam': hist.Hist("Events", 
                                        hist.Cat("chg", "charge"), 
                                        hist.Bin("deltam", "$\Delta m$ [GeV]", 50, 0.138, 0.162)),
                'Dstar_deltamr': hist.Hist("Events", 
                                        hist.Cat("chg", "charge"), 
                                        hist.Bin("deltamr", "$\Delta m_{refit}$ [GeV]", 50, 0.138, 0.162)),
                'reco_dstar_dimu' : hist.Hist("Events", 
                                    hist.Bin("dstar_pt", r"$p_{T, reco D*} [GeV]$", 45, 0, 15),
                                    hist.Bin("dimu_pt", r"$p_{T, reco J/\Psi}$ [GeV]", 60, 0, 30)),
            }),
        })
    
    @property
    def accumulator(self):
        return self._accumulator
     
    def process(self, file):
        output = self.accumulator.identity()
        acc = load(file)

      
        DimuDstar_acc = acc['DimuDstar']
        HLT_2018_acc = acc['HLT_2018']
        DimuDstar_p4 = build_p4(DimuDstar_acc)
        Primary_vertex_acc = acc['Primary_vertex']  

        ######################## Pilep correction ########################
        nPVtx = Primary_vertex_acc['nPVtx'].value
        evaluator = extract_mc_weight(pileup_file)
        corrections = evaluator['weight_histogram'](nPVtx)

        ######################## Cuts ########################   

        is_jpsi = DimuDstar_acc['Dimu']['is_jpsi'].value
        wrg_chg = DimuDstar_acc['Dstar']['wrg_chg'].value

        ## Muons cuts
        
        # Cut in the significance of the decay length.
        dlSig = (DimuDstar_acc['Dimu']['dlSig'].value < 1000000)
        dlSig_D0Dstar = (DimuDstar_acc['Dstar']['D0dlSig'].value  < 1000000) 

        ##### Creates coffea lorentz vector to apply trigger on the data #####

        ## DimuDstar collection

        # Creates the pt, eta, phi, m lorentz vector.
        DimuDstar = ak.zip({
            'jpsi_mass' : DimuDstar_acc['Dimu']['mass'].value,
            'jpsi_pt' : DimuDstar_acc['Dimu']['pt'].value,
            'jpsi_eta' : DimuDstar_acc['Dimu']['eta'].value,
            'jpsi_phi' : DimuDstar_acc['Dimu']['phi'].value,
            'jpsi_rap' : DimuDstar_acc['Dimu']['rap'].value,
            'dstar_deltam' : DimuDstar_acc['Dstar']['deltam'].value,
            'dstar_deltamr' : DimuDstar_acc['Dstar']['deltamr'].value,
            'dstar_pt' : DimuDstar_acc['Dstar']['pt'].value,
            'dstar_eta' : DimuDstar_acc['Dstar']['eta'].value,
            'dstar_phi' : DimuDstar_acc['Dstar']['phi'].value,
            'dstar_rap' : DimuDstar_acc['Dstar']['rap'].value,
            'dimu_dstar_deltarap' : DimuDstar_acc['deltarap'].value,
            'dimu_dstar_mass' : DimuDstar_p4.mass, #is_jpsi & ~wrg_chg & dlSig & dlSig_D0Dstar
            'is_jpsi' : DimuDstar_acc['Dimu']['is_jpsi'].value,
            'wrg_chg': DimuDstar_acc['Dstar']['wrg_chg'].value,}, with_name='PtEtaPhiMCandidate')  
        

        DimuDstar = ak.unflatten(DimuDstar, DimuDstar_acc['nDimuDstar'].value)

        # Trigger cut
        hlt = False
        
        hlt_filter_2018 = ['HLT_Dimuon25_Jpsi']
        hlt_filter = hlt_filter_2018

        HLT_acc = HLT_2018_acc

        if hlt:
            print(f"You are running with the trigger(s): {hlt_filter}")
            
            trigger_cut = HLT_acc[hlt_filter[0]].value
            for i in range(0, len(hlt_filter)):
                trigger_cut |= HLT_acc[hlt_filter[i]].value
                
            ## DimuDstar collection
            DimuDstar = DimuDstar[trigger_cut]
            DimuDstar = DimuDstar[DimuDstar.is_jpsi]
            DimuDstar = DimuDstar[~DimuDstar.wrg_chg]

            # Pileup corrections for DimuDstar
            DimuDstar_corr = DimuDstar      
            correcto_dimu_dstar = np.repeat(corrections, ak.num(DimuDstar_corr))

            # Associated jpsi
            jpsi_asso_mass = ak.flatten(DimuDstar.jpsi_mass)
            jpsi_asso_pt = ak.flatten(DimuDstar.jpsi_pt)
            jpsi_asso_eta = ak.flatten(DimuDstar.jpsi_eta)
            jpsi_asso_phi = ak.flatten(DimuDstar.jpsi_phi)
            jpsi_asso_rap = ak.flatten(DimuDstar.jpsi_rap)

            # Associated dstar
            dimu_dstar_right_charge = DimuDstar
            dimu_dstar_wrong_charge = DimuDstar[DimuDstar.wrg_chg]

            # Pileup corrrections for associated dstar
            DimuDstar_corr_right_charge = dimu_dstar_right_charge
            correcto_dimu_dstar_right_charge = np.repeat(corrections, ak.num(DimuDstar_corr_right_charge)) 

            DimuDstar_corr_wrong_charge = dimu_dstar_wrong_charge
            correcto_dimu_dstar_wrong_charge = np.repeat(corrections, ak.num(dimu_dstar_wrong_charge)) 

            dstar_asso_right_charge_deltamr = ak.flatten(dimu_dstar_right_charge.dstar_deltamr)
            dstar_asso_wrong_charge_deltamr = ak.flatten(dimu_dstar_wrong_charge.dstar_deltamr)
            
            dstar_asso_right_charge_deltam = ak.flatten(dimu_dstar_right_charge.dstar_deltam)
            dstar_asso_wrong_charge_deltam = ak.flatten(dimu_dstar_wrong_charge.dstar_deltam)

            dstar_asso_right_charge_pt = ak.flatten(dimu_dstar_right_charge.dstar_pt)
            dstar_asso_right_charge_eta = ak.flatten(dimu_dstar_right_charge.dstar_eta)
            dstar_asso_right_charge_phi = ak.flatten(dimu_dstar_right_charge.dstar_phi)

            dstar_asso_wrong_charge_pt = ak.flatten(dimu_dstar_wrong_charge.dstar_pt)
            dstar_asso_wrong_charge_eta = ak.flatten(dimu_dstar_wrong_charge.dstar_eta)
            dstar_asso_wrong_charge_phi = ak.flatten(dimu_dstar_wrong_charge.dstar_phi)

            dstar_asso_right_charge_rap = ak.flatten(dimu_dstar_right_charge.dstar_rap)
            dstar_asso_wrong_charge_rap = ak.flatten(dimu_dstar_wrong_charge.dstar_rap)

            # Associated object
            dimuon_dstar_deltarap = ak.flatten(DimuDstar.dimu_dstar_deltarap)
            dimuon_dstar_mass = ak.flatten(DimuDstar.dimu_dstar_mass)
            
        if not hlt:
            print("You are not running with trigger")
            trigger_cut = np.ones(len(DimuDstar), dtype=bool)

            ## DimuonDstar

            # Filters for jpsi and dstar
            is_jpsi = DimuDstar_acc['Dimu']['is_jpsi'].value
            wrg_chg = DimuDstar_acc['Dstar']['wrg_chg'].value

            DimuDstar_corr = DimuDstar[DimuDstar.is_jpsi]
            DimuDstar_corr = DimuDstar_corr[~DimuDstar_corr.wrg_chg]        
            correcto_dimu_dstar = np.repeat(corrections, ak.num(DimuDstar_corr))

            # Associated jpsi
            jpsi_asso_mass = DimuDstar_acc['Dimu']['mass'].value[is_jpsi & ~wrg_chg]
            jpsi_asso_pt = DimuDstar_acc['Dimu']['pt'].value[is_jpsi & ~wrg_chg]
            jpsi_asso_eta = DimuDstar_acc['Dimu']['eta'].value[is_jpsi & ~wrg_chg]
            jpsi_asso_phi = DimuDstar_acc['Dimu']['phi'].value[is_jpsi & ~wrg_chg]
            jpsi_asso_rap = DimuDstar_acc['Dimu']['rap'].value[is_jpsi & ~wrg_chg]

            # Associated dstar
            DimuDstar_corr_right_charge = DimuDstar[DimuDstar.is_jpsi]
            DimuDstar_corr_right_charge = DimuDstar_corr_right_charge[~DimuDstar_corr_right_charge.wrg_chg]
            correcto_dimu_dstar_right_charge = np.repeat(corrections, ak.num(DimuDstar_corr_right_charge)) 

            DimuDstar_corr_wrong_charge = DimuDstar[DimuDstar.is_jpsi]
            DimuDstar_corr_wrong_charge = DimuDstar_corr_wrong_charge[DimuDstar_corr_wrong_charge.wrg_chg]
            correcto_dimu_dstar_wrong_charge = np.repeat(corrections, ak.num(DimuDstar_corr_wrong_charge)) 

            dstar_asso_right_charge_deltamr = DimuDstar_acc['Dstar']['deltamr'].value[is_jpsi & ~wrg_chg]
            dstar_asso_wrong_charge_deltamr = DimuDstar_acc['Dstar']['deltamr'].value[is_jpsi & wrg_chg]
            
            dstar_asso_right_charge_deltam = DimuDstar_acc['Dstar']['deltam'].value[is_jpsi & ~wrg_chg]
            dstar_asso_wrong_charge_deltam = DimuDstar_acc['Dstar']['deltam'].value[is_jpsi & wrg_chg]

            dstar_asso_right_charge_pt = DimuDstar_acc['Dstar']['pt'].value[is_jpsi & ~wrg_chg]
            dstar_asso_right_charge_eta = DimuDstar_acc['Dstar']['eta'].value[is_jpsi & ~wrg_chg]
            dstar_asso_right_charge_phi = DimuDstar_acc['Dstar']['phi'].value[is_jpsi & ~wrg_chg]

            dstar_asso_wrong_charge_pt = DimuDstar_acc['Dstar']['pt'].value[is_jpsi & wrg_chg]
            dstar_asso_wrong_charge_eta = DimuDstar_acc['Dstar']['eta'].value[is_jpsi & wrg_chg]
            dstar_asso_wrong_charge_phi = DimuDstar_acc['Dstar']['phi'].value[is_jpsi & wrg_chg]

            dstar_asso_right_charge_rap = DimuDstar_acc['Dstar']['rap'].value[is_jpsi & ~wrg_chg]
            dstar_asso_wrong_charge_rap = DimuDstar_acc['Dstar']['rap'].value[is_jpsi & wrg_chg]

            # Associated object
            dimuon_dstar_deltarap = DimuDstar_acc['deltarap'].value[is_jpsi & ~wrg_chg & dlSig & dlSig_D0Dstar]
            dimuon_dstar_mass = DimuDstar_p4.mass[is_jpsi & ~wrg_chg & dlSig & dlSig_D0Dstar]

        ################# Filling the histograms #################

        is_jpsi = DimuDstar_acc['Dimu']['is_jpsi'].value
        wrg_chg = DimuDstar_acc['Dstar']['wrg_chg'].value

        # JpsiDstar
        output['JpsiDstar']['Jpsi_mass'].fill(mass=jpsi_asso_mass, weight=correcto_dimu_dstar)
        output['JpsiDstar']['Jpsi_p'].fill(pt=jpsi_asso_pt,
                                           eta=jpsi_asso_eta,
                                           phi=jpsi_asso_phi, weight=correcto_dimu_dstar)
        output['JpsiDstar']['Jpsi_rap'].fill(rap=jpsi_asso_rap, weight=correcto_dimu_dstar)

        output['JpsiDstar']['Dstar_deltamr'].fill(chg='right charge', deltamr=dstar_asso_right_charge_deltamr, weight=correcto_dimu_dstar_right_charge)
        output['JpsiDstar']['Dstar_deltamr'].fill(chg='wrong charge', deltamr=dstar_asso_wrong_charge_deltamr, weight=correcto_dimu_dstar_wrong_charge)
        output['JpsiDstar']['Dstar_deltam'].fill(chg='right charge', deltam=dstar_asso_right_charge_deltam, weight=correcto_dimu_dstar_right_charge)
        output['JpsiDstar']['Dstar_deltam'].fill(chg='wrong charge', deltam=dstar_asso_wrong_charge_deltam)
        output['JpsiDstar']['Dstar_p'].fill(chg='right charge',
                                            pt=dstar_asso_right_charge_pt,
                                            eta=dstar_asso_right_charge_eta,
                                            phi=dstar_asso_right_charge_phi, weight=correcto_dimu_dstar_right_charge)
        output['JpsiDstar']['Dstar_p'].fill(chg='wrong charge',
                                            pt=dstar_asso_wrong_charge_pt,
                                            eta=dstar_asso_wrong_charge_eta,
                                            phi=dstar_asso_wrong_charge_phi, weight=correcto_dimu_dstar_wrong_charge)
        output['JpsiDstar']['Dstar_rap'].fill(chg='right charge', rap=dstar_asso_right_charge_rap, weight=correcto_dimu_dstar_right_charge)
        output['JpsiDstar']['Dstar_rap'].fill(chg='wrong charge', rap=dstar_asso_wrong_charge_rap, weight=correcto_dimu_dstar_wrong_charge)

        output['JpsiDstar']['reco_dstar_dimu'].fill(dstar_pt=dstar_asso_right_charge_pt,
                                                    dimu_pt=jpsi_asso_pt,)

        output['JpsiDstar']['JpsiDstar_deltarap'].fill(deltarap=dimuon_dstar_deltarap, weight=correcto_dimu_dstar)
        output['JpsiDstar']['JpsiDstar_mass'].fill(mass=dimuon_dstar_mass, weight=correcto_dimu_dstar)  

        return output

    def postprocess(self, accumulator):
        return accumulator