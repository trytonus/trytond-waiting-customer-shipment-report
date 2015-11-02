# -*- coding: utf-8 -*-
"""
    __init__.py

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
