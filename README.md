# HiggsTagger
ROOT TMVA based Higgs Tagger

In order to run, you need to have ROOT installed. At PSI you can do 
cd /swshare/ROOT/root_v5.34.18_slc6_amd64_py26_pythia6; export LD_LIBRARY_PATH=/swshare/ROOT/pythia6/pythia6:; source bin/thisroot.sh; cd -

Short description of the scripts:

To run:
python tmva_training.py:

To create jet pt-eta weights and store as separate branch in training trees do:
python createEtaPtWeightHists.py:
This creates 2D histograms of pT versus eta for each sample. These are used to reweight each jet by 1/bin content of the bin the jet falls in. Same procedure as what was done for the CSV
python addWeightBranch.py:
adds a branch b_weight_etaPt to the training trees

After training:
python pt-test.py
Produces pT control plots to make sure QCD lumi reweighting is dne properly.

python performance-comparison.py
Compares performance of different trainings
