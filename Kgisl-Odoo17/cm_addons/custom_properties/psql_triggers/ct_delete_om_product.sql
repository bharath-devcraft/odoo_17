-- FUNCTION: public.ct_delete_om_product()

-- DROP FUNCTION IF EXISTS public.ct_delete_om_product() CASCADE;

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
    OWNER TO odoo;


-- Trigger: ct_delete_om_product --

DO $$
    -- Check if the table exists
    BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
            AND table_name = 'ct_transaction_line'
    ) THEN
        -- Check if the trigger already exists
        IF NOT EXISTS (
            SELECT 1
            FROM pg_trigger
            WHERE tgname = 'ct_delete_om_product'
        ) THEN
            -- Create the trigger
            CREATE TRIGGER ct_delete_om_product
                AFTER DELETE
                ON public.ct_transaction_line
                FOR EACH ROW
                EXECUTE FUNCTION public.ct_delete_om_product();
        END IF;
    END IF;
END $$;