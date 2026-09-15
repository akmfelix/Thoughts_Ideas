SELECT 
recipient_biniin AS biniin, 
amount, 
rating_recip AS rating, 
sign_client AS is_client, 
sign_loan AS is_loan, 
recipient_name as client_name,
recipient_type as client_type
FROM profile.mdm_scf_top_anchors 
WHERE payer_biniin = $1
