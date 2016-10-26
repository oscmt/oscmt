from django.forms import ValidationError
from django.db import models

# Create your models here.

class Client(models.Model):
    """
    Stores a client company's name.
    """
    name = models.CharField(max_length = 32)

    def __str__(self):
        return self.name

class Consultant(models.Model):
    """
    Stores information about a consultant, namely first and last names, as well as comments like "department head"
    """
    first_name = models.CharField(max_length = 32)
    last_name = models.CharField(max_length = 32)

    # comments can e. g. hold a special skill
    comments = models.CharField(max_length = 200, blank = True)

    def __str__(self):
        stringRep = '{0} {1} ({2})'.format(self.first_name,
                self.last_name, self.comments)
        return stringRep

class Contact(models.Model):
    """
    Stores a contact's information.
    The contact's company is not necessarily equal to the :model:`casetool.Case`'s client.
    """

    first_name = models.CharField(max_length = 32)
    last_name = models.CharField(max_length = 32)
    phone_number = models.CharField(max_length = 32, blank = True)
    email_address = models.EmailField(blank = True)

    # company is not necessarily equal to the client
    company = models.CharField(max_length = 32)

    def __str__(self):
        stringRep = '{0} {1} ({2})'.format(self.first_name,
                self.last_name, self.company)
        return stringRep

class Contract(models.Model):
    """
    Stores information about a contract between us and a :model:`casetool.Client`
    """
    def validate_file_extension(value):
        if value.file.content_type != 'application/pdf':
                raise ValidationError('Invalid file type')

    def nda_path(instance, filename):
        date_string = datetime.date.today().strftime('%Y/%m/%d')
        return '/'.join([date_string, instance.client.name, 'nda', 'nda.pdf'])

    client = models.ForeignKey(Client, on_delete = models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    cost_limit = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null = True)
    time_limit = models.PositiveIntegerField(blank = True, null = True)

    # save the nda to the generated path
    nda = models.FileField(upload_to = nda_path,
        blank = True,
        validators = [validate_file_extension,]
    )

    # Contracts are managed in a different application, this field is to
    # conveniently find the connection
    crm_number = models.CharField(
                            max_length = 32,
                            blank = True,
                            default = "No entry specified"
                            )

    def __str__(self):
        return 'CRM: ' + self.crm_number

class Documentation(models.Model):
    """
    Stores the status and the storage location of a :model:`casteool.Case`'s documentation.
    """
    def validate_file_extension(value):
        if value.file.content_type != 'application/pdf':
                raise ValidationError('Invalid file type')

    def doc_path(instance, filename):
        date_string = datetime.date.today().strftime('%Y/%m/%d')
        return '/'.join([date_string, instance.contract.client.name, 'doc', 'doc.pdf'])

    # declare the possible states of a Documentation
    DRAFT = 'DRA'
    REVISION = 'REV'
    ACCEPTED = 'ACC'

    DOC_STAT = (
            (DRAFT, 'draft'),
            (REVISION, 'revision'),
            (ACCEPTED, 'accepted'),
            )

    contract = models.ForeignKey(Contract, on_delete = models.CASCADE)

    data_path = models.FileField(upload_to = doc_path,
        validators = [validate_file_extension,]
    )

    change_date = models.DateField()
    status = models.CharField(max_length = 3, choices = DOC_STAT,
            default = DRAFT)

    def __str__(self):
        return ', '.join([str(self.contract), self.status])

