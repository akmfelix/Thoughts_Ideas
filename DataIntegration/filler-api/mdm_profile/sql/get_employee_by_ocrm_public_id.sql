SELECT
    SUBSTRING(OCRM_SOURCE_ID, 4) AS ocrmId,
    PUBLIC_ID AS publicId,
    HALYK_EMPLOYEE_CODE AS employeeCode,
    TRUST_PHONE_NUMBER as trustedPhoneNumber,
    HALYK_EMPLOYEE_CODE is not NULL AS isEmployee
FROM profile_dm.CUSTOMER_FL
WHERE DATE_VALUE = (select max(actual_date) from profile_dm.PROFILE_ACTUAL_DATE WHERE table_name = 'CUSTOMER_FL')
AND (
  CASE
    WHEN :ocrm_id is NULL THEN PUBLIC_ID = :public_id
	WHEN :public_id is NULL THEN OCRM_SOURCE_ID = :ocrm_id OR SUBSTRING(OCRM_SOURCE_ID, 4) = :ocrm_id
  ELSE (OCRM_SOURCE_ID = :ocrm_id OR SUBSTRING(OCRM_SOURCE_ID, 4) = :ocrm_id)
		 OR PUBLIC_ID = :public_id
  END
)
