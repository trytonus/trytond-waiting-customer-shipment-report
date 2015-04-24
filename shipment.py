# -*- coding: utf-8 -*-
"""
    shipment.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from collections import defaultdict
from openlabs_report_webkit import ReportWebkit

from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.model import ModelView
from trytond.wizard import Wizard, StateAction, StateView, Button

__all__ = [
    'ItemsWaitingShipmentReport', 'ItemsWaitingShipmentStart',
    'ItemsWaitingShipmentReportWizard'
]


class ReportMixin(ReportWebkit):
    """
    Mixin Class to inherit from, for all HTML reports.
    """

    @classmethod
    def wkhtml_to_pdf(cls, data, options=None):
        """
        Call wkhtmltopdf to convert the html to pdf
        """
        Company = Pool().get('company.company')

        company = ''
        if Transaction().context.get('company'):
            company = Company(Transaction().context.get('company')).party.name
        options = {
            'margin-bottom': '0.50in',
            'margin-left': '0.50in',
            'margin-right': '0.50in',
            'margin-top': '0.50in',
            'footer-font-size': '8',
            'footer-left': company,
            'footer-line': '',
            'footer-right': '[page]/[toPage]',
            'footer-spacing': '5',
        }
        return super(ReportMixin, cls).wkhtml_to_pdf(
            data, options=options
        )


class ItemsWaitingShipmentReport(ReportMixin):
    """
    Items Waiting Shipment Report
    """
    __name__ = 'report.items_waiting_shipment'

    @classmethod
    def parse(cls, report, records, data, localcontext):
        ShipmentOut = Pool().get('stock.shipment.out')
        StockLocation = Pool().get('stock.location')
        Date = Pool().get('ir.date')
        Product = Pool().get('product.product')

        domain = [('state', 'in', ['assigned', 'waiting'])]
        shipments = ShipmentOut.search(domain)
        moves_by_products = {}
        product_quantities = defaultdict(int)

        for shipment in shipments:
            for move in shipment.inventory_moves:
                moves_by_products.setdefault(
                    move.product, []).append(move)

        warehouses = StockLocation.search([
            ('type', '=', 'warehouse'),
        ])
        products = moves_by_products.keys()
        with Transaction().set_context(
            stock_skip_warehouse=True,
            stock_date_end=Date.today(),
            stock_assign=True,
        ):
            pbl = Product.products_by_location(
                location_ids=map(int, warehouses),
                product_ids=map(int, products),
            )

            for key, qty in pbl.iteritems():
                _, product_id = key
                product_quantities[product_id] += qty

        localcontext.update({
            'moves_by_products': moves_by_products,
            'report_ext': report.extension,
            'product_quantities': product_quantities,
        })
        return super(ItemsWaitingShipmentReport, cls).parse(
            report, records, data, localcontext
        )

    @classmethod
    def get_jinja_filters(cls):
        rv = super(ItemsWaitingShipmentReport, cls).get_jinja_filters()

        rv['oldest_date'] = lambda moves: sorted(
            moves, key=lambda m: m.planned_date)[0].planned_date
        return rv


class ItemsWaitingShipmentStart(ModelView):
    'Generate Items Waiting Shipments Report'
    __name__ = 'report.items_waiting_shipment_wizard.start'


class ItemsWaitingShipmentReportWizard(Wizard):
    'Generate Items Waiting Shipments Report Wizard'
    __name__ = 'report.items_waiting_shipment_wizard'

    start = StateView(
        'report.items_waiting_shipment_wizard.start',
        'waiting_customer_shipment_report.items_waiting_shipments_start_view_form', [  # noqa
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Generate Report', 'generate', 'tryton-ok', default=True),
        ]
    )
    generate = StateAction(
        'waiting_customer_shipment_report.report_items_waiting_shipment')

    def transition_generate(self):
        return 'end'
