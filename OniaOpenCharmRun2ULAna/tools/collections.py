## About me:
# This module is where we put all the nanoAODplus variables to be used
# All variables as well as their descrition can be found on: https://twiki.cern.ch/twiki/pub/CMS/DPOANanoAODlike/nanoAODlikev0.6.html#GenPart

import numpy as np

# Muon variables
muon_cols = ['Muon_charge', 'Muon_dxy', 'Muon_dxyErr', 'Muon_dz', 'Muon_dzErr', 'Muon_eta', 'Muon_isGlobal', 'Muon_mass',
             'Muon_phi', 'Muon_pt', 'Muon_ptErr', 'Muon_softId', 'Muon_vtxIdx', 'Muon_vtxFlag', 'Muon_simIdx', 'Muon_Id']

dimu_cols = ['Dimu_pt', 'Dimu_eta', 'Dimu_phi', 'Dimu_rap', 'Dimu_mass', 'Dimu_charge', 'Dimu_vtxIdx', 'Dimu_chi2', 'Dimu_dl',
             'Dimu_dlErr', 'Dimu_dlSig', 'Dimu_cosphi', 'Dimu_x', 'Dimu_y', 'Dimu_z', 'Dimu_t1muIdx', 'Dimu_t2muIdx', 'Dimu_simIdx']

d0_cols = ['D0_pt', 'D0_eta', 'D0_phi', 'D0_rap', 'D0_mass12', 'D0_mass21', 'D0_vtxIdx', 'D0_chi2', 'D0_dl', 'D0_dlErr', 'D0_dlSig',
           'D0_cosphi', 'D0_x', 'D0_y', 'D0_z', 'D0_hasMuon', 'D0_t1pt', 'D0_t1eta', 'D0_t1phi', 'D0_t1chindof', 'D0_t1nValid',
           'D0_t1nPix', 'D0_t1dxy', 'D0_t1dz', 'D0_t1chg', 'D0_t2pt', 'D0_t2eta', 'D0_t2phi', 'D0_t2chindof', 'D0_t2nValid',
           'D0_t2nPix', 'D0_t2dxy', 'D0_t2dz', 'D0_t2chg', 'D0_simIdx']

dstar_cols = ['Dstar_pt', 'Dstar_eta', 'Dstar_phi', 'Dstar_rap', 'Dstar_deltam', 'Dstar_deltamr', 'Dstar_vtxIdx', 'Dstar_hasMuon',
              'Dstar_D0pt', 'Dstar_D0eta', 'Dstar_D0phi', 'Dstar_D0mass', 'Dstar_D0chi2', 'Dstar_D0dl', 'Dstar_D0dlErr',
              'Dstar_D0dlSig', 'Dstar_D0cosphi', 'Dstar_D0x', 'Dstar_D0y', 'Dstar_D0z',
              'Dstar_Kpt', 'Dstar_Keta', 'Dstar_Kphi', 'Dstar_KvtxIdx', 'Dstar_Kchindof', 'Dstar_KnValid', 'Dstar_KnPix', 'Dstar_Kdxy',
              'Dstar_Kdz', 'Dstar_Kchg',
              'Dstar_pipt', 'Dstar_pieta', 'Dstar_piphi', 'Dstar_pivtxIdx', 'Dstar_pichindof', 'Dstar_pinValid', 'Dstar_pinPix',
              'Dstar_pidxy', 'Dstar_pidz', 'Dstar_pichg',
              'Dstar_pispt', 'Dstar_piseta', 'Dstar_pisphi', 'Dstar_pisvtxIdx', 'Dstar_pischindof', 'Dstar_pisnValid', 'Dstar_pisnPix',
              'Dstar_pisdxy', 'Dstar_pisdz', 'Dstar_simIdx']

# Total number of reconstructed primary vertices
primary_vertex_cols = ['PV_chi2', 'PV_ndof', 'PV_npvs', 'PV_npvsGood', 'PV_score', 'PV_x', 'PV_y', 'PV_z']

# Primary vertices (AOD, with or w/o cuts)
primary_vertex_aod_cols = ['nPVtx' ,'PVtx_Id', 'PVtx_isGood', 'PVtx_x', 'PVtx_y', 'PVtx_z', 'PVtx_ntrk', 'PVtx_x', 'PVtx_sumPt']

# Interesting gen particles
gen_part_cols = ['GenPart_eta', 'GenPart_genPartIdxMother', 'GenPart_mass', 'GenPart_pdgId', "GenPart_phi", "GenPart_pt", 'GenPart_status',
                 'GenPart_Id', 'GenPart_parpdgId', 'GenPart_sparpdgId', 'GenPart_numberOfDaughters', 'GenPart_nstchgdaug', 'GenPart_vx', 
                 'GenPart_vy', 'GenPart_vz', 'GenPart_mvx', 'GenPart_mvy', 'GenPart_mvz', 'GenPart_recIdx']

hlt_cols_charm_2016 = ['HLT_Dimuon16_Jpsi' , 'HLT_Dimuon20_Jpsi'] #'HLT_Dimuo10_Jpsi_Barrel', 

hlt_cols_charm_2017 = ['HLT_Dimuon0_Jpsi', 'HLT_Dimuon20_Jpsi_Barrel_Seagulls' , 'HLT_Dimuon25_Jpsi']

hlt_cols_charm_2018 = ['HLT_Dimuon20_Jpsi_Barrel_Seagulls', 'HLT_Dimuon25_Jpsi', 'HLT_DoubleMu4_3_Jpsi']

# This function is called to keep the cols in a good way to be read on the EventSelectProcessor.py
def get_vars_dict(events, col_list):
    dict = {}
    col = ''
    for c in col_list:
        if c.startswith('Muon'):
            col = c[5:]
        elif c.startswith('Dimu'):
            col = c[4:]
            if col.startswith('_'): col = col[1:]
        elif c.startswith('D0'):
            col = c[2:]
            if col.startswith('_'): col = col[1:]
        elif c.startswith('Dstar'):
            col = c[5:]
            if col.startswith('_'): col = col[1:]
        elif c.startswith('PVtx'):
            col = c[5:]
            if col.startswith('_'): col = col[1:]
        elif c.startswith('GenPart'):
            col = c[8:]
            if col.startswith('_'): col = col[1:]
        elif c.startswith('HLT'):
            col = c[:]
        else:
            Exception('Not good!')

        if col == 'x' or col == 'y' or col == 'z':
            col = 'vtx_' + col

        if len(events[c]) == 0:
            dict[col] = np.array([])
        else:
            dict[col] = events[c]
    return dict



