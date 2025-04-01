-- FUNCTION: public.ctm_flexi_vendor_invoice_approve_mail(integer, character, character, character, character)

-- DROP FUNCTION IF EXISTS public.ctm_flexi_vendor_invoice_approve_mail(integer, character, character, character, character);

CREATE OR REPLACE FUNCTION public.ctm_flexi_vendor_invoice_approve_mail(
	v_trans_id integer,
	v_trans_state character,
	v_ref_no character,
	v_user_name character,
	v_source character)
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
cursor_1 refcursor;
cursor_2 refcursor;

v_table_heading text;
v_data text;

-- Header fields
v_bc_no char varying(10000);
v_service_name char varying(10000);
v_vendor char varying (10000);
v_invoice_value char varying (10000);
v_mode_of_payment char varying (10000);
v_payment_term char varying (10000);
v_due_date char varying (10000);
v_currency char varying (10000);

BEGIN

v_table_heading='';
v_data='';

			v_table_heading='<html ><head>
			<style type="text/css">
			* {-webkit-font-smoothing: antialiased;}
			body {Margin: 0;padding: 0;min-width: 100%;font-family: "Times New Roman", Times, serif;-webkit-font-smoothing: antialiased;mso-line-height-rule: exactly;}
			table {border-spacing: 0;color: #333333;font-family:"Times New Roman", Times, serif;}
			img {border: 0;}
			table.logo-table {margin-top: 30px;}
			table.table-top {margin-top: 6px;}
			.wrapper {width: 100%;table-layout: fixed;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;}
			.webkit {max-width: 600px;}
			.outer {Margin: 0 auto;width: 100%;max-width: 600px;}
			.full-width-image img {width: 100%;max-width: 600px;height: auto;}
			.inner {padding: 10px;}
			.contents {width: 100%;}
			.two-column img {width: 100%;max-width: 280px;height: auto;margin-top: 20px;}
			#customers,#customers-campus,#customers-nohover {font-family: "Times New Roman", Times, serif;border-collapse: collapse;width: 100%;background: #ffffff;}
			#customers tbody,#customers-campus tbody,#customers-nohover tbody {width: 80%;}
			#customers-nohover th {padding: 8px;background: #fff;}
			#customers td,#customers th,#customers-campus td,#customers-campus th {border-left: 1px solid #2f9780;border-right: 1px solid #2f9780;border-top: 1px solid #2f9780;padding: 8px;border-bottom: 1px solid #2f9780;padding: 8px;}
			#customers th,#customers-campus th {font-weight: normal;}
			#customers tr:nth-child(even) {background-color: #f2f2f2;}
			#customers tr:hover {background-color: #ddd;}
			#customers tr th:hover {background-color: none!important;}
			#customers tbody tr th:hover {background-color: none!important;}
			#customers th,#customers-campus th {text-align: left;padding: 8px;}
			.green {background: #ddd;}
			table tr td#no-border{width:0%;border-left: none;border-right: none;}
            table tr td#remove-left-border{border-left: none}
            table tr td#remove-right-border{border-right: none}
			</style></head>';
			
			
			v_table_heading= v_table_heading || '<body style="Margin:0;padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;min-width:100%;background-color:#ececec;">
			<center class="wrapper" style="width:100%;table-layout:fixed;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;background-color:#ececec;">
			<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ececec;" bgcolor="#ececec;">
			<tr>
			<td width="100%">
			<div class="webkit" style="max-width:1000px;Margin:0 auto;">
			<table class="outer" align="center" cellpadding="0" cellspacing="0" border="0" style="border-spacing:0;Margin:0 auto;width:100%;max-width:1000px;">
			<tr>
			<td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;">
			<!-- ======= start header ======= -->
			<table border="0" width="100%" cellpadding="0" cellspacing="0" class="logo-table">
			<tr>
			<td style="width:100%; border-top-left-radius:10px; border-top-right-radius:10px" height="6" bgcolor="#2f9780" class="contents">
			<table style="width:100%;" cellpadding="0" cellspacing="0" border="0" class="table-top">
			<tbody>
			<tr>
			<td align="center">
			<center>
			<table border="0" align="center" width="100%" cellpadding="0" cellspacing="0" style="Margin: 0 auto;">
			<tbody>
			<tr>
			<td class="one-column" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" bgcolor="#FFFFFF">
			<table class="logo" cellpadding="0" cellspacing="0" border="0" width="100%">
			<tr>
			<td class="two-column" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;text-align:center;font-size:0;">
			<div class="column" style="width:100%;max-width:150px;display:inline-block;vertical-align:top;">
			<table class="contents logo" style="border-spacing:0; width:100%" bgcolor="#ffffff">
			<tr>
			<td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" align="center">
			<a href="#" target="_blank"><!-- <img src="#"  alt="" style="border-width:0; height:auto; display:block" /> --></a>
			</td>
			</tr>
			</table>
			</div>
			</td>
			</tr>
			</table>
			</td>
			</tr>
			</tbody>
			</table>
			</center>
			</td>
			</tr>
			</tbody>
			</table>
			</td>
			</tr>
			</table>
			<table class="one-column" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0" bgcolor="#2f9780">
			<tr>
			<td align="left" style="padding-left:10px; padding-right:20px; padding-top:0px; padding-bottom:10px">
			</td>
			</tr>';
			
			Open cursor_1 FOR
			
				select 
				bc.name as bc_no,
				service.name as service_name,
				vendor.name as vendor_name,
				trans.net_amt as invoice_value,
				(case when trans.payment_mode = 'cash' then 'Cash'
					when trans.payment_mode = 'credit' then 'Credit'
				    when trans.payment_mode = 'credit_card' then 'Credit Card'
					end) as mode_of_payment,
				p_term.name as payment_term,
				to_char(trans.due_date,'dd/mm/yyyy') as due_date,
				currency.name as currency

				from  ct_vendor_invoice trans
				left join ct_business_confirmation bc on bc.id = trans.bc_id
				left join cm_service service on service.id = trans.service_id
				left join cm_vendor_master vendor on vendor.id = trans.vendor_id
				left join cm_payment_term p_term on p_term.id = trans.payment_term_id
				left join res_currency currency on currency.id = trans.currency_id


				where trans.id = v_trans_id;

			LOOP                 
		  		FETCH cursor_1 INTO v_bc_no,v_service_name,v_vendor,
					v_invoice_value,v_mode_of_payment,v_payment_term,v_due_date,v_currency;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_bc_no is null) then
				v_bc_no='';
			end if;

			if(v_service_name is null) then
				v_service_name='';
			end if;

			if(v_vendor is null) then
				v_vendor='';
			end if;
			
			if(v_invoice_value is null) then
				v_invoice_value='';
			end if;
			
			if(v_mode_of_payment is null) then
				v_mode_of_payment='';
			end if;
			
			if(v_payment_term is null) then
				v_payment_term='';
			end if;
			
			if(v_due_date is null) then
				v_due_date='';
			end if;

			if(v_currency is null) then
				v_currency='';
			end if;

			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';


			v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been generated and the details are given below.</span></td></tr>
				</table>';
				
			v_data=v_data || '<table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>Invoice Details:</b></th>';
		    
		     v_data=v_data || '
			 	<tr>
					<td colspan="3" id="remove-right-border">BC No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_bc_no||'</td>
					<td colspan="3" id="remove-right-border">Invoice No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_ref_no||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Service Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_service_name||'</td>
					<td colspan="3" id="remove-right-border">Mode of Payment </td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_mode_of_payment||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Vendor Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_vendor||'</td>
					<td colspan="3" id="remove-right-border">Payment Term</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_payment_term||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Approved By</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_user_name||'</td>
					<td colspan="3" id="remove-right-border">Due Date</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_due_date||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Invoice Value</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||trim(TO_CHAR((v_invoice_value::numeric)::float, '99G99G99G99G99G99G990D99'))||' '|| v_currency ||'</td>
					<td colspan="3" id="remove-right-border"></td>
					<td colspan="3" id="no-border"></td>
					<td colspan="3" id="remove-left-border"></td>
				</tr>';

			v_data=v_data || '</table>
                                
                <br>
                <br>

            <table id="customers">
			<table width="100%" border="0" cellspacing="0" cellpadding="0">
			<tr>
			<td>
				  <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#2f9780">
			<tr>
			<td height="2" align="center" bgcolor="#2f9780" class="one-column"></td>
			</tr>
			<tr>
			<td align="center" bgcolor="#2f9780" class="one-column" style="padding-top:0;padding-bottom:5px;padding-right:10px;padding-left:10px;"><font style="font-size:13px; text-decoration:none; color:#ffffff; font-family: Times New Roman; text-align:right;"> ** This mail is auto generated by ERP System ** Please do not respond to this email </font></td>
			</tr>
			</table>
			</td>
			</tr>
			<tr>
			<td>
			<table width="100%" cellpadding="0" cellspacing="0" border="0">
			<tr>
			<td>&nbsp;</td>
			</tr>
			</table>
			</td>
			</tr>
			</table>
			</td>
			</tr>
			</table>
			</div>
			</td>
			</tr>
			</table>
			</center>
			</body>
			</html>';
	
	END LOOP;
		Close cursor_1;
				
	RETURN v_data;

END;

$BODY$;

ALTER FUNCTION public.ctm_flexi_vendor_invoice_approve_mail(integer, character, character, character, character)
    OWNER TO odoo;
