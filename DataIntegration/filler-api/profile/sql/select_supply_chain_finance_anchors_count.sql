SELECT 
payer_biniin AS biniin,
cnt_anchor AS counterparties_count
FROM profile.mdm_scf_contragents
WHERE payer_biniin = $1