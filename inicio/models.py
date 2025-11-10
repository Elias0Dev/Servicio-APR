from django.db import models

# Create your models here.
class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    rut = models.IntegerField()
    dv = models.CharField(max_length=1)
    nombre = models.CharField(max_length=80)
    apellido_paterno = models.CharField(max_length=45)
    apellido_materno = models.CharField(max_length=45)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    numero_medidor = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} ({self.rut}-{self.dv})"
    

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(
        'Cliente',  # Suponiendo que tienes un modelo Cliente definido
        on_delete=models.CASCADE,
        db_column='id_cliente',
        related_name='facturas'
    )
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.BooleanField()  # tinyint se suele mapear a Boolean si es 0/1, o SmallIntegerField si hay más estados
    lectura_anterior = models.IntegerField()
    lectura_actual = models.IntegerField()
    fecha_actual = models.DateField()
    fecha_anterior = models.DateField()
    consumo = models.IntegerField()

    class Meta:
        db_table = 'factura'
        indexes = [
            models.Index(fields=['id_cliente'], name='FK_IDC_CLI_idx'),
        ]

    def __str__(self):
        return f"Factura {self.id_factura} - Cliente {self.id_cliente}"


class Tarifas(models.Model):
    TIPO_CHOICES = [
        ('AP', 'AP'),
        ('AS', 'AS'),
    ]

    idtarifas = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    rango_desde = models.IntegerField()
    rango_hasta = models.IntegerField()
    cargo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tarifas'

    def __str__(self):
        return f"Tarifa {self.tipo}: {self.rango_desde}-{self.rango_hasta} -> {self.cargo}"


class Tarifas_fijas(models.Model):
    TIPO_CHOICES = [
        ('AP', 'AP'),
        ('AS', 'AS'),
    ]

    id_tarifa = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    cargo_fijo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'tarifas_fija'

    def __str__(self):
        return {self.tipo}



class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    creado_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contactos'

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"