-- FUNCTION: public.ctm_sales_lead_confirm_mail(integer, character, character, character)

-- DROP FUNCTION IF EXISTS public.ctm_sales_lead_confirm_mail(integer, character, character, character);

CREATE OR REPLACE FUNCTION public.ctm_sales_lead_confirm_mail(
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
v_customer_name char varying (10000);
v_contact_person char varying(10000);
v_mobile_no char varying(10000);
v_email char varying(10000);
v_lead_source char varying(10000);
v_req_services char varying(10000);
v_prod_list char varying(10000);
v_next_followup_date char varying(10000);
v_confirmed_by char varying(10000);

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
			
			select trans.name,trans.customer_name,trans.contact_person,trans.mobile_no,
			trans.email,enq.name,trans.service_name,trans.product,
			to_char(trans.next_followup_date,'dd/mm/yyyy') as next_followup_date 
			from  ct_sales_lead trans
			left join cm_enquiry_source enq on enq.id = trans.enq_source_id
			where trans.id = v_trans_id ;			
			
			LOOP                 
		  		FETCH cursor_1 INTO v_trans_name,v_customer_name,v_contact_person,v_mobile_no,v_email,
				v_lead_source,v_prod_list,v_req_services,v_next_followup_date;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_trans_name is null) then
				v_trans_name='';
			end if;

			if(v_customer_name is null) then
				v_customer_name='';
			end if;
			
			if(v_contact_person is null) then
				v_contact_person='';
			end if;
			
			if(v_mobile_no is null) then
				v_mobile_no='';
			end if;
			
			if(v_email is null) then
				v_email='';
			end if;
			
			if(v_lead_source is null) then
				v_lead_source='';
			end if;
			
			if(v_req_services is null) then
				v_req_services='';
			end if;
			
			if(v_prod_list is null) then
				v_prod_list='';
			end if;

			if(v_next_followup_date is null) then
				v_next_followup_date='';
			end if;
			
			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';

			v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been generated.</span></td></tr>
				</table>';
			
			v_data=v_data || '<table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>Lead Details:</b></th>';
		    
		     v_data=v_data || '<tr>
				<td colspan="3">Lead No</td>
				<td colspan="3">'||v_ref_no||'</td>
				</tr>

				<tr>
				<td colspan="3">Customer Name</td>
				<td colspan="3">'||v_customer_name||'</td>
				</tr>

				<tr>
				<td colspan="3">Contact Person</td>
				<td colspan="3">'||v_contact_person||'</td>
				</tr>

				<tr>
				<td colspan="3">Mobile No</td>
				<td colspan="3">'||v_mobile_no||'</td>
				</tr>
				
				<tr>
				<td colspan="3">Email</td>
				<td colspan="3">'||v_email||'</td>
				</tr>

				<tr>
				<td colspan="3">Lead Source</td>
				<td colspan="3">'||v_lead_source||'</td>
				</tr>
				
				<tr>
				<td colspan="3">Required Services</td>
				<td colspan="3">'||v_req_services||'</td>
				</tr>
				
				<tr>
				<td colspan="3">Product List</td>
				<td colspan="3">'||v_prod_list||'</td>
				</tr>

				<tr>
				<td colspan="3">Next Followup Date</td>
				<td colspan="3">'||v_next_followup_date||'</td>
				</tr>
				
				<tr>
				<td colspan="3">Sales Executive</td>
				<td colspan="3">'||v_user_name||'</td>
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
			<td align="center" bgcolor="#2f9780" class="one-column" style="padding-top:0;padding-bottom:5px;padding-right:10px;padding-left:10px;"><font style="font-size:13px; text-decoration:none; color:#ffffff; font-family: Times New Roman; text-align:right;"> ** This mail is auto generated by ERP System </font></td>
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

ALTER FUNCTION public.ctm_sales_lead_confirm_mail(integer, character, character, character)
    OWNER TO odoo;

