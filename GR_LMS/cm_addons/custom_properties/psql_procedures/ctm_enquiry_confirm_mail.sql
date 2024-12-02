-- FUNCTION: public.ctm_enquiry_confirm_mail(integer, character, character, character)

-- DROP FUNCTION IF EXISTS public.ctm_enquiry_confirm_mail(integer, character, character, character);

CREATE OR REPLACE FUNCTION public.ctm_enquiry_confirm_mail(
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
v_service_name char varying(10000);
v_booking_party char varying (10000);
v_business_vertical char varying (10000);
v_contact_person char varying(10000);
v_mobile_no char varying(10000);
v_shipper char varying(10000);
v_agent char varying(10000);
v_last_date_to_submit char varying(10000);
v_product char varying(10000);
v_dg char varying(10000);
v_additional_service char varying(10000);
v_spl_req char varying(10000);

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
			
			select ser.name as service_name,
				(case when bkg_party_id is not null then bkg_cus.name
					  when trans.new_bkg_party is not null then trans.new_bkg_party
					  else '' end) as booking_party,
				bus_vert.name as business_vertical,
				trans.contact_person,
				trans.mobile_no,
				(case when shipper_cus_id is not null then ship_cus.name
					  when trans.new_shipper is not null then trans.new_shipper
					  else '' end) as shipper,
				agent.name as agent,
				to_char(trans.expiry_date,'dd/mm/yyyy') as last_date_to_submit,
				(case when product_id is not null then prod.name
					  when trans.product is not null then trans.product
					  else '' end) as product,
				(case when trans.dg_product = 'yes' then 'Yes'
					  when trans.dg_product = 'no' then 'No'
					  end) as dg,
				(select string_agg(name, ', ') from cm_service where id in
				(select cm_service_id from cm_service_ct_enquiry_rel where ct_enquiry_id = v_trans_id)
				 ) as additional_service,
				trans.spl_req

				from  ct_enquiry trans
				left join cm_service ser on ser.id = trans.service_id
				left join cm_customer bkg_cus on bkg_cus.id = trans.bkg_party_id
				left join cm_business_vertical bus_vert on bus_vert.id = trans.bus_vert_id
				left join cm_customer ship_cus on ship_cus.id = trans.shipper_cus_id
				left join cm_agent agent on agent.id = trans.agent_id
				left join cm_product prod on prod.id = trans.product_id

				where trans.id = v_trans_id;			

			LOOP                 
		  		FETCH cursor_1 INTO v_service_name,v_booking_party,v_business_vertical,v_contact_person,
					v_mobile_no,v_shipper,v_agent,v_last_date_to_submit,v_product,v_dg,
					v_additional_service,v_spl_req;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_service_name is null) then
				v_service_name='';
			end if;

			if(v_booking_party is null) then
				v_booking_party='';
			end if;
			
			if(v_business_vertical is null) then
				v_business_vertical='';
			end if;
			
			if(v_contact_person is null) then
				v_contact_person='';
			end if;
			
			if(v_mobile_no is null) then
				v_mobile_no='';
			end if;
			
			if(v_shipper is null) then
				v_shipper='';
			end if;
			
			if(v_agent is null) then
				v_agent='';
			end if;

			if(v_last_date_to_submit is null) then
				v_last_date_to_submit='';
			end if;
			
			if(v_product is null) then
				v_product='';
			end if;
			
			if(v_dg is null) then
				v_dg='';
			end if;
			
			if(v_additional_service is null) then
				v_additional_service='';
			end if;
			
			if(v_spl_req is null) then
				v_spl_req='';
			end if;
			
			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';

			v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been generated.</span></td></tr>
				</table>';
			
			v_data=v_data || '<table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';
		    
		     v_data=v_data || '
			 	<tr>
					<td colspan="3" id="remove-right-border">Enquiry No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_ref_no||'</td>
					<td colspan="3" id="remove-right-border">Actual Shipper</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_shipper||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Service Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_service_name||'</td>
					<td colspan="3" id="remove-right-border">Business Vertical</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_business_vertical||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Booking Party</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_booking_party||'</td>
					<td colspan="3" id="remove-right-border">Contact Person</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_contact_person||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Agent Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_agent||'</td>
					<td colspan="3" id="remove-right-border">Mobile No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_mobile_no||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Product Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_product||'</td>
					<td colspan="3" id="remove-right-border">Last Date to Submit Quote</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_last_date_to_submit||'</td>
				</tr>

				<tr>
					<td colspan="3" id="remove-right-border">Dangerous Goods</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_dg||'</td>
					<td colspan="3" id="remove-right-border">Sales Executive</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_user_name||'</td>
				</tr>';
					
			if v_additional_service != '' and v_spl_req != '' then 
				v_data=v_data ||'
				<tr>
					<td colspan="3" id="remove-right-border">Additional Services</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_additional_service||'</td>
					<td colspan="3" id="remove-right-border">Special Requirements</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_spl_req||'</td>
				</tr>';
			
			elseif v_additional_service != '' then 
				v_data=v_data ||'
				<tr>
					<td colspan="3" id="remove-right-border">Additional Services</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_additional_service||'</td>
				</tr>';
			
			elseif v_spl_req != '' then 
				v_data=v_data ||'
				<tr>
					<td colspan="3" id="remove-right-border">Special Requirements</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_spl_req||'</td>
				</tr>';
			
			end if;

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

ALTER FUNCTION public.ctm_enquiry_confirm_mail(integer, character, character, character)
    OWNER TO odoo;
