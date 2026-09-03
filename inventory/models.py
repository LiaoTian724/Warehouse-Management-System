from django.db import models
from django.contrib.auth.models import User


# =========================
# 物品表
# =========================
class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)

    status = models.CharField(
      max_length=20,
      choices=[
            ("正常","正常"),
            ("停用","停用"),
      ],
      default="正常"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_items"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# =========================
# 动态属性表
# =========================
class Attribute(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="attributes"
    )

    key = models.CharField(max_length=50)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.item.name}-{self.key}"



# =========================
# 库存流水表
# =========================
class StockRecord(models.Model):
    TYPE_CHOICES = [
        ("IN", "入库"),
        ("OUT", "借出"),
        ("RETURN", "归还"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    quantity = models.IntegerField()
    purpose = models.CharField(
        max_length=200,
        blank=True
    )

    location_image = models.ImageField(
      upload_to="location_records/",
      null=True,
      blank=True
    )

    created_time = models.DateTimeField(
        auto_now_add=True
    )