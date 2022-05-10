import awkward as ak
import numpy as np
import numba
import coffea.processor as processor
from coffea.util import save

from coffea.nanoevents.methods import candidate
ak.behavior.update(candidate.behavior)

import random

from tools.collections import *

D0_PDG_MASS = 1.864

class EventSelectorProcessor(processor.ProcessorABC):
    def __init__(self, analyzer_name):
        self.analyzer_name = analyzer_name

        self._accumulator = processor.dict_accumulator({
            'cutflow': processor.defaultdict_accumulator(int),
        })

    @property
    def accumulator(self):
        return self._accumulator

    def process(self, events):
        output = self.accumulator.identity()

        ############### Cuts
        # Dimu cuts: charge = 0, mass cuts and chi2...
        # test if there is any events in the file
        if len(events) == 0:
            return output

        ############### Get the primary vertices  ############### 
        Primary_vertex = ak.zip({**get_vars_dict(events, primary_vertex_aod_cols)})
     
        # Collection extraction
        Dimus = ak.zip({**get_vars_dict(events, dimu_cols)}, with_name="PtEtaPhiMCandidate")
        Muons = ak.zip({**get_vars_dict(events, muon_cols)}, with_name="PtEtaPhiMCandidate")
        Dstars = ak.zip({'mass': (events.Dstar_D0mass + events.Dstar_deltamr),
                        'charge': events.Dstar_pischg,
                        **get_vars_dict(events, dstar_cols)}, 
                        with_name="PtEtaPhiMCandidate")
        
        # Saves the number of events
        output['cutflow']['Number of events'] += len(events)
        
        # Triggers for 2018 charmonium
        try:
            hlt_char_2018 = ak.zip({**get_vars_dict(events, hlt_cols_charm_2018)})
        except:
            hlt_char_2018 = ak.zip({"HLT_2018" : "HLT_2018"})
                     
        ##### Trigger cut

        # Activate trigger
        hlt = False
        # HLT to be used
        hlt_filter = 'HLT_Dimuon25_Jpsi'

        # Trigger choice
        if hlt:
            print(f"You are running with the trigger: {hlt_filter}")
            trigger_cut = hlt_char_2018[hlt_filter]
            hlt_char_2018 = hlt_char_2018[hlt_filter]
        if not hlt:
            print("You are not running with trigger")
            # Assign 1 to all events.
            trigger_cut = np.ones(len(Dimus), dtype=bool)

        # Trigger filter
        Dimu = Dimus[trigger_cut]
        Muon = Muons[trigger_cut]
        Dstar = Dstars[trigger_cut]

        ## Rec dimuon cuts
        
        # Dimu charge = 0 cut
        Dimu = Dimu[Dimu.charge == 0]

        # Jpsi mass range cut
        Dimu = Dimu[(Dimu.mass > 2.95) & (Dimu.mass < 3.25)]
        
        # Get the Muons from Dimu, for cuts in their params
        Muon = ak.zip({'0': Muon[Dimu.t1muIdx], '1': Muon[Dimu.t2muIdx]})

        # SoftId and Global Muon cuts
        soft_id = (Muon.slot0.softId > 0) & (Muon.slot1.softId > 0)
        Dimu = Dimu[soft_id] 
        Muon = Muon[soft_id] 

        # pt and eta cuts 
        muon_pt_cut = (Muon.slot0.pt > 3) & (Muon.slot1.pt > 3)         
        Dimu = Dimu[muon_pt_cut]
        Muon = Muon[muon_pt_cut]

        muon_eta_cut = (np.absolute(Muon.slot0.eta) <= 2.4) & (np.absolute(Muon.slot1.eta) <= 2.4)
        Dimu = Dimu[muon_eta_cut]
        Muon = Muon[muon_eta_cut]

        # Jpsi flag
        Dimu['is_jpsi'] = (Dimu.mass > 2.95) & (Dimu.mass < 3.25)
        
        ## Cuts for Dstar

        # Dstar has not muon cut
        Dstar = Dstar[~Dstar.hasMuon]

        # Dstar trk pt cut
        Dstar = Dstar[(Dstar.Kpt > 0.5) & (Dstar.pipt > 0.5)]
        
        # Dstar trk chi2 cut
        Dstar = Dstar[(Dstar.Kchindof < 2.5) & (Dstar.pichindof < 2.5)]
        
        # Dstar trk hits cut
        Dstar = Dstar[(Dstar.KnValid > 4) & (Dstar.pinValid > 4) & (Dstar.KnPix > 1) & (Dstar.pinPix > 1)]

        # Dstar trk impact xy cut
        Dstar = Dstar[(Dstar.Kdxy < 0.1) & (Dstar.pidxy < 0.1)]
        
        # Dstar trk impact z cut
        Dstar = Dstar[(Dstar.Kdz < 1) & (Dstar.pidz < 1)]
       
        # Dstar pis pt
        Dstar = Dstar[Dstar.pispt > 0.3]
       
        # Dstar pis chindof
        Dstar = Dstar[Dstar.pischindof < 3]
       
        # Dstar pis nvalid
        Dstar = Dstar[Dstar.pisnValid > 2]
        
        # D0 of Dstar cuts
        Dstar = Dstar[Dstar.D0cosphi > 0.99]
        
        # D0 of Dstar cosphi
        Dstar = Dstar[(Dstar.D0mass < D0_PDG_MASS + 0.028) & (Dstar.D0mass > D0_PDG_MASS - 0.028)]
        
        # D0 of Dstar mass
        Dstar = Dstar[Dstar.D0pt > 4]
        
        # D0 of Dstar mass
        Dstar = Dstar[Dstar.D0dlSig > 3]

        # D* pT
        Dstar = Dstar[Dstar.pt > 4]
        
        # D* Right charge
        Dstar['wrg_chg'] = (Dstar.Kchg == Dstar.pichg)
        Dstar = Dstar[~Dstar.wrg_chg]

        ## Dimu + Dstar

        asso = ak.cartesian([Dimu, Dstar]) # Don't need to apply vtxid because they are already supposed to be in the same vtx???
        asso = asso[asso.slot0.vtxIdx == asso.slot1.vtxIdx]

        Dimu_asso = ak.zip({
                   'pt': asso.slot0.pt,
                   'eta': asso.slot0.eta,
                   'phi': asso.slot0.phi,
                   'mass': asso.slot0.mass,
                   'charge': asso.slot0.charge}, with_name="PtEtaPhiMCandidate")
       
        Dstar_asso = ak.zip({
                    'pt': asso.slot1.pt,
                    'eta': asso.slot1.eta,
                    'phi': asso.slot1.phi,
                    'mass': asso.slot1.mass,
                    'charge': asso.slot1.charge}, with_name="PtEtaPhiMCandidate")
        
        asso['deltarap'] = asso.slot0.rap - asso.slot1.rap
        asso['cand'] = Dimu_asso + Dstar_asso

        DimuDstar = asso
        
        # Saves the total number of DimuDstar in the events
        output['cutflow']['Number of DimuDstar'] += ak.sum(ak.num(DimuDstar))
        # Takes the number of events with DimuonDstar and save it on output.
        evts_with_dimudstar  = DimuDstar[ak.num(DimuDstar) > 0]
        output['cutflow']['Number of evts with DimuDstar'] += len(evts_with_dimudstar)

        ############### Create the accumulators to save output

        ## Trigger accumulator

        # 2018 triggers
        trigger_2018_acc = processor.dict_accumulator({})
        for var in hlt_char_2018.fields:
            trigger_2018_acc[var] = processor.column_accumulator(ak.to_numpy(hlt_char_2018[var]))
        output["HLT_2018"] = trigger_2018_acc

        # Primary vertex accumulator
        primary_vertex_acc = processor.dict_accumulator({})
        for var in Primary_vertex.fields:
            #primary_vertex_acc[var] = processor.column_accumulator(ak.to_numpy(Primary_vertex[var]))
            primary_vertex_acc[var] = processor.column_accumulator(ak.to_numpy(ak.flatten(Primary_vertex[var])))
        primary_vertex_acc["nPVtx"] = processor.column_accumulator(ak.to_numpy(ak.num(Primary_vertex[var]))) 
        output["Primary_vertex"] = primary_vertex_acc

        # Accumulator for the associated candidates
        DimuDstar_acc = processor.dict_accumulator({})
        DimuDstar_acc['Dimu'] = processor.dict_accumulator({})
        DimuDstar_acc['Dstar'] = processor.dict_accumulator({})
        for var in DimuDstar.fields:
            if (var == '0') or (var =='1'):
                continue
            elif var == 'cand':
                for i0 in DimuDstar[var].fields:
                    DimuDstar_acc[i0] = processor.column_accumulator(ak.to_numpy(ak.flatten(DimuDstar[var][i0])))
            else:
                DimuDstar_acc[var] = processor.column_accumulator(ak.to_numpy(ak.flatten(DimuDstar[var])))

        for var in DimuDstar.slot0.fields:
            DimuDstar_acc['Dimu'][var] = processor.column_accumulator(ak.to_numpy(ak.flatten(DimuDstar.slot0[var])))

        for var in DimuDstar.slot1.fields:
            DimuDstar_acc['Dstar'][var] = processor.column_accumulator(ak.to_numpy(ak.flatten(DimuDstar.slot1[var])))
        DimuDstar_acc['nDimuDstar'] = processor.column_accumulator(ak.to_numpy(ak.num(DimuDstar)))
        output['DimuDstar'] = DimuDstar_acc

        file_hash = str(random.getrandbits(128)) + str(len(events))
        save(output, "output/" + self.analyzer_name + "/" + self.analyzer_name + "_" + file_hash + ".coffea")

        # return dummy accumulator
        return processor.dict_accumulator({
                'cutflow': output['cutflow']
        })

    def postprocess(self, accumulator):
        return accumulator
