from django.db import models

# Create your models here.
class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    rut = models.IntegerField()
    dv = models.CharField(max_length=1)
    nombre = models.CharField(max_length=100)
    # ASUMIDO: Agregué el campo 'apellido' que se intentó usar en el Admin.
    apellido = models.CharField(max_length=100) 
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    numero_medidor = models.IntegerField(blank=True, null=True)
    # CORREGIDO: Campo 'es_vigente' renombrado a 'vigente' y añadido.
    vigente = models.BooleanField(default=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut}-{self.dv})"
    

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(
        'Cliente',  # Suponiendo que tienes un modelo Cliente definido
        on_delete=models.CASCADE,
        db_column='id_cliente',
        related_name='facturas'
    )
    # ASUMIDO: Para que la Factura sepa qué tarifa aplicó, se recomienda un FK o un campo de texto.
    tarifa_aplicada = models.CharField(max_length=50, blank=True, null=True) 
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.BooleanField()
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
    # CORREGIDO: 'cargo' en el modelo se mapea a 'valor_m3' que buscabas en Admin.
    cargo = models.DecimalField(max_digits=10, decimal_places=2) 
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tarifas'

    def __str__(self):
        return f"Tarifa {self.tipo}: {self.rango_desde}-{self.rango_hasta} -> {self.cargo}"


class Contacto(models.Model):
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
        db_table = 'contactos'

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"