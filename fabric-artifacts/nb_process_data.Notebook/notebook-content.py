# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "70756d4f-7bef-4b01-a1d5-d8e1ed09db26",
# META       "default_lakehouse_name": "lh_data",
# META       "default_lakehouse_workspace_id": "ae3c9ed6-4d02-4b50-8deb-8b8c204b5bd6",
# META       "known_lakehouses": [
# META         {
# META           "id": "70756d4f-7bef-4b01-a1d5-d8e1ed09db26"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Bizz Summit 2025
# ##### Paso de csv a tablas en el catálogo de Fabric (modo Delta)

# MARKDOWN ********************

# ##### Lectura de CSVs.

# CELL ********************

df_clientes_totales = spark.read.format("csv").option("header","true").load("Files/csv/clientes_totales.csv")
display(df_clientes_totales)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_detalle_pedido = spark.read.format("csv").option("header","true").load("Files/csv/detalle_pedido.csv")
display(df_detalle_pedido)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_facturas = spark.read.format("csv").option("header","true").load("Files/csv/facturas.csv")
display(df_facturas)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_territorios_venta = spark.read.format("csv").option("header","true").load("Files/csv/territorios_venta.csv")
display(df_territorios_venta)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Limpieza de columnas.

# CELL ********************

def clean_column_names(df):
    """
    Limpia nombres de columnas:
    - Quita espacios al inicio y final
    - Reemplaza espacios en medio por guiones bajos
    """
    new_columns = [col.strip().replace(" ", "_") for col in df.columns]
    return df.toDF(*new_columns)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_clientes_totales_clean = clean_column_names(df_clientes_totales)
df_detalle_pedido_clean = clean_column_names(df_detalle_pedido)
df_facturas_clean = clean_column_names(df_facturas)
df_territorios_venta_clean = clean_column_names(df_territorios_venta)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Creación de tablas en el catálogo.

# CELL ********************

df_clientes_totales_clean.write.mode("overwrite").saveAsTable("dimClientes")
df_detalle_pedido_clean.write.mode("overwrite").saveAsTable("fact_detalle_pedido")
df_facturas_clean.write.mode("overwrite").saveAsTable("fact_facturas")
df_territorios_venta_clean.write.mode("overwrite").saveAsTable("dimTerritorios")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
