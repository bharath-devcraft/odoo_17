-- FUNCTION: public.ctm_flexi_store_issue_request_approve_mail(integer, character, character, character, character)

-- DROP FUNCTION IF EXISTS public.ctm_flexi_store_issue_request_approve_mail(integer, character, character, character, character);

CREATE OR REPLACE FUNCTION public.ctm_flexi_store_issue_request_approve_mail(
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
v_customer_name char varying (10000);
v_req_by char varying (10000);
v_vendor_bill_address char varying (10000);
v_vendor_del_address char varying (10000);
v_cus_bill_address char varying (10000);
v_cus_del_address char varying (10000);
v_del_date char varying (10000);
v_service_code char varying(10000);
v_sys_ref char varying(10000);
bill_address char varying(10000);
del_address char varying(10000);

v_bag_name char varying(10000);
v_qty char varying(10000);
v_uom char varying(10000);
v_accessories_req char varying(10000);

v_dub_bag_name char varying(10000);

v_acc_name char varying(10000);
v_acc_qty char varying(10000);
v_acc_uom char varying(10000);

v_sl_no integer;
v_acc_sl_no integer;

BEGIN

v_table_heading='';
v_data='';
v_sl_no =1;
v_acc_sl_no =1;
v_accessories_req='';

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
			
			select ser.sys_ref into v_service_code from ct_store_issue_request trans
			left join cm_service ser on ser.id = trans.service_id
			where trans.id = v_trans_id;
			
			Open cursor_1 FOR
			
				select 
				bc.name as bc_no,
				ser.name as service_name,
				cus.name as customer_name,
				par.name as requested_by,
			    trans.bill_address as vendor_bill_address,
				trans.del_address as vendor_del_address,
				bc.cus_bill_address as cus_bill_address,
				bc.cus_del_address as cus_del_address,
				to_char(trans.del_date,'dd/mm/yyyy') as delivery_date,
				(case when trans.accessories_req = 'yes' then 'Yes'
					when trans.accessories_req = 'no' then 'No'
					end) as accessories_req

				from  ct_store_issue_request trans
				left join ct_business_confirmation bc on bc.id = trans.bc_id
				left join cm_service ser on ser.id = trans.service_id
				left join res_users usr on usr.id = trans.req_user_id
				left join res_partner par on par.id=usr.partner_id
				left join cm_customer cus on cus.id = bc.customer_id

				where trans.id = v_trans_id;

			LOOP                 
		  		FETCH cursor_1 INTO v_bc_no,v_service_name,v_customer_name,v_req_by,v_vendor_bill_address,
					v_vendor_del_address,v_cus_bill_address,v_cus_del_address,v_del_date,v_accessories_req;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_bc_no is null) then
				v_bc_no='';
			end if;

			if(v_service_name is null) then
				v_service_name='';
			end if;

			if(v_customer_name is null) then
				v_customer_name='';
			end if;
			
			if(v_req_by is null) then
				v_req_by='';
			end if;
			
			if(v_vendor_bill_address is null) then
				v_vendor_bill_address='';
			end if;
			
			if(v_vendor_del_address is null) then
				v_vendor_del_address='';
			end if;
			
			if(v_cus_bill_address is null) then
				v_cus_bill_address='';
			end if;

			if(v_cus_del_address is null) then
				v_cus_del_address='';
			end if;
			
			if(v_del_date is null) then
				v_del_date='';
			end if;

			if v_service_code in ('FLBS') then
				bill_address = v_vendor_bill_address;
				del_address = v_vendor_del_address;
			elseif v_service_code in ('FLAS') then
				bill_address = v_cus_bill_address;
				del_address = v_cus_del_address;
			else
				bill_address = '';
				del_address = '';
			end if;

			if(v_accessories_req is null) then
				v_accessories_req='';
			end if;

			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';


			v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been generated and the details are given below. Kindly verify the bag / accessories expiry date and deliver it.</span></td></tr>
				</table>';
				
			v_data=v_data || '<table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>Issue Request Details:</b></th>';
		    
		     v_data=v_data || '
			 	<tr>
					<td colspan="3" id="remove-right-border">BC No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_bc_no||'</td>
					<td colspan="3" id="remove-right-border">Billing Address</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border" style="word-break:break-all">'||bill_address||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Service Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_service_name||'</td>
					<td colspan="3" id="remove-right-border">Delivery Address</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border" style="word-break:break-all">'||del_address||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Customer Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_customer_name||'</td>
					<td colspan="3" id="remove-right-border">Delivery Date</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_del_date||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Requested By</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_req_by||'</td>';

			if v_service_code in ('FLBS') then 
				v_data = v_data || '<td colspan="3" id="remove-right-border">Accessories Required</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_accessories_req||'</td>
					</tr>';
			elseif v_service_code in ('FLAS') then 
				SELECT prod.name->>'en_US' into v_dub_bag_name
					FROM ct_store_issue_request_acc_line flexi
					LEFT JOIN product_template prod
						ON prod.status = 'active' 
					   AND prod.active_trans = 't' 
					   AND prod.custom_type = 'flexi_bag' 
					   AND prod.flexi_type = flexi.flexi_type
					   AND prod.layer_type_id = flexi.flexi_layer_type_id 
					   AND prod.capacity_id = flexi.flexi_capacity_id 
					   AND (prod.vendor_id IS NULL OR prod.vendor_id = flexi.vendor_id)
					WHERE flexi.header_id = v_trans_id
					ORDER BY prod.id
					LIMIT 1;

				if(v_dub_bag_name is null) then
					v_dub_bag_name='';
				end if;

				v_data = v_data || '<td colspan="3" id="remove-right-border">Bag Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dub_bag_name||'</td>
					</tr>';
			end if;

			if v_service_code in ('FLBS') then
			
				v_data=v_data || '</table><table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>Bag Details:</b></th>

				<tr>
					<th colspan="2"><b><center>S.No</center></b></th>
					<th colspan="2"><b><center>Bag Name</center></b></th>
					<th colspan="2"><b><center>UOM</center></b></th>
					<th colspan="2"><b><center>Quantity</center></b></th>
				</tr>';

				Open cursor_2 FOR
					SELECT
						(SELECT prod.name->>'en_US'
						 FROM product_template prod 
						 WHERE prod.status = 'active' 
						   AND prod.active_trans = 't' 
						   AND prod.custom_type = 'flexi_bag' 
						   AND prod.flexi_type = flexi.flexi_type
						   AND prod.layer_type_id = flexi.flexi_layer_type_id 
						   AND prod.capacity_id = flexi.flexi_capacity_id 
						   AND (prod.vendor_id IS NULL OR prod.vendor_id = flexi.vendor_id) 
						 LIMIT 1) AS bag_name,

						(SELECT uom.name->>'en_US'
						 FROM product_template prod
						 LEFT JOIN uom_uom uom ON uom.id = prod.uom_id
						 WHERE prod.status = 'active' 
						   AND prod.active_trans = 't' 
						   AND prod.custom_type = 'flexi_bag' 
						   AND prod.flexi_type = flexi.flexi_type
						   AND prod.layer_type_id = flexi.flexi_layer_type_id 
						   AND prod.capacity_id = flexi.flexi_capacity_id 
						   AND (prod.vendor_id IS NULL OR prod.vendor_id = flexi.vendor_id) 
						 LIMIT 1) AS uom_name,
						flexi.qty

					FROM ct_store_issue_request_acc_line flexi
					WHERE flexi.header_id = v_trans_id LIMIT 1;

				LOOP                 
					FETCH cursor_2 INTO v_bag_name,v_uom,v_qty;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_bag_name is null) then
					v_bag_name='';
				end if;

				if(v_uom is null) then
					v_uom='';
				end if;

				if(v_qty is null) then
					v_qty='';
				end if;

				v_data=v_data ||
					'<tr>
					<td colspan="2"><center>'||v_sl_no||'</center></td>
					<td colspan="2">'||v_bag_name||'</td>
					<td colspan="2">'||v_uom||'</td>
					<td colspan="2" align="right">'||v_qty||'</td>
					</tr>';
					v_sl_no = v_sl_no+1;
					END LOOP;
				Close cursor_2;
			end if;
			
			select accessories_req into v_accessories_req from ct_store_issue_request where id = v_trans_id;

			if v_service_code in ('FLAS') or (v_service_code in ('FLBS') and v_accessories_req = 'yes') then

				v_data=v_data || '</table><table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>Accessories Details:</b></th>

				<tr>
					<th colspan="2"><b><center>S.No</center></b></th>
					<th colspan="2"><b><center>Accessories Name</center></b></th>
					<th colspan="2"><b><center>UOM</center></b></th>
					<th colspan="2"><b><center>Quantity</center></b></th>
				</tr>';

				Open cursor_2 FOR
					select
						prod.name->>'en_US' as accessories_name,
						uom.name->>'en_US' as uom,
						flexi.qty

					from ct_store_issue_request_acc_details_line flexi_details
					left join ct_store_issue_request_acc_line flexi on flexi.id = flexi_details.header_id
					left join product_template prod on prod.id = flexi_details.accessories_id
					left join uom_uom uom on uom.id = flexi_details.uom_id
					where flexi.header_id = v_trans_id;

				LOOP                 
					FETCH cursor_2 INTO v_acc_name,v_acc_uom,v_acc_qty;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_acc_name is null) then
					v_acc_name='';
				end if;

				if(v_acc_uom is null) then
					v_acc_uom='';
				end if;

				if(v_acc_qty is null) then
					v_acc_qty='';
				end if;

				v_data=v_data ||
					'<tr>
					<td colspan="2"><center>'||v_acc_sl_no||'</center></td>
					<td colspan="2">'||v_acc_name||'</td>
					<td colspan="2">'||v_acc_uom||'</td>
					<td colspan="2" align="right">'||v_acc_qty||'</td>
					</tr>';
					v_acc_sl_no = v_acc_sl_no+1;
					END LOOP;
				Close cursor_2;	
			
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

ALTER FUNCTION public.ctm_flexi_store_issue_request_approve_mail(integer, character, character, character, character)
    OWNER TO odoo;
