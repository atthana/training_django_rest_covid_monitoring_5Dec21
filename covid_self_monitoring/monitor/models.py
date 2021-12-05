from django.db import models

from django.contrib.auth import \
    get_user_model  # ที่ไม่ import User เข้ามาเลยตรงๆเหตุผลคือ ในบาง project อาจต้องใช้พวก custom user ที่ไม่ใช่ default ของ Django

User = get_user_model()


class Symptom(models.Model):  # อาการผิดปกติ
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Measurement(models.Model):  # การวัดค่า
    created = models.DateTimeField(auto_now_add=True)
    # auto_now_add ใช้สร้าง created_date (มันจะ stamp แค่ครั้งเดียวตอน new object)
    # ส่วน auto_now=True จะใช้กับ updated (คือทุกครั้งที่มีการ save ค่า มันจะมา time stamp ตรงนี้ใหม่นะ) นี่คือความแตกต่างระหว่าง auto_now_add กับ auto_now ใน DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 1 user สามารถวัดค่าได้หลายๆครั้งเลย จึงเป็น 1 to many
    # ForeignKey จะชี้ไปที่ User และถ้า ForeignKey จะต้องมี on_delete ตามมาด้วย แปลว่า
    # ถ้าเราลบ User(1) ตัวนี้ไป จะต้องมาลบ Measurement(M) ตัวนี้ไปด้วย

    # Vital signs คือ 4 ค่าด้านล่างนีี้นะ เวลาเราไปรพ.จะถูกวัด 4 ค่านี้เสมอ temperature, o2sat, systolic, diastolic
    temperature = models.DecimalField(max_digits=4, decimal_places=2, help_text='อุณหภูมิร่างกาย')
    # ทั้ง max_digit กับ decimal_places เป็น required property นะ
    # max_digits = จำนวนทั้งหมดของ digit เลยนะ รวมทศนิยมด้วย เช่น 34.55 แบบนี้คือ 4 (ไม่ได้สนใจจุดนะ)
    # decimal_places = จำนวนของทศนิยมเท่านั้น 34.55 แบบนี้คือ 2
    o2sat = models.IntegerField(help_text='อ๊อกซิเจนในเลือด')  # ความอิ่มตัวของออกซิเจน
    systolic = models.IntegerField(help_text='ความดันตัวบน')
    diastolic = models.IntegerField(help_text='ความดันตัวล่าง')
    symptoms = models.ManyToManyField(Symptom, blank=True, help_text='อาการที่พบ')
    # อาการ ต้องใช้เป็น ManyToMany เพราะ 1 การวัดมีได้หลายอาการไง, และ 1 อาการก็วัดได้หลายๆครั้งด้วย งงมะ ในหน้า UI มันจะเลือกได้หลากหลายไง เช่นเวลาเดียวกัน มีหลายอาการ
    # การทำเป็น many to many จะได้ table ขึ้นมาใหม่อีกหนึ่งอันนึง
    # blank=True คือ อนุญาตให้ db เก็บเป็น blank ได้ (เพราะบางครั้ง ถ้าไม่มีอาการก็ไม่ต้องใส่เข้ามาก็ได้)
    # null=True ถ้าเป็น many to many ไม่จำเป็นต้องใส่ เพราะระบบมันอนุญาตให้ null=True ได้อยู่แล้ว

    @property  # property ทำให้เราพิมพ์ค่าต่างๆออกมาได้ง่ายๆ
    def symptoms_display(self):
        return ', '.join(self.symptoms.values_list('name', flat=True))
    # ในเคสนี้เราต้องการเปลี่ยน array ของ symptoms ให้ออกมาเป็น String จึงใช้วิธีการ
    # .join() ด้านในมันจะรับค่ามาเปน array นะ

    class Meta:  # class Meta เป็นการบอกว่า model นี้ของเรามีความสามารถอะไรบ้าง ที่เราเล่นได้
        ordering = ['-created']
    # อันนี้คือเวลา query ออกมา จะให้เรียงลำดับตาม created ออกมา มีติดลบคือ เอาจาก มากไปน้อย (เอาจากล่าสุดไล่ลงมานั่นแหละ)
