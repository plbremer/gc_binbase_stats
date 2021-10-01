#compound analysis stats parameters
predecessor_count_top=1
fold_number_top=20
count_meeting_fold_number_top=1



rule step_1_species_transformed:
    input:

    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_1_species_transformed/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
        #output_base="/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/snakemake_mapping_mona_to_best_worst/{adduct}/{instrument}/parameters_minDist_{min_dist}_nNeighbors_{n_neighbors}_blurSigma_{blur_sigma}_depthCutoff_{depth_cutoff}/"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/transform_written_species_to_ncbi_species.py"

rule step_2a_create_organ_networkx:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_1_species_transformed/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_2a_create_organ_and_disease_networkx/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/create_organ_networkx.py"


rule step_2b_organ_transformed:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_2a_create_organ_and_disease_networkx/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_2b_organ_transformed/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"   
        #output_base="/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/snakemake_mapping_mona_to_best_worst/{adduct}/{instrument}/parameters_minDist_{min_dist}_nNeighbors_{n_neighbors}_blurSigma_{blur_sigma}_depthCutoff_{depth_cutoff}/"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/transform_written_organs.py"

rule step_3_bins_transformed:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_2b_organ_transformed/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_3_bins_transformed/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"   
        #output_base="/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/snakemake_mapping_mona_to_best_worst/{adduct}/{instrument}/parameters_minDist_{min_dist}_nNeighbors_{n_neighbors}_blurSigma_{blur_sigma}_depthCutoff_{depth_cutoff}/"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/transform_bins.py"

rule step_4_classes_transformed:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_3_bins_transformed/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_4_classes_transformed/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"      
        #output_base="/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/snakemake_mapping_mona_to_best_worst/{adduct}/{instrument}/parameters_minDist_{min_dist}_nNeighbors_{n_neighbors}_blurSigma_{blur_sigma}_depthCutoff_{depth_cutoff}/"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/transform_classes.py"

rule step_5_clean_panda:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_4_classes_transformed/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_5_panda_cleaned/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/clean_panda_before_hierarchical_analysis.py"

rule step_6_generate_fold_matrices:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_5_panda_cleaned/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_6_generate_fold_matrices/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/generate_fold_change_matrices.py"

rule step_7_prepare_compound_hierarchy:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_6_generate_fold_matrices/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_7_prepare_compound_hierarchy/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/prepare_compound_hierarchy.py"

rule step_8_perform_compound_hierarchical_analysis:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_7_prepare_compound_hierarchy/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_8_perform_compound_hierarchical_analysis/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/perform_compound_hierarchical_analysis.py"

rule step_9_compound_analysis_stats:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_8_perform_compound_hierarchical_analysis/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_9_compound_analysis_stats/dummy.txt"
    params:
        predecessor_count=predecessor_count_top,
        fold_number=fold_number_top,
        count_meeting_fold_number=count_meeting_fold_number_top,   
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/compound_analysis_stats.py"

rule step_10_create_species_taxid_mapping:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_9_compound_analysis_stats/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_10_create_species_taxid_mapping/dummy.txt"
    params:
        #predecessor_count=predecessor_count_top,
        #fold_number=fold_number_top,
        #count_meeting_fold_number=count_meeting_fold_number_top,  
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/create_species_taxid_mapping.py"

rule step_11_prepare_species_networkx:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_10_create_species_taxid_mapping/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_11_prepare_species_networkx/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/prepare_species_networkx.py"

rule step_12_prepare_organ_networkx:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_11_prepare_species_networkx/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_12_prepare_organ_and_disease_networkx/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/prepare_organ_and_disease_networkx.py"

rule step_13_swap_fold_matrix_multiindex:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_12_prepare_organ_and_disease_networkx/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_13_swap_fold_matrix_multiindex/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/swap_fold_matrix_multiindex.py"

rule step_14_reduce_hierarchy_complexity:
    input:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_13_swap_fold_matrix_multiindex/dummy.txt"
    output:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/{count_cutoff}/step_14_reduce_hierarchy_complexity/dummy.txt"
    params:
        count_cutoff="{count_cutoff}"
    script:
        "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/reduce_hierarchy_complexity.py"