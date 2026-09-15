SELECT 
payer_biniin AS biniin, 
amount, 
rating_payer AS rating, 
sign_client AS is_client, 
sign_loan AS is_loan, 
payer_name as client_name,
payer_type as client_type
FROM profile.mdm_scf_top_contragents 
WHERE recipient_biniin = $1