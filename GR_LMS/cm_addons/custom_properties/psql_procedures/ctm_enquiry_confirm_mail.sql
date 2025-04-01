-- FUNCTION: public.ctm_enquiry_confirm_mail(integer, character, character, character, character)

-- DROP FUNCTION IF EXISTS public.ctm_enquiry_confirm_mail(integer, character, character, character, character);

CREATE OR REPLACE FUNCTION public.ctm_enquiry_confirm_mail(
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
cursor_3 refcursor;
cursor_4 refcursor;

v_table_heading text;
v_data text;

-- Header fields
v_service_name char varying(10000);
v_booking_party char varying (10000);
v_sales_person char varying (10000);
v_business_vertical char varying (10000);
v_contact_person char varying(10000);
v_mobile_no char varying(10000);
v_shipper char varying(10000);
v_tank_operator char varying(10000);
v_last_date_to_submit char varying(10000);
v_product char varying(10000);
v_sds_status char varying(10000);
v_dg char varying(10000);
v_un_no char varying(10000);
v_imo_class char varying(10000);
v_pack_grp char varying(10000);
v_tank_qty char varying(10000);
v_additional_service char varying(10000);
v_spl_req char varying(10000);
v_service_code char varying(10000);
v_empty_laden char varying(10000);
v_cleaning_status char varying(10000);

v_ship_term char varying(10000);
v_pol char varying(10000);
v_pol_free_days char varying(10000);
v_pod char varying(10000);
v_pod_free_days char varying(10000);
v_fpod char varying(10000);

v_lease_period char varying(10000);
v_pickup_port_loc char varying(10000);
v_pickup_depot_loc char varying(10000);
v_drop_port_loc char varying(10000);
v_drop_depot_loc char varying(10000);
v_nomination_port char varying(10000);

v_carrier char varying(10000);
v_insurance char varying(10000);

v_flexi_type char varying(10000);
v_layer_type char varying(10000);
v_capacity char varying(10000);
v_bag_qty char varying(10000);
v_city char varying(10000);
v_bag_req_date char varying(10000);
v_vendor char varying(10000);
v_pod_services char varying(10000);

v_del_address char varying(10000);

v_stuff_qty char varying(10000);
v_stuff_address char varying(10000);
v_stuff_date char varying(10000);

v_tank_type char varying(10000);
v_qty char varying(10000);
v_mfg_year char varying(10000);
v_dots_depot_loc char varying(10000);
v_dots_product char varying(10000);
v_dots_dg char varying(10000);

v_dep char varying(10000);
v_prod_weight_kg char varying(10000);
v_trailer_type char varying(10000);
v_route_name char varying(10000);
v_pickup_loc char varying(10000);
v_dropoff_loc char varying(10000);
v_load_address char varying(10000);
v_unload_address char varying(10000);
v_offload_loc char varying(10000);

v_sys_ref char varying(10000);

v_end_dep char varying(10000);
v_end_prod_weight_kg char varying(10000);
v_end_trailer_type char varying(10000);
v_end_route_name char varying(10000);
v_end_pickup_loc char varying(10000);
v_end_dropoff_loc char varying(10000);
v_end_load_address char varying(10000);
v_end_unload_address char varying(10000);
v_end_offload_loc char varying(10000);

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
			
			select ser.sys_ref into v_service_code from ct_enquiry trans
			left join cm_service ser on ser.id = trans.service_id
			where trans.id = v_trans_id;
			
			Open cursor_1 FOR
			
				select ser.name as service_name,
				(case when bkg_party_id is not null then bkg_cus.name
					  when trans.new_bkg_party is not null then trans.new_bkg_party
					  else '' end) as booking_party,
				par.name as sales_person,
				(case when shipper_cus_id is not null then ship_cus.name
					  when trans.new_shipper is not null then trans.new_shipper
					  else '' end) as shipper,
				(select string_agg(short_name, ',') from cm_tank_operator where id in (
					select cm_tank_operator_id from 
						cm_tank_operator_ct_enquiry_rel where ct_enquiry_id = v_trans_id)
					) as tank_operator,
				
				bus_vert.name as business_vertical,
				trans.contact_person,
				trans.mobile_no,
				to_char(trans.expiry_date,'dd/mm/yyyy') as last_date_to_submit,
				
				
				(case when product_id is not null then prod.name
					  when trans.product is not null then trans.product
					  else '' end) as product,
				(case when trans.sds_status = 'available_valid' then 'Available - Valid'
					  when trans.sds_status = 'available_expired' then 'Available - Expired'
				 	  when trans.sds_status = 'not_available' then 'New SDS'
				 	  else '' end) as sds_status,
				(case when trans.dg_product = 'yes' then 'DG'
					  when trans.dg_product = 'no' then 'Non DG'
					  end) as dg,
				trans.un_no,
				trans.imo_class,
				(case when trans.pack_grp = '1' then 'I'
					  when trans.pack_grp = '2' then 'II'
				 	  when trans.pack_grp = '3' then 'III'
					  end) as pack_grp,
				trans.tank_qty,

				(select string_agg(name, ', ') from cm_service where id in
				(select cm_service_id from cm_service_ct_enquiry_rel where ct_enquiry_id = v_trans_id)
				 ) as additional_service,
				trans.spl_req,
				(case when trans.container_category = 'empty' then 'Empty'
					  when trans.container_category = 'laden' then 'Laden'
					  end) as empty_laden,
				(case when trans.cleaning_status = 'cleaned' then 'Cleaned'
					  when trans.cleaning_status = 'un_cleaned' then 'Un Cleaned'
					  end) as cleaning_status

				from  ct_enquiry trans
				left join cm_service ser on ser.id = trans.service_id
				left join cm_customer bkg_cus on bkg_cus.id = trans.bkg_party_id
				left join cm_business_vertical bus_vert on bus_vert.id = trans.bus_vert_id
				left join cm_customer ship_cus on ship_cus.id = trans.shipper_cus_id
				left join cm_product prod on prod.id = trans.product_id
				left join res_users usr on usr.id = trans.generated_user_id
				left join res_partner par on par.id=usr.partner_id

				where trans.id = v_trans_id;			

			LOOP                 
		  		FETCH cursor_1 INTO v_service_name,v_booking_party,v_sales_person,v_shipper,v_tank_operator,
					v_business_vertical,v_contact_person,v_mobile_no,v_last_date_to_submit,
					v_product,v_sds_status,v_dg,v_un_no,v_imo_class,v_pack_grp,v_tank_qty,
					v_additional_service,v_spl_req,v_empty_laden,v_cleaning_status;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_service_name is null) then
				v_service_name='';
			end if;

			if(v_booking_party is null) then
				v_booking_party='';
			end if;
			
			if(v_sales_person is null) then
				v_sales_person='';
			end if;
			
			if(v_shipper is null) then
				v_shipper='';
			end if;
			
			if(v_tank_operator is null) then
				v_tank_operator='';
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

			if(v_last_date_to_submit is null) then
				v_last_date_to_submit='';
			end if;
			
			if(v_product is null) then
				v_product='';
			end if;
			
			if(v_sds_status is null) then
				v_sds_status='';
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
			
			if(v_tank_qty is null) then
				v_tank_qty='';
			end if;
			
			if(v_additional_service is null) then
				v_additional_service='';
			end if;
			
			if(v_spl_req is null) then
				v_spl_req='';
			end if;
			
			if(v_empty_laden is null) then
				v_empty_laden='';
			end if;
			
			if(v_cleaning_status is null) then
				v_cleaning_status='';
			end if;
			
			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';

			if v_source = 'enquiry_confirm' then

				v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been generated.</span></td></tr>
					</table>';
			elseif v_source = 'enquiry_quotation_overdue' then
				v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>Awaiting for quotation approval for the enquiry number <b>'||v_ref_no||'</b></span></td></tr>
					</table>';
			else
				v_data= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been generated.</span></td></tr>
					</table>';
			end if;
				
			v_data=v_data || '<table id="customers">
				<th colspan="18" scope="colgroup" class="table-heading green"><b>Booking Party Details:</b></th>';
		    
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
					<td colspan="3" id="remove-right-border">Tank Operator</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border" style="word-break:break-all">'||v_tank_operator||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Booking Party</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_booking_party||'</td>
					<td colspan="3" id="remove-right-border">Business Vertical</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_business_vertical||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Sales Person</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_sales_person||'</td>
					<td colspan="3" id="remove-right-border">Mobile No</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_mobile_no||'</td>
				</tr>
				
				<tr>
					<td colspan="3" id="remove-right-border">Executed By</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_user_name||'</td>
					<td colspan="3" id="remove-right-border">Last Date to Submit Quote</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_last_date_to_submit||'</td>
				</tr>';
			
			if v_service_code not in ('FLAS', 'FLOS', 'DOTS') and (v_empty_laden != 'Empty' or (v_empty_laden = 'Empty' and v_cleaning_status = 'Un Cleaned')) then
				v_data=v_data || '
					<th colspan="18" scope="colgroup" class="table-heading green"><b>Product Details:</b></th>
					<tr>
						<td colspan="3" id="remove-right-border">Product Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_product||'</td>
						<td colspan="3" id="remove-right-border">Product Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dg||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">SDS Status</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_sds_status||'</td>
						<td colspan="3" id="remove-right-border">UN Number</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_un_no||'</td>
					</tr>
					
					<tr>
						<td colspan="3" id="remove-right-border">Tank Quantity(TEUS</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_tank_qty||'</td>
						<td colspan="3" id="remove-right-border">IMO Class</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_imo_class||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Empty / Laden</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_empty_laden||'</td>
						<td colspan="3" id="remove-right-border">Packing Group</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pack_grp||'</td>
					</tr>';
			end if;

			if v_service_code in ('OSTE', 'OSTI', 'OSNR', 'OSNB') then

			
				Open cursor_2 FOR

					select 

					ship_term.name as shipment_name,
					pol_port.name as pol,
					trans.pol_free_days,
					pod_port.name as pod,
					trans.pod_free_days,
					fpod_port.name as fpod,
					depot_loc.name as pickup_depot_loc,
					nom_port.name

					from  ct_enquiry trans
					left join cm_shipment_term ship_term on ship_term.id = trans.ship_term_id
					left join cm_port pol_port on pol_port.id = trans.pol_port_id
					left join cm_port pod_port on pod_port.id = trans.pod_port_id
					left join cm_port fpod_port on fpod_port.id = trans.fpod_port_id
					left join cm_depot_location depot_loc on depot_loc.id = trans.trip_pickup_depot_id
					left join cm_port nom_port on nom_port.id = trans.nomination_port_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_ship_term,v_pol,v_pol_free_days,v_pod,
						v_pod_free_days,v_fpod,v_pickup_depot_loc,v_nomination_port;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_ship_term is null) then
					v_ship_term='';
				end if;

				if(v_pol is null) then
					v_pol='';
				end if;

				if(v_pol_free_days is null) then
					v_pol_free_days='';
				end if;

				if(v_pod is null) then
					v_pod='';
				end if;

				if(v_pod_free_days is null) then
					v_pod_free_days='';
				end if;

				if(v_fpod is null) then
					v_fpod='';
				end if;

				if(v_pickup_depot_loc is null) then
					v_pickup_depot_loc='';
				end if;
				
				if(v_nomination_port is null) then
					v_nomination_port='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Shipment Term</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_ship_term||'</td>
						<td colspan="3" id="remove-right-border">POD Free Days</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod_free_days||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POL</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pol||'</td>
						<td colspan="3" id="remove-right-border">FPOD</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_fpod||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POL Free Days</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pol_free_days||'</td>
						<td colspan="3" id="remove-right-border">Pick Up Depot Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pickup_depot_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POD</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod||'</td>';
					
					if v_nomination_port != '' then
						v_data=v_data || '
								<td colspan="3" id="remove-right-border">Nomination Port</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_nomination_port||'</td>
							</tr>';
					else
						v_data=v_data || '</tr>';
					
					end if;
						
					END LOOP;
				Close cursor_2;
			
			
			elseif v_service_code in ('ISTL') then

			
				Open cursor_2 FOR

					select 
				
					(trans.lease_period ||' '|| trans.period_choices) as lease_period,
					pickup_port.name as pickup_port_loc,
					pickup_depot_loc.name as pickup_depot_loc,
					drop_port.name as drop_port_loc,
					drop_depot_loc.name as drop_depot_loc

					from  ct_enquiry trans
					left join cm_port pickup_port on pickup_port.id = trans.pickup_port_id
					left join cm_depot_location pickup_depot_loc on pickup_depot_loc.id = trans.pickup_depot_id
					left join cm_port drop_port on drop_port.id = trans.drop_port_id
					left join cm_depot_location drop_depot_loc on drop_depot_loc.id = trans.drop_depot_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_lease_period,v_pickup_port_loc,v_pickup_depot_loc,
						v_drop_port_loc,v_drop_depot_loc;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_lease_period is null) then
					v_lease_period='';
				end if;

				if(v_pickup_port_loc is null) then
					v_pickup_port_loc='';
				end if;

				if(v_pickup_depot_loc is null) then
					v_pickup_depot_loc='';
				end if;

				if(v_drop_port_loc is null) then
					v_drop_port_loc='';
				end if;

				if(v_drop_depot_loc is null) then
					v_drop_depot_loc='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Lease Period</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_lease_period||'</td>
						<td colspan="3" id="remove-right-border">Drop Off Port Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_drop_port_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Pick Up Port Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pickup_port_loc||'</td>
						<td colspan="3" id="remove-right-border">Drop Off Depot Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_drop_depot_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Pick Up Depot Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pickup_depot_loc||'</td>
						
						<td colspan="3" id="remove-right-border"></td>
						<td colspan="3" id="no-border"></td>
						<td colspan="3" id="remove-left-border"></td>
					</tr>';
					END LOOP;
				Close cursor_2;
			
			
			elseif v_service_code in ('DOTL') then

			
				Open cursor_2 FOR

					select 
				
					(trans.lease_period ||' '|| trans.period_choices) as lease_period,
					pickup_port.name as pickup_port_loc,
					pickup_depot_loc.name as pickup_depot_loc,
					drop_port.name as drop_port_loc,
					drop_depot_loc.name as drop_depot_loc

					from  ct_enquiry trans
					left join cm_port pickup_port on pickup_port.id = trans.pickup_port_id
					left join cm_depot_location pickup_depot_loc on pickup_depot_loc.id = trans.pickup_depot_id
					left join cm_port drop_port on drop_port.id = trans.drop_port_id
					left join cm_depot_location drop_depot_loc on drop_depot_loc.id = trans.drop_depot_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_lease_period,v_pickup_port_loc,v_pickup_depot_loc,
						v_drop_port_loc,v_drop_depot_loc;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_lease_period is null) then
					v_lease_period='';
				end if;

				if(v_pickup_port_loc is null) then
					v_pickup_port_loc='';
				end if;

				if(v_pickup_depot_loc is null) then
					v_pickup_depot_loc='';
				end if;

				if(v_drop_port_loc is null) then
					v_drop_port_loc='';
				end if;

				if(v_drop_depot_loc is null) then
					v_drop_depot_loc='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Lease Period</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_lease_period||'</td>
						<td colspan="3" id="remove-right-border">Drop Off Port Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_drop_port_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Pick Up Port Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pickup_port_loc||'</td>
						<td colspan="3" id="remove-right-border">Drop Off Depot Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_drop_depot_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Pick Up Depot Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pickup_depot_loc||'</td>
						
						<td colspan="3" id="remove-right-border"></td>
						<td colspan="3" id="no-border"></td>
						<td colspan="3" id="remove-left-border"></td>
					</tr>';
					END LOOP;
				Close cursor_2;

			elseif v_service_code in ('SOCE', 'SOCR', 'SOCI') then

				Open cursor_2 FOR

					select 
				
					ship_term.name as shipment_name,
					pol_port.name as pol,
					trans.pol_free_days,
					pod_port.name as pod,
					trans.pod_free_days,
					fpod_port.name as fpod,
					depot_loc.name as pickup_depot_loc,
					carrier.name as carrier,
					(case when trans.insurance = 'customer' then 'Customer'
						 when trans.insurance = 'gmpl' then 'GMPL'
						 else '' end) as insurance

					from  ct_enquiry trans
					left join cm_shipment_term ship_term on ship_term.id = trans.ship_term_id
					left join cm_port pol_port on pol_port.id = trans.pol_port_id
					left join cm_port pod_port on pod_port.id = trans.pod_port_id
					left join cm_port fpod_port on fpod_port.id = trans.fpod_port_id
					left join cm_depot_location depot_loc on depot_loc.id = trans.trip_pickup_depot_id
					left join cm_carrier carrier on carrier.id = trans.carrier_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_ship_term,v_pol,v_pol_free_days,v_pod,
						v_pod_free_days,v_fpod,v_pickup_depot_loc,v_carrier,v_insurance;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_ship_term is null) then
					v_ship_term='';
				end if;

				if(v_pol is null) then
					v_pol='';
				end if;

				if(v_pol_free_days is null) then
					v_pol_free_days='';
				end if;

				if(v_pod is null) then
					v_pod='';
				end if;

				if(v_pod_free_days is null) then
					v_pod_free_days='';
				end if;

				if(v_fpod is null) then
					v_fpod='';
				end if;

				if(v_pickup_depot_loc is null) then
					v_pickup_depot_loc='';
				end if;

				if(v_carrier is null) then
					v_carrier='';
				end if;
				
				if(v_insurance is null) then
					v_insurance='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Shipment Term</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_ship_term||'</td>
						<td colspan="3" id="remove-right-border">POD Free Days</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod_free_days||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POL</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pol||'</td>
						<td colspan="3" id="remove-right-border">FPOD</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_fpod||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POL Free Days</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pol_free_days||'</td>
						<td colspan="3" id="remove-right-border">Pick Up Depot Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pickup_depot_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POD</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod||'</td>
						<td colspan="3" id="remove-right-border">Insurance</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_insurance||'</td>
					</tr>
					
					<tr>
						<td colspan="3" id="remove-right-border">Carrier Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_carrier||'</td>
					</tr>';
					END LOOP;
				Close cursor_2;
			
			
			elseif v_service_code in ('FLBS') then

			
				Open cursor_2 FOR

					select 
				
					(case when trans.flexi_type = 'tltd' then 'TLTD'
						  when trans.insurance = 'tlbd' then 'TLBD'
						  when trans.insurance = 'blbd' then 'BLBD'
						 else '' end) as flexi_type,
					layer_type.name as layer_type,
					capacity.name as capacity,
					trans.bag_qty,
					city.name as city,
					to_char(trans.bag_req_date, 'dd/mm/yyyy') as bag_req_date,
					vendor.name as vendor,
					(case when trans.pod_services = 'disposal' then 'Disposal'
						  when trans.pod_services = 'discharge' then 'Discharge'
						  when trans.pod_services = 'both' then 'Both'
						  when trans.pod_services = 'not_required' then 'Not Required'
						 else '' end) as pod_services

					from  ct_enquiry trans
					left join cm_flexi_layer_type layer_type on layer_type.id = trans.flexi_layer_type_id
					left join cm_flexi_capacity capacity on capacity.id = trans.flexi_capacity_id
					left join cm_city city on city.id = trans.city_id
					left join cm_vendor_master vendor on vendor.id = trans.vendor_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_flexi_type,v_layer_type,v_capacity,
						v_bag_qty,v_city,v_bag_req_date,v_vendor,v_pod_services;

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

				if(v_bag_qty is null) then
					v_bag_qty='';
				end if;

				if(v_city is null) then
					v_city='';
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

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Flexi Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_flexi_type||'</td>
						<td colspan="3" id="remove-right-border">City</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_city||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Layer Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_layer_type||'</td>
						<td colspan="3" id="remove-right-border">Bag Required Date</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_bag_req_date||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Capacity</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_capacity||'</td>
						<td colspan="3" id="remove-right-border">Preferred Vendor</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_vendor||'</td>
					</tr>
					
					<tr>
						<td colspan="3" id="remove-right-border">Bag Quantity(Nos)</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_bag_qty||'</td>
						<td colspan="3" id="remove-right-border">POD Services</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod_services||'</td>
					</tr>';
					END LOOP;
				Close cursor_2;
			
			
			
			elseif v_service_code in ('FLAS') then

			
				Open cursor_2 FOR

					select 
				
					trans.del_address,
					city.name as city

					from  ct_enquiry trans
					left join cm_city city on city.id = trans.city_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_del_address,v_city;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_del_address is null) then
					v_del_address='';
				end if;

				if(v_city is null) then
					v_city='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Delivery Address</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_del_address||'</td>
						<td colspan="3" id="remove-right-border">City</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_city||'</td>
					</tr>';
					END LOOP;
				Close cursor_2;

			elseif v_service_code in ('FLOS') then

			
				Open cursor_2 FOR

					select 
				
					trans.flexi_stuff_qty,
					trans.stuff_address,
					to_char(trans.stuff_date, 'dd/mm/yyyy') as stuff_date

					from  ct_enquiry trans

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

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

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

			elseif v_service_code in ('DOTS') then

				Open cursor_2 FOR

					select 
					(case when trans.tank_type = '20_feet' then '20 Feet'
						  when trans.tank_type = '40_feet' then '40 Feet'
						  else '' end) as tank_type,
					trans.tank_sale_qty as qty,
					trans.year_built as mfg_year,
					(select string_agg(name, ', ') from cm_depot_location where id in 
						(select cm_depot_location_id from cm_depot_location_ct_enquiry_rel 
						 where ct_enquiry_id = 115)) as depot_loc,
					(case when tank_sale_product_id is not null then prod.name
						  when trans.tank_sale_product is not null then trans.tank_sale_product
						  else '' end) as product,
					(case when trans.tank_sale_dg_product = 'yes' then 'Yes'
						  when trans.tank_sale_dg_product = 'no' then 'No'
						  end) as dg

					from  ct_enquiry trans
					left join cm_product prod on prod.id = trans.tank_sale_product_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_tank_type,v_qty,v_mfg_year,v_dots_depot_loc,
						v_dots_product,v_dots_dg;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_tank_type is null) then
					v_tank_type='';
				end if;

				if(v_qty is null) then
					v_qty='';
				end if;

				if(v_mfg_year is null) then
					v_mfg_year='';
				end if;

				if(v_dots_depot_loc is null) then
					v_dots_depot_loc='';
				end if;

				if(v_dots_product is null) then
					v_dots_product='';
				end if;

				if(v_dots_dg is null) then
					v_dots_dg='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Tank Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_tank_type||'</td>
						<td colspan="3" id="remove-right-border">Manufacturing Year</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_mfg_year||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Product Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dots_product||'</td>
						<td colspan="3" id="remove-right-border">Depot Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dots_depot_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Quantity(Nos)</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_qty||'</td>
						<td colspan="3" id="remove-right-border">Dangerous Goods</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dots_dg||'</td>
					</tr>';
					END LOOP;
				Close cursor_2;

			elseif v_service_code in ('TRAN') then

				Open cursor_2 FOR

					select 
				
					dep.name as department,
					trans.prod_weight_kg,
					(case when trans.trailer_type = '20_feet' then '20 Feet'
						  when trans.trailer_type = '40_feet' then '40 Feet'
						  when trans.trailer_type = 'both' then 'Both'
						  else '' end) as trailer_type,
					trans_route.name as route_name,
					depot_loc.name as pickup_loc,
					trans_loc.name as dropoff_loc,
					trans.load_address,
					trans.unload_address,
					offload_trans_loc.name as offload_loc

					from  ct_enquiry trans
					left join cm_department dep on dep.id = trans.gr_dep_id
					left join cm_transport_route trans_route on trans_route.id = trans.trans_route_id
					left join cm_depot_location depot_loc on depot_loc.id = trans.trans_pickup_depot_id
					left join cm_transport_location trans_loc on trans_loc.id = trans.empty_pickup_loc_id
					left join cm_transport_location offload_trans_loc on offload_trans_loc.id = trans.empty_offload_loc_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_dep,v_prod_weight_kg,v_trailer_type,v_route_name,
						v_pickup_loc,v_dropoff_loc,v_load_address,v_unload_address,v_offload_loc;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_dep is null) then
					v_dep='';
				end if;

				if(v_prod_weight_kg is null) then
					v_prod_weight_kg='';
				end if;

				if(v_trailer_type is null) then
					v_trailer_type='';
				end if;

				if(v_route_name is null) then
					v_route_name='';
				end if;

				if(v_pickup_loc is null) then
					v_pickup_loc='';
				end if;

				if(v_dropoff_loc is null) then
					v_dropoff_loc='';
				end if;
				
				if(v_load_address is null) then
					v_load_address='';
				end if;

				if(v_unload_address is null) then
					v_unload_address='';
				end if;

				if(v_offload_loc is null) then
					v_offload_loc='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">GR Department Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dep||'</td>
						<td colspan="3" id="remove-right-border">Drop Off Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dropoff_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Product Weight(Kgs)</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_prod_weight_kg||'</td>
						<td colspan="3" id="remove-right-border">Loading Address</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_load_address||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Trailer Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_trailer_type||'</td>
						<td colspan="3" id="remove-right-border">Unloading Address</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_unload_address||'</td>
					</tr>
					<tr>
						<td colspan="3" id="remove-right-border">Route Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_route_name||'</td>
						<td colspan="3" id="remove-right-border">Empty Off Loading Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_offload_loc||'</td>
					</tr>
					<tr>
						<td colspan="3" id="remove-right-border">Pick Up Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pickup_loc||'</td>
						
						<td colspan="3" id="remove-right-border"></td>
						<td colspan="3" id="no-border"></td>
						<td colspan="3" id="remove-left-border"></td>
					</tr>';
					END LOOP;
				Close cursor_2;
			
			elseif v_service_code in ('DOTR') then

				Open cursor_2 FOR

					select 
				
					dep.name as department,
					trans.prod_weight_kg,
					(case when trans.trailer_type = '20_feet' then '20 Feet'
						  when trans.trailer_type = '40_feet' then '40 Feet'
						  when trans.trailer_type = 'both' then 'Both'
						  else '' end) as trailer_type,
					trans_route.name as route_name,
					depot_loc.name as pickup_loc,
					trans_loc.name as dropoff_loc,
					trans.load_address,
					trans.unload_address,
					offload_trans_loc.name as offload_loc

					from  ct_enquiry trans
					left join cm_department dep on dep.id = trans.gr_dep_id
					left join cm_transport_route trans_route on trans_route.id = trans.trans_route_id
					left join cm_depot_location depot_loc on depot_loc.id = trans.trans_pickup_depot_id
					left join cm_transport_location trans_loc on trans_loc.id = trans.empty_pickup_loc_id
					left join cm_transport_location offload_trans_loc on offload_trans_loc.id = trans.empty_offload_loc_id

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_dep,v_prod_weight_kg,v_trailer_type,v_route_name,
						v_pickup_loc,v_dropoff_loc,v_load_address,v_unload_address,v_offload_loc;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_dep is null) then
					v_dep='';
				end if;

				if(v_prod_weight_kg is null) then
					v_prod_weight_kg='';
				end if;

				if(v_trailer_type is null) then
					v_trailer_type='';
				end if;

				if(v_route_name is null) then
					v_route_name='';
				end if;

				if(v_pickup_loc is null) then
					v_pickup_loc='';
				end if;

				if(v_dropoff_loc is null) then
					v_dropoff_loc='';
				end if;
				
				if(v_load_address is null) then
					v_load_address='';
				end if;

				if(v_unload_address is null) then
					v_unload_address='';
				end if;

				if(v_offload_loc is null) then
					v_offload_loc='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">GR Department Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dep||'</td>
						<td colspan="3" id="remove-right-border">Drop Off Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_dropoff_loc||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Product Weight(Kgs)</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_prod_weight_kg||'</td>
						<td colspan="3" id="remove-right-border">Loading Address</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_load_address||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">Trailer Type</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_trailer_type||'</td>
						<td colspan="3" id="remove-right-border">Unloading Address</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_unload_address||'</td>
					</tr>
					<tr>
						<td colspan="3" id="remove-right-border">Route Name</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_route_name||'</td>
						<td colspan="3" id="remove-right-border">Empty Off Loading Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_offload_loc||'</td>
					</tr>
					<tr>
						<td colspan="3" id="remove-right-border">Pick Up Location</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pickup_loc||'</td>
						
						<td colspan="3" id="remove-right-border"></td>
						<td colspan="3" id="no-border"></td>
						<td colspan="3" id="remove-left-border"></td>
					</tr>';
					END LOOP;
				Close cursor_2;
			
			
			elseif v_service_code in ('DOTT') then

				Open cursor_2 FOR

					select 
					ship_term.sys_ref as sys_ref,
					ship_term.name as ship_term,
					pol_port.name as pol,
					trans.rail_pol_free_days,
					pod_port.name as pod,
					trans.rail_pod_free_days

					from ct_enquiry trans
					left join cm_shipment_term ship_term on ship_term.id = trans.ship_term_id
					left join cm_port pol_port on pol_port.id = trans.rail_pol_port_id 
					left join cm_port pod_port on pod_port.id = trans.rail_pod_port_id 

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_sys_ref,v_ship_term,v_pol,v_pol_free_days,
						v_pod,v_pod_free_days;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_sys_ref is null) then
					v_sys_ref='';
				end if;

				if(v_ship_term is null) then
					v_ship_term='';
				end if;

				if(v_pol is null) then
					v_pol='';
				end if;

				if(v_pol_free_days is null) then
					v_pol_free_days='';
				end if;

				if(v_pod is null) then
					v_pod='';
				end if;

				if(v_pod_free_days is null) then
					v_pod_free_days='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Shipment Term</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_ship_term||'</td>
						<td colspan="3" id="remove-right-border">POD ICD</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POL ICD</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pol||'</td>
						<td colspan="3" id="remove-right-border">POD Free Days</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod_free_days||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POL Free Days</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pol_free_days||'</td>
						
						<td colspan="3" id="remove-right-border"></td>
						<td colspan="3" id="no-border"></td>
						<td colspan="3" id="remove-left-border"></td>
					</tr>';
					
					
					if v_sys_ref in ('CYDO', 'DOCY', 'DRDR') then
					
						Open cursor_3 FOR

							select 

							dep.name as department,
							trans.prod_weight_kg,
							(case when trans.trailer_type = '20_feet' then '20 Feet'
								  when trans.trailer_type = '40_feet' then '40 Feet'
								  when trans.trailer_type = 'both' then 'Both'
								  else '' end) as trailer_type,
							trans_route.name as route_name,
							(trans.dotr_pol_free_days || ' - ' || trans.dotr_pol_hrs || ' Hrs') as dotr_pol_free_days,
							(trans.dotr_pod_free_days || ' - ' || trans.dotr_pod_hrs || ' Hrs') as dotr_pod_free_days,
							depot_loc.name as pickup_loc,
							trans_loc.name as dropoff_loc,
							trans.load_address,
							trans.unload_address,
							offload_trans_loc.name as offload_loc

							from  ct_enquiry trans
							left join cm_department dep on dep.id = trans.gr_dep_id
							left join cm_transport_route trans_route on trans_route.id = trans.trans_route_id
							left join cm_depot_location depot_loc on depot_loc.id = trans.trans_pickup_depot_id
							left join cm_transport_location trans_loc on trans_loc.id = trans.empty_pickup_loc_id
							left join cm_transport_location offload_trans_loc on offload_trans_loc.id = trans.empty_offload_loc_id

							where trans.id = v_trans_id;			

						LOOP                 
							FETCH cursor_3 INTO v_dep,v_prod_weight_kg,v_trailer_type,v_route_name,
								v_pickup_loc,v_dropoff_loc,v_load_address,v_unload_address,v_offload_loc;

							IF NOT FOUND then 
								Exit;
							end if; 

						if(v_dep is null) then
							v_dep='';
						end if;

						if(v_prod_weight_kg is null) then
							v_prod_weight_kg='';
						end if;

						if(v_trailer_type is null) then
							v_trailer_type='';
						end if;

						if(v_route_name is null) then
							v_route_name='';
						end if;

						if(v_pickup_loc is null) then
							v_pickup_loc='';
						end if;

						if(v_dropoff_loc is null) then
							v_dropoff_loc='';
						end if;

						if(v_load_address is null) then
							v_load_address='';
						end if;

						if(v_unload_address is null) then
							v_unload_address='';
						end if;

						if(v_offload_loc is null) then
							v_offload_loc='';
						end if;

						 v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>POL:</b></th>';

						 v_data=v_data || '
							<tr>
								<td colspan="3" id="remove-right-border">GR Department Name</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_dep||'</td>
								<td colspan="3" id="remove-right-border">Drop Off Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_dropoff_loc||'</td>
							</tr>

							<tr>
								<td colspan="3" id="remove-right-border">Product Weight(Kgs)</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_prod_weight_kg||'</td>
								<td colspan="3" id="remove-right-border">Loading Address</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_load_address||'</td>
							</tr>

							<tr>
								<td colspan="3" id="remove-right-border">Trailer Type</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_trailer_type||'</td>
								<td colspan="3" id="remove-right-border">Unloading Address</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_unload_address||'</td>
							</tr>
							<tr>
								<td colspan="3" id="remove-right-border">Route Name</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_route_name||'</td>
								<td colspan="3" id="remove-right-border">Empty Off Loading Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_offload_loc||'</td>
							</tr>
							<tr>
								<td colspan="3" id="remove-right-border">Pick Up Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_pickup_loc||'</td>
								
								<td colspan="3" id="remove-right-border"></td>
								<td colspan="3" id="no-border"></td>
								<td colspan="3" id="remove-left-border"></td>
							</tr>';
							END LOOP;
						Close cursor_3;
					
					end if;
					
					if v_sys_ref in ('DRDR') then
					
						Open cursor_4 FOR

							select 
				
							end_dep.name as end_department,
							trans.end_prod_weight_kg,
							(case when trans.end_trailer_type = '20_feet' then '20 Feet'
								  when trans.end_trailer_type = '40_feet' then '40 Feet'
								  when trans.end_trailer_type = 'both' then 'Both'
								  else '' end) as end_trailer_type,
							end_trans_route.name as end_route_name,
							(trans.end_dotr_pol_free_days || ' - ' || trans.end_dotr_pol_hrs || ' Hrs') as end_dotr_pol_free_days,
							(trans.end_dotr_pod_free_days || ' - ' || trans.end_dotr_pod_hrs || ' Hrs') as end_dotr_pod_free_days,
							end_depot_loc.name as end_pickup_loc,
							end_trans_loc.name as end_dropoff_loc,
							trans.end_load_address,
							trans.end_unload_address,
							end_offload_trans_loc.name as end_offload_loc

							from  ct_enquiry trans
							left join cm_department end_dep on end_dep.id = trans.end_gr_dep_id
							left join cm_transport_route end_trans_route on end_trans_route.id = trans.end_trans_route_id
							left join cm_depot_location end_depot_loc on end_depot_loc.id = trans.end_trans_pickup_depot_id
							left join cm_transport_location end_trans_loc on end_trans_loc.id = trans.end_empty_pickup_loc_id
							left join cm_transport_location end_offload_trans_loc on end_offload_trans_loc.id = trans.end_empty_offload_loc_id

							where trans.id = v_trans_id;			

						LOOP                 
							FETCH cursor_4 INTO v_end_dep,v_end_prod_weight_kg,v_end_trailer_type,
								v_end_route_name,v_end_pickup_loc,v_end_dropoff_loc,
								v_end_load_address,v_end_unload_address,v_end_offload_loc;

							IF NOT FOUND then 
								Exit;
							end if; 

						if(v_end_dep is null) then
							v_end_dep='';
						end if;

						if(v_end_prod_weight_kg is null) then
							v_end_prod_weight_kg='';
						end if;

						if(v_end_trailer_type is null) then
							v_end_trailer_type='';
						end if;

						if(v_end_route_name is null) then
							v_end_route_name='';
						end if;

						if(v_end_pickup_loc is null) then
							v_end_pickup_loc='';
						end if;

						if(v_end_dropoff_loc is null) then
							v_end_dropoff_loc='';
						end if;

						if(v_end_load_address is null) then
							v_end_load_address='';
						end if;

						if(v_end_unload_address is null) then
							v_end_unload_address='';
						end if;

						if(v_end_offload_loc is null) then
							v_end_offload_loc='';
						end if;

						 v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>POD:</b></th>';

						 v_data=v_data || '
							<tr>
								<td colspan="3" id="remove-right-border">GR Department Name</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_dep||'</td>
								<td colspan="3" id="remove-right-border">Drop Off Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_dropoff_loc||'</td>
							</tr>

							<tr>
								<td colspan="3" id="remove-right-border">Product Weight(Kgs)</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_prod_weight_kg||'</td>
								<td colspan="3" id="remove-right-border">Loading Address</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_load_address||'</td>
							</tr>

							<tr>
								<td colspan="3" id="remove-right-border">Trailer Type</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_trailer_type||'</td>
								<td colspan="3" id="remove-right-border">Unloading Address</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_unload_address||'</td>
							</tr>
							<tr>
								<td colspan="3" id="remove-right-border">Route Name</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_route_name||'</td>
								<td colspan="3" id="remove-right-border">Empty Off Loading Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_offload_loc||'</td>
							</tr>
							<tr>
								<td colspan="3" id="remove-right-border">Pick Up Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_pickup_loc||'</td>
								
								<td colspan="3" id="remove-right-border"></td>
								<td colspan="3" id="no-border"></td>
								<td colspan="3" id="remove-left-border"></td>
							</tr>';
							END LOOP;
						Close cursor_4;
					end if;
					
					
					END LOOP;
				Close cursor_2;
				
				
			elseif v_service_code in ('DOTC') then

				Open cursor_2 FOR

					select 
					ship_term.sys_ref as sys_ref,
					ship_term.name as ship_term,
					pol_port.name as pol,
					trans.coastal_pol_free_days,
					pod_port.name as pod,
					trans.coastal_pod_free_days

					from ct_enquiry trans
					left join cm_shipment_term ship_term on ship_term.id = trans.ship_term_id
					left join cm_port pol_port on pol_port.id = trans.coastal_pol_port_id 
					left join cm_port pod_port on pod_port.id = trans.coastal_pod_port_id 

					where trans.id = v_trans_id;			

				LOOP                 
					FETCH cursor_2 INTO v_sys_ref,v_ship_term,v_pol,v_pol_free_days,
						v_pod,v_pod_free_days;

					IF NOT FOUND then 
						Exit;
					end if; 

				if(v_sys_ref is null) then
					v_sys_ref='';
				end if;

				if(v_ship_term is null) then
					v_ship_term='';
				end if;

				if(v_pol is null) then
					v_pol='';
				end if;

				if(v_pol_free_days is null) then
					v_pol_free_days='';
				end if;

				if(v_pod is null) then
					v_pod='';
				end if;

				if(v_pod_free_days is null) then
					v_pod_free_days='';
				end if;

				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';

				 v_data=v_data || '
					<tr>
						<td colspan="3" id="remove-right-border">Shipment Term</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_ship_term||'</td>
						<td colspan="3" id="remove-right-border">POD ICD</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POL ICD</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pol||'</td>
						<td colspan="3" id="remove-right-border">POD Free Days</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pod_free_days||'</td>
					</tr>

					<tr>
						<td colspan="3" id="remove-right-border">POL Free Days</td>
						<td colspan="3" id="no-border">:</td>
						<td colspan="3" id="remove-left-border">'||v_pol_free_days||'</td>
						
						<td colspan="3" id="remove-right-border"></td>
						<td colspan="3" id="no-border"></td>
						<td colspan="3" id="remove-left-border"></td>
					</tr>';

					if v_sys_ref in ('CYDO', 'DOCY', 'DRDR') then

						Open cursor_3 FOR

							select 

							dep.name as department,
							trans.prod_weight_kg,
							(case when trans.trailer_type = '20_feet' then '20 Feet'
								  when trans.trailer_type = '40_feet' then '40 Feet'
								  when trans.trailer_type = 'both' then 'Both'
								  else '' end) as trailer_type,
							trans_route.name as route_name,
							(trans.dotr_pol_free_days || ' - ' || trans.dotr_pol_hrs || ' Hrs') as dotr_pol_free_days,
							(trans.dotr_pod_free_days || ' - ' || trans.dotr_pod_hrs || ' Hrs') as dotr_pod_free_days,
							depot_loc.name as pickup_loc,
							trans_loc.name as dropoff_loc,
							trans.load_address,
							trans.unload_address,
							offload_trans_loc.name as offload_loc

							from  ct_enquiry trans
							left join cm_department dep on dep.id = trans.gr_dep_id
							left join cm_transport_route trans_route on trans_route.id = trans.trans_route_id
							left join cm_depot_location depot_loc on depot_loc.id = trans.trans_pickup_depot_id
							left join cm_transport_location trans_loc on trans_loc.id = trans.empty_pickup_loc_id
							left join cm_transport_location offload_trans_loc on offload_trans_loc.id = trans.empty_offload_loc_id

							where trans.id = v_trans_id;			

						LOOP                 
							FETCH cursor_3 INTO v_dep,v_prod_weight_kg,v_trailer_type,v_route_name,
								v_pickup_loc,v_dropoff_loc,v_load_address,v_unload_address,v_offload_loc;

							IF NOT FOUND then 
								Exit;
							end if; 

						if(v_dep is null) then
							v_dep='';
						end if;

						if(v_prod_weight_kg is null) then
							v_prod_weight_kg='';
						end if;

						if(v_trailer_type is null) then
							v_trailer_type='';
						end if;

						if(v_route_name is null) then
							v_route_name='';
						end if;

						if(v_pickup_loc is null) then
							v_pickup_loc='';
						end if;

						if(v_dropoff_loc is null) then
							v_dropoff_loc='';
						end if;

						if(v_load_address is null) then
							v_load_address='';
						end if;

						if(v_unload_address is null) then
							v_unload_address='';
						end if;

						if(v_offload_loc is null) then
							v_offload_loc='';
						end if;

						 v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>POL:</b></th>';

						 v_data=v_data || '
							<tr>
								<td colspan="3" id="remove-right-border">GR Department Name</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_dep||'</td>
								<td colspan="3" id="remove-right-border">Drop Off Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_dropoff_loc||'</td>
							</tr>

							<tr>
								<td colspan="3" id="remove-right-border">Product Weight(Kgs)</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_prod_weight_kg||'</td>
								<td colspan="3" id="remove-right-border">Loading Address</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_load_address||'</td>
							</tr>

							<tr>
								<td colspan="3" id="remove-right-border">Trailer Type</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_trailer_type||'</td>
								<td colspan="3" id="remove-right-border">Unloading Address</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_unload_address||'</td>
							</tr>
							<tr>
								<td colspan="3" id="remove-right-border">Route Name</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_route_name||'</td>
								<td colspan="3" id="remove-right-border">Empty Off Loading Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_offload_loc||'</td>
							</tr>
							<tr>
								<td colspan="3" id="remove-right-border">Pick Up Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_pickup_loc||'</td>
								
								<td colspan="3" id="remove-right-border"></td>
								<td colspan="3" id="no-border"></td>
								<td colspan="3" id="remove-left-border"></td>
							</tr>';
							END LOOP;
						Close cursor_3;

					end if;

					if v_sys_ref in ('DRDR') then

						Open cursor_4 FOR

							select 

							end_dep.name as end_department,
							trans.end_prod_weight_kg,
							(case when trans.end_trailer_type = '20_feet' then '20 Feet'
								  when trans.end_trailer_type = '40_feet' then '40 Feet'
								  when trans.end_trailer_type = 'both' then 'Both'
								  else '' end) as end_trailer_type,
							end_trans_route.name as end_route_name,
							(trans.end_dotr_pol_free_days || ' - ' || trans.end_dotr_pol_hrs || ' Hrs') as end_dotr_pol_free_days,
							(trans.end_dotr_pod_free_days || ' - ' || trans.end_dotr_pod_hrs || ' Hrs') as end_dotr_pod_free_days,
							end_depot_loc.name as end_pickup_loc,
							end_trans_loc.name as end_dropoff_loc,
							trans.end_load_address,
							trans.end_unload_address,
							end_offload_trans_loc.name as end_offload_loc

							from  ct_enquiry trans
							left join cm_department end_dep on end_dep.id = trans.end_gr_dep_id
							left join cm_transport_route end_trans_route on end_trans_route.id = trans.end_trans_route_id
							left join cm_depot_location end_depot_loc on end_depot_loc.id = trans.end_trans_pickup_depot_id
							left join cm_transport_location end_trans_loc on end_trans_loc.id = trans.end_empty_pickup_loc_id
							left join cm_transport_location end_offload_trans_loc on end_offload_trans_loc.id = trans.end_empty_offload_loc_id

							where trans.id = v_trans_id;			

						LOOP                 
							FETCH cursor_4 INTO v_end_dep,v_end_prod_weight_kg,v_end_trailer_type,
								v_end_route_name,v_end_pickup_loc,v_end_dropoff_loc,
								v_end_load_address,v_end_unload_address,v_end_offload_loc;

							IF NOT FOUND then 
								Exit;
							end if; 

						if(v_end_dep is null) then
							v_end_dep='';
						end if;

						if(v_end_prod_weight_kg is null) then
							v_end_prod_weight_kg='';
						end if;

						if(v_end_trailer_type is null) then
							v_end_trailer_type='';
						end if;

						if(v_end_route_name is null) then
							v_end_route_name='';
						end if;

						if(v_end_pickup_loc is null) then
							v_end_pickup_loc='';
						end if;

						if(v_end_dropoff_loc is null) then
							v_end_dropoff_loc='';
						end if;

						if(v_end_load_address is null) then
							v_end_load_address='';
						end if;

						if(v_end_unload_address is null) then
							v_end_unload_address='';
						end if;

						if(v_end_offload_loc is null) then
							v_end_offload_loc='';
						end if;

						 v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green"><b>POD:</b></th>';

						 v_data=v_data || '
							<tr>
								<td colspan="3" id="remove-right-border">GR Department Name</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_dep||'</td>
								<td colspan="3" id="remove-right-border">Drop Off Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_dropoff_loc||'</td>
							</tr>

							<tr>
								<td colspan="3" id="remove-right-border">Product Weight(Kgs)</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_prod_weight_kg||'</td>
								<td colspan="3" id="remove-right-border">Loading Address</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_load_address||'</td>
							</tr>

							<tr>
								<td colspan="3" id="remove-right-border">Trailer Type</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_trailer_type||'</td>
								<td colspan="3" id="remove-right-border">Unloading Address</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_unload_address||'</td>
							</tr>
							<tr>
								<td colspan="3" id="remove-right-border">Route Name</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_route_name||'</td>
								<td colspan="3" id="remove-right-border">Empty Off Loading Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_offload_loc||'</td>
							</tr>
							<tr>
								<td colspan="3" id="remove-right-border">Pick Up Location</td>
								<td colspan="3" id="no-border">:</td>
								<td colspan="3" id="remove-left-border">'||v_end_pickup_loc||'</td>
								
								<td colspan="3" id="remove-right-border"></td>
								<td colspan="3" id="no-border"></td>
								<td colspan="3" id="remove-left-border"></td>
							</tr>';
							END LOOP;
						Close cursor_4;
					end if;

				END LOOP;
			Close cursor_2;
			
			
			end if;

			if v_additional_service != '' and v_spl_req != '' then 
				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green">&nbsp;</th>';
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
				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green">&nbsp;</th>';
				v_data=v_data ||'
				<tr>
					<td colspan="3" id="remove-right-border">Additional Services</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_additional_service||'</td>
					
					<td colspan="3" id="remove-right-border"></td>
					<td colspan="3" id="no-border"></td>
					<td colspan="3" id="remove-left-border"></td>
				</tr>';
			
			elseif v_spl_req != '' then
				v_data=v_data || '<th colspan="18" scope="colgroup" class="table-heading green">&nbsp;</th>';
				v_data=v_data ||'
				<tr>
					<td colspan="3" id="remove-right-border">Special Requirements</td>
					<td colspan="3" id="no-border">:</td>
					<td colspan="3" id="remove-left-border">'||v_spl_req||'</td>
					
					<td colspan="3" id="remove-right-border"></td>
					<td colspan="3" id="no-border"></td>
					<td colspan="3" id="remove-left-border"></td>
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

ALTER FUNCTION public.ctm_enquiry_confirm_mail(integer, character, character, character, character)
    OWNER TO odoo;

