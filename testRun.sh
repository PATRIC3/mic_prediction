#!/bin/bash

bash mic_prediction_fasta.sh test_fasta/1001.fasta temp/ data_files/Kleb.model.pkl 12 test_out/xgbGenomeTest data_files/Kleb.ArrInds data_files/antibioticsList_Kleb.uniq data_files/MICMethods data_files/all_kmrs data_files/Kleb.model.mod_acc

bash mic_prediction_kmc.sh test_fasta/1001.fasta.10.kmrs temp/ data_files/Kleb.model.pkl 1 test_out/xgbGenomeTest.KMC data_files/Kleb.ArrInds data_files/antibioticsList_Kleb.uniq data_files/MICMethods data_files/all_kmrs data_files/Kleb.model.mod_acc