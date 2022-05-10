from coffea import processor, hist

import awkward as ak
from coffea.util import load

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
            'PVtx_ntrk': hist.Hist("Events", hist.Bin("ntrk", "Num of associated tracks", 50, 0, 100)), 
            'Muon_lead_p': hist.Hist("Events", 
                                   hist.Bin("pt", "$p_{T,\mu}$ [GeV]", 100, 0, 100),
                                   hist.Bin("eta", "$\eta_{\mu}$", 60, -2.5, 2.5),
                                   hist.Bin("phi", "$\phi_{\mu}$", 70, -3.5, 3.5)),
            'Muon_trail_p': hist.Hist("Events", 
                                       hist.Bin("pt", "$p_{T,\mu}$ [GeV]", 100, 0, 50),
                                       hist.Bin("eta", "$\eta_{\mu}$", 60, -2.5, 2.5),
                                       hist.Bin("phi", "$\phi_{\mu}$", 70, -3.5, 3.5)),
            'Upsilon_mass': hist.Hist("Events", hist.Bin("mass", "$M_{\mu^+\mu^-}$ [GeV]", 100, 8.6, 11)),
            'Upsilon_p': hist.Hist("Events", 
                                   hist.Bin("pt", "$p_{T,\mu^+\mu^-}$ [GeV]", 100, 0, 50),
                                   hist.Bin("eta", "$\eta_{\mu^+\mu^-}$", 60, -2.5, 2.5),
                                   hist.Bin("phi", "$\phi_{\mu^+\mu^-}$", 70, -3.5, 3.5)),
            'Upsilon_rap': hist.Hist("Events", hist.Bin("rap", "y", 60, -2.5, 2.5)),
            'Upsilon_dl': hist.Hist("Events", hist.Bin("dl", "dl", 50, -0.2, 0.2)),
            'Upsilon_dlSig': hist.Hist("Events", hist.Bin("dlSig", "dl Significance", 100, -20, 20)),
            'Upsilon_chi2': hist.Hist("Events", hist.Bin("chi2", r"$\chi^2$", 50, 0, 5)),
            'Upsilon_cosphi': hist.Hist("Events", hist.Bin("cosphi", "pointing angle", 50, -1, 1)),
            'Jpsi_mass': hist.Hist("Events", hist.Bin("mass", "$M_{\mu^+\mu^-}$ [GeV]", 100, 2.95, 3.25)),
            'Jpsi_p': hist.Hist("Events", 
                                   hist.Bin("pt", "$p_{T,\mu^+\mu^-}$ [GeV]", 100, 0, 100),
                                   hist.Bin("eta", "$\eta_{\mu^+\mu^-}$", 60, -2.5, 2.5),
                                   hist.Bin("phi", "$\phi_{\mu^+\mu^-}$", 70, -3.5, 3.5)),
            'Jpsi_rap': hist.Hist("Events", hist.Bin("rap", "y", 60, -2.5, 2.5)),
            'Jpsi_dl': hist.Hist("Events", hist.Bin("dl", "dl", 100, -1.5, 1.5)),
            'Jpsi_dlSig': hist.Hist("Events", hist.Bin("dlSig", "dl Significance", 100, -20, 50)),
            'Jpsi_chi2': hist.Hist("Events", hist.Bin("chi2", r"$\chi^2$", 50, 0, 5)),
            'Jpsi_cosphi': hist.Hist("Events", hist.Bin("cosphi", r"$cos(\alpha)$", 50, -1, 1)),
            'Psi_mass': hist.Hist("Events", hist.Bin("mass", "$M_{\mu^+\mu^-}$ [GeV]", 100, 3.40, 4.00)),
            'Psi_p': hist.Hist("Events", 
                                   hist.Bin("pt", "$p_{T,\mu^+\mu^-}$ [GeV]", 100, 0, 100),
                                   hist.Bin("eta", "$\eta_{\mu^+\mu^-}$", 60, -2.5, 2.5),
                                   hist.Bin("phi", "$\phi_{\mu^+\mu^-}$", 70, -3.5, 3.5)),
            'Psi_rap': hist.Hist("Events", hist.Bin("rap", "y", 60, -2.5, 2.5)),
            'Psi_dl': hist.Hist("Events", hist.Bin("dl", "dl", 100, -1.5, 1.5)),
            'Psi_dlSig': hist.Hist("Events", hist.Bin("dlSig", "dl Significance", 100, -20, 50)),
            'Psi_chi2': hist.Hist("Events", hist.Bin("chi2", r"$\chi^2$", 50, 0, 5)),
            'Psi_cosphi': hist.Hist("Events", hist.Bin("cosphi", r"$cos(\alpha)$", 50, -1, 1)),
            'D0_mass12': hist.Hist("Events", hist.Bin("mass", "$m_{D^0, 12}$ [GeV]", 100, 1.7, 2.0)),
            'D0_mass21': hist.Hist("Events", hist.Bin("mass", "$m_{D^0, 21}$ [GeV]", 100, 1.7, 2.0)),
            'D0_p': hist.Hist("Events", 
                              hist.Bin("pt", "$p_{T,D^0}$ [GeV]", 100, 0, 50),
                              hist.Bin("eta", "$\eta_{D^0}$", 80, -2.5, 2.5),
                              hist.Bin("phi", "$\phi_{D^0}$", 70, -3.5, 3.5)),
            'D0_rap': hist.Hist("Events", hist.Bin("rap", "y", 60, -2.5, 2.5)),
            'D0_dl': hist.Hist("Events", hist.Bin("dl", "dl", 100, -1, 1)),
            'D0_dlSig': hist.Hist("Events", hist.Bin("dlSig", "dl Significance", 100, -30, 30)),
            'D0_chi2': hist.Hist("Events", hist.Bin("chi2", r"$\chi^2$", 50, 0, 10)),
            'D0_cosphi': hist.Hist("Events", hist.Bin("cosphi", r"$cos(\alpha)$", 50, -1, 1)),
            'D0_eta_pt': hist.Hist("Events",
                                   hist.Bin("eta", "$\eta_{D^0}$", 80, -2.5, 2.5),
                                   hist.Bin("mass", "$p_{T D^0}$ [GeV]", 100, 0, 10)),
            'D0_eta_mass': hist.Hist("Events",
                                     hist.Bin("eta", "$\eta_{D^0}$", 80, -2.5, 2.5),
                                     hist.Bin("mass", "$m_{D^0}$ [GeV]", 100, 1.7, 2.0)),
            'D0_trk_p': hist.Hist("Events", 
                                  hist.Bin("pt", "$p_{T,D^0 trks}$ [GeV]", 100, 0, 50),
                                  hist.Bin("eta", "$\eta_{D^0 trks}$", 80, -2.5, 2.5),
                                  hist.Bin("phi", "$\phi_{D^0 trks}$", 70, -3.5, 3.5)),
            'D0_trk_chindof': hist.Hist("Events", hist.Bin("chindof", r"$\chi^2/ndof$", 50, 0, 2.5)),
            'D0_trk_nValid': hist.Hist("Events", hist.Bin("nValid", "# of Tracker Hits", 40, -0.5, 39.5)),
            'D0_trk_nPix': hist.Hist("Events", hist.Bin("nPix", "# of Pixel Hits", 15, -0.5, 14.5)),
            'D0_trk_dxy': hist.Hist("Events", hist.Bin("dxy", "dxy", 100, 0, 0.1)),
            'D0_trk_dz': hist.Hist("Events", hist.Bin("dz", "dz", 100, -1, 1)),
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
            'Dstar_K_p': hist.Hist("Events", 
                                   hist.Bin("pt", "$p_{T,D* K}$ [GeV]", 100, 0, 30),
                                   hist.Bin("eta", "$\eta_{D* K}$", 60, -2.5, 2.5),
                                   hist.Bin("phi", "$\phi_{D* K}$", 70, -3.5, 3.5)),
            'Dstar_K_chindof': hist.Hist("Events", hist.Bin("chindof", r"$\chi^2/ndof$", 50, 0, 2.5)),
            'Dstar_K_nValid': hist.Hist("Events", hist.Bin("nValid", "# of Tracker Hits", 40, -0.5, 39.5)),
            'Dstar_K_nPix': hist.Hist("Events", hist.Bin("nPix", "# of Pixel Hits", 15, -0.5, 14.5)),
            'Dstar_K_dxy': hist.Hist("Events", hist.Bin("dxy", "dxy", 100, 0, 0.1)),
            'Dstar_K_dz': hist.Hist("Events", hist.Bin("dz", "dz", 100, -0.2, 0.2)),
            'Dstar_K_pt_eta': hist.Hist("Events",
                                        hist.Bin("pt", "$p_{T,D* K}$ [GeV]", 100, 0, 10),
                                        hist.Bin("eta", "$\eta_{D* K}$", 60, -2.5, 2.5)),
            'Dstar_pi_p': hist.Hist("Events", 
                                    hist.Bin("pt", "$p_{T,D* \pi}$ [GeV]", 100, 0, 30),
                                    hist.Bin("eta", "$\eta_{D* \pi}$", 60, -2.5, 2.5),
                                    hist.Bin("phi", "$\phi_{D* \pi}$", 70, -3.5, 3.5)),
            'Dstar_pi_chindof': hist.Hist("Events", hist.Bin("chindof", r"$\chi^2/ndof$", 50, 0, 2.5)),
            'Dstar_pi_nValid': hist.Hist("Events", hist.Bin("nValid", "# of Tracker Hits", 40, -0.5, 39.5)),
            'Dstar_pi_nPix': hist.Hist("Events", hist.Bin("nPix", "# of Pixel Hits", 15, -0.5, 14.5)),
            'Dstar_pi_dxy': hist.Hist("Events", hist.Bin("dxy", "dxy", 100, 0, 0.1)),
            'Dstar_pi_dz': hist.Hist("Events", hist.Bin("dz", "dz", 100, -0.1, 0.1)),
            'Dstar_pi_pt_eta': hist.Hist("Events",
                                          hist.Bin("pt", "$p_{T,D* \pi}$ [GeV]", 100, 0, 10),
                                          hist.Bin("eta", "$\eta_{D* \pi}$", 60, -2.5, 2.5)),
            'Dstar_pis_p': hist.Hist("Events", 
                                     hist.Bin("pt", "$p_{T,D* \pi_s}$ [GeV]", 100, 0, 20),
                                     hist.Bin("eta", "$\eta_{D* \pi_s}$", 60, -2.5, 2.5),
                                     hist.Bin("phi", "$\phi_{D* \pi_s}$", 70, -3.5, 3.5)),
            'Dstar_pis_chindof': hist.Hist("Events", hist.Bin("chindof", r"$\chi^2/ndof$", 50, 0, 5)),
            'Dstar_pis_nValid': hist.Hist("Events", hist.Bin("nValid", "# of Tracker Hits", 40, -0.5, 39.5)),
            'Dstar_pis_nPix': hist.Hist("Events", hist.Bin("nPix", "# of Pixel Hits", 15, -0.5, 14.5)),
            'Dstar_pis_dxy': hist.Hist("Events", hist.Bin("dxy", "dxy", 100, 0, 0.2)),
            'Dstar_pis_dz': hist.Hist("Events", hist.Bin("dz", "dz", 100, -2, 2)),
            'UpsilonDstar': processor.dict_accumulator({
                'Upsilon_mass': hist.Hist("Events", hist.Bin("mass", "$M_{\mu^+\mu^-}$ [GeV]", 100, 8.6, 11)),
                'Upsilon_p': hist.Hist("Events", 
                                    hist.Bin("pt", "$p_{T,\mu^+\mu^-}$ [GeV]", 100, 0, 50),
                                    hist.Bin("eta", "$\eta_{\mu^+\mu^-}$", 60, -2.5, 2.5),
                                    hist.Bin("phi", "$\phi_{\mu^+\mu^-}$", 70, -3.5, 3.5)),
                'Upsilon_rap': hist.Hist("Events", hist.Bin("rap", "y", 60, -2.5, 2.5)),
                'UpsilonDstar_deltarap': hist.Hist("Events", hist.Bin("deltarap", "$\Delta y$", 50, -5, 5)),
                'UpsilonDstar_mass': hist.Hist("Events", hist.Bin("mass", r"$m_{\Upsilon D*}$ [GeV]", 100, 0, 50)),
                'Dstar_p': hist.Hist("Events", 
                                 hist.Bin("pt", "$p_{T,D*}$ [GeV]", 100, 0, 50),
                                 hist.Bin("eta", "$\eta_{D*}$", 80, -2.5, 2.5),
                                 hist.Bin("phi", "$\phi_{D*}$", 70, -3.5, 3.5)),
                'Dstar_deltam': hist.Hist("Events", 
                                          hist.Cat("chg", "charge"), 
                                          hist.Bin("deltam", "$\Delta m$ [GeV]", 50, 0.138, 0.162)),
                'Dstar_deltamr': hist.Hist("Events",
                                           hist.Cat("chg", "charge"),  
                                           hist.Bin("deltamr", "$\Delta m_{refit}$ [GeV]", 50, 0.138, 0.162)),
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
            }),
            'JpsiDstar': processor.dict_accumulator({
                'Jpsi_mass': hist.Hist("Events", hist.Bin("mass", "$M_{\mu^+\mu^-}$ [GeV]", 100, 2.95, 3.25)), 
                'Jpsi_p': hist.Hist("Events", 
                                    hist.Bin("pt", "$p_{T,\mu^+\mu^-}$ [GeV]", 100, 0, 100),
                                    hist.Bin("eta", "$\eta_{\mu^+\mu^-}$", 60, -2.5, 2.5),
                                    hist.Bin("phi", "$\phi_{\mu^+\mu^-}$", 70, -3.5, 3.5)),
                'Jpsi_rap': hist.Hist("Events", hist.Bin("rap", "y", 60, -2.5, 2.5)),
                'JpsiDstar_deltarap': hist.Hist("Events", hist.Bin("deltarap", "$\Delta y$", 50, -5, 5)),
                'JpsiDstar_mass': hist.Hist("Events", hist.Bin("mass", "$m_{J/\psi D*}$ [GeV]", 100, 0, 100)),
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
            }),
            'PsiDstar': processor.dict_accumulator({
                'Psi_mass': hist.Hist("Events", hist.Bin("mass", "$M_{\mu^+\mu^-}$ [GeV]", 100, 3.40, 4.00)), 
                'Psi_p': hist.Hist("Events", 
                                    hist.Bin("pt", "$p_{T,\mu^+\mu^-}$ [GeV]", 100, 0, 100),
                                    hist.Bin("eta", "$\eta_{\mu^+\mu^-}$", 60, -2.5, 2.5),
                                    hist.Bin("phi", "$\phi_{\mu^+\mu^-}$", 70, -3.5, 3.5)),
                'Psi_rap': hist.Hist("Events", hist.Bin("rap", "y", 60, -2.5, 2.5)),
                'PsiDstar_deltarap': hist.Hist("Events", hist.Bin("deltarap", "$\Delta y$", 50, -5, 5)),
                'PsiDstar_mass': hist.Hist("Events", hist.Bin("mass", "$m_{\psi(2S) D*}$ [GeV]", 100, 0, 100)),
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
            }),
        })
        
    @property
    def accumulator(self):
        return self._accumulator
     
    def process(self, file):
        output = self.accumulator.identity()
        acc = load(file)

        Muon_lead_acc = acc['Muon_lead']
        Muon_trail_acc = acc['Muon_trail']
        Dimu_acc = acc['Dimu']
        D0_acc = acc['D0']
        D0_trk_acc = acc['D0_trk']
        Dstar_acc = acc['Dstar']
        Dstar_trk_acc = acc['Dstar_trk']
        DimuDstar_acc = acc['DimuDstar']
        Primary_vertex_acc = acc['Primary_vertex'] 
        HLT_2017_acc = acc['HLT_2017']
        DimuDstar_p4 = build_p4(DimuDstar_acc)

        ######################## Cuts ########################   

        # Cut in the significance of the decay length.
        dlSig = (DimuDstar_acc['Dimu']['dlSig'].value < 1000000)
        dlSig_D0Dstar = (DimuDstar_acc['Dstar']['D0dlSig'].value  < 1000000)  
        
        # Trigger cut
        trigger_cut = HLT_2017_acc['HLT_Dimuon25_Jpsi'] == 1
    
        # Primary vertex
        output['PVtx_ntrk'].fill(ntrk=Primary_vertex_acc['ntrk'].value)
        
        #Muon
        output['Muon_lead_p'].fill(pt=Muon_lead_acc['pt'].value,
                                   eta=Muon_lead_acc['eta'].value,
                                   phi=Muon_lead_acc['phi'].value)
        output['Muon_trail_p'].fill(pt=Muon_trail_acc['pt'].value,
                                    eta=Muon_trail_acc['eta'].value,
                                    phi=Muon_trail_acc['phi'].value)
        # Upsilon
        output['Upsilon_mass'].fill(mass=Dimu_acc['mass'].value[Dimu_acc['is_ups'].value])
        output['Upsilon_p'].fill(pt=Dimu_acc['pt'].value[Dimu_acc['is_ups'].value],
                                 eta=Dimu_acc['eta'].value[Dimu_acc['is_ups'].value],
                                 phi=Dimu_acc['phi'].value[Dimu_acc['is_ups'].value])
        output['Upsilon_rap'].fill(rap=Dimu_acc['rap'].value[Dimu_acc['is_ups'].value])
        output['Upsilon_dl'].fill(dl=Dimu_acc['dl'].value[Dimu_acc['is_ups'].value])
        output['Upsilon_dlSig'].fill(dlSig=Dimu_acc['dlSig'].value[Dimu_acc['is_ups'].value])
        output['Upsilon_chi2'].fill(chi2=Dimu_acc['chi2'].value[Dimu_acc['is_ups'].value])
        output['Upsilon_cosphi'].fill(cosphi=Dimu_acc['cosphi'].value[Dimu_acc['is_ups'].value])

        # Jpsi
        output['Jpsi_mass'].fill(mass=Dimu_acc['mass'].value[Dimu_acc['is_jpsi'].value])
        output['Jpsi_p'].fill(pt=Dimu_acc['pt'].value[Dimu_acc['is_jpsi'].value],
                                 eta=Dimu_acc['eta'].value[Dimu_acc['is_jpsi'].value],
                                 phi=Dimu_acc['phi'].value[Dimu_acc['is_jpsi'].value])
        output['Jpsi_rap'].fill(rap=Dimu_acc['rap'].value[Dimu_acc['is_jpsi'].value])
        output['Jpsi_dl'].fill(dl=Dimu_acc['dl'].value[Dimu_acc['is_jpsi'].value])
        output['Jpsi_dlSig'].fill(dlSig=Dimu_acc['dlSig'].value[Dimu_acc['is_jpsi'].value])
        output['Jpsi_chi2'].fill(chi2=Dimu_acc['chi2'].value[Dimu_acc['is_jpsi'].value])
        output['Jpsi_cosphi'].fill(cosphi=Dimu_acc['cosphi'].value[Dimu_acc['is_jpsi'].value])

        # Psi
        output['Psi_mass'].fill(mass=Dimu_acc['mass'].value[Dimu_acc['is_psi'].value])
        output['Psi_p'].fill(pt=Dimu_acc['pt'].value[Dimu_acc['is_psi'].value],
                                 eta=Dimu_acc['eta'].value[Dimu_acc['is_psi'].value],
                                 phi=Dimu_acc['phi'].value[Dimu_acc['is_psi'].value])
        output['Psi_rap'].fill(rap=Dimu_acc['rap'].value[Dimu_acc['is_psi'].value])
        output['Psi_dl'].fill(dl=Dimu_acc['dl'].value[Dimu_acc['is_psi'].value])
        output['Psi_dlSig'].fill(dlSig=Dimu_acc['dlSig'].value[Dimu_acc['is_psi'].value])
        output['Psi_chi2'].fill(chi2=Dimu_acc['chi2'].value[Dimu_acc['is_psi'].value])
        output['Psi_cosphi'].fill(cosphi=Dimu_acc['cosphi'].value[Dimu_acc['is_psi'].value])

        # D0
        output['D0_mass12'].fill(mass=D0_acc['mass12'].value)
        output['D0_mass21'].fill(mass=D0_acc['mass21'].value)
        output['D0_p'].fill(pt=D0_acc['pt'].value,
                            eta=D0_acc['eta'].value,
                            phi=D0_acc['phi'].value)
        output['D0_rap'].fill(rap=D0_acc['rap'].value)
        output['D0_dl'].fill(dl=D0_acc['dl'].value)
        output['D0_dlSig'].fill(dlSig=D0_acc['dlSig'].value)
        output['D0_chi2'].fill(chi2=D0_acc['chi2'].value)
        output['D0_cosphi'].fill(cosphi=D0_acc['cosphi'].value)
        output['D0_eta_mass'].fill(eta=D0_acc['eta'].value,
                                   mass=D0_acc['mass'].value)

        # D0 trks
        output['D0_trk_p'].fill(pt=D0_trk_acc['t1pt'].value,
                                eta=D0_trk_acc['t1eta'].value,
                                phi=D0_trk_acc['t1phi'].value)
        output['D0_trk_p'].fill(pt=D0_trk_acc['t2pt'].value,
                                eta=D0_trk_acc['t2eta'].value,
                                phi=D0_trk_acc['t2phi'].value)
        output['D0_trk_chindof'].fill(chindof=D0_trk_acc['t1chindof'].value)
        output['D0_trk_chindof'].fill(chindof=D0_trk_acc['t2chindof'].value)
        output['D0_trk_nValid'].fill(nValid=D0_trk_acc['t1nValid'].value)
        output['D0_trk_nValid'].fill(nValid=D0_trk_acc['t2nValid'].value)
        output['D0_trk_nPix'].fill(nPix=D0_trk_acc['t1nPix'].value)
        output['D0_trk_nPix'].fill(nPix=D0_trk_acc['t2nPix'].value)
        output['D0_trk_dxy'].fill(dxy=D0_trk_acc['t1dxy'].value)
        output['D0_trk_dxy'].fill(dxy=D0_trk_acc['t2dxy'].value)
        output['D0_trk_dz'].fill(dz=D0_trk_acc['t1dz'].value)
        output['D0_trk_dz'].fill(dz=D0_trk_acc['t2dz'].value)
        
        # Dstar
        output['Dstar_p'].fill(chg='right charge', 
                               pt=Dstar_acc['pt'].value[~Dstar_acc['wrg_chg'].value],
                               eta=Dstar_acc['eta'].value[~Dstar_acc['wrg_chg'].value],
                               phi=Dstar_acc['phi'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_p'].fill(chg='wrong charge', 
                               pt=Dstar_acc['pt'].value[Dstar_acc['wrg_chg'].value],
                               eta=Dstar_acc['eta'].value[Dstar_acc['wrg_chg'].value],
                               phi=Dstar_acc['phi'].value[Dstar_acc['wrg_chg'].value])
        output['Dstar_rap'].fill(chg='right charge', rap=Dstar_acc['rap'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_rap'].fill(chg='wrong charge', rap=Dstar_acc['rap'].value[Dstar_acc['wrg_chg'].value])
        output['Dstar_deltamr'].fill(chg='right charge', deltamr=Dstar_acc['deltamr'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_deltamr'].fill(chg='wrong charge', deltamr=Dstar_acc['deltamr'].value[Dstar_acc['wrg_chg'].value])
        output['Dstar_deltam'].fill(chg='right charge', deltam=Dstar_acc['deltam'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_deltam'].fill(chg='wrong charge', deltam=Dstar_acc['deltam'].value[Dstar_acc['wrg_chg'].value])
        
        # Dstar trks
        output['Dstar_K_p'].fill(pt=Dstar_trk_acc['Kpt'].value[~Dstar_acc['wrg_chg'].value],
                                 eta=Dstar_trk_acc['Keta'].value[~Dstar_acc['wrg_chg'].value],
                                 phi=Dstar_trk_acc['Kphi'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_K_chindof'].fill(chindof=Dstar_trk_acc['Kchindof'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_K_nValid'].fill(nValid=Dstar_trk_acc['KnValid'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_K_nPix'].fill(nPix=Dstar_trk_acc['KnPix'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_K_dxy'].fill(dxy=Dstar_trk_acc['Kdxy'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_K_dz'].fill(dz=Dstar_trk_acc['Kdz'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_K_pt_eta'].fill(pt=Dstar_trk_acc['Kpt'].value[~Dstar_acc['wrg_chg'].value],
                                      eta=Dstar_trk_acc['Keta'].value[~Dstar_acc['wrg_chg'].value])

        output['Dstar_pi_p'].fill(pt=Dstar_trk_acc['pipt'].value[~Dstar_acc['wrg_chg'].value],
                                  eta=Dstar_trk_acc['pieta'].value[~Dstar_acc['wrg_chg'].value],
                                  phi=Dstar_trk_acc['piphi'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pi_chindof'].fill(chindof=Dstar_trk_acc['pichindof'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pi_nValid'].fill(nValid=Dstar_trk_acc['pinValid'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pi_nPix'].fill(nPix=Dstar_trk_acc['pinPix'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pi_dxy'].fill(dxy=Dstar_trk_acc['pidxy'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pi_dz'].fill(dz=Dstar_trk_acc['pidz'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pi_pt_eta'].fill(pt=Dstar_trk_acc['pipt'].value[~Dstar_acc['wrg_chg'].value],
                                       eta=Dstar_trk_acc['pieta'].value[~Dstar_acc['wrg_chg'].value])

        output['Dstar_pis_p'].fill(pt=Dstar_trk_acc['pispt'].value[~Dstar_acc['wrg_chg'].value],
                                   eta=Dstar_trk_acc['piseta'].value[~Dstar_acc['wrg_chg'].value],
                                   phi=Dstar_trk_acc['pisphi'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pis_chindof'].fill(chindof=Dstar_trk_acc['pischindof'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pis_nValid'].fill(nValid=Dstar_trk_acc['pisnValid'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pis_nPix'].fill(nPix=Dstar_trk_acc['pisnPix'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pis_dxy'].fill(dxy=Dstar_trk_acc['pisdxy'].value[~Dstar_acc['wrg_chg'].value])
        output['Dstar_pis_dz'].fill(dz=Dstar_trk_acc['pisdz'].value[~Dstar_acc['wrg_chg'].value])

        ############# DimuDstar
        is_ups = DimuDstar_acc['Dimu']['is_ups'].value
        is_jpsi = DimuDstar_acc['Dimu']['is_jpsi'].value
        is_psi = DimuDstar_acc['Dimu']['is_psi'].value
        wrg_chg = DimuDstar_acc['Dstar']['wrg_chg'].value

        # Upsilon
        output['UpsilonDstar']['Upsilon_mass'].fill(mass=DimuDstar_acc['Dimu']['mass'].value[is_ups & ~wrg_chg])
        output['UpsilonDstar']['Upsilon_p'].fill(pt=DimuDstar_acc['Dimu']['pt'].value[is_ups & ~wrg_chg],
                                                 eta=DimuDstar_acc['Dimu']['eta'].value[is_ups & ~wrg_chg],
                                                 phi=DimuDstar_acc['Dimu']['phi'].value[is_ups & ~wrg_chg])
        output['UpsilonDstar']['Upsilon_rap'].fill(rap=DimuDstar_acc['Dimu']['rap'].value[is_ups & ~wrg_chg])

        output['UpsilonDstar']['Dstar_deltamr'].fill(chg='right charge', deltamr=DimuDstar_acc['Dstar']['deltamr'].value[is_ups & ~wrg_chg])
        output['UpsilonDstar']['Dstar_deltamr'].fill(chg='wrong charge', deltamr=DimuDstar_acc['Dstar']['deltamr'].value[is_ups & wrg_chg])
        output['UpsilonDstar']['Dstar_deltam'].fill(chg='right charge', deltam=DimuDstar_acc['Dstar']['deltam'].value[is_ups & ~wrg_chg])
        output['UpsilonDstar']['Dstar_deltam'].fill(chg='wrong charge', deltam=DimuDstar_acc['Dstar']['deltam'].value[is_ups & wrg_chg])
        output['UpsilonDstar']['Dstar_p'].fill(chg='right charge',
                                               pt=DimuDstar_acc['Dstar']['pt'].value[is_ups & ~wrg_chg],
                                               eta=DimuDstar_acc['Dstar']['eta'].value[is_ups & ~wrg_chg],
                                               phi=DimuDstar_acc['Dstar']['phi'].value[is_ups & ~wrg_chg])
        output['UpsilonDstar']['Dstar_p'].fill(chg='wrong charge',
                                               pt=DimuDstar_acc['Dstar']['pt'].value[is_ups & wrg_chg],
                                               eta=DimuDstar_acc['Dstar']['eta'].value[is_ups & wrg_chg],
                                               phi=DimuDstar_acc['Dstar']['phi'].value[is_ups & wrg_chg])
        output['UpsilonDstar']['Dstar_rap'].fill(chg='right charge', rap=DimuDstar_acc['Dstar']['rap'].value[is_ups & ~wrg_chg])
        output['UpsilonDstar']['Dstar_rap'].fill(chg='wrong charge', rap=DimuDstar_acc['Dstar']['rap'].value[is_ups & wrg_chg])

        output['UpsilonDstar']['UpsilonDstar_deltarap'].fill(deltarap=DimuDstar_acc['deltarap'].value[is_ups & ~wrg_chg])
        output['UpsilonDstar']['UpsilonDstar_mass'].fill(mass=DimuDstar_p4.mass[is_ups & ~wrg_chg])

        # JpsiDstar
        output['JpsiDstar']['Jpsi_mass'].fill(mass=DimuDstar_acc['Dimu']['mass'].value[is_jpsi & ~wrg_chg])
        output['JpsiDstar']['Jpsi_p'].fill(pt=DimuDstar_acc['Dimu']['pt'].value[is_jpsi & ~wrg_chg],
                                           eta=DimuDstar_acc['Dimu']['eta'].value[is_jpsi & ~wrg_chg],
                                           phi=DimuDstar_acc['Dimu']['phi'].value[is_jpsi & ~wrg_chg])
        output['JpsiDstar']['Jpsi_rap'].fill(rap=DimuDstar_acc['Dimu']['rap'].value[is_jpsi & ~wrg_chg])

        output['JpsiDstar']['Dstar_deltamr'].fill(chg='right charge', deltamr=DimuDstar_acc['Dstar']['deltamr'].value[is_jpsi & ~wrg_chg])
        output['JpsiDstar']['Dstar_deltamr'].fill(chg='wrong charge', deltamr=DimuDstar_acc['Dstar']['deltamr'].value[is_jpsi & wrg_chg])
        output['JpsiDstar']['Dstar_deltam'].fill(chg='right charge', deltam=DimuDstar_acc['Dstar']['deltam'].value[is_jpsi & ~wrg_chg])
        output['JpsiDstar']['Dstar_deltam'].fill(chg='wrong charge', deltam=DimuDstar_acc['Dstar']['deltam'].value[is_jpsi & wrg_chg])
        output['JpsiDstar']['Dstar_p'].fill(chg='right charge',
                                            pt=DimuDstar_acc['Dstar']['pt'].value[is_jpsi & ~wrg_chg],
                                            eta=DimuDstar_acc['Dstar']['eta'].value[is_jpsi & ~wrg_chg],
                                            phi=DimuDstar_acc['Dstar']['phi'].value[is_jpsi & ~wrg_chg])
        output['JpsiDstar']['Dstar_p'].fill(chg='wrong charge',
                                            pt=DimuDstar_acc['Dstar']['pt'].value[is_jpsi & wrg_chg],
                                            eta=DimuDstar_acc['Dstar']['eta'].value[is_jpsi & wrg_chg],
                                            phi=DimuDstar_acc['Dstar']['phi'].value[is_jpsi & wrg_chg])
        output['JpsiDstar']['Dstar_rap'].fill(chg='right charge', rap=DimuDstar_acc['Dstar']['rap'].value[is_jpsi & ~wrg_chg])
        output['JpsiDstar']['Dstar_rap'].fill(chg='wrong charge', rap=DimuDstar_acc['Dstar']['rap'].value[is_jpsi & wrg_chg])

        output['JpsiDstar']['JpsiDstar_deltarap'].fill(deltarap=DimuDstar_acc['deltarap'].value[is_jpsi & ~wrg_chg & dlSig & dlSig_D0Dstar])
        output['JpsiDstar']['JpsiDstar_mass'].fill(mass=DimuDstar_p4.mass[is_jpsi & ~wrg_chg & dlSig & dlSig_D0Dstar])

        # Psi
        output['PsiDstar']['Psi_mass'].fill(mass=DimuDstar_acc['Dimu']['mass'].value[is_psi & ~wrg_chg])
        output['PsiDstar']['Psi_p'].fill(pt=DimuDstar_acc['Dimu']['pt'].value[is_psi & ~wrg_chg],
                                           eta=DimuDstar_acc['Dimu']['eta'].value[is_psi & ~wrg_chg],
                                           phi=DimuDstar_acc['Dimu']['phi'].value[is_psi & ~wrg_chg])
        output['PsiDstar']['Psi_rap'].fill(rap=DimuDstar_acc['Dimu']['rap'].value[is_psi & ~wrg_chg])

        output['PsiDstar']['Dstar_deltamr'].fill(chg='right charge', deltamr=DimuDstar_acc['Dstar']['deltamr'].value[is_psi & ~wrg_chg])
        output['PsiDstar']['Dstar_deltamr'].fill(chg='wrong charge', deltamr=DimuDstar_acc['Dstar']['deltamr'].value[is_psi & wrg_chg])
        output['PsiDstar']['Dstar_deltam'].fill(chg='right charge', deltam=DimuDstar_acc['Dstar']['deltam'].value[is_psi & ~wrg_chg])
        output['PsiDstar']['Dstar_deltam'].fill(chg='wrong charge', deltam=DimuDstar_acc['Dstar']['deltam'].value[is_psi & wrg_chg])
        output['PsiDstar']['Dstar_p'].fill(chg='right charge',
                                            pt=DimuDstar_acc['Dstar']['pt'].value[is_psi & ~wrg_chg],
                                            eta=DimuDstar_acc['Dstar']['eta'].value[is_psi & ~wrg_chg],
                                            phi=DimuDstar_acc['Dstar']['phi'].value[is_psi & ~wrg_chg])
        output['PsiDstar']['Dstar_p'].fill(chg='wrong charge',
                                            pt=DimuDstar_acc['Dstar']['pt'].value[is_psi & wrg_chg],
                                            eta=DimuDstar_acc['Dstar']['eta'].value[is_psi & wrg_chg],
                                            phi=DimuDstar_acc['Dstar']['phi'].value[is_psi & wrg_chg])
        output['PsiDstar']['Dstar_rap'].fill(chg='right charge', rap=DimuDstar_acc['Dstar']['rap'].value[is_psi & ~wrg_chg])
        output['PsiDstar']['Dstar_rap'].fill(chg='wrong charge', rap=DimuDstar_acc['Dstar']['rap'].value[is_psi & wrg_chg])

        output['PsiDstar']['PsiDstar_deltarap'].fill(deltarap=DimuDstar_acc['deltarap'].value[is_psi & ~wrg_chg])
        output['PsiDstar']['PsiDstar_mass'].fill(mass=DimuDstar_p4.mass[is_psi & ~wrg_chg])

        return output

    def postprocess(self, accumulator):
        return accumulator      
