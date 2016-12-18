from django.contrib import admin

from casetool.models import *
from casetool.admin_site import admin_site

# inline classes for convenient matching views
class CaseConsultantMapInline(admin.TabularInline):
    model = CaseConsultantMap
    extra = 0

class CaseContactMapInline(admin.TabularInline):
    model = CaseContactMap
    extra = 0

class ClientInline(admin.TabularInline):
    model = Client
    extra = 0

class CoCInline(admin.TabularInline):
    model = ChainOfCustodyEvent
    extra = 0

#class ContractInline(admin.TabularInline):
#    model = Contract
#    extra = 0

class CaseInline(admin.TabularInline):
    model = Case
    extra = 0

class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 0

class SubEvidenceInline(admin.TabularInline):
    model = SubEvidence
    extra = 0

# registering models, passing inline classes and search fields
@admin.register(Case, site = admin_site)
class CaseAdmin(admin.ModelAdmin):
    inlines = [
        CaseConsultantMapInline,
        CaseContactMapInline,
        EvidenceInline,
    ]

    search_fields = [
        'external_id',
        'additional_info',
    ]

    list_filter = [
        'deletion_date',
        'client',
        'internal_main_contact',
        'contract',
    ]

@admin.register(Evidence, site = admin_site)
class EvidenceAdmin(admin.ModelAdmin):
    inlines = [
        CoCInline,
        SubEvidenceInline,
    ]

    search_fields = [
        'serial_number',
        'storage_location',
    ]

    list_filter = [
        'case',
        'isActive',
        'evidence_type',
        'storage_location',
    ]

@admin.register(Client, site = admin_site)
class ClientAdmin(admin.ModelAdmin):
    inlines = [
        CaseInline,
    ]
    search_fields = [
        'name',
    ]

@admin.register(Consultant, site = admin_site)
class ConsultantAdmin(admin.ModelAdmin):
    search_fields = [
        'first_name',
        'last_name',
        'comments',
    ]

@admin.register(Contact, site = admin_site)
class ContactAdmin(admin.ModelAdmin):
    search_fields = [
        'first_name',
        'last_name',
        'phone_number',
        'email_address',
        'company',
    ]

    list_filter = [
        'company',
    ]

@admin.register(Contract, site = admin_site)
class ContractAdmin(admin.ModelAdmin):
    inlines = [
        CaseInline,
    ]

    list_filter = [
        'client',
        'start',
        'end',
    ]

@admin.register(Documentation, site = admin_site)
class DocumentationAdmin(admin.ModelAdmin):
    pass

@admin.register(SubEvidence, site = admin_site)
class SubEvidenceAdmin(admin.ModelAdmin):
    pass

@admin.register(Seal, site = admin_site)
class SealAdmin(admin.ModelAdmin):
    search_fields = [
        'number',
    ]
