from django.db import models


# Create your models here.
class Cliente(models.Model):
    TIPO_CHOICES_1 = [
        ("persona", "Persona"),
        ("empresa", "Empresa"),
    ]
    id_cliente = models.IntegerField(primary_key=True)
    
    nombre = models.CharField(max_length=80)
    rut = models.IntegerField()
    dv = models.CharField(max_length=1)
    tipo = models.CharField(
        max_length=10,        # debe ser suficientemente largo para la opción más larga
        choices=TIPO_CHOICES_1, # opciones disponibles
        default="persona"       # valor por defecto (opcional)
    )
    razon_social=models.CharField(max_length=200,blank=True) 
    sector = models.CharField(max_length=200, blank=True)    
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.IntegerField(blank=True)
    email = models.CharField(max_length=100, blank=True )
    numero_medidor = models.CharField(max_length=100)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"Medidor: {self.numero_medidor} | Cliente: {self.nombre} ({self.rut}-{self.dv})"
    
    def save(self, *args, **kwargs):
        # para todos los campos que permiten blank=True
        for field in self._meta.fields:
            if getattr(field, "blank", False):  # si el campo permite blank=True
                valor = getattr(self, field.name)

                if valor in (None, ""):
                    # si el campo es numérico → poner 0
                    if isinstance(field, (models.IntegerField, models.FloatField, models.DecimalField)):
                        setattr(self, field.name, 0)
                    else:
                        # caso general: texto
                        setattr(self, field.name, "No Aplica")

        super().save(*args, **kwargs)
    

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
    estado_pago = models.BooleanField()
    corte = models.BooleanField()
    subsidio = models.BooleanField()
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
    


class Tarifa(models.Model):
    TIPO_CHOICES = [
        ('AP', 'AP'),
        ('AS', 'AS'),
    ]

    id_tarifa = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    rango_desde = models.IntegerField()
    rango_hasta = models.IntegerField()
    # CORREGIDO: 'cargo' en el modelo se mapea a 'valor_m3' que buscabas en Admin.
    cargo = models.DecimalField(max_digits=10, decimal_places=2) 
    fecha_inicio = models.DateField()

    class Meta:
        db_table = 'tarifa'

    def __str__(self):
        return f"Tarifa {self.tipo}: {self.rango_desde}-{self.rango_hasta} -> {self.cargo}"


class Cargo(models.Model):
    TIPO_CHOICES = [
        ('CARGO FIJO AP', 'CARGOFIJO AP'),
        ('CARGO FIJO AS', 'CARGO FIJO AS'),
        ('INTERESES', 'INTERESES'),
        ('CORTE DE SUMINISTRO', 'CORTE DE SUMINISTRO'),
        
    ]

    id_cargo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=19, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'cargo'

    def __str__(self):
        return self.tipo

class Subsidio(models.Model):
    id_subsidio = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='subsidios'
    )
    num_decreto = models.CharField(max_length=50)
    tramo_rsh = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_aplicacion = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'subsidio'

    def __str__(self):
        return f"Subsidio {self.num_decreto} - Cliente {self.cliente.nombre}"


class Contacto(models.Model):
    id_contacto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    # CORREGIDO: El campo es 'email', no 'correo'.
    email = models.EmailField() 
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    # CORREGIDO: El campo es 'creado_el', no 'fecha_envio'.
    creado_el = models.DateTimeField(auto_now_add=True) 
    # CORREGIDO: Campo 'revisado' añadido.
    revisado = models.BooleanField(default=False)

    class Meta:
        db_table = 'contacto'

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"
    

