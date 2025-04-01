-- FUNCTION: public.ct_delete_mm_po_product()

-- DROP FUNCTION IF EXISTS public.ct_delete_mm_po_product() CASCADE;

CREATE OR REPLACE FUNCTION public.ct_delete_mm_po_product()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$

BEGIN

delete from ct_purchase_order_line where pr_line_id = OLD.ct_purchase_request_line_id and header_id = OLD.ct_purchase_order_id;
        
  RETURN NULL;
END;
$BODY$;

ALTER FUNCTION public.ct_delete_mm_po_product()
    OWNER TO odoo;


-- Trigger: ct_delete_mm_po_product --

DO $$
    -- Check if the table exists
    BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
            AND table_name = 'ct_purchase_order_ct_purchase_request_line_rel'
    ) THEN
        -- Check if the trigger already exists
	DROP TRIGGER IF EXISTS ct_delete_mm_po_product ON public.ct_purchase_order_ct_purchase_request_line_rel;
	
        -- Create the trigger
        CREATE TRIGGER ct_delete_mm_po_product
            AFTER DELETE
            ON public.ct_purchase_order_ct_purchase_request_line_rel
            FOR EACH ROW
            EXECUTE FUNCTION public.ct_delete_mm_po_product();
    END IF;
END $$;
