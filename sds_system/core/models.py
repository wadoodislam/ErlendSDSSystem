from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Language(models.Model):
    name = models.CharField(max_length=30)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    sds_pdf = models.ForeignKey('SDS_PDF', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    supplier = models.CharField(max_length=100)
    trade_name = models.CharField(max_length=100)
    language = models.CharField(max_length=30)
    matched = models.BooleanField(default=False)
    sds_pdf = models.ForeignKey('SDS_PDF', null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Erlend Models


class SDSHarvestSource(models.Model):
    class STATUS(models.TextChoices):
        RUNNING = 'Running'
        PENDING = 'Pending'
        DEVELOPED = 'Developed'

    class TYPE(models.TextChoices):
        RUNNING = 'Running'
        PENDING = 'Pending'
        DEVELOPED = 'Developed'

    class METHOD(models.TextChoices):
        SCRAPING = 'Scraping'
        ZIP = 'Zip'

    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS.choices, default=STATUS.PENDING, blank=True)
    type = models.CharField(max_length=10, choices=TYPE.choices, blank=True)
    primary = models.BooleanField(default=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    method = models.CharField(max_length=10, choices=METHOD.choices, default=METHOD.ZIP, blank=True)
    rerun_interval_days = models.IntegerField(default=1)
    last_run_at = models.DateTimeField(null=True, blank=True)
    developer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='developer')
    responsible_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='responsible_user')
    ready_for_crawling = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SDSHarvestRun(models.Model):
    sds_harvest_source = models.ForeignKey(SDSHarvestSource, on_delete=models.CASCADE)
    run_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    no_of_revision_found = models.IntegerField(default=1)
    no_of_new_sds_found = models.IntegerField(default=1)
    ended_at = models.DateTimeField(null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sds_harvest_source} ({self.id})'


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    alias = models.ForeignKey('Manufacturer', null=True, on_delete=models.PROTECT, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "SDS Producer"

    def __str__(self):
        return self.name


class ProducerOfSDS(models.Model):
    name = models.CharField(max_length=30)
    alias = models.ForeignKey('ProducerOfSDS', on_delete=models.PROTECT)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SDS_PDF(models.Model):

    class Meta:
        verbose_name = "sds pdf"

    name = models.CharField(max_length=100)
    sds_harvest_run = models.ForeignKey(SDSHarvestRun, null=True, on_delete=models.SET_NULL,)
    sds_harvest_source = models.ForeignKey(SDSHarvestSource, models.PROTECT)
    pdf_md5 = models.CharField(primary_key=True, null=False, max_length=32, editable=False)
    from_primary = models.BooleanField(default=True)

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)

    sds_link = models.URLField()
    sds_download_url = models.URLField(null=True)
    sds_product_name = models.CharField(max_length=100)
    sds_hazards_codes = models.CharField(max_length=250, blank=True, null=True)

    sds_print_date = models.DateField(blank=True, null=True)
    sds_published_date = models.DateField(blank=True, null=True)
    sds_revision_date = models.DateField(blank=True, null=True)
    sds_release_date = models.DateField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
