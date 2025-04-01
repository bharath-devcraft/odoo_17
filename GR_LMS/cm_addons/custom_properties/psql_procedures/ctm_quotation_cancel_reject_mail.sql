-- FUNCTION: public.ctm_quotation_cancel_reject_mail (integer, character, character, character)

-- DROP FUNCTION IF EXISTS public.ctm_quotation_cancel_reject_mail (integer, character, character, character);

CREATE OR REPLACE FUNCTION public.ctm_quotation_cancel_reject_mail (
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
v_enquiry_date char varying (10000);
v_reason char varying(10000);
v_service_name char varying(10000);
v_enquiry_no char varying(10000);
v_rejected_by char varying(10000);
v_canceled_by char varying(10000);
v_remark char varying(10000);



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
			
            select trans.name,to_char(trans.enquiry_date,'dd/mm/yyyy') as enquiry_date,
			service.name as sevice_name, trans.enquiry_no, rej_remark.name, trans.cancel_remark,
			rej_name.name as approved_by from  ct_quotations trans
			left join cm_service service on service.id = trans.service_id
			left join res_users rej_user on rej_user.id = trans.cancel_user_id
			left join res_partner rej_name on rej_name.id = rej_user.partner_id
			left join cm_rejection_remark rej_remark on rej_remark.id = trans.rej_remark_id
			
			where trans.id = v_trans_id ;			
			
			LOOP                 
		  		FETCH cursor_1 INTO v_trans_name,v_enquiry_date,v_service_name,v_enquiry_no,v_reason,v_remark,v_rejected_by;

				IF NOT FOUND then 
		    		Exit;
		   		end if; 

			if(v_trans_name is null) then
				v_trans_name='';
			end if;
			
			if(v_enquiry_date is null) then
				v_enquiry_date='';
			end if;
			
			if(v_service_name is null) then
				v_service_name='';
			end if;

			if(v_enquiry_no is null) then
				v_enquiry_no='';
			end if;
			
			if(v_reason is null) then
				v_reason='';
			end if;
			
			if(v_remark is null) then
				v_remark='';
			end if;

			if(v_rejected_by is null) then
				v_rejected_by=v_user_name;
			end if;
			if(v_canceled_by is null) then
				v_canceled_by=v_user_name;
			end if;

			
			v_table_heading= v_table_heading || '<table id="customers" style="border:none;">
				<tr style="border:1px solid #2f9780;"><td colspan="2" style="border:none;"><b style="margin-top: 15px;">Dear Sir / Mam</b>,</td></tr>';
				
           if(v_trans_state = 'rejected') then
				v_table_heading= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been rejected and the details are given below.</span></td></tr>
				</table>';
		   elseif (v_trans_state = 'cancelled') then
			    v_table_heading= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The <b>'||v_ref_no||'</b> has been cancelled and the details are given below.</span></td></tr>
				</table>';
		   else 
		       v_table_heading= v_table_heading || '<tr style="border-left:1px solid #2f9780;border-right:1px solid #2f9780;"><td colspan="2" style="border:none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>The detailsd of <b>'||v_ref_no||'</b> below, It has been created by '||v_created_by||'.</span></td></tr>
				</table>';
		      end if;
			
			v_data= v_table_heading ;
			
			
			v_data=v_data || '<table id="customers">
			<th colspan="18" scope="colgroup" class="table-heading green"><b>Enquiry Details:</b></th>';
			
		    v_data=v_data || '<tr>
			<td colspan="3">Enquiry No</td>
			<td colspan="3">'||v_ref_no||'</td>
			</tr>';
			
	            v_data=v_data || '<tr>
			<td colspan="3">Enquiry Date</td>
			<td colspan="3">'||v_enquiry_date||'</td>
			</tr>';
		
			v_data=v_data || '<tr>
			<td colspan="3">Service Name</td>
			<td colspan="3">'||v_service_name||'</td>
			</tr>
			
			<tr>
			<td colspan="3"><b>Reason</b></td>
			<td colspan="3"><b>'||v_reason||'</b></td>
			</tr>
			
			<tr>
			<td colspan="3"><b>Remarks</b></td>
			<td colspan="3" style="max-width: 200px; word-wrap: break-word; white-space: normal; overflow-wrap: break-word;" ><b>'||v_remark||'</b></td>
			</tr>';
			
			if(v_trans_state = 'rejected') then
				 v_data=v_data || '<tr>
				<td colspan="3"><b>Rejected By</b></td>
				<td colspan="3"><b>'||v_rejected_by||'</b></td>
				</tr>';
		        else
			
				v_data=v_data || '<tr>
				<td colspan="3"><b>Cancelled By</b></td>
				<td colspan="3"><b>'||v_rejected_by||'</b></td>
				</tr>';
			end if;
			
			if(v_trans_state = 'rejected') then
				 v_data=v_data || '<tr style="background-color: #FFE09A;">
				<td colspan="3">Enquiry Status</td>
				<td colspan="3">Rejected</td>
				</tr>';
		        else
			
				v_data=v_data || '<tr style="background-color: #FFE09A;">
				<td colspan="3">Enquiry Status</td>
				<td colspan="3">Draft</td>
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

ALTER FUNCTION public.ctm_quotation_cancel_reject_mail (integer, character, character, character)
    OWNER TO odoo;

