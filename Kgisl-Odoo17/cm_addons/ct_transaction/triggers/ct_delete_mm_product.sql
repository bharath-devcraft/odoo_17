-- FUNCTION: public.ct_delete_mm_product()

-- DROP FUNCTION IF EXISTS public.ct_delete_mm_product();

CREATE OR REPLACE FUNCTION public.ct_delete_mm_product()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$

BEGIN

delete from ct_transaction_line where product_id = OLD.product_product_id and header_id = OLD.ct_transaction_id;
        
  RETURN NULL;
END;
$BODY$;

ALTER FUNCTION public.ct_delete_mm_product()
    OWNER TO bharath;

