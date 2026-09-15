SELECT 
recipient_biniin AS biniin,
cnt_contragent AS counterparties_count
FROM profile.mdm_scf_anchors
WHERE recipient_biniin = $1
