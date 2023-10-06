#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestAccountInvoice(FatturaPACommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # XXX - a company named "YourCompany" alread exists
        # we move it out of the way but we should do better here
        cls.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )
        cls.env.company.name = "YourCompany"
        cls.env.company.vat = "IT06363391001"
        cls.env.company.fatturapa_art73 = True
        cls.env.company.partner_id.street = "Via Milano, 1"
        cls.env.company.partner_id.city = "Roma"
        cls.env.company.partner_id.state_id = cls.env.ref("base.state_us_2").id
        cls.env.company.partner_id.zip = "00100"
        cls.env.company.partner_id.phone = "06543534343"
        cls.env.company.email = "info@yourcompany.example.com"
        cls.env.company.partner_id.country_id = cls.env.ref("base.it").id
        cls.env.company.fatturapa_fiscal_position_id = cls.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id

        cls.sdi_coop_channel = cls.env["sdi.channel"].create(
            [
                {
                    "name": "Test SdiCoop channel",
                    "channel_type": "sdi_coop",
                }
            ]
        )

    def test_action_open_export_send_sdi(self):
        """
        Check that the "Validate, export and send to SdI" button
        tries to send the e-invoice.
        """
        # Arrange: set the SdI channel
        # and create a draft invoice with no attachment
        self.env.company.sdi_channel_id = self.sdi_coop_channel
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, "draft")
        self.assertFalse(invoice.fatturapa_attachment_out_id)

        # Act and Assert: open, export and send.
        # This raises an exception
        # because sending mechanism will be implemented by depending modules
        with self.assertRaises(NotImplementedError):
            invoice.action_open_export_send_sdi()
