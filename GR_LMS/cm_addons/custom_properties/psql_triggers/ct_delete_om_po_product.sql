-- FUNCTION: public.ct_delete_om_po_product()

-- DROP FUNCTION IF EXISTS public.ct_delete_om_po_product() CASCADE;

CREATE OR REPLACE FUNCTION public.ct_delete_om_po_product()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN

delete from ct_purchase_order_ct_purchase_request_line_rel where ct_purchase_request_line_id = old.pr_line_id and ct_purchase_order_id in
(select distinct id from ct_purchase_order where id = old.header_id and trigger_del = 'f');

	RETURN NULL;  
END;
$BODY$;

ALTER FUNCTION public.ct_delete_om_po_product()
    OWNER TO odoo;


-- Trigger: ct_delete_om_po_product --

DO $$
    -- Check if the table exists
    BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
            AND table_name = 'ct_purchase_order_line'
    ) THEN
        -- Check if the trigger already exists
	DROP TRIGGER IF EXISTS ct_delete_om_po_product ON public.ct_purchase_order_line;
	
        -- Create the trigger
	CREATE TRIGGER ct_delete_om_po_product
            AFTER DELETE
            ON public.ct_purchase_order_line
            FOR EACH ROW
            EXECUTE FUNCTION public.ct_delete_om_po_product();
    END IF;
END $$;
