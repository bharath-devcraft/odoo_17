-- FUNCTION: public.ct_delete_om_rfq_purchase_request()

-- DROP FUNCTION IF EXISTS public.ct_delete_om_rfq_purchase_request() CASCADE;

CREATE OR REPLACE FUNCTION public.ct_delete_om_rfq_purchase_request()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN

delete from ct_purchase_request_line_ct_rfq_rel where ct_purchase_request_line_id = old.pr_line_id and ct_rfq_id in
(select distinct id from ct_rfq where id = old.header_id and trigger_del = 'f');

	RETURN NULL;  
END;
$BODY$;

ALTER FUNCTION public.ct_delete_om_rfq_purchase_request()
    OWNER TO odoo;


-- Trigger: ct_delete_om_rfq_purchase_request --

DO $$
    -- Check if the table exists
    BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
            AND table_name = 'ct_rfq_line'
    ) THEN
        -- Check if the trigger already exists
	DROP TRIGGER IF EXISTS ct_delete_om_rfq_purchase_request ON public.ct_rfq_line;
	
        -- Create the trigger
	CREATE TRIGGER ct_delete_om_rfq_purchase_request
            AFTER DELETE
            ON public.ct_rfq_line
            FOR EACH ROW
            EXECUTE FUNCTION public.ct_delete_om_rfq_purchase_request();
    END IF;
END $$;
