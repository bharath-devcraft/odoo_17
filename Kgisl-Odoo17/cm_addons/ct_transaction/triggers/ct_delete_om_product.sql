-- FUNCTION: public.ct_delete_om_product()

-- DROP FUNCTION IF EXISTS public.ct_delete_om_product();

CREATE OR REPLACE FUNCTION public.ct_delete_om_product()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN

delete from ct_transaction_product_product_rel where product_product_id = old.product_id and ct_transaction_id in
(select distinct id from ct_transaction where id = old.header_id and trigger_del = 'f');

	RETURN NULL;  
END;
$BODY$;

ALTER FUNCTION public.ct_delete_om_product()
    OWNER TO bharath;

