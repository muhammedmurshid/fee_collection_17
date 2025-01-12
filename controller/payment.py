from odoo import http
from odoo.http import request, Response
import json

class QuickPayController(http.Controller):

    @http.route(['/quick_pay'], type='http', auth="public", methods=['GET'])
    def quick_pay(self, **kwargs):
        try:
            # Validate incoming parameters
            name = kwargs.get('Name')
            purpose = kwargs.get('Purpose')
            amount = kwargs.get('Amount')
            phone = kwargs.get('Phone')
            if not name or not purpose or not amount or not phone:
                return Response(
                    json.dumps({'error': 'Missing required parameters'}),
                    status=400,
                    content_type='application/json'
                )

            # Create record in 'fee.quick.pay'
            print('kwrag', kwargs)
            record = request.env['fee.quick.pay'].sudo().create({
                'name': name,
                'purpose': purpose,
                'amount': float(amount),
                'phone': phone,
                'refno': kwargs.get('Refno'),
                'branch': kwargs.get('branch'),
                # 'email_id': kwargs.get('email_id'),
                'batch': kwargs.get('batch'),
                'admission_no': kwargs.get('admission_number'),
            })

            # Return success response
            sample_link = "https://localhost:8069/quick_pay?Name=None&Purpose=admission_fee&Amount=None&Phone=None&Refno=None&branch=None&email_id=None&batch=ca&admission_number="
            response_data = {
                'status': 'success',
                'message': 'Quick pay record created successfully',
                'record_id': record.id
            }
            return Response(
                json.dumps(response_data),
                status=200,
                content_type='application/json'
            )
        except Exception as e:
            # Return error response
            error_response = {
                'status': 'error',
                'message': f"An error occurred: {str(e)}"
            }
            return Response(
                json.dumps(error_response),
                status=500,
                content_type='application/json'
            )
