import os
import logging
import boto3
from io import StringIO
from botocore.exceptions import ClientError
import pandas as pd
import numpy as np
import time
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sqlalchemy import create_engine
from botocore.config import Config
import joblib
from io import BytesIO
import pickle

s3_access = str(os.environ["S3_ACCESS"])
s3_secret = str(os.environ["S3_SECRET"])


driver = str(os.environ['DRIVER_SQL'])
host = str(os.environ['HOST_SQL'])
user = str(os.environ['USER_SQL'])
password = str(os.environ['PASSWORD_SQL'])
database = str(os.environ['DB_SQL'])

bucket_name = 'videos-s3-bucket'
bucket_models_name = 'models-s3-bucket'



def generate_connection():
    engine_info = "{driver}://{user}:{password}@{host}/{database}".format(host=host
                                                                          , user=user
                                                                          , password=password
                                                                          , database=database
                                                                          , driver=driver)
    conn = create_engine(engine_info)
    return (conn)


def get_df_from_query(conn, sql_query):
    df = pd.read_sql(sql_query, conn)
    return (df)


def init_s3_session(s3_access, s3_secret, bucket_name):
    try:
        # s3 Bucket Session Info to login:
        session = boto3.Session(
            aws_access_key_id=s3_access,
            aws_secret_access_key=s3_secret, )
        config = Config(connect_timeout=200, read_timeout=1000)
        s3 = session.resource('s3', config=config)
        print('S3 session successfully created')
        return s3
    except Exception as e:
        print('Exception occurred when trying to generate S3 session: ', e)


def upload_to_s3(df, s3_access, s3_secret, bucket_name, key):
    s3 = init_s3_session(s3_access, s3_secret, bucket_name)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    bkt = s3.Bucket(bucket_name).put_object(Body=csv_buffer.getvalue(), Key=key)
    return True

def write_joblib(file, path):
    '''
       Function to write a joblib file to an s3 bucket or local directory.
       Arguments:
       * file: The file that you want to save
       * path: an s3 bucket or local directory path.
    '''

    # Path is an s3 bucket
    if path[:5] == 's3://':
        s3_bucket, s3_key = path.split('/')[2], path.split('/')[3:]
        s3_key = '/'.join(s3_key)
        with BytesIO() as f:
            pickle.dump(file, f)
            f.seek(0)
            boto3.client("s3", region_name='us-east-1',
                         aws_access_key_id=s3_access,
                         aws_secret_access_key=s3_secret).upload_fileobj(Bucket=s3_bucket, Key=s3_key, Fileobj=f)

    # Path is a local directory
    else:
        with open(path, 'wb') as f:
            pickle.dump(file, f)

def hc_main():
    print('Generating Connection...')
    time_init = time.time()
    timea = time_init
    conn = generate_connection()
    timeb = time.time()
    print('Connection generated in:', (timeb - timea), ' seconds')

    print('Consulting video tfidf...')
    timea = time.time()
    tfidf = pd.read_csv("data_test/video_tfidf.csv")
    timeb = time.time()
    print('Consulted in:', (timeb - timea), ' seconds')

    print('Consulting videos...')
    timea = time_init
    videos = pd.read_csv("data_test/videos.csv")
    timeb = time.time()
    print('Consulted in:', (timeb - timea), ' seconds')

    print('Generanting  Video Clusters...')
    timea = time.time()
    df_binary_f = tfidf
    jok = df_binary_f
    df_binary_f = df_binary_f.to_numpy()
    df_binary_f = df_binary_f[:, 1:]

    hc = AgglomerativeClustering(n_clusters=12, affinity='euclidean', linkage='ward')
    hc.fit(df_binary_f)
    y_hc = hc.fit_predict(df_binary_f)

    rf = RandomForestClassifier(n_estimators=2)

    rf.fit(df_binary_f, y_hc)
    # y_hc[1300]
    # test_cluster = df_binary_f[500, :].reshape(1, -1)
    # rf.predict(test_cluster)

    filename = 'finalized_model.sav'
    pickle.dump(rf, open(filename, 'wb'), -1)

    # save
    joblib.dump(rf, "random_forest.joblib")


    write_joblib(file=rf, path='s3://' + bucket_models_name + '/random_forest3.pickle')

    returnDf = pd.DataFrame({
        "video_id": jok.iloc[:, 0],
        "cluster": y_hc
    }).sort_values(by=['video_id'])
    timeb = time.time()
    print('Generated in:', (timeb - timea), ' seconds')

    print('Uploading Video Clusters...')
    timea = time.time()
    returnDf.to_sql('video_clusters',
                    con=conn,
                    if_exists='append',
                    index=False,
                    chunksize=50000,
                    method='multi'
                    )
    timeb = time.time()
    print('Uploaded in:', (timeb - timea), ' seconds')

    string_len = 10001
    df_bits = pd.DataFrame()
    returnDf = returnDf.sort_values(['video_id'])
    for i in returnDf.cluster.unique():
        videos_ids = list(returnDf.loc[returnDf.cluster == i].video_id.values)
        values =[1 if x in videos_ids else 0 for x in range(string_len)]
        df_bits = df_bits.append({'cluster_id': int(i), 'videos': ''.join([str(x) for x in values])}, ignore_index=True)
    df_bits.cluster_id.astype(int)

    df_bits.to_sql('binary_table',
                   con=conn,
                   schema='mejora',
                   if_exists='append',
                   index=False)
    print('Uploading S3')
    time = time.time()
    upload_to_s3(returnDf, s3_access, s3_secret, bucket_name, 'video_clusters')
    timeb = time.time()
    print('Uploaded in:', (timeb - timea), ' seconds')

    time_fin = time.time()
    print('Total time = ', (time_fin - time_init) / 60, 'minutes')
