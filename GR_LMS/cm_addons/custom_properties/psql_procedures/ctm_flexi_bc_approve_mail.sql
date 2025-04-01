-- FUNCTION: public.ctm_flexi_bc_approve_mail(integer, character, character, character, character)

-- DROP FUNCTION IF EXISTS public.ctm_flexi_bc_approve_mail(integer, character, character, character, character);

CREATE OR REPLACE FUNCTION public.ctm_flexi_bc_approve_mail(
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
v_service_name char varying(10000);
v_customer_name char varying (10000);
v_sales_executive char varying (10000);
v_bc_date char varying (10000);
v_qs_no char varying(10000);
v_qs_date char varying(10000);
v_service_code char varying(10000);
v_sys_ref char varying(10000);
v_accessories_req char varying(10000);

v_product char varying(10000);
v_dg char varying(10000);
v_un_no char varying(10000);
v_imo_class char varying(10000);
v_pack_grp char varying(10000);

v_flexi_type char varying(10000);
v_layer_type char varying(10000);
v_capacity char varying(10000);
v_qty char varying(10000);
v_bag_req_date char varying(10000);
v_vendor char varying(10000);
v_pod_services char varying(10000);

v_stuff_qty char varying(10000);
v_stuff_address char varying(10000);
v_stuff_date char varying(10000);

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
			
			select ser.sys_ref into v_service_code from ct_business_confirmation trans
			left join cm_service ser on ser.id = trans.service_id
			where trans.id = v_trans_id;
			
			Open cursor_1 FOR
			
				select ser.name as service_name,
				cus.name as customer_name,
				par.name as sales_executive,
				to_char(trans.entry_date,'dd/mm/yyyy') as bc_date,
				trans.qs_no,
				to_char(trans.qs_date,'dd/mm/yyyy') as qs_date,
				prod.name as product_name,
				(case when trans.dg_product = 'yes' then 'DG'
					  when trans.dg_product = 'no' then 'Non DG'
					  end) as dg,
				trans.un_no,
				trans.imo_class,
				(case when trans.pack_grp = '1' then 'I'
					  when trans.pack_grp = '2' then 'II'
				 	  when trans.pack_grp = '3' then 'III'
					  end) as pack_grp

				from  ct_business_confirmation trans
				left join cm_service ser on ser.id = trans.service_id
				left join cm_customer cus on cus.id = trans.customer_id
				left join res_users usr on usr.id = trans.user_id
				left join res_partner par on par.id=usr.partner_id
				left join cm_product prod on prod.id = trans.product_id

				where trans.id = v_trans_id;

			LOOP                 
		  		FETCH cursor_1 INTO v_service_name,v_customer_name,v_sales_executive,v_bc_date,
					v_qs_no,v_qs_date,v_product,v_dg,v_un_no,v_imo_class,v_pack_grp;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_service_name is null) then
				v_service_name='';
			end if;

			if(v_customer_name is null) then
				v_customer_name='';
			end if;
			
			if(v_sales_executive is null) then
				v_sales_executive='';
			end if;
			
			if(v_bc_date is null) then
				v_bc_date='';
			end if;
			
			if(v_qs_no is null) then
				v_qs_no='';
			end if;
			
			if(v_qs_date is null) then
				v_qs_date='';
			end if;

			if(v_product is null) then
				v_product='';
			end if;
			
			if(v_dg is null) then
				v_dg='';
			end if;
			
			if(v_un_no is null) then
				v_un_no='';
			end if;
			
			if(v_imo_class is null) then
				v_imo_class='';
			end if;
			
			if(v_pack_grp is null) then
				v_pack_grp='';
			end if;

			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';


			v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been approved and the details are given below.</span></td></tr>
				</table>';
				
			v_data=v_data || '<table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>BC Details:</b></th>';
		    
		     v_data=v_data || '
			 	<tr>
					<td colspan="3" id="remove-right-border">BC No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_ref_no||'</td>
					<td colspan="3" id="remove-right-border">BC Date</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_bc_date||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Service Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_service_name||'</td>
					<td colspan="3" id="remove-right-border">Quotation No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border" style="word-break:break-all">'||v_qs_no||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Customer Name</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_customer_name||'</td>
					<td colspan="3" id="remove-right-border">Quotation Date</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_qs_date||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Sales Executive</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_sales_executive||'</td>
					<td colspan="3" id="remove-right-border"></td>
					<td colspan="3" id="no-border"></td>
					<td colspan="3" id="remove-left-border"></td>
				</tr>';
			
			if v_service_code in ('FLBS') then
				v_data=v_data || '
					<th colspan="18" scope="colgroup" class="table-heading green"><b>Product Details:</b></th>
					<tr>
						<td colspan="3" id="remove-right-border">Product Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_product||'</td>
						<td colspan="3" id="remove-right-border">UN Number</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_un_no||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Product Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dg||'</td>
						<td colspan="3" id="remove-right-border">IMO Class</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_imo_class||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Packing Group</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pack_grp||'</td>
						<td colspan="3" id="remove-right-border"></td>
						<td colspan="3" id="no-border"></td>
						<td colspan="3" id="remove-left-border"></td>
					</tr>';
			end if;

			if v_service_code in ('FLBS', 'FLAS') then

				Open cursor_2 FOR
					select
					(case when flexi.flexi_type = 'tltd' then 'TLTD'
						  when flexi.flexi_type = 'tlbd' then 'TLBD'
						  when flexi.flexi_type = 'blbd' then 'BLBD'
						  end) as flexi_type,
					layer.name as layer_type,
					capacity.name as capacity,
					flexi.qty,
					to_char(flexi.bag_req_date,'dd/mm/yyyy') as bag_req_date,
					(case when flexi.pod_services = 'disposal' then 'Disposal'
						  when flexi.pod_services = 'discharge' then 'Discharge'
						  when flexi.pod_services = 'both' then 'Both'
						  when flexi.pod_services = 'not_required' then 'Not Required'
						  end) as pod_services,
					vendor.name,
					(case when bc.accessories_req = 'yes' then 'Yes'
						  when bc.accessories_req = 'no' then 'No'
						  end) as accessories_required

					from ct_business_confirmation_acc_line flexi
					left join cm_flexi_layer_type layer on layer.id = flexi.flexi_layer_type_id
					left join cm_flexi_capacity capacity on capacity.id = flexi.flexi_capacity_id
					left join cm_vendor_master vendor on vendor.id = flexi.vendor_id
					left join ct_business_confirmation bc on bc.id = flexi.header_id

					where flexi.header_id = v_trans_id limit 1;		

				LOOP                 
					FETCH cursor_2 INTO v_flexi_type,
					v_layer_type,v_capacity,v_qty,v_bag_req_date,v_vendor,v_pod_services,v_accessories_req;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_flexi_type is null) then
					v_flexi_type='';
				end if;

				if(v_layer_type is null) then
					v_layer_type='';
				end if;

				if(v_capacity is null) then
					v_capacity='';
				end if;

				if(v_qty is null) then
					v_qty='';
				end if;

				if(v_bag_req_date is null) then
					v_bag_req_date='';
				end if;

				if(v_vendor is null) then
					v_vendor='';
				end if;

				if(v_pod_services is null) then
					v_pod_services='';
				end if;
				
				if(v_accessories_req is null) then
					v_accessories_req='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Flexi Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Flexi Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_flexi_type||'</td>
						<td colspan="3" id="remove-right-border">Bag Required Date</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_bag_req_date||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Layer Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_layer_type||'</td>
						<td colspan="3" id="remove-right-border">Preferred Vendor</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_vendor||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Capacity</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_capacity||'</td>
						<td colspan="3" id="remove-right-border">POD Services</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod_services||'</td>
					</tr>
					
					<tr>
						<td colspan="3" id="remove-right-border">Quantity</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_qty||'</td>
						<td colspan="3" id="remove-right-border">Accessories Required</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_accessories_req||'</td>
					</tr>';
					END LOOP;
				Close cursor_2;
			
			elseif v_service_code in ('FLOS') then

				Open cursor_2 FOR

					select 
				
					trans.flexi_stuff_qty,
					trans.stuff_address,
					to_char(trans.stuff_date, 'dd/mm/yyyy') as stuff_date

					from  ct_business_confirmation trans

					where trans.id = v_trans_id;		

				LOOP                 
					FETCH cursor_2 INTO v_stuff_qty,v_stuff_address,v_stuff_date;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_stuff_qty is null) then
					v_stuff_qty='';
				end if;

				if(v_stuff_address is null) then
					v_stuff_address='';
				end if;
				
				if(v_stuff_date is null) then
					v_stuff_date='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Flexi Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Flexi Stuffing Qty</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_stuff_qty||'</td>
						<td colspan="3" id="remove-right-border">Stuffing Date</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_stuff_date||'</td>
					</tr>
					<tr>
						<td colspan="3" id="remove-right-border">Exact Stuffing Address</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_stuff_address||'</td>
						
						<td colspan="3" id="remove-right-border"></td>
						<td colspan="3" id="no-border"></td>
						<td colspan="3" id="remove-left-border"></td>
					</tr>';
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

ALTER FUNCTION public.ctm_flexi_bc_approve_mail(integer, character, character, character, character)
    OWNER TO odoo;
