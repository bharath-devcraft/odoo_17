-- FUNCTION: public.ct_delete_mm_product()

-- DROP FUNCTION IF EXISTS public.ct_delete_mm_product() CASCADE;

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
    OWNER TO odoo;


-- Trigger: ct_delete_mm_product --

DO $$
    -- Check if the table exists
    BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
            AND table_name = 'ct_transaction_product_product_rel'
    ) THEN
        -- Check if the trigger already exists
	DROP TRIGGER IF EXISTS ct_delete_mm_product ON public.ct_transaction_product_product_rel;
	
        -- Create the trigger
        CREATE TRIGGER ct_delete_mm_product
            AFTER DELETE
            ON public.ct_transaction_product_product_rel
            FOR EACH ROW
            EXECUTE FUNCTION public.ct_delete_mm_product();
    END IF;
END $$;
