from glob import glob
import pandas as pd
import os

def clean_campaign_data():
    '''
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    '''
    def create_ouptput_directory(output_directory: str):
        if os.path.exists(output_directory):
            for file in glob(f'{output_directory}/*'):
                os.remove(file)
            os.rmdir(output_directory)
        os.makedirs(output_directory)

    in_path = 'files/input'
    out_path = 'files/output'
    zip_files = glob(f'{in_path}/*.zip')
    dataframes = []
    for file in zip_files:
        dataframes.append(pd.read_csv(file, compression='zip', index_col='Unnamed: 0'))

    df = pd.concat(dataframes, ignore_index=True)

    df['job'] = df['job'].apply(lambda x: x.replace('.', '').replace('-', '_'))
    df['education'] = df['education'].apply(lambda x: x.replace('.', '_')).replace('unknown', pd.NA)
    df['credit_default'] = df['credit_default'].apply(lambda x: 1 if x == 'yes' else 0)
    df['mortgage'] = df['mortgage'].apply(lambda x: 1 if x == 'yes' else 0)
    df['previous_outcome'] = df['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0)
    df['campaign_outcome'] = df['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0)
    df['day'] = df['day'].apply(lambda x: str(x).rjust(2, '0'))

    months = dict(zip(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
                      [str(x).rjust(2, '0') for x in range(1, 13)]))

    df['month'] = df['month'].replace(months)
    df['last_contact_day'] = '2022-' + df['month'].astype(str) + '-' + df['day'].astype(str)
    df.rename(columns = {'last_contact_day': 'last_contact_date'}, inplace = True)              # Las indicaciones están mal :)

    create_ouptput_directory(out_path)

    df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].to_csv(f'{out_path}/client.csv', index=False)
    df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'last_contact_date']].to_csv(f'{out_path}/campaign.csv', index=False)
    df[['client_id', 'cons_price_idx', 'euribor_three_months']].to_csv(f'{out_path}/economics.csv', index=False)


if __name__ == "__main__":
    clean_campaign_data()
