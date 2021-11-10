from odoo import api, models, fields,_
from odoo.exceptions import Warning


class ResPartner(models.Model):
    _inherit = 'res.partner'

    prop_list = fields.One2many('anagrafiche.imobile','owner_id', string="Property list")
    coowner_property = fields.Many2many('anagrafiche.imobile','rel_property_coowner', string='Coowner property')

class AnagraficheImobile(models.Model):
    _name = 'anagrafiche.imobile'
    _description = 'Anagrafiche Imobile'

    owner_id = fields.Many2one('res.partner', string="Owner id", required=True)
    property_ty = fields.Many2one('tipologie.im', string="Type of property")
    account_thermal = fields.Many2one('lista.agenzie', string="Account Thermal")
    property_size = fields.Float(string="Size of property")
    roof_size = fields.Float(string="Size of roof")
    roof_type = fields.Many2one('lista.tipologia.copertura', string="Type of roof")
    presence_photov_system = fields.Boolean(string="Presence of a photovoltaic system")
    date_stacking = fields.Date(string="Date Stacking")
    coowner = fields.Boolean(string="Co-Owner")
    inhabited_attic = fields.Boolean(string="Inhabited Attic")
    coowner_ids = fields.Many2many('res.partner', 'rel_property_coowner', string="Name/Surname of the Co-Owner")
    technical_reference = fields.Boolean(string="Technical Reference")
    techn_name = fields.Char(string="Technical Name")
    address = fields.Char(string="Address", required=True)
    city = fields.Char(string="City", required=True)
    presence_prev_solar_thermal_plant = fields.Boolean(string="Presence of a previous solar thermal plant")
    zip = fields.Char(string="ZIP")
    sheet = fields.Char(string="Sheet")
    fixtures = fields.Boolean(string="Are we also interested in the fixtures situation?")
    prev_thermal_system = fields.Boolean(string="Does the property have a previous thermal system?")
    parcel = fields.Char(string="Parcel")
    sub = fields.Char(string="Sub")
    note = fields.Char(string="Note")
    brand = fields.Char(string="Brand")
    cadas_categ = fields.Char(string="Cadastral category")
    costr_year = fields.Date(string="Construction year")
    note_sec = fields.Char(string="Note")
    model = fields.Char(string="Model")
    heat_distrib = fields.Many2one('lista.td.calore', string="Heat Distribution")
    note_third = fields.Char(string="Note")
    urban_congruity = fields.Boolean(string="The assessment of urban congruity is required")
    prop_no_discrep = fields.Boolean(string="The property has no discrepancies")
    dwh_prod_kw = fields.Float(string="Production of Domestic Water Heating (DWH) (kw)")
    prop_tag = fields.Many2many('list.tag.immobile', string="Property Tag")
    dwh_prod_tag = fields.Many2many("list.tag.prod.acs", string="DWH production tag")

    # @api.constrains('coowner_ids')
    # def check_address_data(self):
    #     for each in self:
    #         if each.coowner_ids:
    #             if each.coowner_ids.filtered(lambda l: not l.city):
    #                 raise Warning(_('Please city city of co-owners you add.'))

class ListaAgenzie(models.Model):
    _name = 'lista.agenzie'
    _description = 'Agency List'
    _rec_name = 'agency_descr'

    agency_descr = fields.Char(string="Agency Description", required=True)


class TipologieIm(models.Model):
    _name = 'tipologie.im'
    _description = 'Type of'
    _rec_name = 'property_type'

    property_type = fields.Char(string="Type of property list", required=True)


class ListaTipologiaCopertura(models.Model):
    _name = 'lista.tipologia.copertura'
    _description = 'Type of roof'
    _rec_name = 'roof_type_desc'

    roof_type_desc = fields.Char(string="Roof type description", required=True)


class ListaTdCalore(models.Model):
    _name = 'lista.td.calore'
    _description = 'Heat distribution'
    _rec_name = 'heat_distr_descr'

    heat_distr_descr = fields.Char(string="Heat distribution description", required=True)

class ListTagImmobile(models.Model):
    _name = 'list.tag.immobile'
    _description = 'Property tag'
    _rec_name = 'prop_tag_descr'

    prop_tag_descr = fields.Char(string="Property tag description", required=True)

class ListTagProdAcs(models.Model):
    _name = 'list.tag.prod.acs'
    _description = 'DWH production tag'
    _rec_name = 'prod_dwh_tag'

    prod_dwh_tag = fields.Char(string="Production DWH tag description", required=True)
