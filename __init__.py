# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from shipment import ItemsWaitingShipmentReport, ItemsWaitingShipmentStart, \
    ItemsWaitingShipmentReportWizard


def register():
    Pool.register(
        ItemsWaitingShipmentStart,
        module='waiting_customer_shipment_report', type_='model'
    )
    Pool.register(
        ItemsWaitingShipmentReport,
        module='waiting_customer_shipment_report', type_='report'
    )
    Pool.register(
        ItemsWaitingShipmentReportWizard,
        module='waiting_customer_shipment_report', type_='wizard'
    )
