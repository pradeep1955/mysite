from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """
    Mirrors the section headings in your project reports:
    Power & Charging / Microcontroller & Control / Water & Plumbing / Enclosure & Misc.
    Keeping these as real categories (not hardcoded strings) means new projects
    slot into the same structure automatically.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers display first on the store page"
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    A single component from a Bill of Materials — e.g. 'ESP32-WROOM-32 dev board'
    or 'CN3722 MPPT solar charge controller'.

    Stage 1 of the monetization plan: most Products start as affiliate_url only
    (zero inventory, zero risk) — you earn a small commission and validate demand
    before ever buying stock.
    """
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    specification = models.CharField(
        max_length=200, blank=True, help_text="e.g. '3S Li-ion, up to 2A' or '18V, 10-20W mono/poly'"
    )
    description = models.TextField(blank=True)

    price_min = models.PositiveIntegerField(help_text="Estimated low price in INR")
    price_max = models.PositiveIntegerField(help_text="Estimated high price in INR")

    affiliate_url = models.URLField(
        blank=True, help_text="Amazon / Robu.in / etc link. Leave blank if not sourced yet."
    )
    image = models.ImageField(upload_to="store/products/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category__order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    @property
    def price_display(self):
        if self.price_min == self.price_max:
            return f"₹{self.price_min}"
        return f"₹{self.price_min}–{self.price_max}"


class ProjectKit(models.Model):
    """
    A complete, buildable project — e.g. 'Solar-Powered Balcony Drip Irrigation Kit'.
    Bundles Products together via KitComponent (the BOM), and carries its own
    status so a kit can exist on the site as 'coming soon' long before you've
    bought a single part.
    """
    STATUS_DRAFT = "draft"
    STATUS_COMING_SOON = "coming_soon"
    STATUS_PREORDER = "preorder"
    STATUS_LIVE = "live"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft (hidden)"),
        (STATUS_COMING_SOON, "Coming soon"),
        (STATUS_PREORDER, "Open for preorder"),
        (STATUS_LIVE, "Available now"),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    tagline = models.CharField(
        max_length=200, blank=True, help_text="Short line shown on the store landing page"
    )
    summary = models.TextField(help_text="2-3 sentence overview for the store listing")
    full_description = models.TextField(
        blank=True, help_text="Longer write-up: how it works, wiring notes, safety notes, etc."
    )

    blog_post_url = models.URLField(blank=True, help_text="Link to the matching blog write-up, if any")
    cover_image = models.ImageField(upload_to="store/kits/", blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube/embed link — add when ready")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    components = models.ManyToManyField(Product, through="KitComponent", related_name="kits")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:kit-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    @property
    def total_price_range(self):
        rows = self.kitcomponent_set.select_related("product")
        low = sum(kc.product.price_min * kc.quantity for kc in rows)
        high = sum(kc.product.price_max * kc.quantity for kc in rows)
        return low, high

    @property
    def total_price_display(self):
        low, high = self.total_price_range
        if not low and not high:
            return "Price on request"
        return f"₹{low:,}–₹{high:,}"


class KitComponent(models.Model):
    """Through-table: how many of each Product a given ProjectKit needs — the BOM row."""
    kit = models.ForeignKey(ProjectKit, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    note = models.CharField(
        max_length=150, blank=True, help_text="e.g. 'critical — see wiring notes' or 'optional'"
    )

    class Meta:
        ordering = ["product__category__order", "product__name"]
        unique_together = ("kit", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.kit.name}"


class PreorderInterest(models.Model):
    """
    Zero-payment-gateway MVP for a limited-finance store: capture 'I want this'
    interest instead of processing a real transaction. Follow up manually
    (WhatsApp / UPI) until there's enough volume to justify a payment
    integration like Razorpay.
    """
    kit = models.ForeignKey(ProjectKit, on_delete=models.CASCADE, related_name="preorders")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False, help_text="Tick once you've followed up")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.kit.name} ({self.quantity})"
