-- FUNCTION: public.ct_delete_mm_rfq_purchase_request()

-- DROP FUNCTION IF EXISTS public.ct_delete_mm_rfq_purchase_request() CASCADE;

CREATE OR REPLACE FUNCTION public.ct_delete_mm_rfq_purchase_request()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$

BEGIN

delete from ct_rfq_line where pr_line_id = OLD.ct_purchase_request_line_id and header_id = OLD.ct_rfq_id;
        
  RETURN NULL;
END;
$BODY$;

ALTER FUNCTION public.ct_delete_mm_rfq_purchase_request()
    OWNER TO odoo;


-- Trigger: ct_delete_mm_rfq_purchase_request --

DO $$
    -- Check if the table exists
    BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
            AND table_name = 'ct_purchase_request_line_ct_rfq_rel'
    ) THEN
        -- Check if the trigger already exists
	DROP TRIGGER IF EXISTS ct_delete_mm_rfq_purchase_request ON public.ct_purchase_request_line_ct_rfq_rel;
	
        -- Create the trigger
        CREATE TRIGGER ct_delete_mm_rfq_purchase_request
            AFTER DELETE
            ON public.ct_purchase_request_line_ct_rfq_rel
            FOR EACH ROW
            EXECUTE FUNCTION public.ct_delete_mm_rfq_purchase_request();
    END IF;
END $$;
