-- FUNCTION: public.csm_quotation_bc_pending_mail(integer, character, character, character)

-- DROP FUNCTION IF EXISTS public.csm_quotation_bc_pending_mail(integer, character, character, character);

CREATE OR REPLACE FUNCTION public.csm_quotation_bc_pending_mail(
	v_trans_id integer,
	v_trans_state character,
	v_ref_no character,
	v_user_name character)
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
v_trans_name char varying(10000);
v_entry_date char varying (10000);
v_bkg_party char varying(10000);
v_service_name char varying(10000);
v_enquiry_no char varying(10000);
v_confirmed_by char varying(10000);
v_approved_by char varying(10000);
v_sales_person char varying(10000);
v_executed_by char varying(10000);
v_val_date char varying(10000);
v_currency char varying(1000);
v_net_amt float;

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
			
            select trans.name,to_char(trans.entry_date,'dd/mm/yyyy') as entry_date,
			bkg_party.name as bkg_party,service.name as sevice_name, trans.enquiry_no,
			trans.net_amt as total_amt,to_char(trans.validity_date,'dd/mm/yyyy') as val_date,
			confirm_name.name as confirmed_by,
			ap_name.name as approved_by,currency.name as currency,
			sales_person_name.name as sale_person,executed_user_name.name as executed_by from  ct_quotations trans
			left join cm_service service on service.id = trans.service_id
			left join cm_customer bkg_party on bkg_party.id = trans.bkg_party_id
			left join res_users users on users.id = trans.user_id
			left join res_users ap_user on ap_user.id = trans.ap_rej_user_id
			left join res_users confirm_user on confirm_user.id = trans.confirm_user_id
			left join res_users sales_person on sales_person.id = trans.generated_user_id
			left join res_users executed_user on executed_user.id = trans.executed_user_id
			left join res_partner partner on partner.id = users.partner_id
			left join res_partner confirm_name on confirm_name.id = confirm_user.partner_id
			left join res_partner ap_name on ap_name.id = ap_user.partner_id
			left join res_partner sales_person_name on sales_person_name.id = sales_person.partner_id
			left join res_partner executed_user_name on executed_user_name.id = executed_user.partner_id
			left join res_currency currency on currency.id = trans.quotation_currency_id
			where trans.id = v_trans_id ;			
			
			LOOP                 
		  		FETCH cursor_1 INTO v_trans_name,v_entry_date,v_bkg_party,v_service_name,v_enquiry_no,v_net_amt,v_val_date,v_confirmed_by,v_approved_by,v_currency,v_sales_person,v_executed_by;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_trans_name is null) then
				v_trans_name='';
			end if;
			
			if(v_entry_date is null) then
				v_entry_date='';
			end if;
			
			if(v_bkg_party is null) then
				v_bkg_party='';
			end if;
			
			if(v_service_name is null) then
				v_service_name='';
			end if;

			if(v_enquiry_no is null) then
				v_enquiry_no='';
			end if;

			if(v_val_date is null) then
				v_val_date='';
			end if;

			if(v_confirmed_by is null) then
				v_confirmed_by=v_user_name;
			end if;
			if(v_approved_by is null) then
				v_approved_by=v_user_name;
			end if;
			if(v_net_amt is null) then
				v_net_amt=0;
			end if;
			
			if(v_currency is null) then
				v_currency='';
			end if;
			
			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';
				
           
		  if (v_trans_state = 'quotation_sent') then
			    v_table_heading= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The business confirmation is waiting for <b>'||v_ref_no||'</b>. The details are given below.</span></td></tr>
				</table>';
		   else 
		       v_table_heading= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The detailsd of <b>'||v_ref_no||'</b> below, It has been created by '||v_created_by||'.</span></td></tr>
				</table>';
		      end if;
			
			v_data= v_table_heading ;
			
			
			v_data=v_data || '<table id="customers">
			<th colspan="18" scope="colgroup" class="table-heading green"><b>Quotation Details:</b></th>';
			
		    v_data=v_data || '<tr>
			<td colspan="3">Quotation No</td>
			<td colspan="3">'||v_ref_no||'</td>
			</tr>';
			
	        v_data=v_data || '<tr>
			<td colspan="3">Booking Party Name</td>
			<td colspan="3">'||v_bkg_party||'</td>
			</tr>';
		
			v_data=v_data || '<tr>
			<td colspan="3">Service Name</td>
			<td colspan="3">'||v_service_name||'</td>
			</tr>
			
			
			<tr>
			<td colspan="3">Total Amount</td>
			<td colspan="3">'||trim(TO_CHAR((v_net_amt::numeric)::float, '99G99G99G99G99G99G990D99'))||' '|| v_currency ||'</td>
			</tr>
			
			<tr>
			<td colspan="3">Validity Date</td>
			<td colspan="3">'||v_val_date||'</td>
			</tr>
			<tr>
			<td colspan="3"><b>Approved By</b></td>
			<td colspan="3"><b>'||v_user_name||'</b></td>
			</tr>
			
			<tr>
			<td colspan="3">Enquiry No</td>
			<td colspan="3">'||v_enquiry_no||'</td>
			</tr>
			<tr>
			<td colspan="3">Sales Person Name</td>
			<td colspan="3">'||v_sales_person||'</td>
			</tr>
			<tr>
			<td colspan="3">Executed By</td>
			<td colspan="3">'||v_executed_by||'</td>
			</tr>
			
			';
		    	
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

ALTER FUNCTION public.csm_quotation_bc_pending_mail(integer, character, character, character)
    OWNER TO odoo;