class Case(models.Model):
    """
    Stores information about a case.
    """

    def consecutive_number_generator():
        from django.db.models import Max
        from datetime import date

        year = date.today().year
        max_number = Case.objects.filter(created_at__year = year).aggregate(Max('consecutive_number'))
        if max_number['consecutive_number__max']:
            return max_number['consecutive_number__max'] + 1
        return 1

    external_id = models.CharField(max_length = 32, unique = True)

    # who is in charge of the case on the Client's side
    external_main_contact = models.ForeignKey(Contact, on_delete = models.CASCADE)

    # who is the client
    client = models.ForeignKey(Client, on_delete = models.CASCADE)

    contract = models.ForeignKey(Contract, on_delete = models.CASCADE)

    consecutive_number = models.PositiveIntegerField(default = consecutive_number_generator)

    # who is in charge of the case on our side
    internal_main_contact = models.ForeignKey(Consultant, on_delete = models.CASCADE)

    additional_info = models.CharField(max_length = 500, blank=True)

    analysis_storage = models.CharField(max_length = 256, blank = True)
    documentation = models.ForeignKey(Documentation, blank = True, null = True, on_delete = models.CASCADE)
    case_done = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deletion_date = models.DateField(null = True, blank = True)


    def __str__(self):
        return self.external_id

    def save(self, *args, **kwargs):
        if self.analysis_storage == '':
            vmdir = '/vmpool/' + self.external_id
            self.analysis_storage = vmdir
            import subprocess
            from datetime import date
            subprocess.call(['/vmpool/vm_generator.sh', str(date.today().year)[-2:], str(self.consecutive_number), self.external_id])

        if self.case_done and self.deletion_date is None:
            import datetime
            self.deletion_date = (datetime.date.today() + datetime.timedelta(6*365/12))
        super(Case, self).save(*args, **kwargs)

class CaseConsultantMap(models.Model):
    case = models.ForeignKey(Case, on_delete = models.CASCADE)
    consultant = models.ForeignKey(Consultant, on_delete = models.CASCADE)

class CaseContactMap(models.Model):
    case = models.ForeignKey(Case, on_delete = models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete = models.CASCADE)

class Evidence(models.Model):
    """
    Stores information about pieces of evidence, e. g. a harddisk.
    """
    PHYSICAL = 'PHY'
    LOGICAL = 'LOG'
    OTHER = 'OTH'

    EV_TYPE = (
            (PHYSICAL, 'physical'),
            (LOGICAL, 'logical'),
            (OTHER, 'other'),
            )

    case = models.ForeignKey(Case, on_delete = models.CASCADE)

    serial_number = models.CharField(max_length = 200, blank = True)
    storage_location = models.CharField(max_length = 200, blank = True)
    producer = models.CharField(max_length = 200, blank = True)
    model = models.CharField(max_length = 200, blank = True)
    description = models.CharField(max_length = 500, blank = True)
    pictures = models.ImageField(blank = True)
    evidence_type = models.CharField(max_length = 3, choices = EV_TYPE)

    isActive = models.BooleanField(default = True)

    def __str__(self):
        return self.serial_number

class Seal(models.Model):
    """
    Seals are used whenever a new :model:`casetool.ChainOfCustodyEvent` occurs.
    """
    BAG = 'BAG'
    STICKER = 'STI'

    SEAL_TYPE = (
            (BAG, 'bag'),
            (STICKER, 'sticker'),
            )

    number = models.CharField(max_length = 64)
    seal_type = models.CharField(max_length = 3, choices = SEAL_TYPE)

    def __str__(self):
        return self.number

class SubEvidence(models.Model):
    """
    If a :model:`casetool.Evidence` is copied, e. g. for a working copy, a SubEvidence can be created.
    """
    WORKING_COPY = 'WOR'
    BEST_EVIDENCE = 'BES'

    EV_TYPE = (
            (WORKING_COPY, 'working copy'),
            (BEST_EVIDENCE, 'best evidence'),
            )

    parent_evidence = models.ForeignKey(Evidence, on_delete = models.CASCADE)
    evidence_type = models.CharField(max_length = 3, choices = EV_TYPE)
    seal = models.ForeignKey(Seal, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.evidence_type) + ', sub to ' + str(self.parent_evidence) + ', seal ' + str(self.seal)

class ChainOfCustodyEvent(models.Model):
    """
    Stores information about what happened whenever a :model:`casetool.Seal` is broken.
    """
    evidence = models.ForeignKey(Evidence, on_delete = models.CASCADE)
    seal = models.ForeignKey(Seal, on_delete = models.CASCADE)
    reason = models.CharField(max_length = 200)
    handover_by = models.CharField(max_length = 200)
    received_by = models.CharField(max_length = 200)
    timestamp = models.DateTimeField()
    additional_info = models.CharField(max_length = 500, blank = True)

    def __str__(self):
        return str(self.seal)
