-- FUNCTION: public.ctm_flexi_job_card_approve_mail(integer, character, character, character, character)

-- DROP FUNCTION IF EXISTS public.ctm_flexi_job_card_approve_mail(integer, character, character, character, character);

CREATE OR REPLACE FUNCTION public.ctm_flexi_job_card_approve_mail(
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
v_jc_no char varying(10000);
v_jc_date char varying(10000);
v_nature_of_job char varying (10000);
v_service_provider char varying (10000);
v_service_engineer char varying (10000);
v_vendor char varying (10000);
v_customer char varying (10000);
v_service_address char varying (10000);
v_service_date char varying (10000);
v_exp_service_address char varying (10000);
v_exp_service_engineer char varying (10000);
v_exp_service_date char varying (10000);

service_address char varying (10000);
service_engineer char varying (10000);
service_date char varying (10000);

BEGIN

v_table_heading='';
v_data='';
service_address = '';
service_engineer = '';
service_date = '';

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
				to_char(trans.entry_date,'dd/mm/yyyy') as jc_date,
				(case when trans.nature_of_job = 'container_survey' then 'Container Survey'
					when trans.nature_of_job = 'loading' then 'Loading'
					when trans.nature_of_job = 'unloading' then 'Unloading'
					when trans.nature_of_job = 'cross_loading' then 'Cross Loading'
					when trans.nature_of_job = 'disposal_assistance' then 'Disposal Assistance'
					when trans.nature_of_job = 'expiry_audit' then 'Expiry Audit'
					end) as nature_of_job,
				(case when trans.service_provider = 'internal' then 'Internal'
					when trans.service_provider = 'external' then 'External'
					end) as service_provider,
				emp.name as service_engineer,
				vendor.name as vendor_name,
				cus.name as customer_name,
				trans.service_address,
				to_char(trans.service_date,'dd/mm/yyyy') as service_date,
				trans.audit_address as exp_service_address,
				par.name as exp_service_engineer,
				to_char(trans.audit_date,'dd/mm/yyyy') as exp_service_date

				from  ct_job_card trans
				left join ct_delivery_challan dc on dc.id = trans.dc_id
				left join cm_employee emp on emp.id = trans.emp_id
				left join cm_vendor_master vendor on vendor.id = trans.vendor_id
				left join cm_customer cus on cus.id = trans.customer_id
				left join res_users usr on usr.id = trans.audit_eng_id
				left join res_partner par on par.id = usr.partner_id

				where trans.id = v_trans_id;

			LOOP                 
		  		FETCH cursor_1 INTO v_jc_date,v_nature_of_job,v_service_provider,v_service_engineer,
					v_vendor,v_customer,v_service_address,v_service_date,v_exp_service_address,
					v_exp_service_engineer,v_exp_service_date;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_jc_date is null) then
				v_jc_date='';
			end if;

			if(v_nature_of_job is null) then
				v_nature_of_job='';
			end if;

			if(v_service_provider is null) then
				v_service_provider='';
			end if;
			
			if(v_service_engineer is null) then
				v_service_engineer='';
			end if;
			
			if(v_vendor is null) then
				v_vendor='';
			end if;
			
			if(v_customer is null) then
				v_customer='';
			end if;
			
			if(v_service_address is null) then
				v_service_address='';
			end if;
			
			if(v_service_date is null) then
				v_service_date='';
			end if;
			
			if(v_exp_service_address is null) then
				v_exp_service_address='';
			end if;
			
			if(v_exp_service_engineer is null) then
				v_exp_service_engineer='';
			end if;
			
			if(v_exp_service_date is null) then
				v_exp_service_date='';
			end if;

			if v_nature_of_job != 'Expiry Audit' then
				service_address = v_service_address;
				service_engineer = v_service_engineer;
				service_date = v_service_date;
			elseif v_nature_of_job = 'Expiry Audit' then
				service_address = v_exp_service_address;
				service_engineer = v_exp_service_engineer;
				service_date = v_exp_service_date;
			end if;

			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';


			v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been generated and the details are given below.</span></td></tr>
				</table>';
				
			v_data=v_data || '<table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>Job Card Details:</b></th>';
		    
		     v_data=v_data || '
			 	<tr>
					<td colspan="3" id="remove-right-border">JC No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_ref_no||'</td>
					<td colspan="3" id="remove-right-border">Customer Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_customer||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">JC Date</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_jc_date||'</td>
					<td colspan="3" id="remove-right-border">Service Address</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||service_address||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Nature of Job</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_nature_of_job||'</td>
					<td colspan="3" id="remove-right-border">Service Date</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||service_date||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Service Provider</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_service_provider||'</td>
					<td colspan="3" id="remove-right-border">Service Engineer Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||service_engineer||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Vendor Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_vendor||'</td>
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

ALTER FUNCTION public.ctm_flexi_job_card_approve_mail(integer, character, character, character, character)
    OWNER TO odoo;
